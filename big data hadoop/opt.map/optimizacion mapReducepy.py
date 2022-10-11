#COMO: Analista de datos
#QUIERO: Optimizar la ejecución actual del MapReduce
#PARA: Poder ejectuar la misma o mayor cantidad de datos en menos tiempo

#Criterios de aceptación: 

#Utilizar otra técnica compatible con Hadoop vistas en la clase 

#Documentación de referencia: https://hadoop.apache.org/docs/r1.2.1/mapred_tutorial.html

#Otras técnicas interesantes: https://techvidvan.com/tutorials/mapreduce-job-optimization-techniques/


import xml.etree.ElementTree as ET
import collections
import csv
from pathlib import Path
import time
from multiprocessing import Pool

FILE_PATH = "dataset BIG DATA/112010 Meta Stack Overflow/posts.xml"


def divide_chunks(lista, numero):
    #en esta funcion se van generando los chunks
    

    for i in range(0, len(lista), numero):
        yield lista[i : i + numero]


def chunkify(xmlfile, number_of_chunks=16):
    #nombre del archivo chunk a procesar
        #xmlfile (str): nombre del archivo a procesar
        #number_of_chunks (int, optional): cantidad de chunks en los que se divide la informacion. Defaults to 16.
   

    # create element tree object
    tree = ET.parse(xmlfile)

    # get root element
    root = tree.getroot()

    list_tags = []
    # looping till length l
    for row in root.iter("row"):
        dir_row = row.attrib
      
        if dir_row.get("PostTypeId") == "1":

            # las que alla aceptado como respuesta son mapeadas
            if dir_row.get("AcceptedAnswerId") == None:
                tags_names = (
                    dir_row.get("Tags")
                    .replace("<", "")
                    .replace(">", " ")
                    .lstrip()
                    .split()
                )
                list_tags.append(tags_names)

    list_chunks = list(divide_chunks(list_tags, number_of_chunks))
    return list_chunks


def mapper(chunk):
    #se mapea pasando de una lista de chunks que contienen una lista de listas de tags 
    # a una lista con todas las listas de tags.
  
    listado = []
    for listado_listas_tags in chunk:
        for tags in listado_listas_tags:
            listado.append(tags)
    return listado


def shuffler(mapper):
   #shuffle devuelve la secuencia x pasada como argumento

    lista = []
    for lista_tags in mapper:
        for tag in lista_tags:
            lista.append(tag)
    return lista


# Funcion que reduce y resuelve segun las consignas
def reduce(lista):
 
    # Con la funcion y metodo "collections.Couter", agrupo por tags y cuento sus ocurrencias, se toman los 10 con mas ocurrencias
    # el resultado se agrega a la lista de resultados
    return collections.Counter(lista).most_common(10)


def savetoCSV(data, filename, fields):
    #Esta funcion graba los archivos de salida.
  

    # los datos vienen como una lista y graba el CSV
    with open(f"dev_wl/big_data/{filename}", "w") as csvfile:
        csv_out = csv.writer(csvfile)
        # writing headers (field names)
        csv_out.writerow(fields)
        # writing data rows
        for row in data:
            csv_out.writerow(row)


if __name__ == "__main__":
    #Se ejecunta los diferentes pasos para realizar el Map Reduce.
    

    start = time.time()
    # set path root
    root = Path.cwd()

    # mombre del archivo a mapear y reducir
    file = Path(root / FILE_PATH)

    # divido la informacion a extraer de los tags en 16 chunks
    data_chunks = chunkify(file, number_of_chunks=16)

    # se paraleliza el proceso de mapeado, en Pool se pone processes en None, entonces se utiliza el número retornado por os.cpu_count().
    pool = Pool(processes=None)
    # se procesa cada chunk y se retorna un listado con listados de listas de tags
    mapper = pool.map(mapper, data_chunks, chunksize=16)

    shuffled = shuffler(mapper)

    list_result = reduce(shuffled)

    print(type(list_result))
    print(list_result)

    end = time.time()

    print(end - start)

    # Graba los resultados en un CSV
    savetoCSV(list_result, "OP_top10tags.csv", ["TAG", "COUNT"])
