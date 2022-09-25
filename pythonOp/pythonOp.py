#COMO: Analista de datos
#QUIERO: Implementar el Python Operator
#PARA: procesar los datos obtenidos de la base de datos dentro del DAG

#Criterios de aceptación:
#Configurar el Python Operator para que ejecute las dos funciones que procese los datos para las siguientes universidades:

#Universidad Tecnológica Nacional

#Universidad Nacional De Tres De Febrero
from datetime import timedelta, datetime
from statistics import mode
from config.common_args import default_args
from config.cfg import LOG_ETL, LOGS_PATH
from utils.university_etl_functions import extract_data, transform_data, load_data
from utils.logger import create_logger


from airflow import DAG
from airflow.operators.python_operator import PythonOperator

log_name = LOG_ETL + datetime.today().strftime('%Y-%m-%d')
logger = create_logger(name_logger=log_name, log_path=LOGS_PATH)



def extract():
    extract_data()
    logger.info('Data extracted successfully.')



def transform():
    transform_data()
    logger.info('Data transformed successfully.')



def load(**kgwards):
    load_data()
    logger.info('Data loaded to S3 succesfully.')
    logger.handlers.clear()



with DAG(
        "ETL_para_univ.",
        default_args=default_args,
        description="DAG correspondiente al grupo de universidades D",
        start_date=datetime(2022, 9, 18).replace(hour=00),
        schedule_interval="@daily",
        tags=['ETL_par_univ']
) as dag:

    logging.info('Trying to connect to the database')

    task(task_id='check_db_conn')

    run_this = check_db_connection()

    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract,
        provide_context=True
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
    taskflow_api_etl_dag=taskflow_api_etl()
