
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

from asyncio import tasks
from asyncio.log import logger
from email.policy import default
from json import loads
from airflow import DAG
from datetime import timedelta, datetime, date
from airflow.operators.python_operator import PythonOperator
from scripts.process_data import process_data_univ
from scripts.extrac_data import extrac_from_db

import sys

import logging
#create log
APP_LOGGER_NAME='LogsUniv.'
def setup_applevel_logger(logger_name,log_path):

    logger = logging.getLogger('logger_name')
    logger.setLevel(loggin.INFO)
    #en formato $Y-#M-#D - logger_nombre -mensaje
    formatter=logging.Formatter=("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    datefmt='%Y-%M-%D'

    #para consola utilizo stream habler

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(sh)

    #fileHandler para el formato de mi archivo y configuracion
    fh = logging.FileHandler(
            file_name={0}/{1}.log.format(log_path, name_logger),
        mode ='a')

    fh.setFormatter(formatter)
    logger.addHandler(fh)


    return logger

def get_lloger(module_name):
    return loggint.getLogger(name_logger).getChild(module_name)
default_args ={
    'owner': 'Aiflow' ,
    'retries': 3 ,
    'retry_delay':timedelta(minutes=2)
}

logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger('ETL_task')

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')

#connection_db