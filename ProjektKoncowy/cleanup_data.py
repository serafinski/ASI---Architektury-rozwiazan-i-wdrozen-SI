import pandas as pd
import logging

from markdown import MarkdownTableGenerator

# Konfiguracja loggera
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("cleanup_data.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# Wczytanie danych
df = pd.read_csv('train_data.csv')


suma = 0
# Usuń wiersze, gdzie kolumna 'job' ma wartość 'unknown'
initial_count = df.shape[0]
df = df[df['job'] != 'unknown']
removed_count = initial_count - df.shape[0]
suma += removed_count
logger.info(f"Usunięto {removed_count} wierszy, gdzie 'job' miało wartość 'unknown'.")

post_job_count = df.shape[0]
df = df[df['marital'] != 'unknown']
removed_count = post_job_count - df.shape[0]
suma += removed_count
logger.info(f"Usunięto {removed_count} wierszy, gdzie 'marital' miało wartość 'unknown'.")

post_marital_count = df.shape[0]
df = df[df['education'] != 'unknown']
removed_count = post_marital_count - df.shape[0]
suma += removed_count
logger.info(f"Usunięto {removed_count} wierszy, gdzie 'education' miało wartość 'unknown'.")

post_education_count = df.shape[0]
df = df[df['housing'] != 'unknown']
removed_count = post_education_count - df.shape[0]
suma += removed_count
logger.info(f"Usunięto {removed_count} wierszy, gdzie 'housing' miało wartość 'unknown'.")

post_housing_count = df.shape[0]
df = df[df['loan'] != 'unknown']
removed_count = post_housing_count - df.shape[0]
suma += removed_count
logger.info(f"Usunięto {removed_count} wierszy, gdzie 'loan' miało wartość 'unknown'.")

post_loan_count = df.shape[0]
df = df[df['default'] != 'yes']
removed_count += post_loan_count - df.shape[0]
suma += removed_count
logger.info(f"Usunięto {removed_count} wiersze, gdzie 'default' miało wartość 'yes'.")

logger.info(f"Łącznie usunięto {suma} wierszy.")

# Drop the 'duration' column
df.drop(['duration'], axis=1, inplace=True)


# def display_unique_value_counts(df):
#     for column in df.columns:
#         logger.info(f"Kolumna '{column}' ma {df[column].nunique()} unikalnych wartości:")
#
#         # Wypisuje unikalne wartości oraz ich liczebność
#         value_counts = df[column].value_counts()
#         for value, count in value_counts.items():
#             logger.info(f"  Wartość: {value} - Wystąpienia: {count}")
#
#         logger.info("\n" + "-" * 50 + "\n")


# Wywołanie funkcji
# display_unique_value_counts(df)

# Zapisanie danych do pliku CSV
df.to_csv('train_data_cleaned.csv', index=False)
