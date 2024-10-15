import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import os
import json
import logging

# Konfiguracja loggera
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("log.txt"),
                        logging.StreamHandler()
                    ])

# Stała nazwa pliku CSV
CSV_FILE_NAME = 'data_student_24353.csv'
SPREADSHEET_ID = '1C9GtNQvC53pChj1AOuYgraXO7C8fIGR7Sn5PnEuoKPk'

# Konfiguracja Google Sheets API
def connect_to_sheets():
    # Pobierz dane uwierzytelniające z secretów GitHub lub lokalnie
    logging.info("Rozpoczęcie uwierzytelniania do Google Sheets")
    creds_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
    creds_data = json.loads(creds_json)

    # Scope na dla Google Sheets API
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

    # Uwierzytelnienie konta usługi z ustawionym scope
    creds = Credentials.from_service_account_info(creds_data, scopes=scopes)
    client = gspread.authorize(creds)
    logging.info("Uwierzytelnienie zakończone pomyślnie")
    return client


# Funkcja przesyłająca dane z CSV do Google Sheets
def upload_csv_to_google_sheets():
    # Połącz z Google Sheets
    client = connect_to_sheets()

    # Otwórz Google Sheet
    try:
        # Otwiera pierwszy arkusz w pliku
        sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    except gspread.SpreadsheetNotFound:
        logging.error(f"Arkusz o {SPREADSHEET_ID} nie istnieje!")
        return

    # Wyczyść arkusz przed przesłaniem nowych danych
    logging.info("Czyszczenie arkusza przed przesłaniem nowych danych")
    sheet.clear()

    # Wczytaj dane z pliku CSV
    logging.info(f"Wczytywanie danych z pliku {CSV_FILE_NAME}")
    df = pd.read_csv(CSV_FILE_NAME)

    # Zamień NaN na puste string'i
    df = df.fillna('')

    # Prześlij dane z DataFrame do Google Sheets
    logging.info("Przesyłanie danych do Google Sheets")
    sheet.update([df.columns.values.tolist()] + df.values.tolist())
    logging.info(f"Dane z pliku {CSV_FILE_NAME} zostały przesłane do Google Sheets!")


# Główna część skryptu
if __name__ == "__main__":
    logging.info("Rozpoczęcie procesu przesyłania danych z CSV do Google Sheets")
    upload_csv_to_google_sheets()
    logging.info("Proces przesyłania danych zakończony")