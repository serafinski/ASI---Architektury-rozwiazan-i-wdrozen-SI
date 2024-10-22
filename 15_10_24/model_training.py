import pandas as pd
from pycaret.regression import setup, compare_models, tune_model, plot_model, save_model, pull
import logging
import os

from markdown import MarkdownTableGenerator

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
            normalize=True,  # Normalizacja jest istotna dla modeli wrażliwych na skalę danych
            remove_outliers=True,  # PyCaret ma wbudowaną opcję usuwania outlierów, co może poprawić wyniki modelu
            train_size=0.8,  # Ustawienie zbioru treningowego na 80% danych
            fold=10,  # Walidacja krzyżowa na 10 foldach
            session_id=17  # Powtarzalność wyników
)

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

logger.info(f"Wybrano najlepszy model: {best_model}")
logger.info("PyCaret automatycznie porównał różne algorytmy regresji aby wybrać model z najlepszymi wynikami na podstawie metryk takich jak MAE, MSE, RMSE, R^2, RMSLE, MAPE i TT")

logger.info("Metryki oceny modelu:")
logger.info("MAE (Mean Absolute Error): Średnia wartość bezwzględnych różnic między rzeczywistymi a przewidywanymi wartościami. Im niższa wartość, tym lepsze dopasowanie modelu. Mniejsza wartość MAE oznacza lepszy model.")
logger.info("MSE (Mean Squared Error): Średnia kwadratów różnic między rzeczywistymi a przewidywanymi wartościami. Większa waga jest nadawana większym błędom. Mniejsza wartość MSE jest lepsza, ponieważ oznacza mniej odchyleń.")
logger.info("RMSE (Root Mean Squared Error): Pierwiastek kwadratowy z MSE. Daje wynik w tej samej skali co dane. Mniejsza wartość RMSE oznacza lepsze dopasowanie modelu.")
logger.info("R^2 (R-Squared): Proporcja wariancji w zależnej zmiennej wyjaśnionej przez model. Im wyższa wartość R^2, tym lepsze dopasowanie modelu. R^2 bliskie 1 oznacza bardzo dobre dopasowanie.")
logger.info("RMSLE (Root Mean Squared Log Error): Pierwiastek kwadratowy z błędu logarytmicznego. Mniejsza wartość RMSLE jest lepsza, szczególnie w przypadku, gdy zależy nam na karaniu większych błędów bardziej, ale ignorowaniu małych różnic.")
logger.info("MAPE (Mean Absolute Percentage Error): Średnia procentowa różnica między rzeczywistymi a przewidywanymi wartościami. Mniejsza wartość MAPE oznacza lepszy model, ponieważ mniejsze są odchylenia procentowe między przewidywanymi a rzeczywistymi wartościami.")
logger.info("TT (Sec) (Train Time): Całkowity czas treningu modelu. Mniejszy czas TT oznacza szybszy model, co jest korzystne, szczególnie w przypadku dużych zbiorów danych lub konieczności szybkich predykcji.")


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

# Zapisanie modelu po tuningu (lub oryginalnego, jeśli tuning nie poprawił wyników)
save_model(tuned_model, 'model')
logger.info(f"Model zapisany jako 'model.pkl'")

# Wykres feature importance
logger.info("Generowanie wykresu Feature Importance...")
plot_model(tuned_model, plot='feature', save=True)

# Zapisanie wykresu feature importance pod stałą nazwą
if os.path.exists('Feature Importance.png'):
    # Sprawdź, czy plik 'feature_importance.png' już istnieje
    if os.path.exists('feature_importance.png'):
        os.remove('feature_importance.png')  # Usuń istniejący plik
    os.rename('Feature Importance.png', 'feature_importance.png')

# Wykres learning curve
logger.info("Generowanie wykresu Learning Curve...")
plot_model(tuned_model, plot='learning', save=True)

if os.path.exists('Learning Curve.png'):
    # Sprawdź, czy plik 'feature_importance.png' już istnieje
    if os.path.exists('learning_curve.png'):
        os.remove('learning_curve.png')  # Usuń istniejący plik
    os.rename('Learning Curve.png', 'learning_curve.png')

# Wykres residuals
logger.info("Generowanie wykresu Residuals...")
plot_model(tuned_model, plot='residuals', save=True)



# Wykres prediction error
logger.info("Generowanie wykresu Prediction Error...")
plot_model(tuned_model, plot='error', save=True)

if os.path.exists('Prediction Error.png'):
    # Sprawdź, czy plik 'feature_importance.png' już istnieje
    if os.path.exists('prediction_error.png'):
        os.remove('prediction_error.png')  # Usuń istniejący plik
    os.rename('Prediction Error.png', 'prediction_error.png')


# Wykres Cooks Distance
logger.info("Generowanie wykresu Cooks Distance...")
plot_model(tuned_model, plot='cooks', save=True)

if os.path.exists('Cooks Distance.png'):
    # Sprawdź, czy plik 'feature_importance.png' już istnieje
    if os.path.exists('cooks_distance.png'):
        os.remove('cooks_distance.png')  # Usuń istniejący plik
    os.rename('Cooks Distance.png', 'cooks_distance.png')