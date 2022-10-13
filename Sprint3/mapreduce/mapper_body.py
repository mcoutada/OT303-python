import string

from parceBody import parse_body

def mapper(data: str):
    """
    Crea un diccionario en el que la llave es la palabra y el valor es el numero
    de veces que aparece la palabra.
    """
    data_dict = {}

    for line in data:

        line = line.strip()

        line = line.lower()

        # Quita todos los signos especiales
        line = line.translate(line.maketrans("", "", string.punctuation))

        words = line.split(" ")

        for word in words:
            if not (word in data_dict.keys()):
                data_dict[word] = 1
            else:
                data_dict[word] += 1
    
    return data_dict

def top_10_words(data_dict):
    """
    Recorre todo el diccionario y retorna todas las diez palabras con mayor frecuencia
    de los posts.
    """
    res = sorted(data_dict, key=data_dict.get, reverse=True)[:10]
    max_words = {}

    for key in data_dict:
        if key in res:
            max_words[key] = data_dict.get(key)

    return max_words

if __name__ == '__main__':
    body = open('posts.txt', 'r')
    dict = mapper(body)
    print(top_10_words(dict))
