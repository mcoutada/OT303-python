# base-proyect-da-python
SPRINT 1/5

OT303-19:
//SE CREARON LAS TABLAS CORRESPONDIENTES CON LAS SUBCONSULTAS SQL PARA LAS UNIVERSIDADES , SE CORRIGIO ERRORES DE EDAD E INTERVALOS

DAG.PY :
// implementacion de dags con pycharm para flujos de trabajo

// retries.py
se implementaron los retries para los ingresos a la base de datos de las universidades

# SPRINT 2/5

//carpeta de logs : tiene los logs generados para ambas universidades 
// logger.py con su estructura

//sql operator: se implemento un extractor de sql en codigo para utilizarlo para extraer la informacion de los dag y posteriormente procesarlos con pandas

//PythonOperator : implementacion de un codigo.py para procesar los datos en formato csv y obtener informacion desde la base de datos

//pandasOperator : implementacion de task en Dag de funcion- de normalizacion de datos con pandas para su extraccion en formato txt proveninentes de los archivos csv posteriormente obtenidos 

# sprint 3/5
// utilizamos un operador para poder subir los txt creados en el sprint anterior a amazon s3

// configuramos un bucket para la carga de los archivos de ambas universidades

// se configuraron los logs para la creacion del entorno en big data

//implementacion de un dag dinamico

//utilizacion de mapReduce con python para ambas universidades

#sprint 4/5

//optimizamos el mapreduce por medio de diferentes funciones anteriormente agregadas

//incorporamos el script al cluster de hadoop para separar la informacion en hilos

//ejecutamos un testing QA para el script
