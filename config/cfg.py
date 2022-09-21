import os
from decouple import RepositoryIni, Config
from pathlib import Path

config = Config(RepositoryIni(os.path.join(
    Path().resolve().parent, 'lautaro/airflow/dags/settings.ini')))

# Database Information
DB_USER = config('DB_USER')
DB_PASS = config('DB_PASS')
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')
DB_NAME = config('DB_NAME')

# Root Directory
# /home/lautaro/airflow but in webserver is /home
# so i need to add lautaro/airflow/ to every path.
ROOT = Path().resolve().parent
ROOT_SQL = os.path.join(ROOT, 'lautaro/airflow/dags/sql')
ROOT_CSV = os.path.join(ROOT, 'lautaro/airflow/dags/csv')
LOGS_PATH = os.path.join(ROOT, 'lautaro/airflow/dags/logs')

# Tables Names
FLORES = 'flores_comahue'
VILLA_MARIA = 'salvador_villa_maria'
LOCALIDAD = 'localidad2'

# Loggers
LOG_DB = 'Connection_db-'
LOG_ETL = 'ETL_task-'
