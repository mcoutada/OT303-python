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
from datetime import timedelta, datetime, date
from airflow.operators.python_operator import PythonOperator

log_name = LOG_ETL=datetime.today().strftime('%Y-%M-%D')
logger= create_logger(name_logger=log_name,log_path=LOGS_PATH)

def extract():
    logger.info('Data extracted succefully')


def transform(**kwards):
    logger.info('Data transformed succefully')


def load(**kwards):
    logger.info('Data loaded succefully to s3')

    logger.handlers.clear()


# asignando el log-task
with DAG(
        "ETL_para_univ.",
        default_args=default_args,
        description="DAG correspondiente al grupo de universidades D",
        start_date=datetime(2022, 9, 18).replace(hour=00),
        schedule_interval="@daily",
        tags=['ETL_par_univ']

        ##ejecucion de python operator en las task
        ## definicion de logs para dags universidades
) as dag:

    extract_task=PythonOperator(
        task_id='extract' ,
        python_callable=extract,
        provide_context=True
    )


    logging.info("")

    transform = PythonOperator(tasks_id='transform',
                               python_callable=proces_data_univ,
                               provide_context=True
    )

    load = PythonOperator(tasks_id='load',
                          python_callable=upload_to_s3,
                          provide_context=True
    )


    def print_params_fn(**kwargs):
        import logging
        logging.info(kwargs)
        return None




extract >> transform >> load