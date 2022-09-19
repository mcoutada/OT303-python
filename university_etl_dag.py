'''
TASK ID: OT303-21

COMO: Analista de datos
QUIERO: Configurar un DAG, sin operators.
PARA: Hacer un ETL para 2 universidades distintas.

Criterios de aceptación: 
Configurar el DAG para las siguientes universidades:

Universidad De Flores
Universidad Nacional De Villa María

Documentar los operators que se deberían utilizar a futuro:
    * se va a hacer dos consultas SQL (una para cada universidad), 
    * se van a procesar los datos con pandas 
    * se van a cargar los datos en S3.  
    * Scheduler: El DAG se debe ejecutar cada 1 hora, todos los días.
'''

import logging

from datetime import timedelta, datetime
from config.common_args import default_args
from utils.university_etl_functions import extract_data, transform_data, load_data

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
#from airflow.sensors.external_task_sensor import ExternalTaskSensor

#from airflow.operators.empty import EmptyOperator

# Create and configure log
today = datetime.now().date()
logging.basicConfig(
    format='%(asctime)s %(message)s',
    filemode='w',
    level='DEBUG')


# Esta task levanta los datos de la fuente (en este caso ejecuta la consulta .sql) y
# los guarda en un archivo .csv
def extract():
    """Extract data from some source and save data like .csv for each university.
    """
    # Extract data.
    extract_data()
    logging.info('Data extracted successfully.')


# Esta task procesa los datos extraidos anteriormente y los transforma para
# cumplir con los requerimientos utilizando pandas.
def transform(**kgwards):
    """Transform data from some source.
    """
    # TODO: implement transform next sprint.
    transform_data()
    logging.info('Data transformed successfully.')


# Esta task va a ejecutar el proceso de carga de datos a S3, recive un dataframe o un path .csv,
# y carga los datos a la base.
def load(**kgwards):
    """Load data to some database.
    """
    # TODO: implement transform next sprint.
    load_data()
    logging.info('Data loaded to S3 succesfully.')


# Configure DAG parameters.
with DAG(
        'university_etl_dag',
        default_args=default_args,
        description='ETL DAG for 2 universities.Task id OT303-21',
        schedule_interval=timedelta(hours=1),
        start_date=datetime(2022, 9, 16),
        tags=['university_etl']
) as dag:

    # Use ExternalTaskSensor to listen to the Parent_dag and connection task
    # when connection is finished, extract will be triggered
    # wait_for_connection = ExternalTaskSensor(
    #    task_id='wait_for_connection',
    #    external_dag_id='connection_db_dag',
    #    external_task_id='connection',
    #    start_date=datetime(2022, 9, 16),
    #    execution_delta=timedelta(hours=1),
    #    timeout=5400,
    # )

    # Could use xcom to share data between tasks. (Next Sprint)
    # Use PythonOperator to execute each task. Like:
    extract_task = PythonOperator(
        task_id='extract',  # Id for the task
        python_callable=extract,  # Execution task (extract function)
        provide_context=True  # For share data
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform,
        provide_context=True
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=load,
        provide_context=True
    )

    # First try: EmptyOperator
    #extract = EmptyOperator(task_id='extract')
    #transform = EmptyOperator(task_id='transform')
    #load = EmptyOperator(task_id='load')

    # Podria agregarse al principio el dag del retry connection (el codigo del retry aca)
    #wait_for_connection >> extract_task >> transform_task >> load_task

    extract_task >> transform_task >> load_task
