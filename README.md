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

## TASK ID: OT303-61 (Transform Function)
* En la carpeta extras se encuentra el jupyter notebook creado para transformar los datos, previo a implementarlo como scripts de python (ver para entender mejor esta task).
* Carpeta clear_data contiene los archivos .txt generados de aplicar las transformaciones para las universidades Flores y Villa Maria.
* university_etl_functions.py (funcion transform implementada)
* transform.py (funcion que depura los datos usandos pandas)

## TASK ID: OT303-53 (Transform task)
* En la carpeta clear_data se almacenan los archivos .txt generados al aplicar las transformaciones para ambas universidades.
* university_etl_dag.py se implementa la tarea de procesamiento (transform).

#
# SPRINT III
## TASK ID: OT303-69 y OT303-70 (Load task)
* university_etl_dag.py se implementa la tarea de upload (load).
* university_etl_functions.py (funcion load_data implementada)

## TASK ID: OT303-93 (Logs from file)
* logger.py se crea el log a partir de un archivo de configuración.
* logging.conf se declara la estructura del log, los handlers y formatters.
* myHandler.py se crea un custom FileHandler para manejar los distintos parámetros.

## TASK ID: OT303-85 (Dynamic Dag)
* Usando dag-factory: pip install dag-factory
* No se modifica la lógica de procesamiento/negocio. 
* Si no se quiere utilziar esta librería, el siguiente enlace contiene un tutorial de como implementar un DAG factory personalizado https://towardsdatascience.com/how-to-build-a-dag-factory-on-airflow-9a19ab84084c.
* En config/config_dynamic_dag.yaml se implementa la estructura del dag.
* dynamic_etl_dag.py crea el dag implementado.

## TASK ID: OT303-101 (MapReduce Grupo A)
* En la carpeta big_data se encuentran los archivos de esta tarea.
* mapper_stdin.py y reducer_stdin.py son ejemplos de prueba ejecutados a traves de consola con standar input/output.
* parsing.py es otro archivo de prueba para comprobar el funcionamiento de parsing de datos xml.
* top_10_positive_tags.py: Top 10 tags with higher answer accepted.
* avg_wrods_score.py: Relation between number of words and score in a post.
* avg_answer_post.py: Average time answer in post.

#
# SPRINT IV
## TASK ID: OT303-109 y OT303-117 (MapReduce Grupo A optimizaciones/hadoop)
* Utilice la librería mrjob para implementar nuevamente las funciones de map reduce.
* En la carpeta big_data/map_reduce se enceuntran los scripts anteriores y los nuevos implementados con mrjob.
* Los scripts de mrjobs pueden correrse tanto localmente como en hadoop.
* Para correr en hadoop, si se esta usando un docker container, instalar python sobre el mismo, y las dependencias. Copiar los scripts al container y los inputs.
* Ejecutar: python3 name_script.py input > output
* Hadoop: pyton3 name_script.py input -r hadoop > output

## TASK ID: OT303:125 (Unit Test)
* Utilice PyTest para crear test unitarios.
* Cada funcion de los scripts mrjobs_.py tiene test unitarios.
* Carpeta big_data/tests.

## TASK ID: OT303:133 (Documentar Test)
* Carpeta big_data/tests.
* Todas las funciones desarrolladas a lo largo de esta certificación fueron documentadas utilizando docstrings.
* Si se utiliza Visual Studio: (https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring)

#
# Aclaración:
* Para ejecutar los DAGs, dentro de la carpeta /airflow/dags/ copiar los archivos usados o cambiar las rutas en los scripts.py.
