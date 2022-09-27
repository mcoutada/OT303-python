CREATE OR REPLACE FUNCTION calcular_edad(fechas_nacimiento DATE) RETURNS integer as $$
    DECLARE
        anio_nacimiento integer := date_part('year', fechas_nacimiento);
        anio_actual integer := date_part('year', CURRENT_DATE);
    BEGIN
        IF anio_nacimiento > anio_actual THEN
            RETURN anio_actual - (anio_nacimiento - 100);
        ELSE
            RETURN ROUND((CURRENT_DATE - fechas_nacimiento)/365.25);
        END IF;
    END
$$ LANGUAGE plpgsql;

SELECT 
    RCI.univiersities AS university,
    RCI.carrera AS career,
    TO_DATE(RCI.inscription_dates,'YY/Mon/DD') AS inscription_date,
    SPLIT_PART(RCI.names, '-', 1) AS first_name,
    SPLIT_PART(RCI.names, '-', 2) AS last_name,
    RCI.sexo AS gender,
    calcular_edad(TO_DATE(RCI.fechas_nacimiento, 'YY/Mon/DD')) as age,
    L.codigo_postal AS postal_code,
    REPLACE(RCI.localidad, '-', ' ') AS location,
    RCI.email AS email
FROM 
    rio_cuarto_interamericana RCI
JOIN localidad2 L 
ON LOWER(REPLACE(RCI.localidad, '-', ' ')) = LOWER(L.localidad)
WHERE
    TO_DATE(RCI.inscription_dates,'YY/Mon/DD') BETWEEN '2020-09-01' AND '2021-02-01';