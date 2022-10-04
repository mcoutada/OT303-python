from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from config.config import CONNECTION, BUCKET_NAME

default_args = {
    'owner' : 'airflow',
    'depends_on_past' : False,
    'email' : ['airflow@example.com'],
    'email_on_failure' : False,
    'email_on_retry' : False,
    'retries' : 1,
    'retry_delay' : timedelta(minutes = 1)
}

def load_to_s3(filename: str, key: str, bucket_name: str) -> None:
    hook = S3Hook(CONNECTION)

    hook.load_file(filename = filename,
                    key = key,
                    bucket_name = bucket_name,
                    acl_policy = 'public-read')

with DAG(
    'universidad_moron_s3',
    default_args = default_args,
    description = 'Cargando los datos de la Universidad de Moron a S3',
    schedule_interval = timedelta(hours = 1),
    start_date = datetime(2022, 9, 30),
    tags = ['ETL']
) as dag:
    
    load_task = PythonOperator(
        task_id = 'load_to_S3',
        python_callable = load_to_s3,
        op_kwargs={
            'filename': 'Sprint3/files/universidad_moron.txt',
            'key': 'load_universidad_moron_txt',
            'bucket_name': BUCKET_NAME
        }
    )

    load_task
