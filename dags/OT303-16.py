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
    'owner':'Pablo',
    'retries':5,
    'retry_delay':timedelta(minutes=2)
}

# Context manager 
with DAG(
    "OT303_16",
    default_args=default_args,
    description="DAG correspondiente al grupo de universidades E",
    start_date=datetime(2022,9,18).replace(hour=00),
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
                if insp.has_table("universidad_la_pampa") and insp.has_table("universidad_interamericana"):
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
    logging.info('Processing: Universidad de La Pampa')

    with TaskGroup(group_id='la_pampa_group') as la_pampa_group:
        extract_la_pampa = DummyOperator(task_id='extract_la_pampa')
        # TO DO: Query data from postgres and save it
        transform_la_pampa = DummyOperator(task_id='transform_la_pampa')
        load_la_pampa= DummyOperator(task_id='load_la_pampa')
        # Upload data to S3
        extract_la_pampa >> transform_la_pampa >> load_la_pampa


    with TaskGroup(group_id='abierta_interamericana_group') as abierta_interamericana_group:
        logging.info('Processing: Universidad Abierta Interamericana')
        extract_abierta_interamericana = DummyOperator(task_id='extract_abierta_interamericana')
        # TO DO: Query data from postgres and save it
        transform_abierta_interamericana = DummyOperator(task_id='transform_abierta_interamericana')
        load_abierta_interamericana= DummyOperator(task_id='load_abierta_interamericana')
        # Upload data to S3
        extract_abierta_interamericana >> transform_abierta_interamericana >> load_abierta_interamericana


check_db_connection
la_pampa_group
abierta_interamericana_group