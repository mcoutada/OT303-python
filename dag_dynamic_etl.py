from airflow import DAG
import dagfactory

dag_factory = dagfactory.DagFactory("/root/airflow/dags/config/conf_dynamic_dag")

dag_factory.clean_dags(globals())
dag_factory.generate_dags(globals())
