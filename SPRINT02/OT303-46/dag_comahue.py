from datetime import datetime, timedelta

import pandas as pd
from airflow import DAG
from airflow.decorators import task
from airflow.utils.task_group import TaskGroup
from include import logger, utils

UNIVERSITY_NAME = "Comahue"
uni_log = utils.set_logger(file_path=__file__)
uni_obj = utils.University(UNIVERSITY_NAME, uni_log)

# Extract task


@task(task_id="t_extract", retries=5)
def extract():
    uni_obj.extract()


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
    "owner": uni_obj.os_user,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}


with DAG(
    dag_id=uni_obj.name,
    description=f"Process (ETL) University {uni_obj.name}",
    default_args=default_args,
    start_date=datetime(year=2022, day=19, month=9),
    schedule="@hourly",
    catchup=False,
) as dag:

    t_extract = extract()

    with TaskGroup(group_id="tg_transform") as tg_transform:
        t_task1 = task1()
        t_task2 = task2()
        # Setting up Dependencies for this TaskGroup
        t_task1 >> t_task2

    t_load = load()

    # Setting up Dependencies for this DAG
    t_extract >> tg_transform >> t_load
