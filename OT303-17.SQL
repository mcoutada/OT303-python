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

-- Universidad Interamericana 


SELECT 
    it.univiersities AS university,
    it.carrera AS career,
    TO_DATE(it.inscription_dates ,'YY-Mon-DD') AS inscription_date,
    split_part(it.names, '-', 1) AS first_name,
    split_part(it.names, '-', 2) AS last_name,
    it.sexo AS gender,
    DATE_PART(
        'year',
        AGE(
            CASE
                WHEN
                    TO_DATE(it.fechas_nacimiento ,'YY-Mon-DD') > NOW()
                THEN
                    TO_DATE(it.fechas_nacimiento ,'YY-Mon-DD') - interval '100 year'
                ELSE
                    TO_DATE(it.fechas_nacimiento ,'YY-Mon-DD')
            END  )) AS age,
    lo.codigo_postal AS postal_code,
    it.localidad AS location,
    it.email
FROM 
    rio_cuarto_interamericana it, localidad2 lo
WHERE
    UPPER(replace(it.localidad,'-',' '))=lo.localidad 
AND
    TO_DATE(it.inscription_dates,'YY-Mon-DD') BETWEEN '01/09/2020' AND '01/02/2021'
ORDER BY 
    names;