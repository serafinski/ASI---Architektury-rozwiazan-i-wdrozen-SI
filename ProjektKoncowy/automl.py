import pandas as pd
from pycaret.classification import setup, compare_models, tune_model, pull, get_config, predict_model, save_model
from sklearn.metrics import accuracy_score, mean_absolute_error
import logging

from markdown import MarkdownTableGenerator

# Konfiguracja loggera
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("automl.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()

# Wczytanie danych
logger.info("Wczytywanie danych z 'train_data_cleaned.csv'")
df = pd.read_csv('train_data_cleaned.csv')

binary_mapping = {
    'housing': {'yes': 1, 'no': 0},
    'loan': {'yes': 1, 'no': 0},
    'contact': {'cellular': 1, 'telephone': 0},
    'y': {'yes': 1, 'no': 0},
    'default': {'no': 0, 'unknown': 1},
}

df.replace(binary_mapping, inplace=True)

df = pd.get_dummies(df, columns=['marital','poutcome'], drop_first=True)

# Convert all boolean columns to integers (0 and 1)
df = df.astype({col: 'int' for col in df.select_dtypes('bool').columns})

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



# Ustawienia PyCaret'a
logger.info("Ustawienia PyCaret'a")
cla = setup(data = df,
            target= 'y',
            categorical_features=categorical_features,
            numeric_features=numeric_features,
            normalize=True,
            remove_outliers=True,
            train_size=0.7,
            fold=10,
            session_id=17)

logger.info("PyCaret automatycznie przetwarza dane: zastosowano normalizacje i usunięcie outlierów, aby poprawić wyniki modeli.")

# Porównanie modeli i wybór najlepszego
logger.info("Porównywanie modeli w celu wyboru najlepszego...")
best_model = compare_models()

# Pobranie metryk porównania modeli
comparison_metrics = pull()

# Zapis metryk do pliku CSV
comparison_metrics.to_csv('comparison_metrics.csv', index=False)
logger.info("Metryki porównania modeli zapisane do pliku 'comparison_metrics.csv'")

with open('comparison_metrics.txt', 'w') as f:
    df2 = pd.read_csv("comparison_metrics.csv")
    table_generator = MarkdownTableGenerator(df2)
    markdown_table = table_generator.generate_markdown_table()
    f.write(markdown_table)

# Tunowanie najlepszego modelu
logger.info("Tunowanie najlepszego modelu...")
tuned_model = tune_model(best_model)

# Pobranie metryk tuningu
tuning_metrics = pull()

# Zapis metryk tuningu do pliku CSV
tuning_metrics.to_csv('tuning_metrics.csv', index=True)
logger.info("Metryki tuningu zapisane do pliku 'tuning_metrics.csv'")

with open('tuning_metrics.txt', 'w') as f:
    df2 = pd.read_csv("tuning_metrics.csv")
    table_generator = MarkdownTableGenerator(df2)
    markdown_table = table_generator.generate_markdown_table()
    f.write(markdown_table)

logger.info("Tunowanie hiperparametrów zostało zakończone. PyCaret automatycznie wybrał model, który osiąga najlepsze wyniki — jeśli tuning nie poprawił wyników, oryginalny model zostaje zachowany.")

logger.info("Podział danych na zbiór treningowy i walidacyjny (70/30)...")

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

# zapisanie metryk do pliku
with open('metrics.txt', 'w') as f:
    f.write(f'* Dokładność modelu: {accuracy}\n')
    f.write(f'* Średni błąd bezwzględny (MAE): {mae}\n')

# Zapisanie modelu
save_model(tuned_model, 'prototype')
logger.info("Model został zapisany jako 'prototype'.")