from airflow import DAG
import dagfactory

dag_factory = dagfactory.DagFactory('/home/richarcos/airflow/dags/config/config_dynamic_dag.yaml')

dag_factory.clean_dags(globals())
dag_factory.generate_dags(globals())
