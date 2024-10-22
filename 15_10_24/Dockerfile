# Użyj oficjalnego obrazu Pythona jako bazowego
FROM python:3.9-slim

# Zainstaluj libgomp1 i inne potrzebne zależności systemowe
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 && \
    rm -rf /var/lib/apt/lists/*

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj tylko pliki app.py i model.pkl do kontenera
COPY app.py .
COPY model.pkl .

# Zainstaluj tylko potrzebne biblioteki
RUN pip install --no-cache-dir flask pandas pycaret

# Eksponuj port
EXPOSE 5000

# Uruchom aplikację
CMD ["python", "app.py"]
