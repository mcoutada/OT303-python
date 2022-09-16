COMO: Analista de datos
QUIERO: Escribir el código de dos consultas SQL, una para cada universidad.
PARA: Obtener los datos de las pesonas anotadas en entre las fechas 01/9/2020 al 01/02/2021 para las siguientes facultades:


Facultad Latinoamericana De Ciencias Sociales

SELECT
    f.universities AS university,
    f.careers AS career,
    f.inscription_dates,
    split_part(f.names, '-', 1) AS first_name,
    split_part(f.names, '-', 2) AS last_name,
    f.sexo AS gender,
	l.codigo_postal AS postal_code,
    f.locations,
    f.emails AS email,
     DATE_PART(
        'year',
        AGE(
            CASE
                WHEN
                    TO_DATE(f.birth_dates,'DD-MM-YY') > NOW()
                THEN
                    TO_DATE(f.birth_dates,'DD-MM-YY') - interval '100 year'
                ELSE
                    TO_DATE(f.birth_dates,'DD-MM-YY')
            END  )) AS age
    
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


SELECT
    Uk.universidades AS university,
    Uk.carreras AS career,
    Uk.fechas_de_inscripcion AS inscription_date,
    SPLIT_PART(Uk.nombres, '-', 1) AS first_name,
    SPLIT_PART(Uk.nombres, '-', 2) AS last_name,
    Uk.sexo AS gender,
    DATE_PART(
        'year',
        AGE(
            CASE
                WHEN
                    TO_DATE(Uk.fechas_nacimiento,'YY-MON-DD') > NOW()
                THEN
                    TO_DATE(Uk.fechas_nacimiento,'YY-MON-DD') - interval '100 year'
                ELSE
                    TO_DATE(Uk.fechas_nacimiento,'YY-MON-DD')
            END  )
    ) AS age,
    l.codigo_postal AS postal_code,
    l.localidad AS location,
    emails
FROM
    uba_kenedy fc
LEFT JOIN
    localidad2 l
ON
  Uk.codigos_postales = l.codigo_postal::text
WHERE
    Uk.universidades = ('universidad-j.-f.-kennedy')
AND
    TO_DATE(Uk.fechas_de_inscripcion,'DD-MON-YY')
        BETWEEN
            TO_DATE('01/09/2020','DD/MM/YYYY')
        AND
            TO_DATE('01/02/2021','DD/MM/YYYY');