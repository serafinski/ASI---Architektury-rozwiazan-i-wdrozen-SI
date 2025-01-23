# Użyj oficjalnego obrazu Pythona jako bazowego
FROM python:3.10-slim

# Zainstaluj libgomp1 i inne potrzebne zależności systemowe
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 && \
    rm -rf /var/lib/apt/lists/*

# Ustaw katalog roboczy
WORKDIR /app

# Utwórz katalog dla modeli
RUN mkdir -p airflow/models

# Skopiuj tylko pliki app.py i model.pkl do kontenera
COPY app_local.py .
COPY airflow/models/prototype.pkl airflow/models/

# Zainstaluj tylko potrzebne biblioteki
RUN pip install --no-cache-dir flask pandas pycaret dill

# Eksponuj port
EXPOSE 5000

# Uruchom aplikację
CMD ["python", "app_local.py"]