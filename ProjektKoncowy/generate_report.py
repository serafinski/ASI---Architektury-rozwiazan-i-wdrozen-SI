import pandas as pd
from ydata_profiling import ProfileReport

# Wczytanie dane
df = pd.read_csv('train_data.csv')

# Generowanie raportu
profile = ProfileReport(df, title='Raport - Pandas Profiling', explorative=True)
profile.to_file("raport.html")