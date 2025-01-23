import requests

# Example input data
test_data_1 = {
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

test_data_2 = {
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

test_data_3 = {
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

# Send request to the API
response = requests.post('http://localhost:5000/predict',
                        json=test_data_1)

# Print the response
print(response.json())

response = requests.post('http://localhost:5000/predict',
                        json=test_data_2)

# Print the response
print(response.json())

response = requests.post('http://localhost:5000/predict',
                        json=test_data_3)

# Print the response
print(response.json())