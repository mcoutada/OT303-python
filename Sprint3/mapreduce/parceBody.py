import os
import re
import xml.etree.ElementTree as ET

from numpy import save

file_path = '/home/richarcos/Documentos/Stack Overflow 11-2010/112010 Meta Stack Overflow'
save_path  = 'Sprint3/mapreduce/files'

def parse_body():
    """
    Extrae el body de cada row del archivo xml.    
    """
    tree = ET.parse(os.path.join(file_path, 'posts.xml'))
    root = tree.getroot()
    posts = []

    tag_re = re.compile(r'<[^>]+>')
    link_re = re.compile(r'http\S+')

    with open(os.path.join(save_path, 'posts.txt'), 'w') as f:
        for i in root:
            # Limpiando las etiquetas y enlaces del post usando expresiones regulares
            post = link_re.sub('', tag_re.sub('', i.attrib.get('Body')))
            posts.append(post)
            f.write(f'{post}')
    
    return posts

if __name__ == '__main__':
    print(parse_body())
