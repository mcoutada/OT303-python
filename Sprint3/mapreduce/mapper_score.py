from typing import final
import numpy as np

from datetime import date
from parceScore import parse_score

def mapper_score():
    """
    Esta funcion retorna los 200 scores mas altos junto con sus fechas.
    """
    scores = parse_score()
    res = []
    best_scores = {} # Guarda un diccionario ordenado con 100 valores.

    # Obteniendo las llaves del diccionario para convertirlas en int y ordenarlas.
    for i in scores.keys():
        res.append(int(i))

    res = sorted(res, reverse = True)[:100]

    for key in res:
        if str(key) in scores.keys():
            best_scores[key] = scores.get(str(key))

    return best_scores

def reducer_scores(data):
    avg_data = {} # Guardara la key(score) junto con una fecha promedio
    avg_dates = [] # Guardara las fechas promedio para despues calcular un unico valor
    
    for key in data:
        # Calculando el tiempo promedio de los 100 mejores scores.
        mean = (np.array(data.get(key), dtype='datetime64[s]')
        .view('i8')
        .mean()
        .astype('datetime64[s]'))
        
        # Guardando la llave y el promedio
        avg_data[key] = mean
        avg_dates.append(mean)

    final_avg = (np.array(avg_dates, dtype='datetime64[s]')
        .view('i8')
        .mean()
        .astype('datetime64[s]'))

    return final_avg


if __name__ == '__main__':
    data = mapper_score()
    reducer_scores(data)
