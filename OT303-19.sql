COMO: Analista de datos
QUIERO: Escribir el código de dos consultas SQL, una para cada universidad.
PARA: Obtener los datos de las pesonas anotadas en entre las fechas 01/9/2020 al 01/02/2021 para las siguientes facultades:


Facultad Latinoamericana De Ciencias Sociales

SELECT
    f.universities AS university,
    f.careers AS career,
    f.inscription_dates,
    split_part(f.names, '_', 1) AS first_name,
    split_part(f.names, '_', 2) AS last_name,
    f.sexo AS gender,
    date_part('year',age(TO_DATE(f.birth_dates,'DD-MM-YY'))) AS age,
    l.codigo_postal AS postal_code,
    f.locations,
    f.emails AS email
FROM
    lat_sociales_cine f
INNER JOIN
    localidad2 l
ON
    l.localidad = l.localidad
WHERE
    universities = '-FACULTAD-LATINOAMERICANA-DE-CIENCIAS-SOCIALES'
AND
    TO_DATE(f.inscription_dates,'DD-MM-YY')
        BETWEEN
            TO_DATE('01/09/2020','DD/MM/YYYY')
        AND
            TO_DATE('01/02/2021','DD/MM/YYYY');




Universidad J. F. Kennedy

AND
select U.universidades AS university, U.carreras AS career, U.fechas_de_inscripcion AS inscription_date, 
    split_part(U.nombres, '-', 1) AS first_name,
    split_part(U.nombres, '-', 2) AS last_name,
    U.sexo AS gender, 
    date_part('year',age(TO_DATE(U.fechas_nacimiento, 'YY-MON-DD'))) AS age,
    l.codigo_postal AS postal_code,
    l.localidad AS location,
    U.emails 
FROM uba_kenedy U
LEFT JOIN localidad2 l
ON
  U.codigos_postales = l.codigo_postal::text

WHERE
    U.universidades = 'universidad-j.-f.-kennedy'	
AND
    TO_DATE(U.fechaS_de_inscripcion,'DD-MON-YY')
        BETWEEN
            TO_DATE('01/09/2020','DD/MM/YYYY')
        AND
            TO_DATE('01/02/2021','DD/MM/YYYY');
