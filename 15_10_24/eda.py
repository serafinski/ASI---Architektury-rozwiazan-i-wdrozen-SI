import pandas as pd
import logging
from visualization import Visualization
from markdown import MarkdownTableGenerator

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

with open("missing.txt", "w") as f:
    missing_description = pd.DataFrame({
        'index': missing_values.index,
        'Missing Values': missing_values.values,
        'Missing Percentage': missing_percentage.values
    })

    # Generowanie tabeli markdown
    table_generator = MarkdownTableGenerator(missing_description)
    f.write(table_generator.generate_markdown_table())

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

# Zapisanie wyników analizy numerycznej w formacie Markdown (tabele)
with open("pre_numeric_analysis.txt", "w") as f:
    numeric_description = df.describe().transpose()
    table_generator = MarkdownTableGenerator(numeric_description.reset_index())
    f.write(table_generator.generate_markdown_table())

# Zapisanie wyników analizy kategorycznej w formacie Markdown (tabele)
with open("pre_categorical_analysis.txt", "w") as f:
    categorical_description = df.describe(include=['object']).transpose()
    table_generator = MarkdownTableGenerator(categorical_description.reset_index())
    f.write(table_generator.generate_markdown_table())

# Zapisanie rozkładu zmiennych kategorycznych w formacie Markdown
with open("pre_categorical_distribution.txt", "w") as f:
    for col in ['gender', 'ethnicity', 'fcollege', 'mcollege', 'home', 'urban', 'income', 'region']:
        f.write(f"Dystrybucja dla zmiennej {col}:\n\n")
        value_counts = df[col].value_counts().reset_index()
        value_counts.columns = [col, 'count']
        table_generator = MarkdownTableGenerator(value_counts)
        f.write(table_generator.generate_markdown_table())
        f.write("\n")