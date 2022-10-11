from functools import reduce
import xml.etree.ElementTree as ET
from collections import OrderedDict


def chunkify(iterable, len_of_chunk):
  
    for i in range(0, len(iterable), len_of_chunk):
        yield iterable[i : i + len_of_chunk]


def gets_score_fav(data):
    
    post_type = data.attrib.get("PostTypeId")
    # Si el tipo del post no es pregunta, lo ignoro
    if post_type == "1":
        favorite_count = data.attrib.get("FavoriteCount")
        score = data.attrib.get("Score")
        if str(favorite_count) != "None":
            return [int(favorite_count), int(score)]


def mapper(data):
    
    fav_dict = {}
    for row in data:
        fav_score = gets_score_fav(row)

        
        if fav_score is not None:
            key = fav_score[0]
            value = fav_score[1]
            if key in fav_dict.keys():
                fav_dict[key].append(value)
            else:
                fav_dict[key] = [value]
    return fav_dict


def reducer(dict1, dict2):
    

    for key, value in dict2.items():
        if key in dict1.keys():
            dict1[key] = dict1[key] + value
        else:
            dict1[key] = value
    return dict1


if __name__ == "__main__":
    tree = ET.parse("dataset BIG DATA/meta_stack_overflow/posts.xml")
    root = tree.getroot()
    data_chunks = chunkify(root, 100)

    # Map
    mapped = list(map(mapper, data_chunks))
    # print(mapped)

    
    final_fav_dict = reduce(reducer, mapped)
    # print(final_fav_dict)

   
    for key, value in final_fav_dict.items():
        final_fav_dict[key] = round(sum(value) / len(value), 2)

    
    sorted_fav_dict = OrderedDict(sorted(final_fav_dict.items(), reverse=True))

    # Print the ordered dict from most fav answer to less
    for key, value in sorted_fav_dict.items():
        print(key, value)