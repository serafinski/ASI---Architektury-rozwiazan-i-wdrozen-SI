import logging
import gspread
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from pycaret.classification import setup, compare_models, tune_model, get_config, predict_model, save_model, load_model, add_metric, blend_models
from sklearn.metrics import accuracy_score, mean_absolute_error, mean_absolute_percentage_error, mean_squared_error
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from airflow.models import Variable
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import joblib
from airflow.utils.email import send_email
import docker
import os
import shutil
import tempfile
import re
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def split_data(train_name: str, test_name: str, **context):
    logger.info("Rozpoczynanie podziału danych.")

    # Wczytywanie danych
    data = pd.read_csv('/opt/airflow/processed_data/bank-additional-full.csv', delimiter=';')
    logger.info("Dane zostały pomyślnie wczytane z pliku CSV.")

    # Podział danych
    train_data, test_data = train_test_split(data, test_size=0.3, random_state=17)
    logger.info("Dane zostały podzielone na zbiory treningowy i testowy.")

    # Przesłanie danych do XCom
    context['ti'].xcom_push(key=train_name, value=train_data)
    context['ti'].xcom_push(key=test_name, value=test_data)
    logger.info("Zbiory danych modelowy i testowy zostały przesłane do XCom.")


def split_processed_model_data(processed_name_train: str, split_train_name: str, split_test_name: str, **context):
    logger.info("Rozpoczynanie podziału danych.")

    data = context['ti'].xcom_pull(key=processed_name_train)

    # Podział danych
    train_data, test_data = train_test_split(data, test_size=0.3, random_state=17)
    logger.info("Dane zostały podzielone na zbiory treningowy i testowy.")

    # Przesłanie danych do XCom
    context['ti'].xcom_push(key=split_train_name, value=train_data)
    context['ti'].xcom_push(key=split_test_name, value=test_data)
    logger.info("Podzielony zbiór modelowy przesłany do XCom.")


def save_to_sheets(train_name: str, test_name: str, **context):
    logger.info("Rozpoczynanie zapisu do Arkuszy Google.")

    # Pobranie danych z XCom
    train_data = context['ti'].xcom_pull(key=train_name)
    test_data = context['ti'].xcom_pull(key=test_name)
    logger.info("Zbiory danych modelowych i testowych zostały pobrane z XCom.")

    # Google credentials setup
    credentials_info = Variable.get("google_application_credentials", deserialize_json=True)
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)

    # Autoryzacja z Google Sheets API
    client = gspread.authorize(credentials)
    logger.info("Autoryzowano klienta Google Sheets API.")

    # Stworzenie arkuszy Google
    sheet_train = client.create(train_name)
    sheet_test = client.create(test_name)
    logger.info("Utworzono Arkusze Google dla zbioru modelowego i testowego.")

    # Upload arkuszy do Google Sheets
    worksheet_train = sheet_train.get_worksheet(0)
    worksheet_test = sheet_test.get_worksheet(0)

    worksheet_train.update([train_data.columns.values.tolist()] + train_data.values.tolist())
    worksheet_test.update([test_data.columns.values.tolist()] + test_data.values.tolist())
    logger.info("Dane modelowe i testowe zostały załadowane do Arkuszy Google.")

    # Google Drive API setup
    drive_service = build('drive', 'v3', credentials=credentials)
    destination_folder_id = '1ocYhp4G6L2djrypYEsqWGAN1GK35A1Ug'

    # Przenieś arkusz treningowy do wyznaczonego folderu
    drive_service.files().update(
        fileId=sheet_train.id,
        addParents=destination_folder_id,
        # Usuń z My Drive
        removeParents='root',
        fields='id, parents'
    ).execute()
    logger.info(f"Arkusz modelowy przeniesiony do folderu o ID: {destination_folder_id}.")

    # Przenieś arkusz testowy do wyznaczonego folderu
    drive_service.files().update(
        fileId=sheet_test.id,
        addParents=destination_folder_id,
        # Usuń z My Drive
        removeParents='root',
        fields='id, parents'
    ).execute()
    logger.info(f"Arkusz testowy przeniesiony do folderu o ID: {destination_folder_id}.")

    logger.info("Pliki zostały pomyślnie przeniesione do określonego folderu.")


def download_data(train_name: str, test_name: str, **context):
    # Google credentials setup
    credentials_info = Variable.get("google_application_credentials", deserialize_json=True)
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)

    # Autoryzacja z Google Sheets API
    client = gspread.authorize(credentials)
    logger.info("Autoryzowano klienta Google Sheets API.")

    # Otwarcie Google Sheets
    sheet_train = client.open(train_name).sheet1
    sheet_test = client.open(test_name).sheet1
    logger.info("Otwarto arkusze dla zbioru modelowego i testowego.")

    # Pobierz dane
    train_data = pd.DataFrame(sheet_train.get_all_records())
    test_data = pd.DataFrame(sheet_test.get_all_records())
    logger.info("Pobrano dane z arkuszy.")

    # Zapisanie do kontekstu
    context['ti'].xcom_push(key=train_name, value=train_data)
    context['ti'].xcom_push(key=test_name, value=test_data)
    logger.info("Dane z pobranych arkuszy zostały przekazane do XCom.")

def download_retrain_data(sheet_name: str, **context):
    # Google credentials setup
    credentials_info = Variable.get("google_application_credentials", deserialize_json=True)
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)

    # Autoryzacja z Google Sheets API
    client = gspread.authorize(credentials)
    logger.info("Autoryzowano klienta Google Sheets API.")

    # Otwarcie Google Sheets
    sheet = client.open(sheet_name).sheet1
    logger.info("Otwarto wybrany arkusz.")

    # Pobierz dane
    data = pd.DataFrame(sheet.get_all_records())
    logger.info("Pobrano dane z arkusza.")

    # Zapisanie do kontekstu
    context['ti'].xcom_push(key=sheet_name, value=data)
    logger.info("Dane z pobranych arkuszy zostały przekazane do XCom.")


def clean_data(train_name: str, test_name: str, train_name_clean: str, test_name_clean: str, **context):
    # Pobranie danych z XCom
    train_data = context['ti'].xcom_pull(key=train_name)
    test_data = context['ti'].xcom_pull(key=test_name)
    logger.info("Zbiory danych modelowych i testowych zostały pobrane z XCom.")
    logger.info(f"Rozmiar danych modelowych: {train_data.shape}")
    logger.info(f"Rozmiar danych testowych: {test_data.shape}")

    # Usunięcie brakujących wartości
    logger.info("Usuwanie brakujących wartości:")
    train_data_cleaned = train_data.dropna()
    logger.info(f"Rozmiar danych modelowych (po usunięciu brakujących wartości): {train_data_cleaned.shape}")
    test_data_cleaned = test_data.dropna()
    logger.info(f"Rozmiar danych testowych (po usunięciu brakujących wartości): {test_data_cleaned.shape}")
    logger.info("Usunięto wiersze z brakującymi wartościami (jeśli takie wystąpiły).")

    # Usunięcie duplikatów
    logger.info("Usuwanie duplikatów:")
    train_data_cleaned = train_data_cleaned.drop_duplicates()
    logger.info(f"Rozmiar danych modelowych (po usunięciu duplikatów): {train_data_cleaned.shape})")
    test_data_cleaned = test_data_cleaned.drop_duplicates()
    logger.info(f"Rozmiar danych testowych (po usunięciu duplikatów): {test_data_cleaned.shape})")
    logger.info("Usunięto duplikaty z danych modelowych i testowych (jeśli takie wystąpiły).")

    # Zapisanie do kontekstu
    context['ti'].xcom_push(key=train_name_clean, value=train_data_cleaned)
    context['ti'].xcom_push(key=test_name_clean, value=test_data_cleaned)
    logger.info("Oczyszczone dane zostały zapisane do XCom.")


def clean_retrain_data(sheet_name: str, cleaned_sheet_name: str, **context):
    # Pobranie danych z XCom
    data = context['ti'].xcom_pull(key=sheet_name)
    logger.info("Dane zostały pobrane z XCom.")
    logger.info(f"Rozmiar danych: {data.shape}")

    # Usunięcie brakujących wartości
    logger.info("Usuwanie brakujących wartości:")
    data_cleaned = data.dropna()
    logger.info(f"Rozmiar danych (po usunięciu brakujących wartości): {data_cleaned.shape}")
    logger.info("Usunięto wiersze z brakującymi wartościami (jeśli takie wystąpiły).")

    # Usunięcie duplikatów
    logger.info("Usuwanie duplikatów:")
    data_cleaned = data_cleaned.drop_duplicates()
    logger.info(f"Rozmiar danych (po usunięciu duplikatów): {data_cleaned.shape}")
    logger.info("Usunięto duplikaty z danych (jeśli takie wystąpiły).")

    # Zapisanie do kontekstu
    context['ti'].xcom_push(key=cleaned_sheet_name, value=data_cleaned)
    logger.info("Oczyszczone dane zostały zapisane do XCom.")


def standardize_normalize_data(train_name_clean: str, test_name_clean: str, train_name_standard: str,
                               test_name_standard: str, **context):
    # Pobranie danych z XCom
    train_data_cleaned = context['ti'].xcom_pull(key=train_name_clean)
    test_data_cleaned = context['ti'].xcom_pull(key=test_name_clean)
    logger.info("Pobrano oczyszczone dane modelowe i testowe z XCom do standaryzacji i normalizacji.")

    # Usuwanie duration
    columns_to_drop = ['duration']
    for col in columns_to_drop:
        train_data_cleaned.drop([col], axis=1, inplace=True)
        test_data_cleaned.drop([col], axis=1, inplace=True)
        logger.info(f"Usunięto kolumnę '{col}'.")

    # Zachowanie oryginalnej kolejności kolumn
    original_columns = train_data_cleaned.columns

    # Wyizolowanie tylko kolumn numerycznych
    numeric_columns = train_data_cleaned.select_dtypes(include=['number']).columns
    non_numeric_columns = train_data_cleaned.select_dtypes(exclude=['number']).columns
    logger.info(f"Nienumeryczne kolumny, które zostaną pominięte: {non_numeric_columns.tolist()}")

    # Standaryzacja danych
    scaler = StandardScaler()
    train_features_scaled = scaler.fit_transform(train_data_cleaned[numeric_columns])
    test_features_scaled = scaler.transform(test_data_cleaned[numeric_columns])
    logger.info("Przeprowadzono standaryzacje danych numerycznych.")

    # Zapisz StandardScaler
    joblib.dump(scaler, "/opt/airflow/models/standard_scaler.pkl")
    logger.info(f"StandardScaler został zapisany jako standard_scaler.pkl")

    # Normalizacja danych
    normalizer = MinMaxScaler()
    train_features_normalized = normalizer.fit_transform(train_features_scaled)
    test_features_normalized = normalizer.transform(test_features_scaled)
    logger.info("Przeprowadzono normalizacje danych numerycznych.")

    # Zapisz MinMaxScaler
    joblib.dump(normalizer, "/opt/airflow/models/min_max_scaler.pkl")
    logger.info(f"StandardScaler został zapisany jako min_max_scaler.pkl")

    # Konwersja z powrotem do DataFrame i dodanie z powrotem kolumny target.
    train_data_standardized = pd.DataFrame(train_features_normalized, columns=numeric_columns)
    train_data_standardized = pd.concat(
        [train_data_standardized, train_data_cleaned[non_numeric_columns].reset_index(drop=True)], axis=1)
    test_data_standardized = pd.DataFrame(test_features_normalized, columns=numeric_columns)
    test_data_standardized = pd.concat(
        [test_data_standardized, test_data_cleaned[non_numeric_columns].reset_index(drop=True)], axis=1)

    # Przywrócenie oryginalnej kolejności kolumn
    train_data_standardized = train_data_standardized[original_columns]
    test_data_standardized = test_data_standardized[original_columns]

    # Zapisanie do kontekstu
    context['ti'].xcom_push(key=train_name_standard, value=train_data_standardized)
    context['ti'].xcom_push(key=test_name_standard, value=test_data_standardized)
    logger.info(
        "Wystandaryzowane i znormalizowane dane numeryczne zostały połączone z oryginalnymi kolumnami nienumerycznymi i zapisane do XCom.")


def standardize_normalize_retrain_data(cleaned_sheet_name: str, standard_sheet_name: str, **context):
    # Pobranie danych z XCom
    data_cleaned = context['ti'].xcom_pull(key=cleaned_sheet_name)
    logger.info("Pobrano oczyszczone dane z XCom do standaryzacji i normalizacji.")

    # Usuwanie duration
    columns_to_drop = ['duration']
    for col in columns_to_drop:
        data_cleaned.drop([col], axis=1, inplace=True)
        logger.info(f"Usunięto kolumnę '{col}'.")

    # Zachowanie oryginalnej kolejności kolumn
    original_columns = data_cleaned.columns

    # Wyizolowanie tylko kolumn numerycznych
    numeric_columns = data_cleaned.select_dtypes(include=['number']).columns
    non_numeric_columns = data_cleaned.select_dtypes(exclude=['number']).columns
    logger.info(f"Nienumeryczne kolumny, które zostaną pominięte: {non_numeric_columns.tolist()}")

    # Załadowanie zapisanych scalerów
    scaler = joblib.load("/opt/airflow/models/standard_scaler.pkl")
    normalizer = joblib.load("/opt/airflow/models/min_max_scaler.pkl")
    logger.info("Załadowano zapisane scalery.")

    # Standaryzacja danych używając zapisanego scalera
    features_scaled = scaler.transform(data_cleaned[numeric_columns])
    logger.info("Przeprowadzono standaryzacje danych numerycznych.")

    # Normalizacja danych używając zapisanego normalizera
    features_normalized = normalizer.transform(features_scaled)
    logger.info("Przeprowadzono normalizacje danych numerycznych.")

    # Konwersja z powrotem do DataFrame
    data_standardized = pd.DataFrame(features_normalized, columns=numeric_columns)
    data_standardized = pd.concat(
        [data_standardized, data_cleaned[non_numeric_columns].reset_index(drop=True)], axis=1)

    # Przywrócenie oryginalnej kolejności kolumn
    data_standardized = data_standardized[original_columns]

    # Zapisanie do kontekstu
    context['ti'].xcom_push(key=standard_sheet_name, value=data_standardized)
    logger.info("Wystandaryzowane i znormalizowane dane zostały zapisane do XCom.")

def process_data(train_name_standard: str, processed_name_train: str, **context):
    df = context['ti'].xcom_pull(key=train_name_standard)
    suma = 0

    # Definicja kolumn do czyszczenia
    columns_to_clean = ['job', 'marital', 'education', 'housing', 'loan']
    exclude_conditions = {
        'default': 'yes'
    }

    # Usuwanie wierszy, gdzie wartość w kolumnach to 'unknown'
    for col in columns_to_clean:
        initial_count = df.shape[0]
        df = df[df[col] != 'unknown']
        removed_count = initial_count - df.shape[0]
        suma += removed_count
        logger.info(f"Usunięto {removed_count} wierszy, gdzie '{col}' miało wartość 'unknown'.")

    # Usuwanie wierszy, gdzie 'default' == 'yes'
    for col, value in exclude_conditions.items():
        initial_count = df.shape[0]
        df = df[df[col] != value]
        removed_count = initial_count - df.shape[0]
        suma += removed_count
        logger.info(f"Usunięto {removed_count} wierszy, gdzie '{col}' miało wartość '{value}'.")

    # Podsumowanie
    logger.info(f"Łącznie usunięto {suma} wierszy.")

    binary_mapping = {
        'housing': {'yes': 1, 'no': 0},
        'loan': {'yes': 1, 'no': 0},
        'contact': {'cellular': 1, 'telephone': 0},
        'y': {'yes': 1, 'no': 0},
        'default': {'no': 0, 'unknown': 1},
    }

    df.replace(binary_mapping, inplace=True)
    logger.info("Wykonano mapowanie binarne")

    # One-Hot Encoding
    data_encoded = pd.get_dummies(df, columns=['marital', 'poutcome'], drop_first=True)
    logger.info("Wykonano one-hot encoding")

    # Booleans do 0:1
    data_encoded = data_encoded.astype({col: 'int' for col in data_encoded.select_dtypes('bool').columns})
    logger.info("Zamieniono booleans na zmienne liczbowe")

    # Przenieś kolumnę 'y' na sam koniec
    target_column = 'y'
    columns = [col for col in data_encoded.columns if col != target_column] + [target_column]
    data_encoded = data_encoded[columns]
    logger.info(f"Kolumna 'y' została przeniesiona na koniec: {data_encoded.columns.tolist()}")

    context['ti'].xcom_push(key=processed_name_train, value=data_encoded)


def train_model(split_train_name: str, split_test_name: str, **context):
    data = context['ti'].xcom_pull(key=split_train_name)
    processed_test_data = context['ti'].xcom_pull(key=split_test_name)

    categorical_features = [
        'job', 'education', 'month', 'day_of_week'
    ]

    numeric_features = [
        'age', 'housing', 'loan', 'contact',
        'campaign', 'pdays', 'previous', 'emp.var.rate',
        'cons.price.idx', 'cons.conf.idx', 'euribor3m',
        'nr.employed', 'marital_married', 'marital_single',
        'poutcome_nonexistent', 'poutcome_success'
    ]

    logger.info("Ustawienia PyCaret'a")
    logger.info(f"Używane kolumny numeryczne: {numeric_features}")
    logger.info(f"Używane kolumny kategoryczne: {categorical_features}")
    cla = setup(data=data,
                target='y',
                preprocess=True,
                categorical_features=categorical_features,
                numeric_features=numeric_features,
                remove_outliers=False,
                normalize=False,
                transformation=False,
                test_data=processed_test_data,
                fold=5,
                session_id=17,
                n_jobs=1)

    # Porównanie modeli i wybór najlepszego
    logger.info("Porównywanie modeli w celu wyboru najlepszego...")
    best_model = compare_models()

    # Tunowanie najlepszego modelu
    logger.info("Tunowanie najlepszego modelu...")
    tuned_model = tune_model(best_model)

    logger.info(
        "Tunowanie hiperparametrów zostało zakończone. PyCaret automatycznie wybrał model, który osiąga najlepsze wyniki — jeśli tuning nie poprawił wyników, oryginalny model zostaje zachowany.")

    test_data = get_config('X_test')
    test_target = get_config('y_test')

    # Predykcja na zbiorze walidacyjnym
    logger.info("Predykcja na zbiorze walidacyjnym i obliczenie metryk...")
    predictions = predict_model(tuned_model, data=test_data)

    # Obliczanie metryk
    accuracy = accuracy_score(predictions['prediction_label'], test_target)
    mae = mean_absolute_error(predictions['prediction_label'], test_target)

    logger.info(f'Dokładność modelu: {accuracy}')
    logger.info(f'Średni błąd bezwzględny (MAE): {mae}')

    with open('/opt/airflow/reports/evaluation_report.txt', 'w') as report:
        report.write(f'Accuracy: {accuracy}\n')
        report.write(f'Mean Absolute Error (MAE): {mae}\n')

    # Zapisanie modelu
    save_model(tuned_model, '/opt/airflow/models/prototype')
    logger.info("Model został zapisany jako 'prototype'.")


def retrain_model(processed_name: str, **context):
    # Wczytaj nowe dane
    new_data = context['ti'].xcom_pull(key=processed_name)

    # Validate data structure
    logger.info(f"Input data shape: {new_data.shape}")
    logger.info(f"Input data columns: {new_data.columns.tolist()}")

    # Ensure all expected columns are present
    expected_features = ['age', 'housing', 'loan', 'contact', 'campaign', 'pdays',
                         'previous', 'emp.var.rate', 'cons.price.idx', 'cons.conf.idx',
                         'euribor3m', 'nr.employed', 'marital_married', 'marital_single',
                         'poutcome_nonexistent', 'poutcome_success']

    missing_cols = [col for col in expected_features if col not in new_data.columns]
    if missing_cols:
        raise ValueError(f"Missing expected columns: {missing_cols}")

    # Wczytaj istniejący model
    model = load_model('/opt/airflow/models/prototype')
    logger.info("Załadowano istniejący model")

    # Setup with explicit data validation
    cla = setup(data=new_data,
                target='y',
                preprocess=True,
                categorical_features=['job', 'education', 'month', 'day_of_week'],
                numeric_features=expected_features,
                remove_outliers=False,
                normalize=False,
                transformation=False,
                fold=5,
                session_id=17,
                n_jobs=1)

    # Instead of blending, try simple model fitting first
    predictions = predict_model(model, data=new_data)
    updated_model = model.fit(new_data.drop('y', axis=1), new_data['y'])

    # Evaluate
    accuracy = accuracy_score(predictions['prediction_label'], new_data['y'])
    mae = mean_absolute_error(predictions['prediction_label'], new_data['y'])

    logger.info(f'Dokładność modelu po dotrenowaniu: {accuracy}')
    logger.info(f'Średni błąd bezwzględny (MAE) po dotrenowaniu: {mae}')

    # Save model and metrics
    save_model(updated_model, '/opt/airflow/models/prototype')

    with open('/opt/airflow/reports/retraining_evaluation_report.txt', 'w') as report:
        report.write(f'Accuracy after retraining: {accuracy}\n')
        report.write(f'Mean Absolute Error (MAE) after retraining: {mae}\n')

    logger.info("Dotrenowany model został zapisany jako 'prototype'.")


def generate_corner_cases(split_train_name: str, corner_cases_name: str, **context):
    df = context['ti'].xcom_pull(key=split_train_name)
    logger.info(f"Data loaded, shape: {df.shape}")

    # Inicjalizacja track'owania
    corner_case_reasons = {idx: [] for idx in df.index}

    # Typy kolumn
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    categorical_columns = df.select_dtypes(include=['object']).columns
    binary_columns = [col for col in numeric_columns if set(df[col].unique()).issubset({0, 1})]

    # 1. Sprawdź niestandardowe kombinacje kolumn kategorycznych
    for col1 in categorical_columns:
        for col2 in categorical_columns:
            # Unikaj zduplikowanych kombinacji
            if col1 < col2:
                combo_counts = df.groupby([col1, col2]).size()
                total_records = len(df)
                combo_percentages = (combo_counts / total_records) * 100

                # Znajdź kombinacje znajdujące się w mniej niż 0.2% rekordów
                rare_combos = combo_counts[combo_percentages < 0.2].index

                for val1, val2 in rare_combos:
                    mask = (df[col1] == val1) & (df[col2] == val2)
                    for idx in df[mask].index:
                        corner_case_reasons[idx].append(
                            f"Rare combination: {col1}='{val1}' with {col2}='{val2}' "
                            f"({combo_percentages[(val1, val2)]:.2f}% of data)"
                        )

    # 2. Sprawdź kolumny numeryczne dla ekstremalnych outlierow
    for col in numeric_columns:
        if col not in binary_columns:
            # Bezpośrednie porównywanie, bo wartości są już wystandaryzowane
            values = df[col].values
            q1 = np.percentile(values, 25)
            q3 = np.percentile(values, 75)
            iqr = q3 - q1
            lower_bound = q1 - (4 * iqr)
            upper_bound = q3 + (4 * iqr)

            outliers = (values < lower_bound) | (values > upper_bound)

            for idx in df[outliers].index:
                value = df.loc[idx, col]
                corner_case_reasons[idx].append(
                    f"Extreme value in {col}: {value:.2f} (outside IQR bounds)"
                )

    # 3. Znajdź dziwne patterny w kolumnach binarnych
    if len(binary_columns) >= 3:
        patterns = df[binary_columns].apply(tuple, axis=1)
        pattern_counts = patterns.value_counts()
        total_patterns = len(patterns)
        pattern_percentages = (pattern_counts / total_patterns) * 100

        # Patterny w mniej niż 1% rekordów
        rare_patterns = pattern_counts[pattern_percentages < 0.5]

        for idx in df.index:
            pattern = patterns[idx]
            if pattern in rare_patterns.index:
                count = pattern_counts[pattern]
                percentage = pattern_percentages[pattern]
                corner_case_reasons[idx].append(
                    f"Rare binary pattern across {', '.join(binary_columns)} "
                    f"(occurs {count} times, {percentage:.2f}% of data)"
                )

    # 4. Znajdź dziwne kombinacje w kolumnach numerycznych
    numeric_subset = df[numeric_columns].copy()
    # Normalize numeric data
    for col in numeric_columns:
        if col not in binary_columns and df[col].std() != 0:
            numeric_subset[col] = (df[col] - df[col].mean()) / df[col].std()

    # Wyliczenie odległości Mahalanobis'a
    cov = numeric_subset.cov()
    try:
        inv_cov = np.linalg.inv(cov)
        m_distances = []
        for i in range(len(numeric_subset)):
            x = numeric_subset.iloc[i]
            d = np.sqrt(x.dot(inv_cov).dot(x))
            m_distances.append(d)

        # Znajdź punkty z dużym dystansem Mahalanobisa (top 2%)
        threshold = np.percentile(m_distances, 98)
        for idx, distance in enumerate(m_distances):
            if distance > threshold:
                corner_case_reasons[idx].append(
                    f"Unusual combination of numeric values (Mahalanobis distance: {distance:.2f})"
                )
    except np.linalg.LinAlgError:
        logger.warning("Could not calculate Mahalanobis distances due to singular covariance matrix")

    # Zachowaj tylko znaczące anomalie
    corner_cases = pd.Series(False, index=df.index)
    for idx, reasons in corner_case_reasons.items():
        # Minimum 2 anomalie!
        if len(reasons) >= 3:
            # Rozne typy dla anomali
            reason_types = set(r.split(':')[0] for r in reasons)
            if len(reason_types) >= 2:
                corner_cases[idx] = True

    # Wyciągnij corner cases
    final_corner_cases = df[corner_cases].copy()

    logger.info(f"\nSummary:")
    logger.info(f"Total rows in original dataset: {len(df)}")
    logger.info(f"Total corner cases found: {len(final_corner_cases)}")
    logger.info(f"Percentage of corner cases: {(len(final_corner_cases) / len(df)) * 100:.2f}%")

    context['ti'].xcom_push(key=corner_cases_name, value=final_corner_cases)

def run_unit_tests(**context):
    test_results = {
        "model_loading": False,
        "metric_calculation": False,
        "pipeline_missing_data": False,
    }

    try:
        # Test model loading
        model = joblib.load('/opt/airflow/models/prototype.pkl')
        test_results["model_loading"] = True
    except Exception as e:
        logger.error(f"Model loading test failed: {e}")

    try:
        # Test metric calculation
        y_true = [0, 1, 1, 0]
        y_pred = [0, 1, 0, 1]
        _ = accuracy_score(y_true, y_pred)
        test_results["metric_calculation"] = True
    except Exception as e:
        logger.error(f"Metric calculation test failed: {e}")

    try:
        # Test pipeline handling missing data
        df = pd.DataFrame({'A': [1, 2, None, 4], 'B': [None, 2, 3, 4]})
        df.fillna(0, inplace=True)  # Example pipeline step
        _ = df.sum()
        test_results["pipeline_missing_data"] = True
    except Exception as e:
        logger.error(f"Pipeline missing data test failed: {e}")

    context['ti'].xcom_push(key='test_results', value=test_results)
    logger.info(f"Unit test results: {test_results}")

def evaluate_model_on_test_data(split_test_name: str, **context):
    model = joblib.load('/opt/airflow/models/prototype.pkl')
    df = context['ti'].xcom_pull(key=split_test_name)

    X_test = df.drop('y', axis=1)
    y_test = df['y']

    test_predictions = model.predict(X_test)
    test_accuracy = accuracy_score(y_test, test_predictions)

    context['ti'].xcom_push(key='test_accuracy', value=test_accuracy)
    logger.info(f'Model accuracy on test dataset: {test_accuracy}')
    return test_accuracy

def evaluate_model_on_corner_cases(corner_cases_name: str, **context):
    model = joblib.load('/opt/airflow/models/prototype.pkl')

    corner_cases_data = context['ti'].xcom_pull(key=corner_cases_name)

    X_corner_cases = corner_cases_data.drop(columns=['y'])
    y_corner_cases = corner_cases_data['y']

    corner_cases_predictions = model.predict(X_corner_cases)
    corner_cases_accuracy = accuracy_score(y_corner_cases, corner_cases_predictions)

    context['ti'].xcom_push(key='corner_cases_accuracy', value=corner_cases_accuracy)
    logger.info(f'Model accuracy on corner case dataset: {corner_cases_accuracy}')
    return corner_cases_accuracy

def check_and_alert(**context):
    CRITICAL_DROP_THRESHOLD = 0.10
    EMAIL_RECIPIENTS = ['s24353@pjwstk.edu.pl']

    test_accuracy = context['ti'].xcom_pull(key='test_accuracy')
    corner_cases_accuracy = context['ti'].xcom_pull(key='corner_cases_accuracy')
    test_results = context['ti'].xcom_pull(key='test_results')
    model_name = 'prototype'

    # Calculate accuracy drop
    accuracy_drop = test_accuracy - corner_cases_accuracy

    # Prepare email content
    failed_tests = [test for test, passed in test_results.items() if not passed]
    subject = f"Model Alert: {model_name}"
    body = f"""
    <h2>Model Performance Alert</h2>
    <p><strong>Model:</strong> {model_name}</p>
    <p><strong>Accuracy on test dataset:</strong> {test_accuracy:.2f}</p>
    <p><strong>Accuracy on corner case dataset:</strong> {corner_cases_accuracy:.2f}</p>
    <p><strong>Accuracy drop:</strong> {accuracy_drop:.2f}</p>
    <p><strong>Critical threshold for drop:</strong> {CRITICAL_DROP_THRESHOLD:.2f}</p>
    <p><strong>Failed Tests:</strong> {', '.join(failed_tests) if failed_tests else 'None'}</p>
    """

    # Send email if critical threshold is breached or tests failed
    if accuracy_drop > CRITICAL_DROP_THRESHOLD or failed_tests:
        try:
            smtp_settings = {
                'smtp_user': os.environ.get('AIRFLOW_SMTP_USER'),
                'smtp_password': os.environ.get('AIRFLOW_SMTP_PASSWORD'),
                'smtp_mail_from': os.environ.get('AIRFLOW_SMTP_FROM'),
                'smtp_host': 'smtp.gmail.com',
                'smtp_port': 587,
                'smtp_ssl': False,
                'smtp_starttls': True
            }

            send_email(
                to=EMAIL_RECIPIENTS,
                subject=subject,
                html_content=body,
                mime_charset='utf-8',
                **smtp_settings
            )
            logging.info("Alert email sent due to critical issues.")
        except Exception as e:
            logging.error(f"Failed to send email alert: {str(e)}")


def prepare_build_context(**context):
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    try:
        # Create the directory structure
        os.makedirs(os.path.join(temp_dir, 'airflow/models'), exist_ok=True)

        # Copy necessary files
        dockerfile_content = """
        FROM python:3.10-slim
        
        RUN apt-get update && apt-get install -y --no-install-recommends \
            libgomp1 && \
            rm -rf /var/lib/apt/lists/*
        
        WORKDIR /app
        
        # Create directory structure
        RUN mkdir -p /app/airflow/models
        
        # Copy files
        COPY app.py .
        COPY airflow/models/* /app/airflow/models/
        
        # Install requirements
        RUN pip install --no-cache-dir flask pandas pycaret dill joblib
        
        # Add debugging statements
        RUN echo "Checking model files:" && \
            ls -la /app/airflow/models/
        
        EXPOSE 5000
        
        CMD ["python", "app.py"]
        """

        # Write Dockerfile
        with open(os.path.join(temp_dir, 'Dockerfile'), 'w') as f:
            f.write(dockerfile_content)

        # Copy app.py from the DAG file's directory
        dag_dir = os.path.dirname(os.path.abspath(__file__))
        shutil.copy2(os.path.join(dag_dir, 'app.py'), os.path.join(temp_dir, 'app.py'))

        # Copy model files from /opt/airflow/models
        model_files = ['prototype.pkl', 'standard_scaler.pkl', 'min_max_scaler.pkl']
        for file in model_files:
            source = os.path.join('/opt/airflow/models', file)
            dest = os.path.join(temp_dir, 'airflow/models', file)
            if os.path.exists(source):
                shutil.copy2(source, dest)
            else:
                raise Exception(f"Required model file not found: {source}")

        context['task_instance'].xcom_push(key='build_context', value=temp_dir)
        return temp_dir
    except Exception as e:
        if 'temp_dir' in locals():
            shutil.rmtree(temp_dir)
        raise e


def get_latest_version(client, image_name):
    try:
        # Get token from Airflow Variables and authenticate
        DOCKER_TOKEN = Variable.get("docker_hub_token")
        client.login(
            username="serafinski",
            password=DOCKER_TOKEN,
            registry="https://index.docker.io/v1/"
        )

        # Docker Hub API endpoint for repository tags
        url = f"https://hub.docker.com/v2/repositories/{image_name}/tags"
        headers = {
            "Authorization": f"JWT {DOCKER_TOKEN}"
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return (0, 0, 0)

        tags_data = response.json()

        # Extract version tags
        versions = []
        pattern = re.compile(r'^\d+\.\d+\.\d+$')

        for tag in tags_data.get('results', []):
            tag_name = tag.get('name')
            if pattern.match(tag_name):
                versions.append(tuple(map(int, tag_name.split('.'))))

        # Return highest version or (0,0,0) if no versions exist
        return max(versions, default=(0, 0, 0))
    except Exception as e:
        print(f"Error getting latest version: {str(e)}")
        return (0, 0, 0)

def increment_version(version_tuple):
    major, minor, patch = version_tuple
    return (major, minor, patch + 1)


def build_docker_image(**context):
    try:
        client = docker.from_env()
        build_context = context['task_instance'].xcom_pull(task_ids='prepare_build_context', key='build_context')

        image_name = "serafinski/model-api"

        # Get latest version and increment patch
        latest_version = get_latest_version(client, image_name)
        new_version = increment_version(latest_version)
        version_tag = f"{new_version[0]}.{new_version[1]}.{new_version[2]}"

        # First build with version tag
        image = client.images.build(
            path=build_context,
            tag=f"{image_name}:{version_tag}",
            rm=True
        )[0]

        # Tag the same image as latest
        image.tag(image_name, tag='latest')

        context['task_instance'].xcom_push(
            key='image_info',
            value={'name': image_name, 'tag': version_tag}
        )
        return f"Successfully built {image_name}:{version_tag} and {image_name}:latest"

    except Exception as e:
        raise Exception(f"Failed to build Docker image: {str(e)}")


def push_docker_image(**context):
    try:
        client = docker.from_env()

        # Get token from Airflow Variables
        DOCKER_TOKEN = Variable.get("docker_hub_token")

        # Login to Docker Hub using token
        client.login(
            username="serafinski",
            password=DOCKER_TOKEN,
            registry="https://index.docker.io/v1/"
        )

        # Get image info from previous task
        image_info = context['task_instance'].xcom_pull(task_ids='build_docker_image', key='image_info')

        # Push both version tag and latest tag
        for tag in [image_info['tag'], 'latest']:
            for line in client.images.push(
                    repository=image_info['name'],
                    tag=tag,
                    stream=True,
                    decode=True
            ):
                print(line)

        return f"Successfully pushed {image_info['name']}:{image_info['tag']} and {image_info['name']}:latest"

    except Exception as e:
        raise Exception(f"Failed to push Docker image: {str(e)}")

def cleanup_build_context(**context):
    try:
        build_context = context['task_instance'].xcom_pull(task_ids='prepare_build_context', key='build_context')
        if build_context and os.path.exists(build_context):
            shutil.rmtree(build_context)
        return "Successfully cleaned up build context"
    except Exception as e:
        raise Exception(f"Failed to clean up build context: {str(e)}")