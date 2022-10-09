from collections import Counter
from functools import reduce
import time

from utils import chunkify, parse
import re


def clean_tags(tags: str) -> list[str]:
    """Clean tags, delete html format <>

    Args:
        tags (str): str tags concatenated.

    Returns:
        list[str]: list of tags.
    """
    list_tags = re.sub('[<>]', ' ', tags).split()
    return list_tags


def get_tags(data):
    """Get tags from question.

    Args:
        data (iterable_object): one row of data.

    Returns:
        list[str]: return list of tags normalized.
    """
    # Get attributes (dictionary with the information)
    dict_atrib = data.attrib
    post_type = dict_atrib.get("PostTypeId")
    # Select only Questions.
    if post_type == '1':
        # Get tags.
        tags = dict_atrib.get('Tags')
        return clean_tags(tags)


def mapper(data):
    """Creates a list with Counter. Each counter is a list of {tag:appearances}

    Args:
        data (chunk_element): iterable element with chunk_size data.

    Returns:
        Counter: counter with tags and appearances.
    """
    # Create empty dictionary to store data.
    tags_answer = []
    # Iterate through data batch. (loop chunk_size elements)
    for row in data:
        tags = get_tags(row)
        if tags:
            # Add all tags to main list.
            tags_answer.extend(tags)
    return Counter(tags_answer)


def reducer(c1, c2):
    """Receive 2 counter objects and concat them.

    Args:
        c1 (Counter): counter 1. [{tag:appearances}]
        c2 (Counter): counter 2. [{tag:appearances}]

    Returns:
        Counter: concat c1 with c2.
    """
    for key, value in c2.items():
        if key in c1.keys():
            c1[key] += value
        else:
            c1[key] = value
    return c1


if __name__ == "__main__":
    '''Top 10 tags with higher answer accepted'''
    start_time = time.time()
    # Main path where data is.
    root_path = '/home/lautaro/Cursos/Alkemy/Stack Overflow 11-2010/112010 Meta Stack Overflow'
    # Get root from xml file.
    root = parse(root_path, 'posts.xml')
    # Chunk data in batches.
    data_chunks = chunkify(root, 100)

    # Map(function,data)
    mapped_list = list(map(mapper, data_chunks))

    # Now we have all the tags from the questions with answer accepted.
    # Call reduce to combine all Counters in one.
    reduce_counter = reduce(reducer, mapped_list)

    # Print top 10.
    for x in reduce_counter.most_common(10):
        print(f' Tag: {x[0]} , Score: {x[1]}')

    print('Final time: ', round((time.time() - start_time), 2))


# Pseudocode
    # Por cada post de posts.xml ->
    #   IF PostTypeId=1 THEN tiene AcceptedAnswerId <get tags y map>.
    #   ELSE saltear
    # Map < Nombre_Tag, 1>
    # Cuando termina el for, llamar a reduce.
    # Seleccionar los 10 tags con mayor valor.
