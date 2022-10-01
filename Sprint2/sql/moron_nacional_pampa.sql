SELECT 
    MNP.universidad AS university,
    MNP.carrerra AS career,
    MNP.fechaiscripccion AS inscription_date,
    SPLIT_PART(MNP.nombrre, ' ', 1) AS first_name,
    SPLIT_PART(MNP.nombrre, ' ', 2) AS last_name,
    MNP.sexo AS gender,
    date_part('year', age(TO_DATE(MNP.nacimiento,'DD/MM/YYYY'))) as age,
    MNP.codgoposstal AS postal_code,
    L.localidad AS location,
    MNP.eemail AS email
FROM
    moron_nacional_pampa MNP
INNER JOIN localidad2 L ON MNP.codgoposstal = CAST(L.codigo_postal AS varchar)
WHERE 
    TO_DATE(MNP.fechaiscripccion,'DD/MM/YYYY') BETWEEN '01/9/2020' AND '01/02/2021';