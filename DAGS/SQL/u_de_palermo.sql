--Universidad de Palermo

SELECT 
	p.universidad as university, 
	p.careers as career, 
	p.fecha_de_inscripcion as inscription_date,
	split_part(p.names ,'_',1) AS first_name,
	split_part(p.names ,'_',2) AS last_name,
	p.sexo  as gender,
	DATE_PART(
        'year',
        AGE(
            CASE
                WHEN
                    TO_DATE(p.birth_dates,'DD-Mon-YY') > NOW()
                THEN
                    TO_DATE(p.birth_dates,'DD-Mon-YY') - interval '100 year'
                ELSE
                    TO_DATE(p.birth_dates,'DD-Mon-YY')
            END
        )
    ) AS age,
	p.codigo_postal  as postal_code,
	lower(l.localidad) as location,
	p.correos_electronicos as email  
FROM palermo_tres_de_febrero p
left join localidad2 l 
on 
	p.codigo_postal::int = l.codigo_postal
where p.universidad  like '_universidad_de_palermo'
and 
 	TO_DATE(p.fecha_de_inscripcion,'DD-Mon-YY')
        BETWEEN
            TO_DATE('01/09/2020','DD-MM-YYYY')
        AND
            TO_DATE('01/02/2021','DD-MM-YYYY')
;
