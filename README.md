# base-proyect-da-python

# SPRINT I
##  TASK ID: OT303-13 (Scripts SQL)
* Para leer las querys por separado separé el archivo original .sql, uno para cada universidad.
* Carpeta sql contiene la solución a la task OT303-13.

## TASK ID: OT303-21 (ETL DAGs)
* Archivo university_etl_dag.py contiene el DAG principal, con el flujo de trabajo.
* Archivo university_etl_functions.py contiene las funciones de cada tarea del DAG.
* Al ejecutar el DAG se crea una carpeta csv con los archivos .csv correspondientes a la operación de 'extract' (para cada universidad).
* Crear archivo settings.ini con la información necesaria para realizar la conexión con postgresql.
* Carpeta sql contiene las querys de cada universidad.
* Archivos university_etl_dag.py, university_etl_functions.py, utils.py, db_connection.py, cfg.py, common_args.py y carpeta sql componen la task OT303-21.

## TASK ID: OT303-29 (Retry connection)
* El archivo connection_db_dag.py contiene el dag de retry connection.
* La función que se encarga de conectar con la base de datos se encuentra en db_connection.py
* Archivos connection_db_dag.py, db_connection.py, cfg.py componen la task OT303-29.

#
# SPRINT II

## TASK ID: OT303-37 (Logs)
* Carpeta logs contiene los .log generados al ejecutar los dag.
* Archivo /utils/logger.py contiene la estructura del log utilizado.
* Se actualizaron los dags y agregaron logs en las distintas task.

## TASK ID: OT303-45 (Extract)
* Carpeta csv contiene los archivos .csv extraidos de la base de datos para las universidades Flores y Villa Maria.
* university_etl_dag.py (task extract), university_etl_functions.py (funcion extract implementada)

## TASK ID: OT303-61 (Transform)
* En la carpeta extras se encuentra el jupyter notebook creado para transformar los datos, previo a implementarlo como scripts de python (ver para entender mejor esta task).
* Carpeta clear_data contiene los archivos .txt generados de aplicar las transformaciones para las universidades Flores y Villa Maria.
* university_etl_functions.py (funcion transform implementada)
* transform.py (funcion que depura los datos usandos pandas)

#
# Aclaración:
* Para ejecutar los DAGs, dentro de la carpeta /airflow/dags/ copiar los archivos usados o cambiar las rutas en los scripts.py.
