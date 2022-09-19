
#COMO: Analista de datos
#QUIERO: Configurar un DAG, sin consultas, ni procesamiento
#PARA: Hacer un ETL para 2 universidades distintas.

#Criterios de aceptación:
#Configurar el DAG para procese las siguientes universidades:

#Universidad Tecnológica Nacional

#Universidad Nacional De Tres De Febrero
#Documentar los operators que se deberían utilizar a futuro,
#teniendo en cuenta que se va a hacer dos consultas SQL
#(una para cada universidad),
#se van a procesar los datos con pandas y se van a cargar los datos en S3.
#El DAG se debe ejecutar cada 1 hora, todos los días
...


from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import timedelta, datetime

print(datetime.today)

with DAG(
            "DAG_universidades_A",
            description = "DAG universidades_Argentina",
            schedule_interval = timedelta(hours=1),
            start_date = datetime.today()

          ) as dag:

            universidad_tecnologica_nacional_extract = DummyOperator(task_id="universidad_tecnologica_nacional")
            u_tres_de_febrero_load = DummyOperator(task_id=" u_tres_de_febrero")
            [universidad_tecnologica_nacional , universidad_tres_de_febrero]
