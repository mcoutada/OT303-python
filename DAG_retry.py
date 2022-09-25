from datetime import datime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import time
from sqlalchemy import exc, create_engine , inspect
from decouple  import config

def check_db_connection():
    retry_flag = True
    retry_count = 0
    while retry_flag and retry_count <5:
        try:
            engine = create_engine(config("DB_DATA_CONNECT"))
            engine.connect()
            insp = inspect(engine)

            #se inspecciona si existen tablas, sino prueba conectar de nuevo

            if insp.has_table(jujuy_utn) and insp.has_table(palermo_tres_de_febrero)
                retry_flag=False
            else:
                retry_count = retry_count + 1
                time.sleep(60)   
        except exc.SQLAlchemyError:
                retry_count=retry_count+1
                time.sleep(60)    
}

with DAG(
    "check_db_connection",
    description="comprobar conexion DB",
    schedule_interval=timedelta(days=1),
    start_date=datetime.today(),
    ) as dag:
    task_check_db_connection = PythonOperator(task_id= "check_db_connection", python_callable = "check_db_connection")
