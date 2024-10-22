import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import logging
from visualization import Visualization
from markdown import MarkdownTableGenerator

# Konfiguracja loggera
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("feature_engineering.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()

# Ustawienie wyświetlania wszystkich kolumn
pd.set_option('display.max_columns', None)

# Wczytywanie danych
logger.info("Wczytywanie danych z pliku CSV...")
df = pd.read_csv('CollegeDistance.csv')
logger.info(f"Dane załadowane: {df.shape[0]} wierszy, {df.shape[1]} kolumn")

# Usunięcie kolumny 'rownames', ponieważ nie jest potrzebna
if 'rownames' in df.columns:
    logger.info("Usunięcie kolumny 'rownames' (kolumna numeracyjna, zbędna dla analizy)...")
    df = df.drop('rownames', axis=1)

# Zmienne do konwersji
logger.info("Rozpoczynamy przetwarzanie zmiennych...")

# Kodowanie zmiennej 'ethnicity' na dwie zmienne 'hispanic' i 'afam'
logger.info("Konwertowanie zmiennej 'ethnicity' na dwie zmienne: 'hispanic' i 'afam'")
df['hispanic'] = df['ethnicity'].apply(lambda x: 1 if x == 'hispanic' else 0)
df['afam'] = df['ethnicity'].apply(lambda x: 1 if x == 'afam' else 0)
df = df.drop('ethnicity', axis=1)

# Kodowanie zmiennej 'gender': 1 dla mężczyzn, 0 dla kobiet
logger.info("Kodowanie zmiennej 'gender': 1 dla mężczyzn, 0 dla kobiet")
df['gender'] = df['gender'].apply(lambda x: 1 if x == 'male' else 0)

# Kodowanie zmiennych binarnych: 'fcollege', 'mcollege', 'home', 'urban': 1 dla 'yes', 0 dla 'no'
binary_features = ['fcollege', 'mcollege', 'home', 'urban']
logger.info(f"Kodowanie binarnych zmiennych: {binary_features}")
for feature in binary_features:
    df[feature] = df[feature].apply(lambda x: 1 if x == 'yes' else 0)

# Kodowanie zmiennej 'income': 1 dla 'high', 0 dla 'low'
logger.info("Kodowanie zmiennej 'income': 1 dla 'high', 0 dla 'low'")
df['income'] = df['income'].apply(lambda x: 1 if x == 'high' else 0)

# Kodowanie zmiennej 'region': 1 dla 'west', 0 dla innych
logger.info("Kodowanie zmiennej 'region': 1 dla 'west', 0 dla innych")
df['region'] = df['region'].apply(lambda x: 1 if x == 'west' else 0)

# Obliczanie średnich arytmetycznych dla każdej kolumny przed usunięciem outlierów
logger.info("Obliczanie średnich arytmetycznych dla każdej zmiennej przed usunięciem outlierów...")
column_means_before = df.mean()
logger.info(f"Średnie arytmetyczne kolumn przed usunięciem outlierów:\n{column_means_before}")

# Obliczanie macierzy korelacji
logger.info("Obliczanie macierzy korelacji dla zmiennych...")
correlation_matrix = df.corr().round(2)

# Zamiana wartości NA (jeśli występują) na 0
logger.info("Zamiana wartości NA w macierzy korelacji na 0")
correlation_matrix = correlation_matrix.fillna(0)

# Wyświetlenie podsumowania macierzy korelacji
logger.info("Podsumowanie macierzy korelacji:")
logger.info(f"\n{correlation_matrix.head()}")

# Wizualizacja korelacji za pomocą heatmapy
logger.info("Tworzenie wizualizacji korelacji (heatmapa)")
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Heatmap - College Distance Data')
plt.tight_layout()

# Zapisanie heatmapy do pliku
heatmap_file = 'correlation_heatmap.png'
plt.savefig(heatmap_file)
logger.info(f"Zapisano heatmapę korelacji do pliku: {heatmap_file}")


# Dodanie logiki usuwania outlierów
def get_unusual_points(model, df):
    influence = model.get_influence()
    leverage = influence.hat_matrix_diag
    residuals = np.abs(influence.resid_studentized_internal)
    cooks_d = influence.cooks_distance[0]

    # Kryteria nietypowych punktów
    leverage_threshold = 2 * np.mean(leverage)
    residual_threshold = 2
    cooks_d_threshold = 4 / len(df)

    high_leverage_points = np.where(leverage > leverage_threshold)[0]
    large_residual_points = np.where(residuals > residual_threshold)[0]
    influential_points = np.where(cooks_d > cooks_d_threshold)[0]

    return np.unique(np.concatenate((high_leverage_points, large_residual_points, influential_points)))


# Tworzenie modelu dla outlierów
X = df[['gender', 'fcollege', 'mcollege', 'home', 'urban', 'wage', 'distance', 'tuition', 'education', 'income',
        'hispanic', 'afam']]
X = sm.add_constant(X)
y = df['score']
model = sm.OLS(y, X).fit()

# Usuwanie outlierów
min_data_points = 2000
while len(df) > min_data_points:
    unusual_points = get_unusual_points(model, df)

    if len(df) - len(unusual_points) < min_data_points or len(unusual_points) == 0:
        break

    df = df.drop(df.index[unusual_points])

    # Ponowne dopasowanie modelu po usunięciu outlierów
    X = df[['gender', 'fcollege', 'mcollege', 'home', 'urban', 'wage', 'distance', 'tuition', 'education', 'income',
            'hispanic', 'afam']]
    X = sm.add_constant(X)
    y = df['score']
    model = sm.OLS(y, X).fit()

# Zapisanie przetworzonych danych do pliku CSV
output_file = 'CollegeDistance_processed.csv'
df.to_csv(output_file, index=False)
logger.info(f"Zapisano przetworzone dane do pliku CSV: {output_file}")

# Ponowna generacja wykresów po usunięciu outlierów
vis = Visualization(df)
vis.plot_histogram('score', "Histogram dla zmiennej score po usunięciu outlierów", "histogram_processed.png")

vis.plot_scatter_plots('score', ['wage', 'unemp', 'distance', 'tuition'],
                              ["Score vs Wage", "Score vs Unemp", "Score vs Distance", "Score vs Tuition"],
                              'scatter_plots_processed.png')

# Tworzenie wykresów dla zmiennych kategorycznych w jednym obrazku
categorical_columns = ['gender', 'fcollege', 'mcollege', 'home', 'urban', 'income', 'region', 'hispanic', 'afam']

# Mapa zamiany wartości 0 i 1 na etykiety dla poszczególnych zmiennych
label_map = {
    'gender': {1: 'male', 0: 'female'},
    'fcollege': {1: 'yes', 0: 'no'},
    'mcollege': {1: 'yes', 0: 'no'},
    'home': {1: 'yes', 0: 'no'},
    'urban': {1: 'yes', 0: 'no'},
    'income': {1: 'high', 0: 'low'},
    'region': {1: 'west', 0: 'other'},
    'hispanic': {1: 'hispanic', 0: 'non-hispanic'},
    'afam': {1: 'afam', 0: 'non-afam'}
}

vis.plot_categorical_distributions(categorical_columns, {}, 'distribution_processed.png', label_map=label_map)

# Obliczanie średnich arytmetycznych dla każdej kolumny po usunięciu outlierów
column_means_after = df.mean()
logger.info(f"Średnie arytmetyczne kolumn po usunięciu outlierów:\n{column_means_after}")

# Analiza statystyczna zmiennych numerycznych
logger.info("\nOpis statystyczny danych numerycznych (po usunięciu outlierów):")
logger.info(df.describe())

# Opis statystyczny danych kategorycznych
logger.info("Opis zmiennych kategorycznych:")

categorical_description = {}

for col in categorical_columns:
    # Sprawdzanie i mapowanie wartości binarnych na etykiety
    if col in label_map:
        mapped_values = df[col].map(label_map[col])
        description = mapped_values.describe().to_string()
        categorical_description[col] = description
        logger.info(f"\n{description}")
    else:
        description = df[col].describe().to_string()
        categorical_description[col] = description
        logger.info(f"\n{description}")


# Eksploracja zmiennych kategorycznych: Sprawdzenie dystrybucji dla 'gender', 'ethnicity', 'fcollege', 'mcollege', 'home', 'urban', 'income', 'region'
# Zmapowanie wartości binarnych na etykiety przy logowaniu dystrybucji
for col in categorical_columns:
    logger.info(f"\nDystrybucja dla zmiennej {col}:")

    # Mapowanie wartości binarnych na etykiety
    if col in label_map:
        mapped_values = df[col].map(label_map[col])
        logger.info(mapped_values.value_counts())
    else:
        # Dla zmiennych, które nie mają mapowania (na wszelki wypadek)
        logger.info(df[col].value_counts())


# Lista zmiennych binarnych, które logicznie są kategoryczne
binary_categorical_columns = ['gender', 'fcollege', 'mcollege', 'home', 'urban', 'income', 'region', 'hispanic', 'afam']


with open("post_numeric_analysis.txt", "w") as f:
    numeric_columns = ['score', 'unemp', 'wage', 'distance', 'tuition', 'education']
    numeric_description_after = df[numeric_columns].describe().transpose()
    table_generator = MarkdownTableGenerator(numeric_description_after.reset_index())
    f.write(table_generator.generate_markdown_table())

with open("post_categorical_distribution.txt", "w") as f:
    # Eksploracja zmiennych kategorycznych
    for col in binary_categorical_columns:
        f.write(f"Dystrybucja dla zmiennej {col}:\n\n")

        # Zastosowanie mapowania wartości 0/1 na etykiety
        if col in label_map:
            value_counts = df[col].map(label_map[col]).value_counts().reset_index()
            value_counts.columns = [col, 'count']
        else:
            value_counts = df[col].value_counts().reset_index()
            value_counts.columns = [col, 'count']

        # Tworzenie i zapisanie tabeli w formacie Markdown
        table_generator = MarkdownTableGenerator(value_counts)
        f.write(table_generator.generate_markdown_table())
        f.write("\n")

# Mapowanie wartości binarnych na etykiety przed analizą kategoryczną
for col in binary_categorical_columns:
    if col in label_map:
        df[col] = df[col].map(label_map[col])

# Zapisanie wyników analizy kategorycznej w formacie Markdown (tabele)
with open("post_categorical_analysis.txt", "w") as f:
    # Analiza kategoryczna
    categorical_description_after = df[binary_categorical_columns].astype('category').describe().transpose()
    table_generator = MarkdownTableGenerator(categorical_description_after.reset_index())
    f.write(table_generator.generate_markdown_table())