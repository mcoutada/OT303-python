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
