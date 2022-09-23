SELECT 
    univiersities AS university,
    carrera AS career,
    TO_DATE(inscription_dates,'YY/Mon/DD') AS inscription_date,
    SPLIT_PART(names, '-', 1) AS first_name,
    SPLIT_PART(names, '-', 2) AS last_name,
    sexo AS gender,
    fechas_nacimiento AS fecha_nacimiento,
    direcciones AS direccion,
    email AS email
FROM 
    public.rio_cuarto_interamericana
WHERE
    TO_DATE(inscription_dates,'YY/Mon/DD') BETWEEN '2020-09-01' AND '2021-02-01';