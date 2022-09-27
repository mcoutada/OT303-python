--COMO: Analista de datos
--QUIERO: Escribir el código de dos consultas SQL, una para cada universidad.
--PARA: Obtener los datos de las pesonas anotadas en entre las fechas 01/9/2020 al 01/02/2021 para las siguientes facultades:

--Universidad Tecnológica Nacional

--Universidad Nacional De Tres De Febrero

-- jujuy_utn--

SELECT 
	ju.university, 
	ju.career, 
	ju.inscription_date,
	split_part(ju.nombre,' ',1) AS first_name,
	split_part(ju.nombre ,' ',2) AS last_name,
	ju.sexo as gender,
	date_part('year',age(TO_DATE(ju.birth_date,'YYYY-MM-DD'))) AS age,
	l.codigo_postal as postal_code,
	 ju.location as location,
	email  
FROM jujuy_utn ju 
left join localidad2 l 
on 
upper(ju.location)  = l.localidad
where university  like 'universidad nacional de jujuy'
and 
 	TO_DATE(inscription_date,'YYYY-MM-DD')
        BETWEEN TO_DATE('01/09/2020','DD/MM/YYYY')
        AND TO_DATE('01/02/2021','DD/MM/YYYY')
;
