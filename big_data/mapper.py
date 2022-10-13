import sys
import re 

# Top 10 fechas con mayor cantidad de post creados -> Then mapping dates and posts

# Relación entre cantidad de respuestas y sus visitas. -> Then mapping answers and views

# Del ranking de los primeros 0-100 por score tomar el tiempo de respuesta promedio 
# informar un único valor.  -> Then mapping scores 


# Mapping information and returning data

for line in sys.stdin:
    line = line.strip()
    post = (str(re.findall("PostTypeId=\".*?\"",line)).replace("PostTypeId=\"","").replace("\"",""))
    date = (str(re.findall("CreationDate=\".*?\"",line)).replace("CreationDate=\"","").replace("\"",""))
    score = (str(re.findall("Score=\".*?\"",line)).replace("Score=\"","").replace("\"",""))
    views = (str(re.findall("ViewCount=\".*?\"",line)).replace("ViewCount=\"","").replace("\"",""))
    answers = (str(re.findall("AnswerCount=\".*?\"",line)).replace("AnswerCount=\"","").replace("\"",""))

    print '%s\t%s' % (post, date, score, views, answers)

