/*************************************************************************
https://alkemy-labs.atlassian.net/browse/OT303-14

COMO: Analista de datos
QUIERO: Escribir el código de dos consultas SQL, una para cada universidad.
PARA: Obtener los datos de las pesonas anotadas en entre las fechas 01/9/2020 al 01/02/2021 para las siguientes facultades:

Univ. Nacional Del Comahue

Universidad Del Salvador

Criterios de aceptación: 
Deben presentar la consulta en un archivo .sql. La consulta debe disponibilizar únicamente la información necesaria para que en un futuro sea procesada y genere los siguientes datos para las fechas indicadas.
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
Aclaración: Las tablas tienen dos universidades cada una. No hace falta interpretar datos que no parezcan lógicos como fechas de nacimiento y de inscripción fuera del rango de interés. Lo importante es traer toda la información de la base de datos en las fechas especificadas y cada tarea se debe ejecutar 5 veces antes de fallar.
    
*************************************************************************/

-- Univ. Nacional Del Comahue
SELECT
    fc.universidad AS university,
    fc.carrera AS career,
    fc.fecha_de_inscripcion AS inscription_date,
    SPLIT_PART(fc.name, ' ', 1) AS first_name,
    SPLIT_PART(fc.name, ' ', 2) AS last_name,
    fc.sexo AS gender,
    DATE_PART('year', AGE(TO_DATE(fc.fecha_nacimiento,'YYYY-MM-DD'))) AS age,
    fc.codigo_postal AS postal_code,
    l.localidad AS location,
    fc.correo_electronico AS email
FROM
    flores_comahue fc
LEFT JOIN
    localidad2 l
ON
    fc.codigo_postal = l.codigo_postal::text
WHERE
    fc.universidad = UPPER('Univ. Nacional Del Comahue')
AND
    TO_DATE(fc.fecha_de_inscripcion,'YYYY-MM-DD')
        BETWEEN
            TO_DATE('01/09/2020','DD/MM/YYYY')
        AND
            TO_DATE('01/02/2021','DD/MM/YYYY');


-- Universidad Del Salvador
SELECT
    svm.universidad AS university,
    svm.carrera AS career,
    svm.fecha_de_inscripcion AS inscription_date,
    SPLIT_PART(svm.nombre, '_', 1) AS first_name,
    SPLIT_PART(svm.nombre, '_', 2) AS last_name,
    svm.sexo AS gender,
    DATE_PART(
        'year',
        AGE(
            CASE
                WHEN
                    TO_DATE(svm.fecha_nacimiento,'DD-Mon-YY') > NOW()
                THEN
                    TO_DATE(svm.fecha_nacimiento,'DD-Mon-YY') - interval '100 year'
                ELSE
                    TO_DATE(svm.fecha_nacimiento,'DD-Mon-YY')
            END
        )
    ) AS age,
    l.codigo_postal AS postal_code,
    l.localidad AS location,
    svm.email
FROM
    salvador_villa_maria svm
LEFT JOIN
    localidad2 l
ON
    svm.localidad = REPLACE(l.localidad, ' ', '_')
WHERE
    svm.universidad = REPLACE(UPPER('Universidad Del Salvador'), ' ', '_')
AND
    TO_DATE(svm.fecha_de_inscripcion,'DD-Mon-YY')
        BETWEEN
            TO_DATE('01/09/2020','DD/MM/YYYY')
        AND
            TO_DATE('01/02/2021','DD/MM/YYYY');
