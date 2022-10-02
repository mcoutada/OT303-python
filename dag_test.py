from airflow import DAG
from airflow.operators.python.operators import PythonOperator
from datetime import datetime

#test de un dag dinamico
def create_dag(
        dag_id,
        dag_number,
        defaults_args):
 def dag_test ():
    print("dag.test.py")
 print("dag.test",(),format(str(dag_numer)))
dag=DAG(
      dag_id,
      dag_number,
      schedule_interval=schedule,
      defaults_args=defaults_args

)
with DAG:
        t1= PythonOperator(
            task_id="daga_execution",
            python_callable=dag_execution,)


variable_of_DAG=Variable.get('dag_number')
variable_of_DAG= int(numer_of_DAG)

#generamos un bucle for para repetir las tareas de manera dinamica
for n in range(1,5):
        dag_id="print_dag_execution",(),format(str(n))

        default_args=(
                    owner,"airflow",
                    start_date, datetime.date(2022, 10, 1))

             
    schedule='@daily'
dag_number= n 
        
task = (dag_id)=create_dag(
                        dag_id,
                         dag_number,
                        defaults_args,
    )
    

#en esta carpeta se encuentra el dag dinaimco , su configuracion y una prueba del mismo