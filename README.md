# base-proyect-da-python

# Sprint 1:

Task OT303-15: Escribir el código de dos consultas SQL, una para cada universidad. para el grupo de universidades C.
* Consultas en la carpeta SQL.

Task OT303-23: Configurar un DAG, sin consultas, ni procesamiento para el grupo de universidades C
* DAGs divididos por universidad en carpeta DAGS

Task OT303-31: Configurar los retries con la conexión al a base de datos para el grupo de universidades C
* El archivo DB_connection.py contiene las funciones para establecer conexion y retries a la BD
* El archivo config.py se encuentran los datos para la conexion. 


# Sprint 2:

Task OT303-39: Configurar los log para el grupo de universidades C
* archivo logger.py contiene la funcion para configurar los logs

Task OT303-47: Implementar SQL Operator para el grupo de universidades C
* La carpeta files tiene los csvs de las universidades
* En el archivo functions.py se encuentra la funcion extract y en la carpeta dags se encuentran los operators para cada universidad con la funcion extract.

Task OT303-55: Implementar el Python Operator para el grupo de universidades C
* En la carpeta dags se encuentran los operators para cada universidad con la funcion transform y la ejecucion de la normalizacion de los datos del siguiente task.

Task OT303-63: Crear una función Python con Pandas para cada universidad para el grupo de universidades C
* En el archivo functions.py se encuentra la funcion normalization() 
* En la carpeta files se encuentran los archivos .txt requeridos por la task

# Sprint 3:

Task OT303-73: Utilizar un operador creado por la comunidad para subir a S3 el archivo de Universidad Nacional De Jujuy.

Task OT303-74: Utilizar un operador creado por la comunidad para subir a S3 el archivo de Universidad De Palermo.
* En el archivo functions.py se encuentra la funcion load() utilizando la libreria boto3 
* En la carpeta DAGS se encuentran en cada archivo de universidad el operator con la funcion load y la ejecucion de la normalizacion de los datos del siguiente task.

 


