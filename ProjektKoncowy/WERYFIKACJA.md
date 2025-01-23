# Jak wykonano weryfikację?

## Weryfikacja pipeline'u
Pipeline został zweryfikowany poprzez uruchomienie go na zbiorze testowym. Weryfikacja polegała na sprawdzeniu, czy model zwraca poprawne wyniki dla zbioru testowego.
Wygenerowany raport znalazł się w folderze `airflow/reports`.
Wyglądał on następująco:
```text
Accuracy: 0.8969251836175774
Mean Absolute Error (MAE): 0.10307481638242251
```

## Weryfikacja modelu
Model ma możliwość zwrócenia 3 opcji:
- `yes` - jeśli model przewidział, że klient wykupi lokatę
- `no` - jeśli model przewidział, że klient nie wykupi lokaty
- zwróci błąd — jeśli model dostał nieprawidłowe dane

### Przykłady
#### Przykład 1 - model zwraca `yes`
```json
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
```
response:
```json
{
    "prediction": [
        "yes"
    ]
}
```

#### Przykład 2 - model zwraca `no`
```json
{
    "age": 56,
    "job": "housemaid",
    "marital": "married",
    "education": "basic.4y",
    "default": "no",
    "housing": "no",
    "loan": "no",
    "contact": "telephone",
    "month": "may",
    "day_of_week": "mon",
    "duration": 261,
    "campaign": 1,
    "pdays": 999,
    "previous": 0,
    "poutcome": "nonexistent",
    "emp.var.rate": 1.1,
    "cons.price.idx": 93.994,
    "cons.conf.idx": -36.4,
    "euribor3m": 4.857,
    "nr.employed": 5191
}
```
response:
```json
{
    "prediction": [
        "no"
    ]
}
```

#### Przykład 3 - model zwraca informacje, że dostał niepoprawne dane
```json
{
    "age": 86,
    "job": "retired",
    "marital": "married",
    "education": "unknown",
    "default": "unknown",
    "housing": "yes",
    "loan": "yes",
    "contact": "cellular",
    "month": "sep",
    "day_of_week": "tue",
    "duration": 211,
    "campaign": 1,
    "pdays": 7,
    "previous": 4,
    "poutcome": "success",
    "emp.var.rate": -1.1,
    "cons.price.idx": 94.199,
    "cons.conf.idx": -37.5,
    "euribor3m": 0.877,
    "nr.employed": 4963.6
}
```
response:
```json
{
    "details": [
        "'education' contains 'unknown' value"
    ],
    "error": "Invalid input data"
}
```