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