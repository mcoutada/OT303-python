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