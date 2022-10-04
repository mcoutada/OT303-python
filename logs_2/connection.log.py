#COMO: Analista de datos
#QUIERO: Configurar los log
#PARA: Mostrarlos en consola

#Criterios de aceptación: 

#Utilizar Libreria Loging.

#Loguear en 2 hilos por consola y por fichero rotativo cada 7 dias.

#Consola:  %Y/%m/%d;levelname;name;message

#Fichero:  %Y/%m/%d;levelname;name;message

#La configuración debe estar en un archivo .cfg

#Actividad
#https://docs.python.org/3/howto/logging.html#configuring-logging
#https://docs.python.org/3/library/logging.handlers.html#timedrotatingfilehandler

from airflow.operatos.python_operator import PythonOperator

from airflow import DAG
from datetime import timedelta , datetime
from config.cfg import LOG_CFG, LOG_DB
from config.common_args import default_args
from db.db_connection import connection_db
from utils.logger import create_logger_from_file, get_logger

#create y configurar log

create_logger_from_file(LOG_CFG)
logger=get_logger(LOG_DB)

#parametros que ya hemos usado anteriormente
with dag(

    "OT303_19",
    default_args=default_args,
    description="DAG universidades D",
    start_date=datetime(2022,9,18).replace(hour=00),
    schedule_interval=timedelta(hours=1),
    tag=['retry_connect']

) as dag:
    connection_task=PythonOperator (
        python_callable= connection_db ,
    retry=5,
    retry_delay=timedelta(60s),
    task(task_id='check_connection')
    
    )

    connection_db