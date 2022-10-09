from functools import reduce
import time
from bs4 import BeautifulSoup
import re
from utils import parse, chunkify


def clean_body(body: str) -> str:
    """Clean body ussing Beautiful Soup.

    Args:
        body (str): html body.

    Returns:
        str: body without html tags.
    """
    # Parse data.
    parsed_body = BeautifulSoup(body, features="html.parser")
    # Get only text.
    body_text = parsed_body.get_text()
    # Normalize data.
    # First all the words to lowercase.
    body_text = body_text.lower()
    # Then delete special chars and newlines \n.
    body_text = re.sub("[^a-z]+", " ", body_text)
    return body_text


def get_words_score(data):
    """Create list with 2 elements or None. list[words_count:score]

    Args:
        data (iterable_object): one data element.

    Returns:
        list[int,int] or None: return the number of words in the body with the post score.
    """
    # Get attributes (dictionary with the information)
    dict_atrib = data.attrib
    post_type = dict_atrib.get("PostTypeId")
    # Post type must be 1 (question) or 2 (answer)
    if post_type == "1" or post_type == "2":
        # Normalize text body.
        body = clean_body(dict_atrib.get("Body"))
        # Get score post.
        score = dict_atrib.get("Score")
        # Count the number of words.
        body_count = len(body.split())
        if str(body) != "None":
            return [int(body_count), int(score)]


def mapper(data):
    """Creates a dict{key:number_words_post, value:list[score_post]}

    Args:
        data (chunk_element): iterable element with chunk_size data.

    Returns:
        dict: dictionary with number_words and scores on posts.
    """
    # Create empty dictionary to store data.
    number_words_dict = {}
    # Iterate through data batch. (loop chunk_size elements)
    for row in data:
        # Get list with 2 elements [words_count:score_post] or None.
        words_score = get_words_score(row)

        # key: count_words, value: score_post.
        if words_score is not None:
            key = words_score[0]
            value = words_score[1]
            # If exist key, add new value to list.
            if key in number_words_dict.keys():
                number_words_dict[key].append(value)
            # Else, create the key and add the value.
            else:
                number_words_dict[key] = [value]
    return number_words_dict


def reducer(d1, d2):
    """Receive 2 dictionaries objects and concat them

    Args:
        d1 (dictionary): object dictionary 1 [{int:list[int]}]
        d2 (dictionary): object dictionary 2 [{int:list[int]}]

    Returns:
        dict: concat d1 with d2. [{int:list[int]}]
    """
    # Loop through second dictionary.
    for key, value in d2.items():
        # If key exist in main dict, add values.
        if key in d1.keys():
            d1[key] = d1[key] + value
        # Else, add the key and value.
        else:
            d1[key] = value
    return d1


if __name__ == "__main__":
    '''Relation between number of words and score in a post'''
    start_time = time.time()
    # Main path where data is.
    root_path = '/home/lautaro/Cursos/Alkemy/Stack Overflow 11-2010/112010 Meta Stack Overflow'
    # Get root from xml file.
    root = parse(root_path, 'posts.xml')
    # Chunk data in batches.
    data_chunks = chunkify(root, 100)

    # Map(function,data)
    mapped_dictionary = list(map(mapper, data_chunks))

    # Now we have a list of dictionaries{word_count:list[scores]}
    # Call reduce to combine all dicts in one.
    reduce_dictionary = reduce(reducer, mapped_dictionary)

    # Average for each word count.
    for key, value in reduce_dictionary.items():
        reduce_dictionary[key] = round(sum(value) / len(value), 2)

    # Just for test purpose spy on data (not required).
    # Sort dict by value.
    sorted_dict = sorted(reduce_dictionary.items(),
                         key=lambda x: x[1], reverse=True)

    for i in sorted_dict:
        print(f'Key: {i[0]} , Value: {i[1]}')

    print('Final time: ' , round((time.time() - start_time), 2))

# Pseudocode
    # Por cada post de posts.xml ->
    # Si PostTypeId = 1o2 (Question/Answer)
    #   Contar palabras del Body. (usra beutyfulsoup html parser)
    #   Map. Devolver [cant_words, score]
    # Al finalizar el loop. Reduce de cada dict generado.
    #
