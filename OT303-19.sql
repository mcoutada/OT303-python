--COMO: Analista de datos
--QUIERO: Escribir el código de dos consultas SQL, una para cada universidad.
--PARA: Obtener los datos de las pesonas anotadas en entre las fechas 01/9/2020 al 01/02/2021 para las siguientes facultades:

--Universidad Tecnológica Nacional

--Universidad Nacional De Tres De Febrero

-- jujuy_utn--
	SELECT
    f.university AS university,
    f.career AS career,
    f.inscription_date AS inscription_date,
    split_part(f.nombre, ' ', 1) AS first_name,
    split_part(f.nombre, ' ', 2) AS last_name,
    f.sexo AS gender,
    date_part('year',age(TO_DATE(f.birth_date,'DD-MM-YYYY'))) AS age,
    l.codigo_postal AS postal_code,
    f.location AS location,
    f.email AS email,
	--se agrego un case debido a que muchas fechas estaban en texto y no en entero--
	 DATE_PART(
        'year',
        AGE(
            CASE
                WHEN
                    TO_DATE(f.birth_date,'DD-MM-YY') > NOW()
                THEN
                    TO_DATE(f.birth_date,'DD-MM-YY') - interval '100 year'
                ELSE
                    TO_DATE(f.birth_date,'DD-MM-YY')
            END  )) AS age
FROM jujuy_utn f
INNER JOIN localidad2 l
ON l.codigo_postal= l.codigo_postal::text
WHERE university = 'universidad_tecnologica_nacional'
AND TO_DATE(f.inscription_date,'DD-Mon-YY')
BETWEEN TO_DATE('19/01/2020','DD/MM/YYYY') AND TO_DATE('01/02/2021','DD/MM/YYYY');

--universidad de tres de febrero--

SELECT f.universidad AS university, f.careers AS career,f.fecha_de_inscripcion AS inscription_date,
    split_part(f.names, '_', 1) AS first_name,
    split_part(f.names, '_', 2) AS last_name,
    f.sexo AS gender,
    l.codigo_postal AS postal_code,
    l.localidad AS location, f.correos_electronicos as correos_electronicos,
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
FROM palermo_tres_de_febrero f
INNER JOIN localidad2 l
ON CAST(f.codigo_postal AS INT) = l.codigo_postal
WHERE universidad = 'universidad_nacional_de_tres_de_febrero'
AND TO_DATE(f.fecha_de_inscripcion,'YYYY-MM-DD')
        BETWEEN TO_DATE('01/09/2020','DD/MM/YY')
        AND TO_DATE('01/02/2021','DD/MM/YY');