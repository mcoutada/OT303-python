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
    "DAG_C_u_de_palermo",
    description="DAG_C_u_de_palermo",
    schedule_interval=timedelta(hours=1), 
    start_date=datetime.today() 
    
) as dag:

    u_palermo_extract = DummyOperator(task_id="u_palermo_extract")
    u_palermo_transform = DummyOperator(task_id="u_palermo_transform")
    u_palermo_load = DummyOperator(task_id="u_palermo_load")

    u_palermo_extract >> u_palermo_transform >> u_palermo_load