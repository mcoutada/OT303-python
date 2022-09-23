from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.utils.task_group import TaskGroup


@task(task_id="t_get_db_conn", retries=5)
def get_db_conn():
    from include.db_utils import get_db_conn

    return get_db_conn()


# Extract task


@task(task_id="t_extract")
def extract(e_conn):
    pass


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


##########################################################################
# This is just a template, the proper naming and grouping will be done
# once we get more details on future sprints
##########################################################################


# default_args will get passed on to each task
# Its purpose to define a set of parameters common to all tasks
# You can override them on a per-task basis during operator initialization
default_args = {
    "owner": "mcoutada",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="university_id_xxxxxxxx",
    description="Process (ETL) University xxxxxxxx",
    default_args=default_args,
    start_date=datetime(year=2022, day=19, month=9),
    schedule_interval="@hourly",
    catchup=False,
) as dag:

    with TaskGroup(group_id="tg_extract") as tg_extract:
        t_get_engine = get_db_conn()
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
