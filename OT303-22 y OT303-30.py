"""
-------------------------------------------------------------------------------
https://alkemy-labs.atlassian.net/browse/OT303-22

COMO: Analista de datos
QUIERO: Configurar un DAG, sin consultas, ni procesamiento
PARA: Hacer un ETL para 2 universidades distintas.

Criterios de aceptación:
Configurar el DAG para procese las siguientes universidades:

Univ. Nacional Del Comahue

Universidad Del Salvador
Documentar los operators que se deberían utilizar a futuro, teniendo en cuenta que se va a hacer dos consultas SQL (una para cada universidad), se van a procesar los datos con pandas y se van a cargar los datos en S3.  El DAG se debe ejecutar cada 1 hora, todos los días.
-------------------------------------------------------------------------------
https://alkemy-labs.atlassian.net/browse/OT303-30

COMO: Analista de datos
QUIERO: Configurar los retries con la conexión al a base de datos
PARA: poder intentar nuevamente si la base de datos me produce un error

Criterios de aceptación:
Configurar el retry para las tareas del DAG de las siguientes universidades:

Univ. Nacional Del Comahue

Universidad Del Salvador
-------------------------------------------------------------------------------
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task

"""
Arguments details

'owner'
owner (str) – the owner of the task, using the unix username is recommended
As far as I see in the Airflow repository, it's just information. It's shown as a column in the main DAG view in Airflow, and if you click on that name it will show you all the DAGs from that owner (at least in Airflow 2).

'retries'
retries (int) – the number of retries that should be performed before failing the task

'retry_delay'
retry_delay (datetime.timedelta) – delay between retries

'schedule_interval'
if you run a DAG on a schedule_interval of one day, the run stamped 2016-01-01 will be trigger soon after 2016-01-01T23:59. In other words, the job instance is started once the period it covers has ended.
Use schedule_interval=None when you don’t want to schedule your DAG.

'start_date'
Defines the date at which your DAG will start being scheduled.
Each task or operator can have a different start_date, but this is strongly discouraged to keep things simple and homogenous.
The start_date for the task, determines the execution_date for the first task instance. The best practice is to have the start_date rounded to your DAG’s schedule_interval.
Daily jobs have their start_date some day at 00:00:00, hourly jobs have their start_date at 00:00 of a specific hour.
Airflow executes the DAG after start_date + interval. If start_date = 01/01/22 and interval = @daily, airflow will trigger the first tast at 02/01/22 00:00
For the reason above, you should never use a dynamic start date with a function like datetime.now(), as start_date + interval will never be reached, use static dates.

'catchup'
Airflow automatically runs non triggered DAG Runs between the latest executed DAG Run and the current date.
If there's missing runs, airflow will try to catch up and run them, set this to false to avoid this behaviour.
Let’s imagine that your DAG has a start_date set to 1 year ago with a schedule interval set to 10 minutes. If you start scheduling that DAG, you will end up with thousands of DAG.
It's recommendedu to turn off this parameter by default, you can still use the command: airflow backfill from the Airflow CLI to catch up non triggered DAG Runs.

dag_id and task_id
The 'dag_id' is a unique identifier for your DAG, and the 'task_id' is a unique name (within the DAG's namespace) for a task. It's nice if these names are meaningful to you and briefly describe your workflow and individual tasks.
The state of a task instance's PK in the database is (dag_id, task_id, execution_date).
"""


@task(task_id="t_get_db_conn", retries=5)
def get_db_conn():

    # https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html
    # top-level imports might take surprisingly a lot of time and they can generate
    # a lot of overhead and this can be easily avoided by converting them to
    # local imports inside Python callables

    from decouple import config
    from sqlalchemy import create_engine

    POSTGRES_USER = config("POSTGRES_USER")
    POSTGRES_PASSWORD = config("POSTGRES_PASSWORD")
    POSTGRES_DB = config("POSTGRES_DB")
    POSTGRES_PORT = config("POSTGRES_PORT")
    POSTGRES_HOST = config("POSTGRES_HOST")
    POSTGRES_SCHEMA = config("POSTGRES_SCHEMA")

    url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    engine = create_engine(url)
    engine.connect()

    return engine

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
