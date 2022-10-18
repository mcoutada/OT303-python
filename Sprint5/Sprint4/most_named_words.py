import string
import xml.etree.ElementTree as ET
import re
import os

def parseBody(data):
    """ Extrae el contenido (Body) de los datos. Quita las etiquetas html.

    Args:
        data (iterable): conjunto de datos (xml)

    Returns:
        list: Lista con el contenido (Body) de los posts.
    """
    content = []

    tag_re = re.compile(r'<[^>]+>')
    link_re = re.compile(r'^https?:\/\/.*[\r\n]*')

    for i in data:
        post = link_re.sub('',
                            tag_re.sub('',
                            i.attrib.get('Body')))
        content.append(post)

    return content

def mapBody(data):
    """ Cuenta el número de ocurrencias que aparece cada palabra.

    Args:
        data (list): Lista para contar las palabras.

    Returns:
        dict: Diccionario con la palabra y el número de ocurrencias.
    """
    freq_dict = {}

    for post in data:
        
        post = post.strip()

        post = post.lower()

        for val in string.punctuation:
            if val not in ("'"):
                post = post.replace(val,"")
        
        words = post.split(" ")

        for word in words:
            if not (word in freq_dict.keys()):
                freq_dict[word] = 1
            else:
                freq_dict[word] += 1
    
    return freq_dict

def reduceBody(data):
    """ Ordena los datos para obtener las diez palabras con mayor ocurrencia.

    Args:
        data (dict): Diccionario con palabras y el número de ocurrencias.

    Returns:
        dict: Diccionario con diez elementos.
    """
    
    res = sorted(data, key=data.get, reverse=True)[:10]
    max_words = {}

    for key in data:
        if key in res:
            max_words[key] = data.get(key)
    
    return max_words

if __name__ == '__main__':
    file_path = '/home/richarcos/Documentos/Stack Overflow 11-2010/112010 Meta Stack Overflow'
    tree = ET.parse(os.path.join(file_path, 'posts.xml'))
    root = tree.getroot()

    print(reduceBody(mapBody(parseBody(root))))
