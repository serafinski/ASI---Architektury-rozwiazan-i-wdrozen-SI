import pandas as pd
from sklearn.model_selection import train_test_split
import logging

# Konfiguracja loggera
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("split_data.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()


# Ustawienie wyświetlania wszystkich kolumn
pd.set_option('display.max_columns', None)

logger.info("Wczytywanie danych")
data = pd.read_csv("bank-additional-full.csv", sep=';')

# Podstawowe statystyki dla całego zestawu danych
logger.info("Podstawowe statystyki dla całego zestawu danych:\n%s", data.describe())

# Podział na zestawy treningowy (70%) i testowy (30%)
train_data, test_data = train_test_split(data, test_size=0.3, random_state=17)

# Wypisanie podstawowych statystyk dla obu zestawów
logger.info("\nPodstawowe statystyki dla zestawu treningowego:\n%s", train_data.describe())
logger.info("\nPodstawowe statystyki dla zestawu testowego:\n%s", test_data.describe())

# Zapisanie zestawów do plików CSV
logger.info("Zapisywanie zestawów do plików CSV")
train_data.to_csv("train_data.csv", index=False)
logger.info("Zapisano zestaw treningowy do pliku train_data.csv")
test_data.to_csv("test_data.csv", index=False)
logger.info("Zapisano zestaw testowy do pliku test_data.csv")