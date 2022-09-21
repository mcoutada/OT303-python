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

Aclaración: Las tablas tienen dos universidades cada una. No hace falta interpretar datos que no parezcan lógicos
como fechas de nacimiento y de inscripción fuera del rango de interés.
Ambas tablas contienen datos poco confiables (ej: personas inscriptas que nacieron hace menos de 15 años
o personas inscriptas con mas de 90/100 años)

Solución: se interpretaron correctamente los rangos de inscripción. Se controló la edad negativa.
*/


-- Script para Universidad De Flores. 
SELECT FC.universidad AS university,
       FC.carrera AS career,
       FC.fecha_de_inscripcion AS inscription_date,
       --Replace all characters after first white space to get name.
       regexp_replace(FC.name, '\s\S+', '') AS first_name,
       --Replace all characters before first white space to get last name.
       regexp_replace(FC.name, '.+[\s]', '') AS last_name,
       FC.sexo AS gender,
       EXTRACT(YEAR
               FROM AGE(TO_DATE(FC.fecha_nacimiento, 'YYYY-MM-DD'))) AS age,
       FC.codigo_postal AS postal_code,
       L.localidad AS location,
       FC.correo_electronico AS email
FROM flores_comahue FC
INNER JOIN localidad2 L ON CAST(FC.codigo_postal AS INT) = L.codigo_postal
WHERE FC.universidad = UPPER('Universidad De Flores')
  AND TO_DATE(FC.fecha_de_inscripcion, 'YYYY-MM-DD') 
  	BETWEEN TO_DATE('01/9/2020', 'DD-MM-YYYY') AND TO_DATE('01/02/2021', 'DD-MM-YYYY');