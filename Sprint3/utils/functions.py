from webbrowser import get
from sqlalchemy import create_engine, exc, inspect
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from config.config import DB_USER, PASSWORD, HOST, PORT, DB_NAME, CONNECTION, BUCKET_NAME
from utils.logger import get_logger

import time
import pandas as pd

log = get_logger()

# Funciones de conexion a la BD
def get_engine():
    """
    Se crea el engine de la base de datos.
    """
    url = f"postgresql://{DB_USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
    return create_engine(url)

def connect_db():
    """
    Esta función se conecta a la base de datos. Intenta conectarse 5 veces, si falla se cancela la conexion.
    Devuelve un elemento de conexion.
    """
    rety_flag = True
    retry_count = 0
    while rety_flag and retry_count < 5:
        try:
            engine = get_engine()
            engine.connect()
            insp = inspect(engine)
            log.info('Estableciendo conexion a la base de datos.')
            # Comprobando que existen las tablas.
            if (insp.has_table("moron_nacional_pampa") and insp.has_table("rio_cuarto_interamericana")):
                log.info('Se ha establecido la conexion con la base de datos.')
                rety_flag = False
            else:
                retry_count += 1
                time.sleep(60)
        except exc.SQLAlchemyError:
            log.info('No se ha podido establecer la conexion a la base de datos.')
            retry_count += 1
            time.sleep(60)

# Funcion para extraer los datos de la base de datos
def extract_data():
    engine = get_engine()
    connection = engine.raw_connection()

    # Ejecutando la consulta SQL para la Universidad de Moron.
    log.info('Obteniendo datos de la Universidad de Moron.')
    with open("/home/richarcos/airflow/dags/sql/moron_nacional_pampa.sql") as file:
        query = file.read()
        table_df = pd.read_sql(query, connection)
    
    # Ejecutando la consulta SQL para la Universidad Nacional del Rio Cuarto.
    log.info('Obteniendo datos de la Universidad Nacional del Rio Cuarto.')
    with open("/home/richarcos/airflow/dags/sql/rio_cuarto_interamericana.sql") as file:
        query = file.read()
        table_df = table_df.append(pd.read_sql(query, connection), ignore_index = True)
    
    # Guardando los datos en el archivo .csv
    log.info('Guardando los datos obtenidos.')
    table_df.to_csv(path_or_buf = '/home/richarcos/airflow/dags/files/universidades.csv')
    
    log.info('Se han guardado todos los datos correctamente.')
    
    """
    Se retorna el df de las universidades 
    para usarlo y normalizar los datos
    sin necesidad de cargar el csv.
    """
    return table_df

# Funcion para transformar los datos obtenidos por la funcion
def transform_data():
    log.info('Extrayendo datos.')
    df = extract_data()

    log.info('Normalizando los datos.')
    # Normalizando la columna university
    df.university = df.university.str.replace('-',' ')
    df.university = df.university.str.lower()

    # Normalizando la columna career
    df.career = df.career.str.replace('-', ' ')
    df.career = df.career.str.lower()

    # Normalizando la columna inscription_date
    df.inscription_date = pd.to_datetime(df.inscription_date)

    # Normalizando las columnas first_name y last_name
    df.first_name = df.first_name.str.lower()
    df.last_name = df.last_name.str.lower()

    # Normalizando la columna gender
    df.gender = df.gender.map({'F': 'female', 'M': 'male'})

    # Normalizando la columna age
    df.age = df.age.astype('int64')

    # Normalizando la columna location
    df.location = df.location.str.lower()
    
    # Normalizando la columna email
    df.email = df.email.str.lower()

    # Filtrando la columna university para crear dos dataframes nuevos
    df_moron = df[(df.university == 'universidad de morón') | (df.university == 'universidad nacional de la pampa')]
    df_rio = df[(df.university == 'universidad nacional de río cuarto') | (df.university == 'universidad abierta interamericana')]
    
    # Guardando los datos en un archivo .txt
    log.info('Guardando los datos normalizados de la Universidad de Moron en un archivo txt.')
    df_file = open('/home/richarcos/airflow/dags/files/universidad_moron.txt', 'a')
    df_file.write(df_moron.to_string())
    df_file.close()

    log.info('Guardando los datos normalizados de la Universidad de Río Cuarto en un archivo txt.')
    df_file = open('/home/richarcos/airflow/dags/files/universidad_rio.txt', 'a')
    df_file.write(df_rio.to_string())
    df_file.close()

# Funcion para hacer la carga de los archivos a S3
def load_to_s3(file):
    log.info('Iniciando tarea de carga.')

    hook = S3Hook(CONNECTION)
    
    hook.load_file(filename = file,
                key = 'load_txt_file',
                bucket_name = BUCKET_NAME,
                acl_policy = 'public-read')
    
    log.info('Carga de archivo completada.')
