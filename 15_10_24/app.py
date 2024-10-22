from flask import Flask, request, jsonify
import pandas as pd
from pycaret.regression import load_model, predict_model
import io

app = Flask(__name__)

# Załaduj model PyCaret
model = load_model('model')


# Funkcja przetwarzania danych wejściowych (bez dodatkowej normalizacji)
def preprocess_input_data(df):
    # Zakoduj zmienne kategoryczne w taki sam sposób jak podczas treningu modelu
    df['hispanic'] = df['ethnicity'].apply(lambda x: 1 if x == 'hispanic' else 0)
    df['afam'] = df['ethnicity'].apply(lambda x: 1 if x == 'afam' else 0)
    df['gender'] = df['gender'].apply(lambda x: 1 if x == 'male' else 0)

    binary_features = ['fcollege', 'mcollege', 'home', 'urban']
    for feature in binary_features:
        df[feature] = df[feature].apply(lambda x: 1 if x == 'yes' else 0)

    df['income'] = df['income'].apply(lambda x: 1 if x == 'high' else 0)
    df['region'] = df['region'].apply(lambda x: 1 if x == 'west' else 0)

    # Dodaj interakcje
    df['gender_education_interaction'] = df['gender'] * df['education']
    df['tuition_education_interaction'] = df['tuition'] * df['education']

    return df


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Sprawdź typ danych (JSON lub CSV)
        if request.content_type == 'application/json':
            # Pobierz dane z żądania (JSON)
            data = request.get_json()
            # Przekształć dane do DataFrame
            input_data = pd.DataFrame(data)
        elif request.content_type == 'text/csv':
            # Pobierz dane z żądania (CSV)
            csv_data = request.data.decode('utf-8')
            input_data = pd.read_csv(io.StringIO(csv_data))
        else:
            return jsonify({'error': 'Unsupported content type. Only JSON and CSV are supported.'})

        # Przetwórz dane
        input_data = preprocess_input_data(input_data)

        pd.set_option('display.max.columns', None)
        pd.set_option('display.expand_frame_repr', False)

        # Logowanie przetworzonych danych
        print("Przetworzone dane: \n", input_data)

        # Zrób przewidywanie z wykorzystaniem modelu PyCaret
        predictions = predict_model(model, data=input_data)

        # Zwróć tylko kolumnę 'prediction_label' z przewidywaniami
        return jsonify({'prediction': predictions['prediction_label'].tolist()})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
