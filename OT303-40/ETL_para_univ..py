#COMO: Analista de datos
#QUIERO: Configurar los log
#PARA: Mostrarlos en consola

#Criterios de aceptación:

#Configurar logs para Universidad Tecnológica Nacional

#Configurar logs para Universidad Nacional De Tres De Febrero

#Utilizar la librería de Loggin de python: https://docs.python.org/3/howto/logging.html

#Realizar un log al empezar cada DAG con el nombre del logger

#Formato del log: %Y-%m-%d - nombre_logger - mensaje
#Aclaración:
#Deben dejar la configuración lista para que se pueda incluir dentro de las funciones futuras. No es necesario empezar a escribir logs.

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


def transform(kwards):
    logger.info('Data transformed succefully')


def load(kwards):
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

    extrat_task=PythonOperator(
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