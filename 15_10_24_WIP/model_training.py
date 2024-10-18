import pandas as pd
from pycaret.regression import setup, compare_models, tune_model, plot_model
import logging
import os

# Konfiguracja loggera
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("model_training.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()

# Wczytanie danych
logger.info("Wczytywanie danych z 'CollegeDistance_processed.csv'")
df = pd.read_csv('CollegeDistance_processed.csv')

# Dodanie nowych zmiennych z interakcjami i wielomianami
logger.info("Dodawanie nowych cech do dataset'u")
df['gender_education_interaction'] = df['gender'] * df['education']
df['tuition_education_interaction'] = df['tuition'] * df['education']

# Ustawienia PyCaret'a
logger.info("Ustawienia PyCaret'a")
reg = setup(data=df,
            target='score',
            categorical_features=['gender', 'fcollege', 'mcollege', 'home', 'urban', 'region', 'hispanic', 'afam'],
            numeric_features=['unemp', 'wage', 'distance', 'tuition', 'education', 'gender_education_interaction', 'tuition_education_interaction'],
            normalize=True,
            remove_outliers=True,  # PyCaret's built-in option for outlier removal
            train_size=0.8,
            fold=10,
            session_id=17
)

# Porównanie modeli i wybór najlepszego
logger.info("Porównywanie modeli w celu wyboru najlepszego...")
best_model = compare_models()

# Tunowanie najlepszego modelu
logger.info("Tunowanie najlepszego modelu...")
tuned_model = tune_model(best_model)

# Wykres feature importance
plot_model(best_model, plot='feature', save=True)

# Zmień nazwę pliku na 'feature_importance.png'
if os.path.exists('Feature Importance.png'):
    os.rename('Feature Importance.png', 'feature_importance.png')

logger.info("Feature importance plot saved as 'feature_importance.png'")