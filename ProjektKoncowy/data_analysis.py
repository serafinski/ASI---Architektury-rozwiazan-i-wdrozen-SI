import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import math

from markdown import MarkdownTableGenerator

# Konfiguracja loggera
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data_analysis.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# Wczytanie danych
df = pd.read_csv('train_data.csv')

# Sprawdzenie rozkładu zmiennych numerycznych i kategorycznych
numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
# Zapisanie wyników analizy numerycznej w formacie Markdown (tabele)
with open("numeric_analysis.txt", "w") as f:
    numeric_description = df.describe().transpose()
    table_generator = MarkdownTableGenerator(numeric_description.reset_index())
    f.write(table_generator.generate_markdown_table())

# Kategoryczne kolumny
categorical_columns = df.select_dtypes(include=['object']).columns
with open("categorical_analysis.txt", "w") as f:
    categorical_description = df.describe(include=['object']).transpose()
    table_generator = MarkdownTableGenerator(categorical_description.reset_index())
    f.write(table_generator.generate_markdown_table())

# Analiza brakujących wartości
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


# Układ 4x3 dla histogramów (4 wiersze po 3 kolumny)
n_cols = 3
n_rows = math.ceil(len(numerical_columns) / n_cols)
fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(18, 4 * n_rows))
axes = axes.flatten()

for i, col in enumerate(numerical_columns):
    sns.histplot(df[col], kde=True, ax=axes[i])
    axes[i].set_title(f'Rozkład {col}')
    axes[i].set_xlabel(col)
    axes[i].set_ylabel('Częstość')

# Usunięcie pustych osi (jeśli liczba wykresów jest nieparzysta)
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.savefig("histograms.png")
plt.close()
logger.info("Histogramy dla zmiennych numerycznych zostały zapisane jako 'histograms.png'.")

# Układ 4x3 dla wykresów pudełkowych
fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(18, 4 * n_rows))
axes = axes.flatten()

for i, col in enumerate(numerical_columns):
    sns.boxplot(x=df[col], ax=axes[i])
    axes[i].set_title(f'Wykres pudełkowy {col}')
    axes[i].set_xlabel(col)

# Usunięcie pustych osi (jeśli liczba wykresów jest nieparzysta)
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.savefig("boxplots.png")
plt.close()
logger.info("Wykresy pudełkowe dla zmiennych numerycznych zostały zapisane jako 'boxplots.png'.")

# Macierz korelacji
plt.figure(figsize=(12, 10))
correlation_matrix = df[numerical_columns].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Macierz korelacji')
plt.xticks(rotation=45, ha='right')  # Obrót etykiet na osi x
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig("correlation_matrix.png")
plt.close()
logger.info("Macierz korelacji została zapisana jako 'correlation_matrix.png'.")
