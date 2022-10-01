import logging

from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from Sprint2.conexion_db import connect_db

default_args = {
    'owner' : 'airflow',
    'depends_on_past' : False,
    'email' : ['airflow@example.com'],
    'email_on_failure' : False,
    'email_on_retry' : False,
    'retries' : 1,
    'retry_delay' : timedelta(minutes = 1)
}

# Creando DAG que intenta conectarse a la base de datos.
with DAG(
    'conexion_bd',
    default_args = default_args,
    description = 'Retry de conexion',
    schedule_interval = timedelta(hours = 1),
    start_date = datetime(2022, 9, 12),
    tags = ['retry']
    ) as dag:
        logging.info('Intentando conexion a la base de datos.')
        connection_task = PythonOperator(
            task_id = 'conexionBD',
            python_callable = connect_db
        )
