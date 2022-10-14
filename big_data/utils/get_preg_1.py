from preg_1 import get_data, mapper, chunkify, reducer_counter
from functools import reduce

def get_preg_1():
    # get results of top 10 elements
    xml_data = get_data()
    chunker_list = chunkify(xml_data, 32)
    mapped = list(map(mapper, chunker_list))
    mapped = reduce(reducer_counter, mapped)
    top_10_acept =mapped.most_common(10)
    return list(top_10_acept)