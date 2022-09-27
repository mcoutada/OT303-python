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
log_name= "LOG_NAME" + datetime.today().strftime('%Y-%m-%d')
logger=set_logger(name_logger=log_name)
logger.info("DAG started")

universidad = "u_de_jujuy"

def extract_data():
    """Python operator to extract data
    """
    extract()

def transform():
     """Python operator to transform data
    """
    normalization()


with DAG(
    "DAG_jujuy",
    description="DAG_jujuy",
    schedule_interval=None, 
    start_date=datetime.today()     

) as dag:
    u_jujuy_extract = PythonOperator(task_id="u_jujuy_extract",  # Id for the task
                        python_callable=extract_data,  # Execution task (extract function)
                        provide_context=True  # For share data)
    )                    

    u_jujuy_transform = PythonOperator(task_id="u_jujuy_transform",
                          python_callable=transform,  # Execution task (transform function)
                          provide_context=True  # For share data
                          )

    u_jujuy_load = DummyOperator(task_id="u_jujuy_load")
       
    u_jujuy_extract >> u_jujuy_transform >> u_jujuy_load