

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
    f.email AS email
FROM jujuy_utn f
LEFT JOIN localidad2 l
ON l.localidad= l.localidad
WHERE university = 'universidad_tecnologica_nacional'
AND TO_DATE(f.inscription_date,'DD-Mon-YY')
BETWEEN TO_DATE('19/01/2020','DD/MM/YYYY') AND TO_DATE('01/02/2021','DD/MM/YYYY');

--universidad de tres de febrero--

SELECT f.universidad AS university, f.careers AS career,f.fecha_de_inscripcion AS inscription_date,
    split_part(f.names, '_', 1) AS first_name,
    split_part(f.names, '_', 2) AS last_name,
    f.sexo AS gender,
    date_part('year',age(TO_DATE(f.birth_dates,'DD-Mon-YY'))) AS age,
    l.codigo_postal AS postal_code,
    l.localidad AS location, f.correos_electronicos
FROM palermo_tres_de_febrero f
LEFT JOIN localidad2 l
ON l.localidad = l.localidad::text
WHERE universidad = 'universidad_nacional_de_tres_de_febrero'
AND TO_DATE(f.fecha_de_inscripcion,'DD-Mon-YY')
        BETWEEN TO_DATE('01/09/2020','DD/MM/YYYY')
        AND TO_DATE('01/02/2021','DD/MM/YYYY');