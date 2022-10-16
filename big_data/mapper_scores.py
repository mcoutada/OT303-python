import sys
import re 

# Del ranking de los primeros 0-100 por score tomar el tiempo de respuesta promedio 
# informar un único valor.

for line in sys.stdin:
    line = line.strip()

    post_id = (str(re.findall(" Id=\".*?\"",line)).replace(" Id=\"","").replace("\"","")) #Individual Id 
    posttype = (str(re.findall("PostTypeId=\".*?\"",line)).replace("PostTypeId=\"","").replace("\"","")) #Type 1-Question 2-Answer
    parent_post = (str(re.findall("ParentId=\".*?\"",line)).replace("ParentId=\"","").replace("\"","")) #Parent Id
    date = (str(re.findall("CreationDate=\".*?\"",line)).replace("CreationDate=\"","").replace("\"",""))
    score = (str(re.findall("Score=\".*?\"",line)).replace("Score=\"","").replace("\"",""))
    print '%s\t%s' % (post_id, posttype, date, score, parent_post)
