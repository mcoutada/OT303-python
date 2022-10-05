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
from functions.uploader_univ import uploader_txt_s3

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


    logging.info('Trying to connect to the database...')
    @task(task_id='check_db_conn')
    
    # checking the db connection 
    def check_db_connection():
        retry_flag = True
        retry_count = 0
        while retry_flag and retry_count<5:
            try:
                engine = create_engine(config('DB_DATA_CONNECT_POSTGRES'))
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
    logger >> check_db_connection()
    #run_this = check_db_connection()

    # db connection, querying data and downloading into csv (universidad de la pampa)
    def extract_la_pampa():
        logging.info('Downloading data...')
        extracting_univ(
        config('path_file_la_pampa'),
        "la_pampa_raw")
        logging.info('Done')
    dag_extract_la_pampa=PythonOperator(task_id="dag_extract_la_pampa",
    python_callable=extract_la_pampa,
    dag=dag)
    

    # Using raw data from csv file la_pampa_raw.csv
    # Then returning .txt
    def transform_la_pampa():
        logging.info('Cleaning data...')
        norm_universidades(
        "PATH_la_pampa_raw.csv",
        "la_pampa")
        logging.info('Done')
    dag_transform_la_pampa=PythonOperator(task_id="dag_transform_la_pampa",
    python_callable=transform_la_pampa,
    dag=dag)


    ## Uploading .txt to S3 using BOTO3
    def upload_la_pampa():
        logging.info('Uploading_data...')
        uploader_txt_s3(config('AWS_ACCESS_KEY'),
        config('AWS_SECRET_ACCESS'),
        config('s3_output_key'),
        config('bucket_name'),
        config('path_file_la_pampa'))
    logging.info('Done')
    dag_upload_la_pampa=PythonOperator(task_id='dag_upload_la_pampa',
    python_callable=upload_la_pampa,
    dag=dag)


    logger >> dag_extract_la_pampa >> dag_transform_la_pampa >> dag_upload_la_pampa




    # db connection, querying data and downloading into csv (universidad de abierta interamericana)
    def extract_abierta_interamericana():
        logging.info('Downloading data...')
        extracting_univ(
        config('path_file_la_interamericana'),
        "abierta_interamericana_raw")
        logging.info('Done')

    dag_extract_abierta_interamericana=PythonOperator(task_id="dag_extract_abierta_interamericana",
    python_callable=extract_abierta_interamericana,
    dag=dag)
    

    # Using raw data from csv file abierta_interamericana_raw.csv
    # Then returning .txt
    def transform_abierta_interamericana():
        logging.info('Cleaning data...')
        norm_universidades(
        "PATH_abierta_interamericana_raw.csv",
        "abierta_interamericana")
        logging.info('Done')
    dag_transform_abierta_interamericana=PythonOperator(task_id="dag_transform_abierta_interamericana",
    python_callable=transform_abierta_interamericana,
    dag=dag)

    # Uploading .txt to S3 using BOTO3
    def upload_interamericana():
        logging.info('Uploading_data...')
        uploader_txt_s3(config('AWS_ACCESS_KEY'),
        config('AWS_SECRET_ACCESS'),
        config('s3_output_key'),
        config('bucket_name'),
        config('path_file_interamericana'))
    logging.info('Done')
    dag_upload_interamericana=PythonOperator(task_id='dag_upload_interamericana',
    python_callable=upload_interamericana,
    dag=dag)


    logger >> dag_extract_abierta_interamericana >> dag_transform_abierta_interamericana >> dag_upload_interamericana  
