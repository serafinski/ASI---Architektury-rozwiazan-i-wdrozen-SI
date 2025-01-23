from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from functions import prepare_build_context, build_docker_image, push_docker_image, cleanup_build_context


with DAG('containerisation_and_api',start_date=datetime(2024, 12, 15), schedule_interval=None) as dag:
    # Build context task
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

    # Define task dependencies
    prepare_context >> build_image >> push_image >> cleanup