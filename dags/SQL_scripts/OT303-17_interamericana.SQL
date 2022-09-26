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
