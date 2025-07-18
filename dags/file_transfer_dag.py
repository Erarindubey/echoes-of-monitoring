from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from Scripts.Extractor import file_extractor_operator
import logging

default_args = {
    'owner': 'arin',
    'start_date': datetime(2023, 10, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}
with DAG(
    dag_id='echoes_of_monitoring',
    default_args=default_args,
    schedule=None,
    catchup=False,
    tags=['file_transfer', 'monitoring'],
) as dag:
    logging.info("Dag 'echoes_of_monitoring' Started.....")
    resilent_transfer_task = PythonOperator(
        task_id='resilient_file_transfer',
        python_callable=file_extractor_operator,
        op_kwargs={
            'source_dir': 'give location according to docker-compose and env',
            'dest_dir': 'give location according to docker-compose and env'
        }
    )
    resilent_transfer_task