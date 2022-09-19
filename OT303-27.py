# COMO Analista de datos
# QUIERO Configurar un DAG, sin consultas, ni procesamiento
# PARA Hacer un ETL para 2 universidades distintas.

# Criterios de aceptación: 
# Configurar el DAG para procese las siguientes universidades:

# Facultad Latinoamericana De Ciencias Sociales

# Universidad J. F. Kennedy
# Documentar los operators que se deberían utilizar a futuro,
# teniendo en cuenta que se va a hacer dos consultas SQL (una para cada universidad), se van a procesar los datos con pandas y se van a cargar los datos en S3.
# El DAG se debe ejecutar cada 1 hora, todos los días.





from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import BranchPythonOperator  # Importar libreria
from datetime import timedelta, datetime

import random  # Importar libreria
print(datetime.today)

with DAG(
        "DAG_universidades_G",
        description="DAG_universidades_G",
        schedule_interval=timedelta(hours=1),
        start_date=datetime.today()
) as dag:

    run_this_first = DummyOperator(
        task_id='branching',
        dag=dag,
    )
 
    options = ['DAG_universidades_G']

    branching = BranchPythonOperator(
        # Este id no puede ser el mismo que otro, cambiar.
        task_id='branching2',
        # Aca DAG_universidades_A no existe?
        python_callable=lambda: random.choice('DAG_universidades_G'),
        dag=dag,
    )

    run_this_first >> branching

    join = DummyOperator(
        task_id='enable_system',
        trigger_rule='one_success',
        dag=dag,
    )

    for option in options:
        t = DummyOperator(
            task_id=option,
            dag=dag,
        )

        dummy_follow = DummyOperator(
            task_id='follow_' + option,
            dag=dag,
        )

        branching >> t >> dummy_follow >> join

    u_uba_kenedy_extract = DummyOperator(
        task_id="u_uba_kenedy_extract")
    u_uba_kenedy_transform = DummyOperator(
        task_id="u_uba_kenedy_transform")
    u_uba_kenedy_load = DummyOperator(
        task_id="u_uba_kenedy_load")

    [u_uba_kenedy_extract >>
        u_uba_kenedy_transform >> u_uba_kenedy_load]

    # Error airflow:
    # airflow.exceptions.AirflowException: The key ' u_tres_de_febrero_extract' has to be made
    # of alphanumeric characters, dashes, dots and underscores exclusively
    u_lat_sociales_cine_extract = DummyOperator(
        task_id="u_lat_sociales_cine_extract")  # El id no puede tener espacios en blanco
    u_lat_sociales_cine_transform = DummyOperator(
        task_id="u_lat_sociales_cine_transform")  # El id no puede tener espacios en blanco
    # El id no puede tener espacios en blanco
    u_lat_sociales_cine_load = DummyOperator(task_id="u_lat_sociales_cine_load")

    [u_lat_sociales_cine_extract >> u_lat_sociales_cine_transform >> u_lat_sociales_cine_load]  