from datetime import timedelta, datetime
from utils.functions import extract_data, transform_data, load_to_s3
from utils.logger import log

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner' : 'airflow',
    'depends_on_past' : False,
    'email' : ['airflow@example.com'],
    'email_on_failure' : False,
    'email_on_retry' : False,
    'retries' : 1,
    'retry_delay' : timedelta(minutes = 1)
}

def extract():
    df = extract_data()
    log.info('Extraccion completada.')

def transform():
    transform_data()
    log.info('Datos transformados correctamente.')

def load_moron():
    log.info('Se va a cargar el archivo de la Universidad de Moron.')

    load_to_s3('/home/richarcos/airflow/dags/files/universidad_moron.txt')
    log.info('Se ha cargado el archivo de la Universidad de Moron.')

def load_rio():
    log.info('Se va a cargar el archivo de la Universidad de Rio.')

    load_to_s3('/home/richarcos/airflow/dags/files/universidad_rio.txt')
    log.info('Se ha cargado el archivo de la Universidad de Rio.')

with DAG(
    'etl_universidades',
    default_args = default_args,
    description = 'ETL de las Universidades de Moron y de Rio',
    schedule_interval = timedelta(hours = 1),
    start_date = datetime(2022, 9, 30),
    tags = ['ETL']
) as dag:

    extract_task = PythonOperator(
        task_id = 'extract_task',
        python_callable = extract
    )

    transform_task = PythonOperator(
        task_id = 'transform_task',
        python_callable = transform
    )

    load_moron_task = PythonOperator(
        task_id = 'load_moron_task',
        python_callable = load_moron
    )

    load_rio_task = PythonOperator(
        task_id = 'load_rio_task',
        python_callable = load_rio
    )

    extract_task >> transform_task >> load_moron_task >> load_rio_task
