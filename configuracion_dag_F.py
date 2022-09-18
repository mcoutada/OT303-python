from email.policy import default
import logging

from datetime import timedelta, datetime

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

def consultas():
    """
    Se hacen las dos consultas sql a las dos tablas.
    """
    logging.info('Haciendo consultas.')

def procesamiento():
    """
    Se van a procesar los datos usando pandas.
    """
    logging.info('Haciendo el procesamiento de los datos.')

def carga():
    """
    Se van a cargar los datos a S3.
    """
    logging.info('Haciendo la carga a S3.')

with DAG(
    'configuracion',
    default_args = default_args,
    description = 'Configurar un DAG',
    schedule_interval = timedelta(hours = 1),
    start_date = datetime(2022, 9, 12),
    tags = ['configuracion']
    ) as dag:
        hacer_consultas = PythonOperator(task_id = 'consultasSQL', python_callable = consultas)
        hacer_procesamiento = PythonOperator(task_id = 'procesamientoDatos', python_callable = procesamiento)
        hacer_carga = PythonOperator(task_id = 'cargaDatos', python_callable = carga)

        hacer_consultas >> hacer_procesamiento >> hacer_carga
