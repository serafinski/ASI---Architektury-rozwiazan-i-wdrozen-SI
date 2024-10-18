import matplotlib.pyplot as plt
import seaborn as sns
import logging

# Konfiguracja loggera
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("visualization.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()

class Visualization:
    def __init__(self, df):
        self.df = df

    def plot_histogram(self, column, title, filename):
        self.df[[column]].hist(figsize=(12, 10))
        plt.suptitle(title)
        plt.savefig(filename)
        logging.info(f"Zapisano histogram jako {filename}")
        plt.close()

    def plot_scatter_plots(self, x_col, y_cols, titles, filename):
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.flatten()
        for i, y_col in enumerate(y_cols):
            sns.scatterplot(x=self.df[x_col], y=self.df[y_col], ax=axes[i])
            axes[i].set_title(titles[i])
        plt.tight_layout()
        plt.savefig(filename)
        logging.info(f"Zapisano wykresy punktowe jako {filename}")
        plt.close()

    def plot_categorical_distributions(self, categorical_columns, title_map, filename, label_map=None):
        if label_map:
            n_rows, n_cols = 3, 3  # Fixed 3x3 grid when label_map is provided
        else:
            n_cols = 4  # Define the number of columns dynamically
            n_rows = (len(categorical_columns) + n_cols - 1) // n_cols  # Dynamic number of rows without label_map

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 5 * n_rows))  # Adjust the figure size accordingly
        axes = axes.flatten()  # Flatten the axes array for easier indexing

        for i, col in enumerate(categorical_columns):
            if label_map and col in label_map:
                # Map values using label_map if available
                plot_data = self.df[col].map(label_map[col])
            else:
                plot_data = self.df[col]

            # Sort the labels alphabetically before plotting
            sorted_categories = sorted(plot_data.unique())

            sns.countplot(x=plot_data, ax=axes[i], order=sorted_categories)
            axes[i].set_title(f"Rozkład kategorii dla {title_map.get(col, col)}")
            axes[i].tick_params(axis='x', rotation=45)

        # Remove any extra axes if there are fewer plots than available slots
        for j in range(len(categorical_columns), len(axes)):
            fig.delaxes(axes[j])

        plt.tight_layout()
        plt.savefig(filename)
        logging.info(f"Zapisano wykresy dla zmiennych kategorycznych jako {filename}")
        plt.close()