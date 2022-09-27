from datetime import timedelta

default_args= {
    'owner':'Airflow',
    'depends_on_past': False ,
    'email':[ 'exampple@gmail.com'],
    'email_on_failure': False ,
    'retries': 3,
    'retry_delay': timedelta(minutes=2),
    }