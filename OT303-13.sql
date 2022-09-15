/*
Tarea: OT303-13

Objetivo: 
Obtener los datos de las pesonas anotadas en entre las fechas 01/9/2020 al 01/02/2021.
Para las universidades "Universidad De Flores" y "Universidad Nacional De Villa María"

Datos esperados:
university
career
inscription_date
first_name
last_name
gender
age
postal_code
location 
email

Anotaciones: 
usar tabla "localidad2"
Si la fecha de nacimiento > fecha_actual, la edad resulta en negativo (podrían descartarse estos datos).

*/

-- Script para Universidad De Flores. 
SELECT FC.universidad AS university,
       FC.carrera AS career,
       FC.fecha_de_inscripcion AS inscription_date,
       regexp_replace(name, '\s\S+', '') AS first_name,
       regexp_replace(name, '.+[\s]', '') AS last_name,
       FC.sexo AS gender,
       EXTRACT(YEAR
               FROM AGE(TO_DATE(FC.fecha_nacimiento, 'YYYY-MM-DD'))) AS age,
       FC.codigo_postal AS postal_code,
       L.localidad AS LOCATION,
       FC.correo_electronico AS email
FROM flores_comahue FC
INNER JOIN localidad2 L ON CAST(FC.codigo_postal AS INT) = L.codigo_postal
WHERE FC.universidad = UPPER('Universidad De Flores')
  AND TO_DATE(FC.fecha_de_inscripcion, 'YYYY-MM-DD') 
  	BETWEEN TO_DATE('01/9/2020', 'DD-MM-YYYY') AND TO_DATE('01/02/2021', 'DD-MM-YYYY');


-- Script para Universidad Nacional De Villa María. 
SELECT REPLACE(VM.universidad, '_', ' ') AS university,
       REPLACE(VM.carrera, '_', ' ') AS career,
       TO_DATE(VM.fecha_de_inscripcion, 'DD-Mon-YY') AS inscription_date,
       regexp_replace(REPLACE(VM.nombre, '_', ' '), '\s\S+', '') AS first_name,
       regexp_replace(REPLACE(VM.nombre, '_', ' '), '.+[\s]', '') AS last_name,
       VM.sexo AS gender,
       EXTRACT(YEAR
               FROM AGE(TO_DATE(VM.fecha_nacimiento, 'DD-Mon-YY'))) AS age,
       L.codigo_postal AS postal_code,
       VM.localidad AS LOCATION,
       VM.email AS email
FROM salvador_villa_maria VM
INNER JOIN localidad2 L ON REPLACE(VM.localidad, '_', ' ') = L.localidad
WHERE REPLACE(VM.universidad, '_', ' ') = UPPER('Universidad Nacional De Villa María')
  AND TO_DATE(VM.fecha_de_inscripcion, 'DD-Mon-YY') 
  	BETWEEN TO_DATE('01/9/2020', 'DD/MM/YYYY') AND TO_DATE('01/02/2021', 'DD/MM/YYYY');