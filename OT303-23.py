from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import timedelta,datetime


with DAG(
    "DAG_universidades_C",
    description="DAG_universidades_C",
    schedule_interval=timedelta(hours=1), 
    start_date=datetime.today()     

) as dag:
    u_jujuy_extract = DummyOperator(task_id="u_jujuy_extract")
    u_jujuy_transform = DummyOperator(task_id="u_jujuy_transform")
    u_jujuy_load = DummyOperator(task_id="u_jujuy_load")
   
    
    [u_jujuy_extract >> u_jujuy_transform >> u_jujuy_load]

    u_palermo_extract = DummyOperator(task_id="u_palermo_extract")
    u_palermo_transform = DummyOperator(task_id="u_palermo_transform")
    u_palermo_load = DummyOperator(task_id="u_palermo_load")

    [u_palermo_extract >> u_palermo_transform >> u_palermo_load]