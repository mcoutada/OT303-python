https://alkemy-labs.atlassian.net/browse/OT303-46

Description

COMO: Analista de datos
QUIERO: Implementar SQL Operator
PARA: tomar los datos de las bases de datos en el DAG

Criterios de aceptación: 
Configurar un Python Operators, para que extraiga información de la base de datos utilizando el .sql disponible en el repositorio base de las siguientes universidades: 

Univ. Nacional Del Comahue

Universidad Del Salvador

-----------------------------------------------------------------------------------------------------------------------
https://alkemy-labs.atlassian.net/browse/OT303-54

COMO: Analista de datos
QUIERO: Implementar el Python Operator
PARA: procesar los datos obtenidos de la base de datos dentro del DAG

Criterios de aceptación: 
Configurar el Python Operator para que ejecute las dos funciones que procese los datos para las siguientes universidades:

Univ. Nacional Del Comahue

Universidad Del Salvador

-----------------------------------------------------------------------------------------------------------------------
https://alkemy-labs.atlassian.net/browse/OT303-62

Description

COMO: Analista de datos
QUIERO: Crear una función Python con Pandas para cada universidad
PARA: poder normalizar los datos de las mismas

Criterios de aceptación: 
Una funcion que devuelva un txt para cada una de las siguientes universidades con los datos normalizados:

Univ. Nacional Del Comahue

Universidad Del Salvador

Datos Finales:

university: str minúsculas, sin espacios extras, ni guiones

career: str minúsculas, sin espacios extras, ni guiones

inscription_date: str %Y-%m-%d format

first_name: str minúscula y sin espacios, ni guiones

last_name: str minúscula y sin espacios, ni guiones

gender: str choice(male, female)

age: int

postal_code: str

location: str minúscula sin espacios extras, ni guiones

email: str minúsculas, sin espacios extras, ni guiones

Aclaraciones:

Para calcular codigo postal o locación se va a utilizar el .csv que se encuentra en el repo.
La edad se debe calcular en todos los casos