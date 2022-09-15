-- Universidad de Moron
SELECT 
    universidad AS university,
    carrerra AS career,
    fechaiscripccion AS inscription_date,
    SPLIT_PART(nombrre, ' ', 1) AS first_name,
    SPLIT_PART(nombrre, ' ', 2) AS last_name,
    sexo AS gender,
    date_part('year', age(TO_DATE(nacimiento,'DD/MM/YYYY'))) as age,
    codgoposstal AS postal_code,
    direccion AS location,
    eemail AS email
FROM 
    public.moron_nacional_pampa
WHERE 
    TO_DATE(fechaiscripccion,'DD/MM/YYYY') BETWEEN '01/9/2020' AND '01/02/2021';

-- Universidad Nacional del Rio Cuarto
SELECT 
    univiersities AS university,
    carrera AS career,
    TO_DATE(inscription_dates,'YY/Mon/DD') AS inscription_date,
    SPLIT_PART(names, '-', 1) AS first_name,
    SPLIT_PART(names, '-', 2) AS last_name,
    sexo AS gender,
    date_part('year', age(TO_DATE(fechas_nacimiento,'YY/Mon/DD'))) as age,
    SPLIT_PART(direcciones, '-', 6) AS postal_code,
    direcciones AS location,
    email AS email
FROM 
    public.rio_cuarto_interamericana
WHERE
    TO_DATE(inscription_dates,'YY/Mon/DD') BETWEEN '2020-09-01' AND '2021-02-01';
