/*
Tarea: OT303-13

Objetivo: Obtener los datos de las pesonas anotadas en entre las fechas 01/9/2020 al 01/02/2021.
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

Anotaciones: usar tabla "localidad2"
Si la fecha de nacimiento > fecha_actual, la edad resulta en negativo (podrían descartarse estos datos).

*/

-- Script para Universidad De Flores. 
SELECT FC.universidad AS university,
       FC.carrera AS career,
       FC.fecha_de_inscripcion AS inscription_date,
       regexp_replace(name, '\s\S+', '') AS first_name,
       regexp_replace(name, '.+[\s]', '') AS last_name,
       FC.sexo AS gender,
       EXTRACT(YEAR
               FROM AGE(TO_DATE(FC.fecha_nacimiento, 'YYYY-MM-DD'))) AS age,
       FC.codigo_postal AS postal_code,
       L.localidad AS LOCATION,
       FC.correo_electronico AS email
FROM flores_comahue FC
INNER JOIN localidad2 L ON CAST(FC.codigo_postal AS INT) = L.codigo_postal
WHERE FC.universidad = UPPER('Universidad De Flores')
  AND TO_DATE(FC.fecha_de_inscripcion, 'YYYY-MM-DD') 
  	BETWEEN TO_DATE('01/9/2020', 'DD-MM-YYYY') AND TO_DATE('01/02/2021', 'DD-MM-YYYY');


-- BORRAR chequeos

/*
SELECT FC.fecha_de_inscripcion AS inscripcion 
FROM FLORES_COMAHUE FC
WHERE TO_DATE(FC.fecha_de_inscripcion,'YYYY-MM-DD') 
BETWEEN TO_DATE('01/9/2020','DD/MM/YYYY')
AND TO_DATE('01/02/2021','DD/MM/YYYY')
LIMIT 5;
*/

--SELECT 
--	FC.FECHA_NACIMIENTO AS FECHA_NAC, 
--	EXTRACT(YEAR FROM AGE(TO_DATE(FC.FECHA_NACIMIENTO,'YYYY-MM-DD'))) AS AGE,
--	AGE(TO_DATE(FC.FECHA_NACIMIENTO,'YYYY-MM-DD')) as age2
--FROM FLORES_COMAHUE FC LIMIT 5;

--SELECT name as NOMBRE_COMPLETO, regexp_replace(name,'\s\S+','') AS nombre, regexp_replace(name,'.+[\s]','')   as apellido FROM FLORES_COMAHUE FC LIMIT 5;
-- Nombre: me quedo con la primer parte, elimino todo lo que sigue al espacio.
-- Apellido: me quedo con la segunda parte, elimino todo lo que viene antes del espacio en blanco.
-- .Lo anterior, +repeticiones (hasta), [\s] un blanco. (https://regex101.com/)

--SELECT * FROM localidad2 WHERE codigo_postal = 3722 OR codigo_postal=7261 or codigo_postal=5471;
-- 2 de mayo, saladillo norte, agua blanca.



-- Script para Universidad Nacional De Villa María. 
SELECT REPLACE(VM.universidad, '_', ' ') AS university,
       REPLACE(VM.carrera, '_', ' ') AS career,
       TO_DATE(VM.fecha_de_inscripcion, 'DD-Mon-YY') AS inscription_date,
       regexp_replace(REPLACE(VM.nombre, '_', ' '), '\s\S+', '') AS first_name,
       regexp_replace(REPLACE(VM.nombre, '_', ' '), '.+[\s]', '') AS last_name,
       VM.sexo AS gender,
       EXTRACT(YEAR
               FROM AGE(TO_DATE(VM.fecha_nacimiento, 'DD-Mon-YY'))) AS age,
       L.codigo_postal AS postal_code,
       VM.localidad AS LOCATION,
       VM.email AS email
FROM salvador_villa_maria VM
INNER JOIN localidad2 L ON REPLACE(VM.localidad, '_', ' ') = L.localidad
WHERE REPLACE(VM.universidad, '_', ' ') = UPPER('Universidad Nacional De Villa María')
  AND TO_DATE(VM.fecha_de_inscripcion, 'DD-Mon-YY') 
  	BETWEEN TO_DATE('01/9/2020', 'DD/MM/YYYY') AND TO_DATE('01/02/2021', 'DD/MM/YYYY');

--SELECT * FROM salvador_villa_maria VM WHERE VM.nombre = 'CLAUDIA_MCGEE';

--Borrar chequeos:

--Fecha entre
/*
SELECT VM.fecha_de_inscripcion, TO_DATE(VM.fecha_de_inscripcion,'DD-Mon-YY') as inscription_date 
FROM salvador_villa_maria VM 
WHERE TO_DATE(VM.fecha_de_inscripcion,'DD-Mon-YY') 
BETWEEN TO_DATE('01/9/2020','DD/MM/YYYY')
AND TO_DATE('01/02/2021','DD/MM/YYYY')
ORDER BY inscription_date DESC
LIMIT 5;
*/

--Universidad
/*
SELECT * FROM salvador_villa_maria VM 
WHERE REPLACE(VM.universidad,'_',' ') = UPPER('Universidad Nacional De Villa María') 
LIMIT 5;
*/

--Codigo Postal
/*
SELECT  L.codigo_postal, L.localidad, REPLACE(VM.localidad,'_',' ')  
FROM salvador_villa_maria VM INNER JOIN localidad2 L
ON REPLACE(VM.localidad,'_',' ') = L.localidad ;
*/

--Edad
/*
SELECT TO_DATE(VM.fecha_nacimiento,'DD-Mon-YY') AS fecha_nac,
EXTRACT(YEAR FROM AGE(TO_DATE(VM.fecha_nacimiento,'DD-Mon-YY'))) AS age
FROM salvador_villa_maria VM 
LIMIT 5;
*/

--Fecha 
/*
SELECT VM.fecha_de_inscripcion, TO_DATE(VM.fecha_de_inscripcion,'DD-Mon-YY') as inscription_date 
FROM salvador_villa_maria VM 
LIMIT 5;
*/

--Nombre y apellido.
/*
SELECT regexp_replace(REPLACE(VM.nombre,'_',' '),'\s\S+','') AS FIRST_NAME,
	regexp_replace(REPLACE(VM.nombre,'_',' '),'.+[\s]','') AS LAST_NAME 
FROM salvador_villa_maria VM limit 5;
*/
