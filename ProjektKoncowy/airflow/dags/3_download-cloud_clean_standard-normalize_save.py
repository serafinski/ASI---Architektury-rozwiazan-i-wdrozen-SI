# Pobranie zbioru modelowego z chmury.
# Czyszczenie danych (usuwanie braków, błędów).
# Standaryzacja i normalizacja danych.
# Zapis przetworzonych danych z powrotem do chmury.

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from functions import download_data, clean_data, standardize_normalize_data, save_to_sheets

with DAG('download_cloud_clean_standard-normalize_save',start_date=datetime(2024, 12, 11),schedule_interval=None) as dag:

    train_name = 'Zbiór_modelowy'
    test_name = 'Zbiór_testowy'
    train_name_clean = 'Zbiór_modelowy_clean'
    test_name_clean = 'Zbiór_testowy_clean'
    train_name_standard = 'Zbiór_modelowy_standaryzacja'
    test_name_standard = 'Zbiór_testowy_standaryzacja'

    download_data_task = PythonOperator(
        task_id='download_data',
        python_callable=download_data,
        op_kwargs={'train_name': train_name, 'test_name': test_name},
        provide_context=True
    )

    clean_data_task = PythonOperator(
        task_id='clean_data',
        python_callable=clean_data,
        op_kwargs={'train_name': train_name, 'test_name': test_name,
                   'train_name_clean': train_name_clean,
                   'test_name_clean': test_name_clean},
        provide_context=True
    )

    standardize_normalize_data_task = PythonOperator(
        task_id='standardize_normalize_data',
        python_callable=standardize_normalize_data,
        op_kwargs={'train_name_clean': train_name_clean,
                   'test_name_clean': test_name_clean,
                   'train_name_standard' : train_name_standard,
                   'test_name_standard' : test_name_standard},
        provide_context = True
    )

    save_to_sheets_task = PythonOperator(
        task_id='save_to_sheets',
        python_callable=save_to_sheets,
        op_kwargs={'train_name': train_name_standard, 'test_name': test_name_standard},
        provide_context=True
    )

    download_data_task >> clean_data_task >> standardize_normalize_data_task >> save_to_sheets_task