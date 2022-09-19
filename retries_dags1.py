from datetime import datetime ,timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import time
from sqlalchemy import exc,create_engine , inspect
from decouple import config

default_args={
    'retries': 5,
    'retry_delay':timedelta(minutes=1)
}

with dag(
    "OT303_19",
    default_args=default_args,
    description="DAG universidades A",
    start_date=datetime(2022,9,18).replace(hour=00),
    schedule_interval="@daily"
) as dag:
    logging.info('Trying to connect to the database...')
    task(task_id='check_db_connection')

    def check_db_connectioncheck_db_connection():
        retry_flag = True
        retry_count =0
    while retry_flag and retry_count < 5:
        try:
            engine =create_engine(config('DB_DATA_CONNECT'))
            engine.connnect()
            inscp = inspect(engine)

            if insp.has_table("universidad_tecnologica_nacional") and insp.has_table("universidad de tres de febrero"):
                retry_flag = False
            else:
                retry_count = retry_count +1
                time.sleep(60)
        except exc.SQLAlchemyError:

            retry_count = retry_count + 1

    time.sleep(60)
    run_this=check_db_connection()


    logging.info('Processing:uniersidad tecnologica nacional')


    with TaskGroup(group_id='utn_group') as utn_group:
           extract_utn=DummyOperator(task_id='transform_utn')
           load_utn=DummyOperator(task_id='load_utn')

           #carga a s3
           extract_utn >> transform_utn >> load_utn


    with TaskGroup(group_id='nacional_tres_de_febrero_group') as nacional_tres_de_febrero_group:
        extract_nacional_tres_de_febrero = DummyOperator(task_id='transform_nacional_tres_de_febrero')
        load_nacional_tres_de_febrero = DummyOperator(task_id='load_nacional_tres_de_febrero')

        # carga a s3
        extract_nacional_tres_de_febrero >> transform_nacional_tres_de_febrero>> load_nacional_tres_de_febrero


#check_db_connection
utn_group
nacional_tres_de_febrero_group
