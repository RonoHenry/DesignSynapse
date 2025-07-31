"""
Sample Airflow DAG to test Airflow installation and DAG loading.
This DAG simply prints 'Hello Airflow' to the logs.
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def hello_airflow():
    print("Hello Airflow!")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 7, 29),
}

dag = DAG(
    'test_hello_airflow',
    default_args=default_args,
    description='A simple test DAG',
    schedule_interval=None,  # Manual trigger
    catchup=False,
)

hello_task = PythonOperator(
    task_id='hello_task',
    python_callable=hello_airflow,
    dag=dag,
)
