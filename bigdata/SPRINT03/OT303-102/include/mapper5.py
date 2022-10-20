# import sys because we need to read and write data to STDIN and STDOUT
import sys
import xml.etree.ElementTree as ET

# Mapper para: Relacion entre la cantidad de respuestas en un post y su puntaje
# (no era requerimiento mío, pero lo expusimos en el proyecto final así que lo hice)



# input comes from STDIN (standard input)
for line in sys.stdin:

    # 'PostTypeId="1"'  --> It's a question
    if 'PostTypeId="1"' in line and "AnswerCount" in line and "Score" in line:

        mapped = ET.fromstring(line)

        if "AnswerCount" in mapped.attrib:
            answ_cnt = mapped.attrib["AnswerCount"]
        else:
            answ_cnt = 0

        if "Score" in mapped.attrib:
            sco_cnt = mapped.attrib["Score"]
        else:
            sco_cnt = 0
        
        print(f"{answ_cnt}\t{sco_cnt}")
