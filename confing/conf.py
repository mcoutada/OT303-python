import os
from decouple import Config, RepositoryIni
from pathlib import Path

config = Config(RepositoryIni(os.path.join(
    Path().resolve().parent, 'Prueba/settings.ini')))

DB_USER = config('DB_USER')
DB_PASS = config('DB_PASS')
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')
DB_NAME = config('DB_NAME')


# Root Directory
# /home/airflow but in webserver is /home
# so i need to add /airflow/ to every path.
ROOT = Path().resolve().parent
ROOT_SQL = os.path.join(ROOT, '/Prueba/dags/sql')
ROOT_CSV = os.path.join(ROOT, '/Prueba/dags/csv')
ROOT_TXT = os.path.join(ROOT, '/Prueba/dags/clear_data')
LOGS_PATH = os.path.join(ROOT, '/Prueba/dags/logger')

# Tables Names
UBA_KENEDY = 'uba_kenedy'
LAT_SOCIALES_CINE = 'lat_sociales_cine'
LOCALIDAD = 'localidad2'

# Loggers
LOG_DB = 'Connection_db-'
LOG_ETL = 'ETL_task-'
