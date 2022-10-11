# In this file where tested xml functions.

import xml.etree.ElementTree as ET
import os
# Properties
# Tag (represents type of data)
# Attributes (att stored as dict)
# Text String (text string having information that needs to be displayed )
# Tail String ( optional )
# Child Elements ( numbers of child elements stored as sequences)

root_path = '/home/lautaro/Cursos/Alkemy/Stack Overflow 11-2010/112010 Meta Stack Overflow'


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
    # Por cada post de posts.xml ->
    #   IF PostTypeId=1 THEN tiene AcceptedAnswerId <get tags y map>.
    #   ELSE saltear
    # Map < Nombre_Tag, 1>
    # Cuando termina el for, llamar a reduce.
    # Seleccionar los 10 tags con mayor valor.


def avg_answer_post():
    '''Demora de respuesta promedio en posts'''
    pass
    # Por cada post de posts.xml ->
    # Si PostTypeId = 1 (Question) CreationDate
    #   Guardar en un map <postId, fecha de creación>
    # Si PostTypeId = 2 (Answer) CreationDate
    #   Guardar en un map <ParentID, list<CreationDate>
    #
    # Al finalizar el for, recorrer la lista de Creation date, calcular un promedio.
    # Map < promedio, 1>
    # Reduce


def avg_words_score():
    '''Relación entre cantidad de palabras en un post y su puntaje'''
    pass
    # Por cada post de posts.xml ->
    # Si PostTypeId = 1o2 (Question/Answer)
    #   Contar palabras del Body. (usra beutyfulsoup html parser)
    #   Devolver [cant_words, score]


if __name__ == '__main__':
    root = parse()
    find_element(root)
