# Pobierania nowych danych z chmury (np. Google Sheets) - zbiór douczeniowy.
# Dotrenowanie modelu na podstawie nowych danych (retraining).
# Zapisywania nowej wersji modelu w pliku i wdrażania jej do istniejącej aplikacji API w Kubernetes.

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from functions import (download_retrain_data, clean_retrain_data, standardize_normalize_retrain_data, process_data, retrain_model,
                       prepare_build_context, build_docker_image, push_docker_image, cleanup_build_context)

with DAG('retrain_model', start_date=datetime(2025,1,9),schedule_interval=None) as dag:

        zbior_douczeniowy = 'Zbiór_testowy'
        zbior_douczeniowy_clean = 'Douczeniowy_clean'
        zbior_douczeniowy_standard = 'Douczeniowy_standaryzacja'
        zbior_douczeniowy_processed = 'Douczeniowy_processed'


        download_retrain_data_task = PythonOperator(
            task_id='download_retrain_data',
            python_callable=download_retrain_data,
            op_kwargs={'sheet_name': zbior_douczeniowy},
            provide_context=True
        )

        clean_retrain_data_task = PythonOperator(
            task_id='clean_retrain_data',
            python_callable=clean_retrain_data,
            op_kwargs={'sheet_name': zbior_douczeniowy,
                       'cleaned_sheet_name': zbior_douczeniowy_clean},
            provide_context=True
        )

        standardize_normalize_retrain_data_task = PythonOperator(
            task_id='standardize_normalize_retrain_data',
            python_callable=standardize_normalize_retrain_data,
            op_kwargs={'cleaned_sheet_name': zbior_douczeniowy_clean,
                       'standard_sheet_name': zbior_douczeniowy_standard},
            provide_context=True
        )

        process_retrain_data_task = PythonOperator(
            task_id='process_retrain_data',
            python_callable=process_data,
            op_kwargs={'train_name_standard': zbior_douczeniowy_standard,
                       'processed_name_train': zbior_douczeniowy_processed},
            provide_context=True
        )

        retrain_model_task = PythonOperator(
            task_id='retrain_model',
            python_callable=retrain_model,
            op_kwargs={'processed_name': zbior_douczeniowy_processed},
            provide_context=True
        )

        prepare_context = PythonOperator(
            task_id='prepare_build_context',
            python_callable=prepare_build_context,
            provide_context=True
        )

        # Build image task
        build_image = PythonOperator(
            task_id='build_docker_image',
            python_callable=build_docker_image,
            provide_context=True
        )

        # Push to registry task
        push_image = PythonOperator(
            task_id='push_docker_image',
            python_callable=push_docker_image,
            provide_context=True
        )

        # Cleanup task
        cleanup = PythonOperator(
            task_id='cleanup_build_context',
            python_callable=cleanup_build_context,
            provide_context=True
        )

        download_retrain_data_task >> clean_retrain_data_task >> standardize_normalize_retrain_data_task >> process_retrain_data_task >> retrain_model_task >> prepare_context >> build_image >> push_image >> cleanup