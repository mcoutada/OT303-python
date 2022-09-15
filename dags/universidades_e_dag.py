from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import timedelta,datetime


with DAG(
    "universidades_e_dag",
    description="DAG correspondiente al grupo de universidades E",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2022, 9, 14)

)