from sched import scheduler
from airflow import DAG
from airflow.decorators import task
from datetime import datetime

with DAG(dag_id="get_processing_la_pampa",
    start_date=datetime(2022, 10, 6),
    schedule_interval='@hourly',
    catchup=False) as dag:

    @task
    def extract_univ(symbol):
        return symbol
        

    @task
    def proces_univ(symbol):
        return symbol

    @task
    def upload_univ(symbol):
        return symbol
        
    upload_univ(proces_univ(extract_univ()))
        