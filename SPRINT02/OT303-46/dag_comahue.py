from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.utils.task_group import TaskGroup

from include import utils, logger


UNIVERSITY_NAME = "Comahue"

log = logger.set_logger(logger_name=logger.get_rel_path(__file__))
uni = utils.University(UNIVERSITY_NAME, log)



@task(task_id="t_get_db_conn", retries=5)
def get_db_connection():
    return utils.get_db_conn()


# Extract task
@task(task_id="t_extract")
def extract(e_conn):
    import pandas as pd

    pd.read_sql(sql = uni.sql_query, con=e_conn).to_csv(path_or_buf=uni.csv_file, index=False)


# Transform task1
@task(task_id="t_task1")
def task1(**kwargs):
    pass


# Transform task2
@task(task_id="t_task2")
def task2(**kwargs):
    pass


# Load task
@task(task_id="t_load")
def load(**kwargs):
    pass


default_args = {
    "owner": uni.os_user,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id=uni.name,
    description=f"Process (ETL) University {uni.name}",
    default_args=default_args,
    start_date=datetime(year=2022, day=19, month=9),
    schedule="@hourly",
    catchup=False,
) as dag:

    with TaskGroup(group_id="tg_extract") as tg_extract:
        t_get_engine = get_db_connection()
        t_extract = extract(e_conn=t_get_engine)
        # Setting up Dependencies for this TaskGroup
        t_get_engine >> t_extract

    with TaskGroup(group_id="tg_transform") as tg_transform:
        t_task1 = task1()
        t_task2 = task2()
        # Setting up Dependencies for this TaskGroup
        t_task1 >> t_task2

    t_load = load()

    # Setting up Dependencies for this DAG
    tg_extract >> tg_transform >> t_load

import pandas as pd

pd.read_sql(uni.sql_query, con=utils.get_db_conn()).to_csv(uni.csv_file, index=False)
