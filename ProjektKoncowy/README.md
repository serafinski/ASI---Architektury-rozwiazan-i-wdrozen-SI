### Ostatnia aktualizacja: Sun Dec 15 17:18:40 CET 2024
# Jak pobrać projekt?
## Uruchomienie lokalne
1. Sklonuj repozytorium przy użyciu poniższej komendy:
```bash
git clone https://github.com/PJATK-ASI-2024/s24353_Bank-Marketing.git
```
2. Przełącz się na odpowiedni branch
```bash
cd s24353_Bank-Marketing
git checkout Projekt-7-Publikacja-Modelu
```
3. Otwórz projekt w swoim preferowanym IDE (Integrated Development Environment) takim jak PyCharm czy VS Code.
4. Zainstaluj potrzebne dependencje:
```bash
pip install -r requirements.txt
```
5. Wygeneruj model przy użyciu Airflow'a. [Patrz sekcja poniżej.](#budowa-modelu-przy-użyciu-apache-airflow)
6. Odpal serwis REST API poprzez wywołanie `app_local.py`. Aplikacja powinna słuchać na porcie 5000.
7. Wyślij przykładowe zapytanie do aplikacji z użyciem cURL'a na endpoint `/predict`.
8. Przykłady zapytań:

`JSON`
```bash
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '[
    {
        "age": 34,
        "job": "admin.",
        "marital": "married",
        "education": "university.degree",
        "default": "no",
        "housing": "yes",
        "loan": "no",
        "contact": "cellular",
        "month": "jul",
        "day_of_week": "thu",
        "duration": 417,
        "campaign": 1,
        "pdays": 6,
        "previous": 3,
        "poutcome": "success",
        "emp.var.rate": -1.7,
        "cons.price.idx": 94.215,
        "cons.conf.idx": -40.3,
        "euribor3m": 0.899,
        "nr.employed": 4991.6
    }
]'
```
9. Alternatywnie, możesz użyć `test_response.py` które zawiera gotowe przykłady zapytań.
## Budowa modelu przy użyciu Apache Airflow
1. Przejdź do folderu z plikami Airflow'a:
```bash
cd airflow
```
2. Zbuduj customowy obraz airflow z potrzebnymi dependencjami:
```bash
docker build .
```
3. Uruchom airflow z użyciem docker-compose:
```bash
docker-compose up -d
```
4. Otwórz przeglądarkę i przejdź do [http://localhost:8080](http://localhost:8080).
5. Zaloguj się domyślnymi danymi: login: `airflow`, hasło: `airflow`.
5. Przejdź przez wszystkie DAG'i po kolei: `download-public-split-save` -> `download_cloud_clean_standard-normalize_save` -> `building_model`.
6. Oczekuj na zakończenie procesu budowy modelu.
7. Po zakończeniu procesu, model zostanie zapisany w folderze `models`.
## Uruchomienie przy użyciu Docker'a
1. Pobierz obraz z DockerHub'a:
```bash
docker pull serafinski/model-api
```
2. Uruchom kontener z pobranym obrazem (wymaga otwarcia portu 5000 - jeżeli zajęty można zmienić go na dowolny inny: `[twoj_port]:5000`):
```bash
docker run -p 5000:5000 serafinski/model-api:latest
```
3. Wyślij przykładowe zapytanie do aplikacji z użyciem cURL'a na endpoint `/predict`.
4. Przykłady zapytań:

`JSON`
```bash
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '[
    {
        "age": 34,
        "job": "admin.",
        "marital": "married",
        "education": "university.degree",
        "default": "no",
        "housing": "yes",
        "loan": "no",
        "contact": "cellular",
        "month": "jul",
        "day_of_week": "thu",
        "duration": 417,
        "campaign": 1,
        "pdays": 6,
        "previous": 3,
        "poutcome": "success",
        "emp.var.rate": -1.7,
        "cons.price.idx": 94.215,
        "cons.conf.idx": -40.3,
        "euribor3m": 0.899,
        "nr.employed": 4991.6
    }
]'
```
## Zapytanie do modelu na platformie GCP
1. Wyślij przykładowe zapytanie do modelu na platformie GCP na endpoint `https://s24353-683779376482.europe-central2.run.app/predict`.
2. Przykłady zapytań:

`JSON`
```bash
curl -X POST https://s24353-683779376482.europe-central2.run.app/predict -H "Content-Type: application/json" -d '[
    {
        "age": 34,
        "job": "admin.",
        "marital": "married",
        "education": "university.degree",
        "default": "no",
        "housing": "yes",
        "loan": "no",
        "contact": "cellular",
        "month": "jul",
        "day_of_week": "thu",
        "duration": 417,
        "campaign": 1,
        "pdays": 6,
        "previous": 3,
        "poutcome": "success",
        "emp.var.rate": -1.7,
        "cons.price.idx": 94.215,
        "cons.conf.idx": -40.3,
        "euribor3m": 0.899,
        "nr.employed": 4991.6
    }
]'
```
## Wysyłanie zapytań przy użyciu Postmana
1. Pobierz i zainstaluj [Postmana](https://www.postman.com/downloads/).
2. Otwórz Postmana i zaimportuj plik [ASI.postman_collection.json](ASI.postman_collection.json).
3. Wybierz odpowiedni request i wyślij go do aplikacji.
# Przewidywanie skuteczności kampanii marketingowej banku
## Plan projektu
### Opis tematu i problemu biznesowego/technicznego
Projekt dotyczy przewidywania skuteczności kampanii telemarketingowych prowadzonych przez bank, których celem jest nakłonienie klientów do wykupienia lokat terminowych.

W bankowości skuteczność kampanii marketingowych ma kluczowe znaczenie dla zwiększenia zysków i zminimalizowania kosztów związanych z kontaktowaniem się z niechętnymi klientami.

Dlatego zrozumienie, które cechy klientów oraz wskaźniki społeczno-ekonomiczne zwiększają szansę na sprzedaż lokaty, pozwala bankom optymalizować działania marketingowe, skutecznie zarządzać zasobami i w efekcie osiągać lepsze wyniki finansowe.
### Źródło danych, ich charakterystyka i uzasadnienie wyboru zbioru danych
Dane pochodzą z publicznie dostępnego zestawu Bank Marketing opublikowanego w 2014 roku przez Sérgio Moro, Paulo Cortez i Paulo Ritę dostępnego na [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/222/bank+marketing).

Dane zawierają informacje z okresu od maja 2008 do listopada 2010 roku o klientach banku.
  Zostały one wzbogacone o pięć wskaźników społeczno-ekonomicznych na poziomie narodowym (m.in. kwartalna stopa zatrudnienia, miesięczny wskaźnik cen konsumpcyjnych, euribor), publikowanych przez Banco de Portugal.
  Zbiór zawiera 41 188 rekordów oraz 21 atrybutów dotyczących klientów banku, atrybutów kampanii telemarketingowej oraz danych makroekonomicznych, dzięki czemu analitycy mogą zrozumieć wpływ zarówno danych demograficznych, jak i kontekstu ekonomicznego na decyzje klientów.

Zbiór ten jest idealny do zastosowań związanych z modelowaniem predykcyjnym, gdyż zawiera wiele zróżnicowanych zmiennych wpływających na wyniki kampanii.
### Cele projektu
Głównym celem projektu jest stworzenie modelu predykcyjnego, który prognozuje, czy dany klient zdecyduje się na zakup lokaty terminowej.
### Diagram przepływu
![Diagram przepływu](workflow_diagram.png)
## Analiza danych
### Opis zmiennych
Zmienne klienta:
1. __age__ — wiek klienta (zmienna liczbowa)
2. __default__ — czy klient ma niespłacony kredyt (zmienna kategoryczna)
3. __education__ — wykształcenie klienta (zmienna kategoryczna)
4. __housing__ — czy klient posiada kredyt mieszkaniowy (zmienna kategoryczna)
5. __job__ — rodzaj pracy klienta (zmienna kategoryczna)
6. __loan__ — czy klient ma pożyczkę (zmienna kategoryczna)
7. __marital__ — stan cywilny klienta (zmienna kategoryczna)

Zmienne związane z ostatnim kontaktem z klientem w bieżącej kampanii:
1. __contact__ — typ komunikacji z klientem (zmienna kategoryczna)
2. __day_of_week__ — dzień tygodnia ostatniego kontaktu (zmienna kategoryczna)
3. __duration__ — czas trwania ostatniego kontaktu, w sekundach (zmienna liczbowa)
4. __month__ — miesiąc ostatniego kontaktu w roku (zmienna kategoryczna)

Inne zmienne:
1. __campaign__ — liczba kontaktów wykonana podczas aktualnej kampanii dla danego klienta (zmienna liczbowa, wlicza ostatni kontakt)
2. __pdays__ — liczba dni od ostatniego kontaktu z klientem podczas poprzedniej kampanii (zmienna liczbowa, 999 - nie było wcześniejszego kontaktu z klientem)
3. __poutcome__ — wynik poprzedniej kampanii marketingowej (zmienna kategoryczna)
4. __previous__ — liczba kontaktów wykonana przed aktualną kampanią dla danego klienta (zmienna liczbowa)

Zmienne związane z kontekstem społecznym i ekonomicznym:
1. __cons.conf.idx__ — indykator miesięczny, wskaźnik ufności konsumenckiej (zmienna liczbowa)
2. __cons.price.idx__ — indykator miesięczny, wskaźnik cen towarów i usług konsumpcyjnych (zmienna liczbowa)
3. __emp.var.rate__ — indykator kwartalny, wskaźnik zmienności zatrudnienia (zmienna liczbowa)
4. __euribor3m__ — indykator dzienny, 3-miesięczna stopa EURIBOR — referencyjna wysokość oprocentowania depozytów i kredytów na rynku międzybankowym strefy euro (zmienna liczbowa)
5. __nr.employed__ — indykator kwartalny, liczba pracowników (zmienna liczbowa)
Zmienna wynikowa:
__y__ — czy klient założył lokatę (zmienna binarna: 'yes' lub 'no')
### Rozkład zmiennych numerycznych
### Rozkład zmiennych kategorycznych
### Wizualizacje
Histogramy
![Histogramy](histograms.png)
Wykresy pudełkowe
![Wykresy pudełkowe](boxplots.png)
Macierz korelacji
![Macierz korelacji](correlation_matrix.png)
### Wnioski na podstawie automatycznej analizy danych - Pandas Profiling
1. Przegląd zbioru danych:
* Zbiór danych zawiera 28,831 obserwacji i 21 zmiennych.
* Brak brakujących wartości – dane są kompletne.
* Występuje 7 duplikatów wierszy, co stanowi mniej niż 0,1% danych, więc ma minimalny wpływ na analizy.
2. Typy zmiennych:
* Zbiór danych zawiera 10 zmiennych numerycznych, 10 kategorycznych oraz 1 logiczną.
* Różnorodność ta sugeruje możliwość zastosowania różnorodnych analiz, zwłaszcza przy kodowaniu zmiennych kategorycznych.
3. Wnioski z korelacji:
* Kilka zmiennych wykazuje wysoką korelację, co może wskazywać na potencjalną współliniowość. W szczególności:
    * `cons.conf.idx` i `month`
    * `emp.var.rate` z `cons.price.idx` i `euribor3m`
    * `pdays` z `poutcome` i `previous`
* Korelacje te sugerują, że niektóre zmienne mogą dostarczać podobnej informacji, co można zoptymalizować w modelach poprzez redukcję nadmiarowości.
4. Niezrównoważone zmienne:
* W przypadku kilku zmiennych występuje wysoki poziom niezrównoważenia, co może wpływać na jakość modeli predykcyjnych:
    * `default ` (skos 53%)
    * `loan` (skos 51,2%)
    * `poutcome` (skos 56,5%)
* Radzenie sobie z tymi niezrównoważeniami może wymagać zastosowania technik takich jak próbkowanie lub nadawanie wag w klasyfikacji.
5. Statystyki opisowe:
* Wiele zmiennych wykazuje wysokie wartości skośności i kurtozy, co sugeruje nienormalny rozkład. Na przykład:
    * Odchylenie standardowe niektórych zmiennych, takich jak `cons.price.idx` i `emp.var.rate`, jest znacznie zróżnicowane, co może wymagać normalizacji lub skalowania w procesie przetwarzania wstępnego.
* Zmienna `pdays` zawiera znaczny procent zerowych wartości (86,2%), co może wymagać przekształcenia dla lepszej interpretowalności i efektywności modelu
## Jak czyszczono dane
1. Usuwanie wierszy z nieznanymi wartościami w kluczowych kolumnach:
* Kolumna `job`: Usunięto 244 wiersze, w których wartość w tej kolumnie wynosiła `unknown`.
* Kolumna `marital:` Usunięto 42 wiersze, w których wartość wynosiła `unknown`.
* Kolumna `education`: Usunięto 1110 wierszy z wartością `unknown`.
* Kolumna `housing`: Usunięto 657 wierszy z wartością `unknown`.
* Kolumna `loan`: Po usunięciu poprzednich wierszy w tej kolumnie nie wystąpiły przypadki wartości `unknown`, więc nie usunięto żadnych wierszy.
2. Usuwanie wierszy ze znikomymi wartościami:
* Kolumna `default`: Usunięto 3 wiersze, gdzie wartość wynosiła `yes`. Wartości było tak mało, że nie miały wpływu na analizę.
3. Usunięcie zmiennej `duration`:
* Zmienna `duration` reprezentuje czas trwania ostatniego kontaktu z klientem w bieżącej kampanii. Analiza wykazała, że zmienna ta miała bardzo duży wpływ na prognozy modelu — często dwukrotnie większy niż wpływ kolejnych cech. Przykładem jest przypadek, gdy wartość `duration=0`, co prawie zawsze skutkuje prognozą `y=no`.
* Zmienna `duration` nie jest znana przed rozpoczęciem kontaktu z klientem. Ponadto, po zakończeniu rozmowy, informacja o decyzji klienta (czy wziął lokatę) jest już dostępna. W związku z tym użycie tej zmiennej mogłoby prowadzić do nienaturalnych prognoz, niewykorzystujących rzeczywistych informacji dostępnych przed kontaktem.
Zdecydowano się na usunięcie zmiennej `duration` z zestawu danych, ponieważ wprowadzała nierealistyczny aspekt predykcji i nie wspierała poprawy rzeczywistej jakości modelu.
## Wybór modelu przy użyciu AutoML - PyCaret
PyCaret podzieli dane na w stosunku 70/30 gdzie 70% to dane treningowe: `train_size=0.7`
### Metryki modeli
Najlepszy model został wybrany wg. poniższych metryk oceny modelu:
* MAE (Mean Absolute Error): Średnia wartość bezwzględnych różnic między rzeczywistymi a przewidywanymi wartościami. Im niższa wartość, tym lepsze dopasowanie modelu. Mniejsza wartość MAE oznacza lepszy model.
* MSE (Mean Squared Error): Średnia kwadratów różnic między rzeczywistymi a przewidywanymi wartościami. Większa waga jest nadawana większym błędom. Mniejsza wartość MSE jest lepsza, ponieważ oznacza mniej odchyleń.
* RMSE (Root Mean Squared Error): Pierwiastek kwadratowy z MSE. Daje wynik w tej samej skali co dane. Mniejsza wartość RMSE oznacza lepsze dopasowanie modelu.
* R^2 (R-Squared): Proporcja wariancji w zależnej zmiennej wyjaśnionej przez model. Im wyższa wartość R^2, tym lepsze dopasowanie modelu. R^2 bliskie 1 oznacza bardzo dobre dopasowanie.
* RMSLE (Root Mean Squared Log Error): Pierwiastek kwadratowy z błędu logarytmicznego. Mniejsza wartość RMSLE jest lepsza, szczególnie w przypadku, gdy zależy nam na karaniu większych błędów bardziej, ale ignorowaniu małych różnic.
* MAPE (Mean Absolute Percentage Error): Średnia procentowa różnica między rzeczywistymi a przewidywanymi wartościami. Mniejsza wartość MAPE oznacza lepszy model, ponieważ mniejsze są odchylenia procentowe między przewidywanymi a rzeczywistymi wartościami.
* TT (Sec) (Train Time): Całkowity czas treningu modelu. Mniejszy czas TT oznacza szybszy model, co jest korzystne, szczególnie w przypadku dużych zbiorów danych lub konieczności szybkich predykcji.

### Rekomendacje modeli
1. Logistic Regression (LR)
* __Dokładność__: 90.09%
* __AUC__: 0.7845
* __F1__: 0.366
* __Opis__: Logistic Regression to model liniowy stosowany w klasyfikacji binarnej. W przypadku tego zestawu danych wyróżnia się wysoką dokładnością, co sugeruje, że dobrze radzi sobie z klasyfikacją klientów.
* __Uzasadnienie__: Model ten jest dobrze zrozumiały, łatwy w interpretacji i pozwala na szybką identyfikację ważnych zmiennych. Dobrze nadaje się do zastosowań, gdzie ważna jest przejrzystość wyników.
2. Gradient Boosting Classifier (GBC)
* __Dokładność__: 90.02%
* __AUC__: 0.7945
* __F1__: 0.3224
* __Opis__: Gradient Boosting Classifier jest bardziej zaawansowanym modelem, który osiągnął najwyższy wynik AUC spośród rozważanych opcji. Algorytm ten iteracyjnie buduje kolejne modele, skupiając się na przykładach trudniejszych do klasyfikacji.
* __Uzasadnienie__: Model ten jest dobrym wyborem w sytuacjach, gdy głównym celem jest maksymalizacja dokładności klasyfikacji trudniejszych przypadków. Dzięki wysokiemu wynikowi AUC jest przydatny, gdy chcemy skupić się na dokładności przewidywań.
3. Light Gradient Boosting Machine (LightGBM)
* __Dokładność__: 89.7%
* __AUC__: 0.7899
* __F1__: 0.3214
* __Opis__: LightGBM to model zoptymalizowany pod kątem dużych zbiorów danych i wydajności obliczeniowej. Mimo że jego wyniki są minimalnie niższe niż w przypadku LR i GBC, jest w stanie skutecznie przetwarzać dane i dostosowywać się do bardziej złożonych zbiorów.
* __Uzasadnienie__: Model ten dobrze sprawdzi się w dalszych etapach, szczególnie jeśli dane będą bardziej złożone lub rozmiar zbioru danych wzrośnie. To mocna alternatywa dla bardziej wymagających obliczeniowo zadań.
### Wybór modelu
Na podstawie wyników zalecane jest rozpoczęcie analizy od Logistic Regression ze względu na wysoką dokładność oraz łatwość interpretacji. Jeśli projekt będzie wymagał większej precyzji, rozważany będzie Gradient Boosting Classifier, który ma najlepszy wynik AUC i może zapewnić wyższą dokładność w bardziej złożonych klasyfikacjach.
### Dokładność i Średni błąd bezwzględny (MAE) dla wybranego modelu dla danych testowych

Uzyskana dokładność modelu na poziomie 89,69% oraz MAE 0,103 wskazują na wysoką skuteczność klasyfikacji przy niskim średnim błędzie przewidywań, co sugeruje dobrze dopasowany model. W dalszym rozwijaniu modelu można rozważyć optymalizację hiperparametrów przy użyciu bardziej zaawansowanych technik tuningu lub eksperymentowanie z bardziej złożonymi modelami, jak gradient boosting, aby poprawić precyzję klasyfikacji przy zachowaniu interpretowalności wyników.
