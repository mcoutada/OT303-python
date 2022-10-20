# import sys because we need to read and write data to STDIN and STDOUT
import sys
import xml.etree.ElementTree as ET

# Mapper para: Relación entre cantidad de palabras en un post y su cantidad de respuestas
# (no era requerimiento mio, pero lo expusimos en el proyecto final así que lo hice)

# input comes from STDIN (standard input)
for line in sys.stdin:

    # 'PostTypeId="1"'  --> It's a question (anwsers have their viewCount set to 0)
    #'Body="' in line --> Just making sure it has a body, it should, this might not be needed...
    if 'PostTypeId="1"' in line and 'Body="' in line:
        mapped = ET.fromstring(line)
        # Simple aproach
        wrd_cnt = len(mapped.attrib["Body"].split())

        if "AnswerCount" in mapped.attrib:
            answ_cnt = mapped.attrib["AnswerCount"]
        else:
            answ_cnt = 0

        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py

        print(f"{wrd_cnt}\t{answ_cnt}")
