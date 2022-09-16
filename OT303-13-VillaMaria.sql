/*
Tarea: OT303-13

Objetivo: 
Obtener los datos de las pesonas anotadas en entre las fechas 01/9/2020 al 01/02/2021.
Para las universidades "Universidad De Flores" y "Universidad Nacional De Villa María"

Datos esperados:
university
career
inscription_date
first_name
last_name
gender
age
postal_code
location 
email

Anotaciones: 
usar tabla "localidad2"
Si la fecha de nacimiento > fecha_actual, la edad resulta en negativo (podrían descartarse estos datos).

Aclaración: Las tablas tienen dos universidades cada una. No hace falta interpretar datos que no parezcan lógicos
como fechas de nacimiento y de inscripción fuera del rango de interés.
Ambas tablas contienen datos poco confiables (ej: personas inscriptas que nacieron hace menos de 15 años
o personas inscriptas con mas de 90/100 años)

Solución: se interpretaron correctamente los rangos de inscripción. Se controló la edad negativa.
*/

-- Script para Universidad Nacional De Villa María.


-- Si el año de nacimiento de la persona es mayor al año actual, entonces nacio en 19xx.
-- El problema son los nacidos en el año 22,21,20... O tienen 1 año o 100.
-- Si se considera que para ir a la universidad tenes que ser mayor de edad
-- o mayor de 16/17 años y no se admiten personas menor a esa edad, 
-- entonces estaríamos permitiendo personas de hasta 116/117 años anotadas.

-- Solución elegida: si año > año_actual, nacieron en 1900.
-- PROS: No hay edades negativas.
-- CONTRAS: Se permiten personas de menos de 16/17 años.

-- Mejora posible : retornar una tabla en lugar de un entero,  descartar todas las filas
-- de más de X edad (100) y menos de Y edad (16/17). Retornar el id asociado y en la consulta
-- principal hacer join por el id, descartando las filas que no estén en esta nueva tabla.  

CREATE OR REPLACE FUNCTION calculate_age(fecha_nacimiento DATE) RETURNS integer AS $$
	DECLARE 
		born_year integer := date_part('year', fecha_nacimiento);
		current_year integer := date_part('year', CURRENT_DATE);
	BEGIN
		IF born_year > current_year THEN
			RETURN current_year - (born_year - 100);
		ELSE
			RETURN ROUND((CURRENT_DATE - fecha_nacimiento)/365.25);
		END IF;
	END
$$ LANGUAGE plpgsql;

-- salvador_villa_maria uses '_' instead of ' ' as separator.
SELECT REPLACE(VM.universidad, '_', ' ') AS university,
       REPLACE(VM.carrera, '_', ' ') AS career,
       TO_DATE(VM.fecha_de_inscripcion, 'DD-Mon-YY') AS inscription_date,
	   --Replace all characters after first white space to get name.
       regexp_replace(REPLACE(VM.nombre, '_', ' '), '\s\S+', '') AS first_name,
	   --Replace all characters before first white space to get last name.
       regexp_replace(REPLACE(VM.nombre, '_', ' '), '.+[\s]', '') AS last_name,
       VM.sexo AS gender,
	   --Get age using a function.
       calculate_age(TO_DATE(VM.fecha_nacimiento, 'DD-Mon-YY')) as age, 
       L.codigo_postal AS postal_code,
       REPLACE(VM.localidad,'_', ' ') AS location,
       VM.email AS email
FROM salvador_villa_maria VM
JOIN localidad2 L ON REPLACE(VM.localidad, '_', ' ') = L.localidad
WHERE REPLACE(VM.universidad, '_', ' ') = UPPER('Universidad Nacional De Villa María')
  AND TO_DATE(VM.fecha_de_inscripcion, 'DD-Mon-YY') 
  	BETWEEN TO_DATE('01/9/2020', 'DD/MM/YYYY') AND TO_DATE('01/02/2021', 'DD/MM/YYYY');