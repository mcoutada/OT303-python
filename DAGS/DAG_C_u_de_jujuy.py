from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import timedelta,datetime
import logging
from logger import set_logger

# Logs configuration for the dag
log_name= "DAG_C_u_de_palermo" + datetime.today().strftime('%Y-%m-%d')
logger=set_logger(name_logger=log_name)
logger.info("DAG started")

# Retries config

with DAG(
    "DAG_C_u_de_jujuy",
    description="DAG_C_u_de_jujuy",
    schedule_interval=timedelta(hours=1), 
    start_date=datetime.today()     

) as dag:
    u_jujuy_extract = DummyOperator(task_id="u_jujuy_extract")
    u_jujuy_transform = DummyOperator(task_id="u_jujuy_transform")
    u_jujuy_load = DummyOperator(task_id="u_jujuy_load")
       
    u_jujuy_extract >> u_jujuy_transform >> u_jujuy_load