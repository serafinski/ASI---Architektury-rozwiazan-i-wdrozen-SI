from flask import Flask, request, jsonify
import pandas as pd
import logging
from pycaret.classification import load_model, predict_model
import io
import joblib

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load model and scalers with correct paths
model = load_model('/app/airflow/models/prototype')
standard_scaler = joblib.load('/app/airflow/models/standard_scaler.pkl')
minmax_scaler = joblib.load('/app/airflow/models/min_max_scaler.pkl')


def validate_input(data):
    if isinstance(data, dict):
        df = pd.DataFrame([data])
    else:
        df = pd.DataFrame(data)

    # Columns that shouldn't contain 'unknown'
    columns_to_check = ['job', 'marital', 'education', 'housing', 'loan']
    invalid_values = []

    # Check for 'unknown' values
    for col in columns_to_check:
        if col in df.columns and (df[col] == 'unknown').any():
            invalid_values.append(f"'{col}' contains 'unknown' value")

    # Check for 'default' == 'yes'
    if 'default' in df.columns and (df['default'] == 'yes').any():
        invalid_values.append("'default' contains 'yes' value")

    return invalid_values


def preprocess_input(data):
    # Convert single record to DataFrame
    if isinstance(data, dict):
        df = pd.DataFrame([data])
    else:
        df = pd.DataFrame(data)

    logger.info(f"Initial columns: {df.columns.tolist()}")

    # Isolate numeric columns for scaling
    numeric_columns = [
        'age', 'campaign', 'pdays', 'previous', 'emp.var.rate',
        'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed'
    ]
    non_numeric_columns = df.drop(columns=numeric_columns, errors='ignore').columns

    if all(col in df.columns for col in numeric_columns):
        # Apply StandardScaler and MinMaxScaler
        df_numeric = df[numeric_columns]
        df_scaled = standard_scaler.transform(df_numeric)
        df_normalized = minmax_scaler.transform(df_scaled)

        # Replace numeric columns with scaled values
        df[numeric_columns] = pd.DataFrame(df_normalized, columns=numeric_columns)
        logger.info("Applied scaling and normalization to numeric columns.")

    # Drop duration column as it's not used in prediction
    if 'duration' in df.columns:
        df = df.drop('duration', axis=1)

    # Binary encoding
    binary_mapping = {
        'housing': {'yes': 1, 'no': 0},
        'loan': {'yes': 1, 'no': 0},
        'contact': {'cellular': 1, 'telephone': 0},
        'default': {'no': 0, 'unknown': 1}
    }

    for col, mapping in binary_mapping.items():
        if col in df.columns:
            df[col] = df[col].map(mapping)

    # Manual one-hot encoding for marital status
    if 'marital' in df.columns:
        df['marital_married'] = (df['marital'] == 'married').astype(int)
        df['marital_single'] = (df['marital'] == 'single').astype(int)
        df = df.drop('marital', axis=1)

    # Manual one-hot encoding for poutcome
    if 'poutcome' in df.columns:
        df['poutcome_nonexistent'] = (df['poutcome'] == 'nonexistent').astype(int)
        df['poutcome_success'] = (df['poutcome'] == 'success').astype(int)
        df = df.drop('poutcome', axis=1)

    expected_columns = [
        'age', 'job', 'education', 'default', 'housing', 'loan',
        'contact', 'month', 'day_of_week', 'campaign', 'pdays',
        'previous', 'emp.var.rate', 'cons.price.idx', 'cons.conf.idx',
        'euribor3m', 'nr.employed', 'marital_married', 'marital_single',
        'poutcome_nonexistent', 'poutcome_success',
    ]

    # Reorder columns to match training data
    df = df[expected_columns]

    logger.info(f"Final columns: {df.columns.tolist()}")
    return df


def convert_prediction_to_label(predictions):
    return ['yes' if pred == 1 else 'no' for pred in predictions]


@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Check if model and scalers are loaded
        if model is None:
            return jsonify({
                'status': 'error',
                'message': 'Model not loaded'
            }), 503

        if standard_scaler is None or minmax_scaler is None:
            return jsonify({
                'status': 'error',
                'message': 'Scalers not loaded'
            }), 503

        # If everything is OK
        return jsonify({
            'status': 'healthy',
            'model_loaded': True,
            'scalers_loaded': True
        }), 200

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 503


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Check data type (JSON or CSV)
        if request.content_type == 'application/json':
            data = request.get_json()
        elif request.content_type == 'text/csv':
            csv_data = request.data.decode('utf-8')
            data = pd.read_csv(io.StringIO(csv_data))
        else:
            return jsonify({'error': 'Unsupported content type. Only JSON and CSV are supported.'})

        # Validate input data
        invalid_values = validate_input(data)
        if invalid_values:
            return jsonify({
                'error': 'Invalid input data',
                'details': invalid_values
            }), 400

        # Preprocess data
        processed_data = preprocess_input(data)

        # Log processed data
        logger.info("Processed data: \n%s", processed_data)

        # Make prediction using PyCaret model
        predictions = predict_model(model, data=processed_data)

        # Convert numerical predictions to yes/no labels
        prediction_labels = convert_prediction_to_label(predictions['prediction_label'])

        # Return prediction labels
        return jsonify({'prediction': prediction_labels})

    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
