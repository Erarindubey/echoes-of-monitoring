from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from Scripts.hybrid import streamlinepipline4, heartbeat
import logging

default_args = {
    'owner': 'arin',
    'start_date': datetime(2023, 10, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}
with DAG(
    dag_id='Hybrid_DAG',
    default_args=default_args,
    schedule=None,
    catchup=False,
    tags=['hybrid', 'streamline']
 ) as dag:
    streamline_task = PythonOperator(
        task_id='streamline_pipeline_task',
        python_callable=streamlinepipline4,
        op_kwargs={
            'local_dir': '/opt/input',
            'output_dir': '/opt/output/streamline2_run'
        }
    )
    heartbeat_task = PythonOperator(
        task_id='heartbeat_task',
        python_callable=heartbeat
    )
    heartbeat_task >> streamline_task
