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
    univiersities AS university,
    carrera AS career,
    TO_DATE(inscription_dates,'YY/Mon/DD') AS inscription_date,
    SPLIT_PART(names, '-', 1) AS first_name,
    SPLIT_PART(names, '-', 2) AS last_name,
    sexo AS gender,
    calcular_edad(TO_DATE(fechas_nacimiento, 'YY/Mon/DD')) as age,
    SPLIT_PART(direcciones, '-', 6) AS postal_code,
    direcciones AS location,
    email AS email
FROM 
    public.rio_cuarto_interamericana
WHERE
    TO_DATE(inscription_dates,'YY/Mon/DD') BETWEEN '2020-09-01' AND '2021-02-01';