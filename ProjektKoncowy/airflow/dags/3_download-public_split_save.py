# Pobranie danych z publicznego źródła (np. plik CSV, API).
# Podział danych na dwa zbiory:
# Modelowy (70%).
# Douczeniowy (30%).
# Zapis obu zbiorów do Google Sheets lub innej chmury.

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

from functions import split_data, save_to_sheets

with DAG('download-public-split-save',start_date=datetime(2024, 12, 11),schedule_interval=None) as dag:

    train_name = 'Zbiór_modelowy'
    test_name = 'Zbiór_testowy'

    download_and_extract_task = BashOperator(
        task_id='download_and_extract_data',
        bash_command="""
        curl -o bank+marketing.zip https://archive.ics.uci.edu/static/public/222/bank+marketing.zip && \
        unzip bank+marketing.zip && \
        unzip bank-additional.zip && \
        mv bank-additional/bank-additional-full.csv /opt/airflow/processed_data/bank-additional-full.csv && \
        rm -rf bank+marketing.zip bank.zip __MACOSX bank-additional bank-additional.zip
        """
    )

    split_data_task = PythonOperator(
        task_id='split_data',
        python_callable=split_data,
        op_kwargs={'train_name': train_name, 'test_name': test_name},
        provide_context=True
    )

    save_to_sheets_task = PythonOperator(
        task_id='save_to_sheets',
        python_callable=save_to_sheets,
        op_kwargs={'train_name': train_name, 'test_name': test_name},
        provide_context=True
    )

    download_and_extract_task >> split_data_task >> save_to_sheets_task