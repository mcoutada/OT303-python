--Universidad de Palermo

CREATE OR REPLACE FUNCTION calculate_age(p.birth_dates DATE) RETURNS integer
	DECLARE 
		born_year integer := date_part('year', (p.birth_dates);
		current_year integer := date_part('year', CURRENT_DATE);
	BEGIN
		IF born_year > current_year THEN
			RETURN current_year - (born_year - 100);
		ELSE
			RETURN ROUND((CURRENT_DATE - (p.birth_dates)/365.25);
		END IF;
	END


SELECT 
	p.universidad as university, 
	p.careers as career, 
	p.fecha_de_inscripcion as inscription_date,
	split_part(p.names ,'_',1) AS first_name,
	split_part(p.names ,'_',2) AS last_name,
	p.sexo  as gender,
	calculate_age(TO_DATE(p.birth_dates, 'DD-Mon-YY')) as age,
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
