import logging

# Konfiguracja loggera
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("markdown_table.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()

class MarkdownTableGenerator:
    def __init__(self, df):
        self.df = df

    def generate_markdown_table(self):
        # Tworzenie nagłówka tabeli
        markdown_table = '| ' + ' | '.join(self.df.columns) + ' |\n'
        markdown_table += '| ' + ' | '.join(['---'] * len(self.df.columns)) + ' |\n'

        # Tworzenie wierszy tabeli
        for index, row in self.df.iterrows():
            markdown_table += '| ' + ' | '.join(row.astype(str)) + ' |\n'

        logger.info("Wygenerowano tablice w formacie markdown!")
        return markdown_table
