from asyncio.log import logger
from distutils.command.config import config

from airflow import DAG
from airflow.decorators import task
from airflow.utils.task_group import TaskGroup
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

from datetime import timedelta,datetime
import time
import logging

from functions.logger_universidades import logger_universidades
from functions.norm_universidades import norm_universidades
from functions.extracting_univ import extracting_univ

from sqlalchemy import exc, create_engine, inspect

from decouple import config


# default args for my config
default_args = {
    'owner':'Pablo',
    'retries':1,
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


    logger=PythonOperator(task_id="logger",python_callable=logger_universidades,dag=dag)

    logger

    logging.info('Trying to connect to the database...')
    @task(task_id='check_db_conn')
    
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
    

    # db connection, querying data and downloading into csv (universidad de la pampa)
    def extract_la_pampa():
        logging.info('Downloading data...')
        extracting_univ(
        "path_univ_de_la_pampa.SQL",
        "la_pampa")
        logging.info('Done')
    dag_extract_la_pampa=PythonOperator(task_id="dag_extract_la_pampa",
    python_callable=extract_la_pampa,
    dag=dag)
    dag_extract_la_pampa


    # Pandas data cleaning with Pandas (universidad de la pampa)
    #@task(task_id='transform_la_pampa')
    #def transform_la_pampa():
    #    normalizado=norm_universidades("{{path}}la_pampa_raw.csv")
    #    normalizado.to_csv("la_pampa.csv",header=True,index=False)

    #transform_la_pampa = DummyOperator(task_id='transform_la_pampa')
    #load_la_pampa= DummyOperator(task_id='load_la_pampa')
    # Upload data to S3



    # db connection, querying data and downloading into csv (universidad de abierta interamericana)
    def extract_abierta_interamericana():
        logging.info('Downloading data...')
        extracting_univ(
        "path_univ_interamericana.SQL",
        "interamericana_raw")
        logging.info('Done')

    dag_extract_abierta_interamericana=PythonOperator(task_id="dag_extract_abierta_interamericana",
    python_callable=extract_abierta_interamericana,
    dag=dag)
    dag_extract_abierta_interamericana


    # Pandas data cleaning with Pandas (universidad Abierta Interamericana)

    #transform_abierta_interamericana = DummyOperator(task_id='transform_abierta_interamericana')
    #load_abierta_interamericana= DummyOperator(task_id='load_abierta_interamericana')
    # Upload data to S3

