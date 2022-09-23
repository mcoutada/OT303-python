--COMO: Analista de datos
--QUIERO: Escribir el código de dos consultas SQL, una para cada universidad.
--PARA: Obtener los datos de las pesonas anotadas en entre las fechas 01/9/2020 al 01/02/2021 para las siguientes facultades:

--Universidad Tecnológica Nacional

--Universidad Nacional De Tres De Febrero

-- funcion donde se limita la edad/rango edad--
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


--universidad de tres de febrero--

SELECT f.universidad AS university, f.careers AS career,f.fecha_de_inscripcion AS inscription_date,
    split_part(f.names, '_', 1) AS first_name,
    split_part(f.names, '_', 2) AS last_name,
    f.sexo AS gender,
    l.codigo_postal AS postal_code,
    l.localidad AS location, f.correos_electronicos as correos_electronicos
	
FROM palermo_tres_de_febrero f
LEFT JOIN localidad2 l
ON f.codigo_postal::INT = l.codigo_postal
WHERE universidad LIKE 'universidad_nacional_de_tres_de_febrero'
AND TO_DATE(f.fecha_de_inscripcion,'DD-Mon-YY')
        BETWEEN TO_DATE('01/09/2020','DD/MM/YYYY')
        AND TO_DATE('01/02/2021','DD/MM/YYYY');
