# Descripción "OT203-43"

# COMO: Analista de datos
# QUIERO: Configurar los log
# PARA: Mostrarlos en consola
# Criterios de aceptación: 
# Configurar logs para  Facultad Latinoamericana De Ciencias Sociales
# Configurar logs para Universidad J. F. Kennedy
# Utilizar la librería de Loggin de python: https://docs.python.org/3/howto/logging.html
# Realizar un log al empezar cada DAG con el nombre del logger
# Formato del log: %Y-%m-%d - nombre_logger - mensaje

from airflow.operators.python import PythonOperator
from airflow import DAG

from datetime import timedelta, datetime
from config import LOG_DB, LOGS_PATH
from common_args import default_args
from db_connections import connection_db
from logger import create_logger

# Create and configure log
log_name = LOG_DB + datetime.today().strftime('%Y-%m-%d')
logger = create_logger(log_name, LOGS_PATH)

# Configure DAG parameters.
with DAG(
        'connection_db_dag',
        default_args=default_args,
        description='Retry connection task.',
        schedule_interval=timedelta(hours=1),
        start_date=datetime(2022, 9, 16),
        tags=['retry_connection']
) as dag:

    # Make the connection and return Engine.
    connection_task = PythonOperator(
        task_id='connection',
        python_callable=connection_db,
        retries=5,  # Number of times to retry THIS task if fail.
        retry_delay=timedelta(minutes=1),
    )
    connection_task
