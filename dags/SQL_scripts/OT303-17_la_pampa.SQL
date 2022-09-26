-- Universidad de La Pampa


SELECT 
    universidad AS university,
    carrerra AS career,
    fechaiscripccion AS inscription_date,
    split_part(nombrre, ' ', 1) AS first_name,
    split_part(nombrre, ' ', 2) AS last_name,
    sexo AS gender,
    date_part('year',age(now()::date,TO_DATE(nacimiento,'DD-MM-YYYY'))) AS age,
    codgoposstal AS postal_code,
    localidad AS location,
    eemail AS email
FROM
    moron_nacional_pampa, localidad2
WHERE
    CAST(codgoposstal AS INT)=codigo_postal
AND
    TO_DATE(fechaiscripccion,'DD-MM-YYYY') BETWEEN '01/09/2020' AND '01/02/2021'
ORDER BY 
    nombrre;

