SELECT 
    universidad AS university,
    carrerra AS career,
    fechaiscripccion AS inscription_date,
    SPLIT_PART(nombrre, ' ', 1) AS first_name,
    SPLIT_PART(nombrre, ' ', 2) AS last_name,
    sexo AS gender,
    nacimiento AS fecha_nacimiento,
    direccion AS direccion,
    eemail AS email
FROM
    public.moron_nacional_pampa
WHERE 
    TO_DATE(fechaiscripccion,'DD/MM/YYYY') BETWEEN '01/9/2020' AND '01/02/2021';