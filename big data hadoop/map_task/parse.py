#funcion parser para los xml

import xml.etree.ElementTree as ET
import os


root_path = '/dataset BIG DATA/hadoop/Stack Overflow 11-2010/112010 Meta Stack Overflow.xml'


def parse() -> ET.Element:
    my_tree = ET.parse(os.path.join(root_path, 'posts.xml'))
    my_root = my_tree.getroot()
    return my_root


def find_element(root: ET.Element):
    print('Main Tag: ', root.tag)
    print('Total rows: ', len(root))
    print('Root 0 Tag: ', root[0].tag)
    print('Total rows: ', len(root[0]))
    # Print 56974 rows.
    for x in root:
        print(x.tag)  # row
        print(x.text)  # none
        print(x.attrib)  # dict with key-value
        break

    attributes = root[0].attrib
    for k, v in attributes.items():
        print(f'Key: {k} , Value: {v}')

    # Print some att
    print(f'The post {attributes["Id"]} have scored {attributes["Score"]}')

    # Find all rows and get items.
    for x in root.findall('row'):
        item = x.get('Id')
        score = x.get('Score')
        print(f'The id is {item} and the score {score}')
        break


def top_10_positive_tags():
    '''Top 10 tags con mayores respuestas aceptadas'''
    pass


def avg_answer_post():
    
    pass
   

def avg_words_score():
    '''Relación entre cantidad de palabras en un post y su puntaje'''
    pass
   

if __name__ == '__main__':
    root = parse()
    find_element(root)