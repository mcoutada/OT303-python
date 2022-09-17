# base-proyect-da-python

# SPRINT I
##  TASK ID: OT303-13 (Scripts SQL)
* Para leer las querys por separado separé el archivo original .sql, uno para cada universidad.
* Carpeta sql contiene la solución a la task 0T303-13.

## TASK ID: OT303-21 (ETL DAGs)
* Archivo university_etl_dag.py contiene el DAG principal, con el flujo de trabajo principal.
* Archivo university_etl_functions.py contiene las funciones de cada tarea del DAG.
* Al ejecutar el DAG se crea una carpeta csv con los archivos .csv correspondientes a la operación de extract (para cada universidad).
* Crear archivo settings.ini con la información necesaria para realizar la conexión con postgres.
* Carpeta sql contiene las querys de cada universidad.
* Archivos university_etl_dag.py, university_etl_functions.py, utils.py, db_connection.py, cfg.py, common_args.py y sql componen la task 0T303-21.

## TASK ID: OT303-29 (Retry connection)
* El archivo connection_db_dag.py contiene el dag de retry connection.
* La función que se encarga de conectar con la base de datos se encuentra en db_connection.py
* Archivos connection_db_dag.py, db_connection.py, cfg.py componen la task 0T303-29.

## Aclaración:
* Para ejecutar los DAGs, dentro de la carpeta /airflow/dags/ copiar los archivos usados o cambiar las rutas en los scripts.py.
