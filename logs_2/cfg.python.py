from asyncio.constants import LOG_THRESHOLD_FOR_CONNLOST_WRITES
from importlib.resources import path
from logging import root
from multiprocessing.dummy.connection import Connection
from decouple import config
import os
from pathlib import Path
#datos de db anteriores

USER = config('USER')
PASSWORD = config('PASSWORD')
HOST = config('SERVER')
PORT = config('PORT')
DB_NAME = config('DB_NAME')

#s3 bucket
Connection=config('connection')
Bucket_name=config('se//alkemy23')

#anexar el root desde mi home

root=path()resolve().parent

root_sql=os.path.join('airflow/dags/sql_op')
root_csv=os.path.join('airflo/dags/CSV_univ')
root_txt=os.path.join('airflow/dags/datos_pandas.txt')

#universidades

UTN='universidad_tecnologica_nacional'
TRES_DE_FEBRERO='universidad_de_tres_de_febrero'
localidad='localidad2'
codigo_postal='localidad2'

#logs llamados anteriormente
LOG_ETL= 'ETL_task'
LOG_DB ='connection.log'
LOG_CFG='config.logs'