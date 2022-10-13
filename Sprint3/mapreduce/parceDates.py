import os
import xml.etree.ElementTree as ET

file_path = '/home/richarcos/Documentos/Stack Overflow 11-2010/112010 Meta Stack Overflow'
save_path  = 'Sprint3/mapreduce/files'

# Parsing data to get all the dates and their posts
def parse_dates():
    """
    Extrae las fechas del archivo xml y las guarda en un archivo txt
    """
    tree = ET.parse(os.path.join(file_path, 'posts.xml'))

    root = tree.getroot()
    
    dates = []

    with open(os.path.join(save_path, 'dates.txt'), 'w') as f:
        for i in root:
            date = i.attrib.get('CreationDate')[0:10]
            dates.append(date)
            f.write(f'{date}\n')
    
    return dates

if __name__ == '__main__':
    parse_dates()

