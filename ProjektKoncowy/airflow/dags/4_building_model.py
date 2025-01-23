# Wczytanie danych ze zbioru modelowego z Google Sheets lub innej chmury.
# Podział na zbiór treningowy i testowy.
# Trenowanie modelu ML.
# Ocena wydajności modelu (np. na podstawie metryki).
# Zapis wytrenowanego modelu do pliku.
# Zapis raportu wydajności modelu.

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from functions import download_data, process_data, split_processed_model_data, save_to_sheets, train_model

with DAG('building_model',start_date=datetime(2024, 12, 11),schedule_interval=None) as dag:

    train_name_standard = 'Zbiór_modelowy_standaryzacja'
    test_name_standard = 'Zbiór_testowy_standaryzacja'

    processed_name_train = 'Modelowy_processed'

    split_train_name = 'Podzielony_train'
    split_test_name = 'Podzielony_test'

    download_data_task = PythonOperator(
        task_id='download_data',
        python_callable=download_data,
        op_kwargs={'train_name': train_name_standard,
                   'test_name': test_name_standard},
        provide_context=True
    )

    process_data_task = PythonOperator(
        task_id='process_data',
        python_callable=process_data,
        op_kwargs={'train_name_standard': train_name_standard,
                   'processed_name_train': processed_name_train},
        provide_context=True
    )

    split_processed_data_task = PythonOperator(
        task_id='split_processed_data',
        python_callable=split_processed_model_data,
        op_kwargs={'processed_name_train': processed_name_train,
                   'split_train_name': split_train_name,
                   'split_test_name': split_test_name},
        provide_context=True
    )

    save_to_sheets_task = PythonOperator(
        task_id='save_to_sheets',
        python_callable=save_to_sheets,
        op_kwargs={'train_name': split_train_name, 'test_name' : split_test_name},
        provide_context=True
    )

    train_model_task = PythonOperator(
        task_id='train_model',
        python_callable=train_model,
        op_kwargs={'split_train_name': split_train_name, 'split_test_name': split_test_name},
        provide_context=True
    )

    download_data_task >> process_data_task >> split_processed_data_task >> save_to_sheets_task >> train_model_task