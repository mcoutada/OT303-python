#COMO: Analista de datos
#QUIERO: Realizar test unitarios
#PARA: Para poder hacer un desarrollo escalable y a prueba de errores

#Criterios de aceptación: 
#Para esto necesitamos realizar test unitarios de cada funcion que se utilice en el script de map reduce que procesa los siguientes datos:

#Top 10 tipo de post sin respuestas aceptadas

#Relación entre cantidad de respuestas de un post y su puntaje.

#Top 10 preguntas que tuvieron mayor tiempo de actividad


from functions import *
from pathlib import Path
import os
import xml.etree.ElementTree as ET

log_file_path = Path(f"{os.path.dirname(os.path.realpath(__file__))}").parent.parent
mytree = ET.parse(f'{log_file_path}/information/posts.xml')
myroot = mytree.getroot()

def test_xmlFile_exist():
    """el texto xml existe asi se puede importar """
    assert mytree != None

def test_preguntas_sin_respuest():
   
    assert test_preguntas_sin_respuest(myroot) != None
    assert len(test_preguntas_sin_respuest(myroot)) > 0

def test_avg_post_mapper():
    
    assert test_avg_post_mapper(myroot) != None
    assert len(test_avg_post_mapper(myroot)) > 0

def test_top10_pregunt():
   
    assert test_top10_pregunt(myroot) != None
    assert len(test_top10_pregunt(myroot)) > 0


def test_preguntas_sin_respuest():
   
    assert reducerAcceptedAnswers(test_preguntas_sin_respuest(myroot)) != None
    assert len(reducerAcceptedAnswers(test_preguntas_sin_respuest(myroot))) == 10

def test_avg_post_mapper():
    """se controla que la informacion obtenida del mapper este bien ara las 3 preguntas"""

    assert reducerAcceptedAnswers(test_avg_post_mapper(myroot)) != None
    assert len(reducerAcceptedAnswers(test_avg_post_mapper(myroot))) == 10

def test_top10_pregunt():
    
    assert reducerAcceptedAnswers(test_top10_pregunt(myroot)) != None
    assert len(reducerAcceptedAnswers(test_top10_pregunt(myroot))) > 0
    