from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import timedelta,datetime
import logging
from functions import extract, normalization
from config import LOG_NAME
from logger import set_logger
from DB_connection import get_engine

# Logs configuration for the dag
log_name= LOG_NAME + datetime.today().strftime('%Y-%m-%d')
logger=set_logger(name_logger=log_name)
logger.info("DAG started")

universidad = "u_de_palermo"

def extract_data():
    extract()

def transform():
    normalization()

with DAG(
    "DAG_C_u_de_palermo",
    description="DAG_C_u_de_palermo",
    schedule_interval=timedelta(hours=1), 
    start_date=datetime.today() 
    
) as dag:

    u_palermo_extract = PythonOperator(task_id="u_palermo_extract",  # Id for the task
                        python_callable=extract_data,  # Execution task (extract function)
                        provide_context=True  # For share data)
    )                    

    u_palermo_transform = PythonOperator(task_id="u_palermo_transform",
                          python_callable=transform,  # Execution task (extract function)
                          provide_context=True  # For share data
                          )

    u_palermo_load = DummyOperator(task_id="u_palermo_load")

    u_palermo_extract >> u_palermo_transform >> u_palermo_load