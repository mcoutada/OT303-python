
# Descripción "OT203-35"

# COMO: Analista de datos
# QUIERO: Configurar los retries con la conexión al a base de datos
# PARA: poder intentar nuevamente si la base de datos me produce un error

# Criterios de aceptación: 
# Configurar el retry para las tareas del DAG de las siguientes universidades:

# Facultad Latinoamericana De Ciencias Sociales

# Universidad J. F. Kennedy


from distutils.command.config import config

from airflow import DAG
from airflow.decorators import task
from airflow.utils.task_group import TaskGroup
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

from datetime import timedelta,datetime
import time
import logging

from sqlalchemy import exc, create_engine,inspect

from decouple import config


# default args for my config
default_args = {
    'retries':5,
    'retry_delay':timedelta(minutes=2)
}

# Context manager 
with DAG(
    "DB_DATA_CONNECT",
    default_args=default_args,
    description="DAG correspondiente al grupo de universidades G",
    start_date=datetime(2022,9,19).replace(hour=00),
    schedule_interval="@hourly"

) as dag:
    logging.info('Trying to connect to the database...')
    @task(task_id='check_db_connection')
    
    # checking the db connection 
    def check_db_connection():
        retry_flag = True
        retry_count = 0
        while retry_flag and retry_count<5:
            try:
                engine = create_engine(config('DB_DATA_CONNECT'))
                engine.connect()
                insp = inspect(engine)
                if insp.has_table("lat_sociales_cine") and insp.has_table("uba_kenedy"):
                    retry_flag=False
                else:
                    retry_count=retry_count+1
                    time.sleep(60)
            except exc.SQLAlchemyError:
                retry_count=retry_count+1
                time.sleep(60)
    run_this = check_db_connection()


    # TO DO: Connection with postgres db 
    # TO DO: Establish connection with S3
    logging.info('Processing: Facultad Latinoamericana De Ciencias Sociales')

    with TaskGroup(group_id='lat_sociales_cine_group') as lat_sociales_cine_group:
        extract_lat_sociales_cine = DummyOperator(task_id='extract_lat_sociales_cine')
        # TO DO: Query data from postgres and save it
        transform_lat_sociales_cine = DummyOperator(task_id='transform_lat_sociales_cine')
        load_lat_sociales_cine= DummyOperator(task_id='load_lat_sociales_cine')
        # Upload data to S3
        extract_lat_sociales_cine >> transform_lat_sociales_cine>> load_lat_sociales_cine


    with TaskGroup(group_id='uba_kenedy_group') as uba_kenedy_group:
        logging.info('Processing: universidad-j.-f.-kennedy')
        extract_uba_kenedy = DummyOperator(task_id='extract_uba_kenedy')
        # TO DO: Query data from postgres and save it
        transform_uba_kenedy = DummyOperator(task_id='transform_uba_kenedy')
        load_uba_kenedy= DummyOperator(task_id='load_uba_kenedy')
        # Upload data to S3
        extract_uba_kenedy >> transform_uba_kenedy >> load_uba_kenedy

check_db_connection
lat_sociales_cine_group
uba_kenedy_group