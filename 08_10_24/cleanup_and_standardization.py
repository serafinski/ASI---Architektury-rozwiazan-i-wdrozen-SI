import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import json
import os
import csv
import logging

# Konfiguracja loggera
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("log.txt"),
                        logging.StreamHandler()
                    ])

SPREADSHEET_ID = '1C9GtNQvC53pChj1AOuYgraXO7C8fIGR7Sn5PnEuoKPk'
CSV_FILE_NAME = 'spreadsheets_24353.csv'
PROCESSED_CSV_FILE_NAME = 'data_student_24353_processed.csv'
REPORT_FILE_NAME = 'report.txt'

# Konfiguracja Google Sheets API
def connect_to_sheets():
    # Pobierz dane uwierzytelniające z secretów GitHub lub lokalnie
    logging.info("Rozpoczęcie uwierzytelniania do Google Sheets")
    creds_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
    creds_data = json.loads(creds_json)

    # Scope dla Google Sheets API
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

    # Uwierzytelnienie konta usługi z ustawionym scope
    creds = Credentials.from_service_account_info(creds_data, scopes=scopes)
    client = gspread.authorize(creds)
    logging.info("Uwierzytelnienie zakończone pomyślnie")
    return client

# Pobierz dane z Google Sheets i zapisz je jako plik CSV
def download_csv_from_google_sheets():
    client = connect_to_sheets()

    # Otwórz Google Sheet
    try:
        # Otwiera pierwszy arkusz w pliku
        sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    except gspread.SpreadsheetNotFound:
        logging.error(f"Arkusz o {SPREADSHEET_ID} nie istnieje!")
        return None

    # Pobierz wszystkie dane z arkusza
    rows = sheet.get_all_values()

    # Zapisz dane do pliku CSV
    with open(CSV_FILE_NAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    logging.info(f"Dane zostały pobrane z Google Sheets i zapisane jako '{CSV_FILE_NAME}'.")

# Funkcja do odczytu danych z pliku CSV
def read_data_from_csv():
    logging.info(f"Odczyt danych z pliku '{CSV_FILE_NAME}'")
    df = pd.read_csv(CSV_FILE_NAME)
    logging.info(f"Odczytano {len(df)} wierszy i {len(df.columns)} kolumn")
    return df

# Czyszczenie danych
def cleanup(df):
    logging.info("Rozpoczęcie czyszczenia danych")
    original_length = len(df)
    original_cells = original_length * len(df.columns)

    # Usunięcie wierszy, gdzie brak ponad 50% danych
    df_cleaned = df.dropna(thresh=len(df.columns) // 2).copy()
    cleaned_length = len(df_cleaned)
    cells_removed = (original_length - cleaned_length) * len(df.columns)

    # Zaktualizowana liczba braków po usunięciu wierszy
    missing_after_removal = df_cleaned.isnull().sum().sum()

    # Zastąp przecinki w liczbach na kropki i przekonwertuj kolumny na liczby zmiennoprzecinkowe
    df_cleaned['Średnie Zarobki'] = df_cleaned['Średnie Zarobki'].replace(',', '.', regex=True).astype(float)

    # Uzupełnianie brakujących wartości
    df_cleaned['Wiek'] = df_cleaned['Wiek'].fillna(df_cleaned['Wiek'].median()).astype(int)
    df_cleaned['Średnie Zarobki'] = df_cleaned['Średnie Zarobki'].fillna(df_cleaned['Średnie Zarobki'].median())
    df_cleaned[['Płeć', 'Wykształcenie', 'Cel Podróży']] = df_cleaned[['Płeć', 'Wykształcenie', 'Cel Podróży']].fillna(
        'BRAK')
    df_cleaned[['Czas Początkowy Podróży', 'Czas Końcowy Podróży']] = df_cleaned[
        ['Czas Początkowy Podróży', 'Czas Końcowy Podróży']].fillna('00:00')

    total_changed_cells = missing_after_removal  # Uzupełniono dokładnie tyle braków, ile zostało po usunięciu wierszy

    # Nowa liczba komórek po usunięciu
    total_cells_after_removal = cleaned_length * len(df_cleaned.columns)

    percent_removed = (cells_removed / original_cells) * 100

    logging.info(f"Czyszczenie zakończone. Usunięto {cells_removed} komórek.")
    logging.info(f"Czyszczenie zakończone. Uzupełniono {total_changed_cells} komórek.")

    return df_cleaned, percent_removed, total_changed_cells, total_cells_after_removal, cells_removed


# Standaryzacja średnich zarobków
def standardize(df):
    logging.info("Rozpoczęcie standaryzacji danych")
    zarobki_col = 'Średnie Zarobki'

    # Obliczenie średniej i odchylenia standardowego przed standaryzacją
    mean_value = df[zarobki_col].mean()
    std_value = df[zarobki_col].std()

    # Standaryzacja = (wartość - średnia) / odchylenie standardowe
    df[zarobki_col] = (df[zarobki_col] - mean_value) / std_value

    # Liczba zmienionych komórek po standaryzacji to liczba wierszy
    stand_cells_changed = len(df)

    logging.info(f"Standaryzacja zakończona. Standaryzowano {stand_cells_changed} komórek.")

    return df, stand_cells_changed


# Funkcja do generowania raportu
def generate_report(percent_removed, cells_removed, total_changed_cells, total_cells_after_removal,
                    stand_cells_changed):
    # Całkowita liczba zmodyfikowanych komórek (uzupełnione braki + standaryzacja)
    total_changed = total_changed_cells + stand_cells_changed

    # Procent zmodyfikowanych komórek względem zmniejszonej liczby komórek po usunięciu
    percent_modified = (total_changed / total_cells_after_removal) * 100

    # Procent komórek poddanych standaryzacji
    percent_standardized = (stand_cells_changed / total_cells_after_removal) * 100

    report_content = (
        f"Raport przetwarzania danych:\n"
        f"Procent usuniętych danych: {percent_removed:.2f}%\n"
        f"Liczba usuniętych komórek: {cells_removed} z {total_cells_after_removal + cells_removed}\n\n"

        f"Procent zmodyfikowanych danych (uzupełnione braki): {(total_changed_cells / total_cells_after_removal) * 100:.2f}%\n"
        f"Liczba zmodyfikowanych komórek (uzupełnione braki): {total_changed_cells} z {total_cells_after_removal}\n\n"

        f"Procent komórek poddanych standaryzacji: {percent_standardized:.2f}%\n\n"
        f"Liczba komórek poddanych standaryzacji: {stand_cells_changed} z {total_cells_after_removal}\n"

        f"Procent zmodyfikowanych komórek (standaryzacja + uzupełnione braki): {percent_modified:.2f}%\n"
        f"Liczba zmodyfikowanych komórek (standaryzacja + uzupełnione braki): {total_changed} z {total_cells_after_removal}\n"
    )
    with open(REPORT_FILE_NAME, "w") as report_file:
        report_file.write(report_content)

    logging.info(f"Raport został zapisany jako '{REPORT_FILE_NAME}'.")

# Funkcja główna: czyszczenie i standaryzacja
def process_data():
    # Odczyt danych z pliku CSV
    df = read_data_from_csv()

    # Czyszczenie danych, zmienne raportu
    df_cleaned, percent_removed, total_changed_cells, total_cells_after_removal, cells_removed = cleanup(df)

    # Standaryzacja
    df_standardized, stand_cells_changed = standardize(df_cleaned)

    # Generowanie raportu
    generate_report(percent_removed, cells_removed, total_changed_cells, total_cells_after_removal, stand_cells_changed)
    return df_standardized

# Zapisz przetworzone dane do nowego pliku CSV
def return_data(df):
    df.to_csv(PROCESSED_CSV_FILE_NAME, index=False)
    logging.info(f"Dane zostały zapisane do pliku '{PROCESSED_CSV_FILE_NAME}'.")

if __name__ == "__main__":
    logging.info("Rozpoczęcie procesu przetwarzania danych")

    # Pobierz dane z Google Sheets i zapisz je jako CSV
    download_csv_from_google_sheets()

    # Procesowanie danych
    data = process_data()

    # Zapisz przetworzone dane do pliku CSV
    return_data(data)

    logging.info("Zakończono proces przetwarzania danych")