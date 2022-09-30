from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from include import utils

from getpass import getuser


def create_dag(p_university_name):

    # Extract task
    @task(task_id="t_extract", retries=5)
    def extract():
        uni_obj = utils.University(p_name=p_university_name, p_dag_file=__file__)
        uni_obj.extract()

    # Transform task
    @task(task_id="t_transform")
    def transform():
        uni_obj = utils.University(p_name=p_university_name, p_dag_file=__file__)
        uni_obj.transform()

    # Load task
    @task(task_id="t_load")
    def load(**kwargs):
        pass

    default_args = {
        # Set the OS's username as the Dag owner
        "owner": getuser(),
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
    }

    with DAG(
        dag_id=p_university_name,
        description=f"Process (ETL) University {p_university_name}",
        default_args=default_args,
        start_date=datetime(year=2022, day=19, month=9),
        schedule="@hourly",
        catchup=False,
    ) as dag:

        t_extract = extract()
        t_transform = transform()
        t_load = load()

        # Setting up Dependencies for this DAG
        t_extract >> t_transform >> t_load


for university_name in ["Salvador", "Comahue"]:
    # globals()[university_name] = create_dag(p_university_name=university_name)
    uni_obj = utils.University(p_name=university_name, p_dag_file=__file__)
    uni_obj.extract()
    uni_obj.transform()
