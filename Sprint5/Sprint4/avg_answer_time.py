import os
import xml.etree.ElementTree as ET
import datetime

def getScores(data):
    """ Extrae el PostTypeId, Id, Score y CreationDate de los datos y dependiendo si es una pregunta (post_type == 1).

    Args:
        data (iterable): Conjunto de datos (xml)

    Returns:
        dict: Diccionario con los datos de los elementos que son preguntas.
    """

    scores = {}

    for i in data:
        post_type = i.attrib.get('PostTypeId')

        if post_type == '1': # Es una pregunta (Is a question)
            id = i.attrib.get('Id')
            score = i.attrib.get('Score')
            creation_date = i.attrib.get('CreationDate')
            # Preguntando si el id ya existe en el diccionario
            if score not in scores.keys():
                scores[id] = [int(score), creation_date]
        elif post_type == '2': # Es un respuesta (Is an answer)
            pass
    
    # dict {id:[score, creation_date]} tomando solo los id de los que no tienen ParentId
    return scores
    

def ordScores(data):
    """ Ordena los datos y devuelve un diccionario con los 200 scores
        mas altos.

    Args:
        data (dict): Diccionario con los ids y los scores.

    Returns:
        dict: Diccionario de 200 elementos.
    """

    return dict(sorted(data.items(), key=lambda item: item[1], reverse = True)[:200])
    
        
def getParentIds(data, bestIds):
    """ Extrae los ParentsId de la data y compara si estan entre los mejores
        y agrupa las fechas de respuesta.

    Args:
        data (iterable): Conjunto de datos(xml)
        bestIds (dict): Diccionario con los 200 mejores scores.

    Returns:
        dict: Diccionario con los ParentsId y las fechas de cada respuesta.
    """
    parent_scores = {}

    for i in data:
        post_type = i . attrib.get('PostTypeId')

        parent_id = None
        if post_type == '1':
            pass
        elif post_type == '2': 
            parent_id = i.attrib.get('ParentId')
            creation_date = i.attrib.get('CreationDate')
        
        # Preguntando si el ParentId se encuentra dentro de los mejores scores
        if parent_id in bestIds.keys():
            # si se encuentra añadirlo al diccionario junto con las fechas
            if parent_id not in parent_scores.keys():
                parent_scores[parent_id] = []
                parent_scores[parent_id].append(creation_date)
            else:
                parent_scores[parent_id].append(creation_date)
    
    return parent_scores


def mapIds(bestIds, parentsIds):
    """ Recibe los mejores scores y sus "hijos" para agrupar las fechas.

    Args:
        bestIds (dict): Diccionario con los mejores scores
        parentsIds (dict): Diccionario con las respuestas de los posts con mejor score.

    Returns:
        dict: Diccionario con el id(key) y una lista de fechas(value).
    """
    best_scores = {}

    for key in bestIds.keys():
        best_scores[key] = []
        best_scores[key].append(bestIds.get(key)[-1])
        for values in parentsIds.get(key):
            best_scores[key].append(values)

    return best_scores


def avgDate(data):
    """ Saca el promedio del tiempo de todas las fechas de respuesta.

    Args:
        data (dict): Diccionario con las fechas de respuesta 

    Returns:
        dict: Diccionario con el id y el valor (objeto de tipo timedelta) es el promedio de las fechas.
    """
    avg_dates = {}

    for key in data.keys():
        # Extrayendo las dates(values) 
        dates = data.get(key)
        dates_datetime = []
        for date in dates:
            # Transformando la fecha de str a datetime
            dates_datetime.append(datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f'))
        
        date_timedeltas = [dates_datetime[i-1]-dates_datetime[i] for i in range(1, len(dates_datetime))]

        avg_dates[key] = sum(date_timedeltas, datetime.timedelta(0))/len(date_timedeltas)
    
    return avg_dates

def reduceDates(dates):
    """ Saca el promedio de los valores de las fechas previamente promediadas.

    Args:
        dates (dict): Diccionario con los valores promediados de los mejores scores.

    Returns:
        timedelta: Promedio del promedio de las fechas de respuesta de los mejores scores.
    """

    return sum(dates.values(), datetime.timedelta(0))/len(dates.values())


if __name__ == '__main__':
    file_path = '/home/richarcos/Documentos/Stack Overflow 11-2010/112010 Meta Stack Overflow'
    tree = ET.parse(os.path.join(file_path, 'posts.xml'))
    root = tree.getroot()

    best_scores = ordScores(getScores(root))
    parents_ids = getParentIds(root, best_scores)

    print(reduceDates(avgDate(mapIds(best_scores, parents_ids))))
