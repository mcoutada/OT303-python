SELECT 
    RCI.univiersities AS university,
    RCI.carrera AS career,
    TO_DATE(RCI.inscription_dates,'YY/Mon/DD') AS inscription_date,
    SPLIT_PART(RCI.names, '-', 1) AS first_name,
    SPLIT_PART(RCI.names, '-', 2) AS last_name,
    RCI.sexo AS gender,
    DATE_PART(
    'year',
    AGE(
        CASE
            WHEN
                TO_DATE(RCI.fechas_nacimiento, 'YY/Mon/DD') > CURRENT_DATE
            THEN
                TO_DATE(RCI.fechas_nacimiento, 'YY/Mon/DD') - INTERVAL '100 YEARS'
            ELSE
                TO_DATE(RCI.fechas_nacimiento, 'YY/Mon/DD')
        END
        )
    ) AS age,
    L.codigo_postal AS postal_code,
    REPLACE(RCI.localidad, '-', ' ') AS location,
    RCI.email AS email
FROM 
    rio_cuarto_interamericana RCI
JOIN localidad2 L 
ON LOWER(REPLACE(RCI.localidad, '-', ' ')) = LOWER(L.localidad)
WHERE
    TO_DATE(RCI.inscription_dates,'YY/Mon/DD') BETWEEN '2020-09-01' AND '2021-02-01';