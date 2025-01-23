# Analiza dokładności modelu (lub innej metryki jakości).
# Uruchomienie testów modelu.
# Stworzenie raportu jakościowego.
# Powiadomienie na e-mail w przypadku niepowodzenia (np. niska jakość modelu lub błędy w testach).

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from functions import download_data, generate_corner_cases, run_unit_tests, evaluate_model_on_test_data, evaluate_model_on_corner_cases, check_and_alert

with DAG('monitoring',start_date=datetime(2024, 12, 11),schedule_interval=None) as dag:

    split_train_name = 'Podzielony_train'
    split_test_name = 'Podzielony_test'
    corner_cases_name = 'Corner_cases'

    download_data_task = PythonOperator(
        task_id='download_data',
        python_callable=download_data,
        op_kwargs={'train_name': split_train_name,
                   'test_name': split_test_name},
        provide_context=True
    )

    generate_corner_cases_task = PythonOperator(
        task_id='generate_corner_cases',
        python_callable=generate_corner_cases,
        op_kwargs={'split_train_name': split_train_name, 'corner_cases_name': corner_cases_name},
        provide_context=True
    )

    run_unit_tests_task = PythonOperator(
        task_id = 'run_unit_tests',
        python_callable = run_unit_tests,
        provide_context=True
    )

    evaluate_model_on_test_data_task = PythonOperator(
        task_id='evaluate_model_on_test_data',
        python_callable=evaluate_model_on_test_data,
        op_kwargs={'split_test_name': split_test_name},
        provide_context=True
    )

    evaluate_model_on_corner_cases_task = PythonOperator(
        task_id='evaluate_model_on_corner_cases',
        python_callable=evaluate_model_on_corner_cases,
        op_kwargs={'corner_cases_name': corner_cases_name},
        provide_context=True
    )

    check_and_alert_task = PythonOperator(
        task_id='check_and_alert',
        python_callable=check_and_alert,
        provide_context=True
    )

    download_data_task >> generate_corner_cases_task >> run_unit_tests_task >> evaluate_model_on_test_data_task >> evaluate_model_on_corner_cases_task >> check_and_alert_task