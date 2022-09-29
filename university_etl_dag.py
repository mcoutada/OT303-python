from datetime import timedelta, datetime
from statistics import mode
from config.common_args import default_args
from config.cfg import LOG_ETL, LOGS_PATH
from utils.university_etl_functions import extract_data, transform_data, load_data
from utils.logger import create_logger


from airflow import DAG
from airflow.operators.python_operator import PythonOperator
#from airflow.sensors.external_task_sensor import ExternalTaskSensor
log_name = LOG_ETL + '-' + datetime.today().strftime('%Y-%m-%d')
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
def transform(**kwargs):
    """Transform data from .csv source. TASK OT303-53
    """
    # Get task instance.
    ti = kwargs['ti']
    routes = transform_data()
    ti.xcom_push(key='routes', value=routes)
    logger.info('Data transformed successfully.')


# Esta task ejecuta el proceso de carga de datos a S3, recive un path
# y carga los datos a la base.
def load(**kwargs):
    """Upload data to Simple Storage Service (S3). TASK OT303-69/70
    """
    # Get task instance.
    ti = kwargs['ti']
    routes = ti.xcom_pull(task_ids='transform', key='routes')
    load_data(routes)
    logger.info('Data loaded to S3 succesfully.')
    # Clear Handlers.
    logger.handlers.clear()


# Configure DAG parameters.
with DAG(
        'university_etl_dag',
        default_args=default_args,
        description='ETL DAG for 2 universities.',
        schedule_interval=timedelta(hours=1),
        start_date=datetime(2022, 9, 28),
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

    extract_task >> transform_task >> load_task
