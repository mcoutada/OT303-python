# Descripción "OT203-43"

# CCOMO: Analista de datos
# QUIERO: Configurar los log
# PARA: Mostrarlos en consola

# Criterios de aceptación: 

# Configurar logs para Facultad Latinoamericana De Ciencias Sociales

# Configurar logs para Universidad J. F. Kennedy

# Utilizar la librería de Loggin de python: https://docs.python.org/3/howto/logging.html

# Realizar un log al empezar cada DAG con el nombre del logger

# Formato del log: %Y-%m-%d - nombre_logger - mensaje
# Aclaración:
# Deben dejar la configuración lista para que se pueda incluir dentro de las funciones futuras. No es necesario empezar a escribir logs

from datetime import timedelta, datetime
from statistics import mode
from common_args import default_args
from config import LOG_ETL, LOGS_PATH
from university_etl_functions import extract_data, transform_data, load_data
from logger import create_logger


from airflow import DAG
from airflow.operators.python import PythonOperator
#from airflow.sensors.external_task_sensor import ExternalTaskSensor
log_name = LOG_ETL + datetime.today().strftime('%Y-%m-%d')
logger = create_logger(name_logger=log_name, log_path=LOGS_PATH)


# Esta task levanta los datos de la fuente (en este caso ejecuta la consulta .sql) y
# los guarda en un archivo .csv
def extract():
    """Extract data from .sql query and save data as .csv for each university. TASK OT303-45
    """
    # Extract data.
    extract_data()
    logger.info('Data extracted successfully.')


# Esta task procesa los datos extraidos anteriormente y los transforma para
# cumplir con los requerimientos utilizando pandas.
def transform():
    """Transform data from .csv source. 
    """
    transform_data()
    logger.info('Data transformed successfully.')


# Esta task va a ejecutar el proceso de carga de datos a S3, recive un dataframe o un path .csv,
# y carga los datos a la base.
def load(**kgwards):
    """Load data to some database.
    """
    # TODO: implement transform next sprint.
    load_data()
    logger.info('Data loaded to S3 succesfully.')
    # Clear Handlers.
    logger.handlers.clear()


# Configure DAG parameters.
with DAG(
        'university_etl_dag',
        default_args=default_args,
        description='ETL DAG for 2 universities.',
        schedule_interval=timedelta(hours=1),
        start_date=datetime(2022, 9, 18),
        tags=['university_etl']
) as dag:

    # Use ExternalTaskSensor to listen to the Parent_dag and connection task
    # when connection is finished, extract will be triggered
    # wait_for_connection = ExternalTaskSensor(
    #    task_id='wait_for_connection',
    #    external_dag_id='connection_db_dag',
    #    external_task_id='connection',
    #    start_date=datetime(2022, 9, 17),
    #    execution_delta=timedelta(hours=1),
    #    timeout=3600,
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

    # Podria agregarse al principio el dag del retry connection (el codigo del retry aca)
    #wait_for_connection >> extract_task >> transform_task >> load_task

    extract_task >> transform_task >> load_task