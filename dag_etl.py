from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

from conexion_db import connect_db

from config.logger_base import log

default_args = {
    'owner' : 'airflow',
    'depends_on_past' : False,
    'email' : ['airflow@example.com'],
    'email_on_failure' : False,
    'email_on_retry' : False,
    'retries' : 1,
    'retry_delay' : timedelta(minutes = 1)
}

# Creando para que se conecte a una base de datos, realice un par de consultas, extraiga los datos y los procese con pandas.
with DAG(
    'dag_etl',
    default_args = default_args,
    description = 'ETL: Grupo de universidades F',
    schedule_interval = timedelta(hours = 1),
    start_date = datetime(2022, 9, 12),
    tags = ['ETL']
    ) as dag:
        log.info('Intentando conexion a la base de datos.')
        connection_task = PythonOperator(
            task_id = 'conexionBD',
            python_callable = connect_db
        )