import pandas as pd
import logging
from visualization import Visualization

# Konfiguracja loggera
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("analysis.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()

# Ustawienie wyświetlania wszystkich kolumn
pd.set_option('display.max_columns', None)

# Wczytywanie danych
df = pd.read_csv('CollegeDistance.csv')
vis = Visualization(df)

# Podgląd danych
logger.info("Podgląd pierwszych 5 wierszy danych:")
logger.info(df.head())

# Procent brakujących wartości
missing_values = df.isnull().sum()
missing_percentage = (missing_values / len(df)) * 100
logger.info("\nProcent brakujących wartości w każdej kolumnie:")
logger.info(missing_percentage)

# Usunięcie kolumny 'rownames', ponieważ służy tylko do numeracji
if 'rownames' in df.columns:
    df = df.drop('rownames', axis=1)

# Analiza statystyczna zmiennych numerycznych
logger.info("\nOpis statystyczny danych numerycznych:")
logger.info(df.describe())

# Analiza zmiennych kategorycznych
logger.info("\nOpis zmiennych kategorycznych:")
logger.info(df.describe(include=['object']))

# Tworzenie wykresów

# Histogramy dla zmiennych numerycznych
vis.plot_histogram('score', "Histogram dla zmiennej score", "histogram.png")

# Tworzenie 1 wykresu z 4 mniejszymi wykresami punktowymi (scatter plots)
vis.plot_scatter_plots('score', ['wage', 'unemp', 'distance', 'tuition'],
                              ["Score vs Wage", "Score vs Unemp", "Score vs Distance", "Score vs Tuition"],
                              'scatter_plots.png')

# Tworzenie wykresów dla zmiennych kategorycznych w jednym obrazku
categorical_columns = df.select_dtypes(include=['object']).columns
vis.plot_categorical_distributions(categorical_columns, {},'distribution.png')

# Eksploracja zmiennych kategorycznych: Sprawdzenie dystrybucji dla 'gender', 'ethnicity', 'fcollege', 'mcollege', 'home', 'urban', 'income', 'region'
for col in ['gender', 'ethnicity', 'fcollege', 'mcollege', 'home', 'urban', 'income', 'region']:
    logger.info(f"\nDystrybucja dla zmiennej {col}:")
    logger.info(df[col].value_counts())


# Funkcja do generowania tabeli w formacie Markdown
def generate_markdown_table(dataframe):
    # Tworzenie nagłówka tabeli
    markdown_table = '| ' + ' | '.join(dataframe.columns) + ' |\n'
    markdown_table += '| ' + ' | '.join(['---'] * len(dataframe.columns)) + ' |\n'

    # Tworzenie wierszy tabeli
    for index, row in dataframe.iterrows():
        markdown_table += '| ' + ' | '.join(row.astype(str)) + ' |\n'
    return markdown_table


# Zapisanie wyników analizy numerycznej w formacie Markdown (tabele)
with open("pre_numeric_analysis.txt", "w") as f:
    numeric_description = df.describe().transpose()
    f.write(generate_markdown_table(numeric_description.reset_index()))

# Zapisanie wyników analizy kategorycznej w formacie Markdown (tabele)
with open("pre_categorical_analysis.txt", "w") as f:
    categorical_description = df.describe(include=['object']).transpose()
    f.write(generate_markdown_table(categorical_description.reset_index()))

# Zapisanie rozkładu zmiennych kategorycznych w formacie Markdown
with open("pre_categorical_distribution.txt", "w") as f:
    for col in ['gender', 'ethnicity', 'fcollege', 'mcollege', 'home', 'urban', 'income', 'region']:
        f.write(f"Dystrybucja dla zmiennej {col}:\n\n")
        value_counts = df[col].value_counts().reset_index()
        value_counts.columns = [col, 'count']
        f.write(generate_markdown_table(value_counts))
        f.write("\n")