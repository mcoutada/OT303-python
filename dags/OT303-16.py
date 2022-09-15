from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import timedelta,datetime


with DAG(
    "universidades_e_dag",
    description="DAG correspondiente al grupo de universidades E",
    schedule_interval=timedelta(hours=1),
    now=datetime.now()
    start_date=now.hour

) as dag:
    universidad_la_pampa = DummyOperator(task_id="universidad_la_pampa")
    universidad_interamericana = DummyOperator(task_id="universidad_interamericana")

[universidad_la_pampa, universidad_interamericana]