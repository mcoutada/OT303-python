import os
import xml.etree.ElementTree as ET

from collections import defaultdict

file_path = '/home/richarcos/Documentos/Stack Overflow 11-2010/112010 Meta Stack Overflow'
save_path = 'Sprint3/mapreduce/files'

def parse_score():
    """
    Extrae el score, fecha y parentId de cada registro.
    """
    tree = ET.parse(os.path.join(file_path, 'posts.xml'))
    root = tree.getroot()

    scores = []
    dates = []

    rows = {}
    n = 0

    with open(os.path.join(save_path, 'scores.txt'), 'w') as f:
        for i in root:
            # Extrayendo los atributos
            score = i.attrib.get('Score')
            date = i.attrib.get('CreationDate')

            # Agregando los atributos a una lista
            scores.append(score)
            dates.append(date)

            f.write(f'{score},{date},')

    for score in scores:
        # Si el score (llave) no existe, agregarla al diccionario junto con su fecha.
        if score not in rows.keys():
            rows[score] = []
            rows[score].append(dates[n])
            n += 1
        else:
            rows[score].append(dates[n])
            n += 1
    
    return rows
    

if __name__ == '__main__':
    print(parse_score())
