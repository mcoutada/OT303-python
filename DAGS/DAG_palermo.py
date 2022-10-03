from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator
import os
from datetime import timedelta,datetime
import logging
from functions import extract, normalization, load
from config import LOG_NAME
from logger import set_logger
from DB_connection import get_engine

# Logs configuration for the dag
log_name = LOG_NAME + datetime.today().strftime('%Y-%m-%d')
logger = set_logger(name_logger=log_name)
logger.info("DAG started")

university = "u_de_palermo"

if os.getcwd() != os.path.dirname(os.path.realpath(__file__)):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))


def extract_data(p_university=university):
    extract(p_university)


def transform(p_university=university):
    normalization(p_university)


def load_data(p_university=university):
    load(p_university)    


with DAG(
    "DAG_palermo",
    description="DAG_palermo",
    schedule_interval=timedelta(hours=1), 
    start_date=datetime.today() 
    
) as dag:

    u_palermo_extract = PythonOperator(
                        task_id="u_palermo_extract",  # Id for the task
                        python_callable=extract_data,  # Execution task (extract function)
                        provide_context=True  # For share data)
    )                    

    u_palermo_transform = PythonOperator(
                        task_id="u_palermo_transform",
                        python_callable=transform,  # Execution task (transform function)
                        provide_context=True  # For share data
                        )

    u_palermo_load = PythonOperator(
                    task_id="u_palermo_load",
                    python_callable=load_data,  # Execution task (load function)
                    provide_context=True  # For share data
    )
    u_palermo_extract >> u_palermo_transform >> u_palermo_load