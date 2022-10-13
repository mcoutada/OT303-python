from parceDates import parse_dates

def mapper(data: str):
    """
    Crea un diccionario en el que la llave es la fecha y el valor es el numero
    de veces que aparece la fecha.
    """
    data_dict = {}
    for i in data:
        if not (i in data_dict.keys()):
            data_dict[i] = 1
        else:
            data_dict[i] += 1
    
    return data_dict

def top_10_lowest_dates(data_dict):
    """
    Recorre todo el diccionario y retorna un nuevo diccionario que contiene
    las fechas que menor cantidad de publicaciones tienen.
    """
    res = sorted(data_dict, key=data_dict.get, reverse=False)[:10]
    lowest_dates = {}

    for key in data_dict:
        if key in res:
            lowest_dates[key] = data_dict.get(key)

    return lowest_dates

if __name__ == '__main__':
    dates = parse_dates()
    dict = mapper(dates)
    print(dict)
    print(top_10_lowest_dates(dict))
