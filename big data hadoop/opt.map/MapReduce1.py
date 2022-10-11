import xml.etree.ElementTree as ET
import collections
import csv
import pandas as pd
from pathlib import Path
import time

FILE_PATH = "dataset BIG DATA /112010 Meta Stack Overflow/posts.xml"
def mapper(xmlfile):
   
    # creo un tree
    tree = ET.parse(xmlfile)

    # obtengo un root
    root = tree.getroot()

    # listas que usare para mapp
    list_mapper = []
    list_tags = []
    list_dic = []
    list_dic_question = []
    list_dic_answer = []

    
    #iteracion a travez de los rows del xml file hacia los mapp
    for row in root.iter("row"):
        dir_row = row.attrib
        # The record is selected and it is processed, if it is a question type
        if dir_row.get("PostTypeId") == "1":
            body = (
                dir_row.get("Body").replace("<", "").replace(">", " ").lstrip().split()
            )
            view_count = dir_row.get("ViewCount")
            body_count_words = len(body)
            
            if dir_row.get("AcceptedAnswerId") == None:
                tags_names = (
                    dir_row.get("Tags")
                    .replace("<", "")
                    .replace(">", " ")
                    .lstrip()
                    .split()
                )
                list_tags.append(tags_names)
                list_dic.append(
                    {
                        "body_count_words": body_count_words,
                        "view_count": int(view_count),
                    }
                )
            # los favoritos pasan a mapp
            if dir_row.get("FavoriteCount") != None:
                favorite_count = dir_row.get("FavoriteCount")
                id = dir_row.get("Id")
                list_dic_question.append({"id": id, "favorite_count": favorite_count})
        
        else:
            parent_id = dir_row.get("ParentId")
            score_answer = dir_row.get("Score")
            list_dic_answer.append(
                {"parent_id": parent_id, "score_answer": score_answer}
            )

    # guardamos la lista y luego es convertida a mapp
    list_mapper.append(list_tags)
    list_mapper.append(list_dic)
    list_mapper.append(list_dic_question)
    list_mapper.append(list_dic_answer)
    return list_mapper


# Funcion que acomoda y ordena los datos mapeados para que sean reducidos
def shuffle_sort(list_mapper):
#Acomoda y ordena las listas que se reciben como parametro con los datos mapeados.
    
   
    # lista en donde se devolveran las listas que contienen el resultado del proceso.
    list_shuffled = []

    # para almacenar los tags
    # "list_mapper[0]" trae los TAGs de las preguntas si respuesta aceptada mapeados
    list_all_tags = []
    for list_tags in list_mapper[0]:
        for tags in list_tags:
            list_all_tags.append(tags)
    list_shuffled.append(list_all_tags)

    # proceso el segundo mapeado de palabras y vistas, cada valor dentro de la lista es un diccionario
    # clave: word y valor: vistas, se crea un dataframe con dos columnas: "body_count_words", "view_count"

    df_words_views = pd.DataFrame(list_mapper[1])
    data_w_v = df_words_views.sort_values(
        by="body_count_words", axis=0, ascending=False, inplace=False
    )
    list_shuffled.append(data_w_v)

    # proceso 3 y 4, Puntaje promedio de las repuestas con mas favoritos, para obtener este dato se trabaja con los registros
   
    df_questions = pd.DataFrame(list_mapper[2])
    df_questions.favorite_count = df_questions.favorite_count.astype("int64")
    
    # "list_mapper[3]" trae los registros de las respuetas mapeadas
    df_answers = pd.DataFrame(list_mapper[3])
    df_answers.score_answer = df_answers.score_answer.astype("int64")
    
    
    df_questions_answers = pd.merge(
        df_questions, df_answers, how="left", left_on="id", right_on="parent_id"
    )

 
    list_shuffled.append(df_questions_answers)

    return list_shuffled


# Funcio que reduce y resuelve segun las consignas
def reduce(list_shuffled):
    # Esta funcion reduce los datos que se reciben acomodados y ordenados para generar la resplucion de las consignas
   
    #lista que se retornara con los elementos reducidos
    list_result = []
    
    # Con la funcion y metodo "collections.Couter", agrupo por tags y cuento sus ocurrencias, se toman los 10 con mas ocurrencias
    # el resultado se agrega a la lista de resultados
    list_result.append(collections.Counter(list_shuffled[0]).most_common(10))

    # reduzco lo mapeado para conseguir la relación entre cantidad de palabras en un post y su cantidad de visitas
    df = list_shuffled[1]
    tabla_words_count_views = []
    list_word_count = df.body_count_words.unique().tolist()
    for word_count in list_word_count:
        mask = df.body_count_words == word_count
        serie_views = df[mask].view_count.sort_values(
            axis=0, ascending=False, inplace=False
        )
        list_views = serie_views.tolist()
        tabla_words_count_views.append([word_count, list_views])
    
    # el resultado se agrega a la lista de resultados
    list_result.append(tabla_words_count_views)

    # reduzco lo mapeado para conseguir el puntaje promedio de las repuestas con mas favoritos
    df = list_shuffled[2]
    
    # agrupo por favoritos y calcula el promedio de los scores para cada cantidad de favoritos
    tabla_promedios = df.groupby(df.favorite_count).score_answer.mean().round(2)

    # tabla_promedios = tabla_promedios.sort_values()
    list_result.append(tabla_promedios)

    return list_result


def savetoCSV(data, filename, fields, type_data):
    #Esta funcion graba los archivos de salida.
   
    if type_data == 1:
        # los datos vienen como una lista y graba el CSV
        with open(f"/dataset big_data/{filename}", "w") as csvfile:
            csv_out = csv.writer(csvfile)
            # writing headers (field names)
            csv_out.writerow(fields)
            # writing data rows
            for row in data:
                csv_out.writerow(row)
    else:
        # los datos vienen en una serie de pandas y graba el CSV
        df = data.to_frame().sort_index(ascending=False)
        df.index.name = fields[0]
        df.to_csv(f"./dataset big_data/{filename}", sep=",", encoding="utf-8")


if __name__ == "__main__":

    root_path = '/home/nmoya/dataset BIG DATA/Stack Overflow 11-2010/112010 Meta Stack Overflow'
    # Get root from xml file.
root = parse(root_path, 'posts.xml')
    # Chunk data in batches.
data_chunks = chunkify(root, 100)

    
start = time.time()
    # set path root
root = Path.cwd()
    
    # mombre del archivo a mapear y reducir
file = Path( root / FILE_PATH)
    
    # llama a la funcion que realiza el mapeo de los datos, esta funcion retorna un listado de 3 elementos con los datos mapeados
list_mapper = mapper(file)
    
    # llama a la funcion que ordena el mapeo de los datos y retorna un listado de 3 elementos con los datos ordenados
list_shuffled = shuffle_sort(list_mapper)
    
    # llama a la funcion que reduce los datos segun las consignas a resolver y retorna un listado con 3 elementos con los datos reducidos
list_result = reduce(list_shuffled)
    
end = time.time()

print(end - start)

    # Graba los resultados en un CSV
savetoCSV(list_result[0], "top10_pregunts_map.csv", ["TAG", "COUNT"], 1)
savetoCSV(list_result[1], "top10_sin_respuest.csv", ["WORDS_COUNT", "VIEW_COUNT" , "TAG"], 1)
savetoCSV(list_result[2], "respuestas_fav.csv", ["FAVORITE_COUNT"],2 )