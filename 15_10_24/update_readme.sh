#!/bin/bash

{
  echo "# Jak pobrać projekt?"
  echo "## Uruchomienie lokalne"
  echo "1. Sklonuj repozytorium przy użyciu poniższej komendy:"
  echo "\`\`\`bash"
  echo "git clone https://github.com/PJATK-ASI-2024/Lab-3-4_s24353.git"
  echo "\`\`\`"
  echo "2. Otwórz projekt w swoim preferowanym IDE (Integrated Development Environment) takim jak PyCharm czy VS Code."
  echo "3. Zainstaluj potrzebne dependencje:"
  echo "\`\`\`bash"
  echo "pip install -r requirements.txt"
  echo "\`\`\`"
  echo "4. Repozytorium powinno zawierać gotowy model (\`model.pkl\`) do odpalenia. Jeżeli jednak tak by się nie stało, jesteś w stanie wygenerować model poprzez odpalenie \`feature_engineering.py\`, a następnie \`model_training.py\`"
  echo "5. Odpal \`app.py\`. Aplikacja powinna słuchać na porcie 5000."
  echo "6. Wyślij przykładowe zapytanie do aplikacji z użyciem cURL'a na endpoint \`/predict\`. Aplikacja przyjmuje zapytania w postaci CSV czy JSON."
  echo "7. Przykłady zapytań:"
  echo ""
  echo "\`JSON\`"
  echo "\`\`\`bash"
  echo "curl -X POST http://localhost:5000/predict -H \"Content-Type: application/json\" -d '["
  echo "    {"
  echo "        \"gender\": \"female\","
  echo "        \"ethnicity\": \"other\","
  echo "        \"fcollege\": \"no\","
  echo "        \"mcollege\": \"no\","
  echo "        \"home\": \"yes\","
  echo "        \"urban\": \"yes\","
  echo "        \"unemp\": 5.90,"
  echo "        \"wage\": 8.09,"
  echo "        \"distance\": 3.0,"
  echo "        \"tuition\": 0.889,"
  echo "        \"education\": 15,"
  echo "        \"income\": \"low\","
  echo "        \"region\": \"other\""
  echo "    }"
  echo "]'"
  echo "\`\`\`"
  echo "\`CSV\`"
  echo "\`\`\`bash"
  echo "curl -X POST http://localhost:5000/predict -H \"Content-Type: text/csv\" --data-binary 'gender,ethnicity,fcollege,mcollege,home,urban,unemp,wage,distance,tuition,education,income,region"
  echo "female,other,no,no,yes,yes,5.90,8.09,3.0,0.889,15,low,other'"
  echo "\`\`\`"
  echo "## Uruchomienie przy użyciu Docker'a"
  echo "1. Pobierz najnowszy obraz z DockerHub'a:"
  echo "\`\`\`bash"
  echo "docker pull serafinski/asi-04:latest"
  echo "\`\`\`"
  echo "2. Uruchom kontener z pobranym obrazem (wymaga otwarcia portu 5000 - jeżeli zajęty można zmienić go na dowolny inny: \`[twoj_port]:5000\`):"
  echo "\`\`\`bash"
  echo "docker run -p 5000:5000 serafinski/asi-04:latest"
  echo "\`\`\`"
  echo "3. Wyślij przykładowe zapytanie do aplikacji z użyciem cURL'a na endpoint \`/predict\`. Aplikacja przyjmuje zapytania w postaci CSV czy JSON."
  echo "4. Przykłady zapytań:"
  echo ""
  echo "\`JSON\`"
  echo "\`\`\`bash"
  echo "curl -X POST http://localhost:5000/predict -H \"Content-Type: application/json\" -d '["
  echo "    {"
  echo "        \"gender\": \"female\","
  echo "        \"ethnicity\": \"other\","
  echo "        \"fcollege\": \"no\","
  echo "        \"mcollege\": \"no\","
  echo "        \"home\": \"yes\","
  echo "        \"urban\": \"yes\","
  echo "        \"unemp\": 5.90,"
  echo "        \"wage\": 8.09,"
  echo "        \"distance\": 3.0,"
  echo "        \"tuition\": 0.889,"
  echo "        \"education\": 15,"
  echo "        \"income\": \"low\","
  echo "        \"region\": \"other\""
  echo "    }"
  echo "]'"
  echo "\`\`\`"
  echo "\`CSV\`"
  echo "\`\`\`bash"
  echo "curl -X POST http://localhost:5000/predict -H \"Content-Type: text/csv\" --data-binary 'gender,ethnicity,fcollege,mcollege,home,urban,unemp,wage,distance,tuition,education,income,region"
  echo "female,other,no,no,yes,yes,5.90,8.09,3.0,0.889,15,low,other'"
  echo "\`\`\`"

  echo "# Raport z Analizy Danych"
  echo "### Ostatnia aktualizacja: $(date)"

  echo "## Przed Czyszczeniem Danych"

  echo "### Braki w danych:"
  cat missing.txt

  echo "### Opis statystyczny danych numerycznych"
  cat pre_numeric_analysis.txt

  echo "### Opis zmiennych kategorycznych"
  cat pre_categorical_analysis.txt

  echo "### Dystrybucja zmiennych kategorycznych"
  cat pre_categorical_distribution.txt

  echo "### Histogram dla Score"
  echo "![Histogram](histogram.png)"
  echo "### Wykresy Punktowe"
  echo "![Wykresy Punktowe](scatter_plots.png)"
  echo "### Zmienne Kategoryczne"
  echo "![Zmienne Kategoryczne](distribution.png)"

  echo "### Heatmap'a Korelacji"
  echo "![Heatmapa Korelacji](correlation_heatmap.png)"

  echo "## Po Czyszczeniu Danych"

  echo "### Opis statystyczny danych numerycznych"
  cat post_numeric_analysis.txt

  echo "### Opis zmiennych kategorycznych"
  echo "Ethnicity rozdzielono na hispanic i afam"
  cat post_categorical_analysis.txt

  echo "### Dystrybucja zmiennych kategorycznych"
  cat post_categorical_distribution.txt

  echo "### Histogram dla Score"
  echo "![Histogram Processed](histogram_processed.png)"
  echo "### Wykresy Punktowe"
  echo "![Wykresy Punktowe Processed](scatter_plots_processed.png)"
  echo "### Zmienne Kategoryczne"
  echo "![Zmienne Kategoryczne Processed](distribution_processed.png)"

  echo "## Wybór modelu przy użyciu AutoML - PyCaret"
  echo "PyCaret podzieli dane na w stosunku 80/20 gdzie 80% to dane treningowe: \`train_size=0.8\`"
  echo "### Metryki modeli"
  echo "Najlepszy model został wybrany wg. poniższych metryk oceny modelu:"
  echo "* MAE (Mean Absolute Error): Średnia wartość bezwzględnych różnic między rzeczywistymi a przewidywanymi wartościami. Im niższa wartość, tym lepsze dopasowanie modelu. Mniejsza wartość MAE oznacza lepszy model."
  echo "* MSE (Mean Squared Error): Średnia kwadratów różnic między rzeczywistymi a przewidywanymi wartościami. Większa waga jest nadawana większym błędom. Mniejsza wartość MSE jest lepsza, ponieważ oznacza mniej odchyleń."
  echo "* RMSE (Root Mean Squared Error): Pierwiastek kwadratowy z MSE. Daje wynik w tej samej skali co dane. Mniejsza wartość RMSE oznacza lepsze dopasowanie modelu."
  echo "* R^2 (R-Squared): Proporcja wariancji w zależnej zmiennej wyjaśnionej przez model. Im wyższa wartość R^2, tym lepsze dopasowanie modelu. R^2 bliskie 1 oznacza bardzo dobre dopasowanie."
  echo "* RMSLE (Root Mean Squared Log Error): Pierwiastek kwadratowy z błędu logarytmicznego. Mniejsza wartość RMSLE jest lepsza, szczególnie w przypadku, gdy zależy nam na karaniu większych błędów bardziej, ale ignorowaniu małych różnic."
  echo "* MAPE (Mean Absolute Percentage Error): Średnia procentowa różnica między rzeczywistymi a przewidywanymi wartościami. Mniejsza wartość MAPE oznacza lepszy model, ponieważ mniejsze są odchylenia procentowe między przewidywanymi a rzeczywistymi wartościami."
  echo "* TT (Sec) (Train Time): Całkowity czas treningu modelu. Mniejszy czas TT oznacza szybszy model, co jest korzystne, szczególnie w przypadku dużych zbiorów danych lub konieczności szybkich predykcji."
  echo ""
  cat comparison_metrics.txt

  echo "### Metryki dla tuningowanego modelu"

  cat tuning_metrics.txt

  echo "### Wykres ważności cech dla najlepszego modelu"
  echo "![Feature Importance](feature_importance.png)"

  echo "### Wykres Krzywej Uczenia"
  echo "![Learning Curve](learning_curve.png)"

  echo "### Wykres Reszt"
  echo "![Residuals](Residuals.png)"

  echo "### Wykres Błędów Predykcji"
  echo "![Prediction Error](prediction_error.png)"

  echo "### Wykres Dystansu Cook'a"
  echo "![Cooks Distance](cooks_distance.png)"

} > README.md
