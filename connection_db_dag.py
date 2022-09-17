'''
TASK ID: OT303-29 
    
COMO: Analista de datos
QUIERO: Configurar los retries con la conexión al a base de datos
PARA: poder intentar nuevamente si la base de datos me produce un error

Criterios de aceptación: 
Configurar el retry para las tareas del DAG de las siguientes universidades:

Universidad De Flores
Universidad Nacional De Villa María
'''

import logging

from airflow.operators.python_operator import PythonOperator
from airflow import DAG

from datetime import timedelta, datetime
from config.common_args import default_args
from db.db_connection import connection_db

# Create and configure log
today = datetime.now().date()
logging.basicConfig(
    format='%(asctime)s %(message)s',
    filemode='w',
    level='DEBUG')

# Configure DAG parameters.
with DAG(
        'connection_db_dag',
        default_args=default_args,
        description='Retry connection task.Task id OT303-29',
        schedule_interval=timedelta(hours=1),
        start_date=datetime(2022, 9, 16),
        tags=['retry_connection']
) as dag:

    logging.info('Trying to connect to the database...')
    # Make the connection and return Engine.
    connection_task = PythonOperator(
        task_id='connection',
        python_callable=connection_db,
        retries=5,  # Number of times to retry THIS task if fail.
        retry_delay=timedelta(minutes=1),
    )
    logging.info('Connection task finished.')


