from datetime import datetime
from functools import reduce
import time
from utils import chunkify, parse


def get_question_answer(data):
    """Take a row of data and return the type, creation date and id/parentId. 

    Args:
        data (iterable_object): one data element.

    Returns:
        str/None: return the type (Question/Answer), creation_date(str), id (postId/parentId)
    """
    # Get attributes (dictionary with the information)
    dict_atrib = data.attrib
    post_type = dict_atrib.get("PostTypeId")
    # Is a Questions.
    id = None
    creation_date = None
    if post_type == '1':
        # Get creation date..
        creation_date = dict_atrib.get('CreationDate')
        id = dict_atrib.get('Id')
    elif post_type == '2':
        # Answer.
        creation_date = dict_atrib.get('CreationDate')
        id = dict_atrib.get('ParentId')
    return post_type, creation_date, id


def mapper(data):
    """Creates a list with 2 maps: one for questions and one for answers.
    Question_dict: dict{key:postId,value:creationDate}
    Answer_dict: dict{key:parentId,value:list[creation_date]}

    Args:
        data (chunk_element): iterable element with chunk_size data.

    Returns:
        list[dict,dict]: return a list with 2 dicts.
    """
    question_dict = {}
    answer_dict = {}
    for row in data:
        type, date, id = get_question_answer(row)
        # Valid data.
        if type and id:
            # Is question
            if type == '1':
                # Key: postId, Value: Creation date. postId is unique.
                question_dict[id] = date
            else:
                # Is answer
                if id in answer_dict.keys():
                    answer_dict[id].append(date)
                else:
                    answer_dict[id] = [date]
    return [question_dict, answer_dict]


def question_answer_list(mapped_data):
    """Map all the question and answer together.

    Args:
        mapped_data (list[dict,dict]): list with all the questions and answers.

    Returns:
        dict: return a dictionary for questions and a dictionary for answers.
    """
    questions = []
    answers = []
    for m in mapped_data:
        questions.append(m[0])
        answers.append(m[1])

    return questions, answers


def reducer(d1, d2):
    """Receive 2 dictionaries objects and concat them

    Args:
        d1 (dictionary): object dictionary 1 
        d2 (dictionary): object dictionary 2 

    Returns:
        dict[key:list[values]]: concat d1 with d2.
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


def convert_to_datetime(date: str) -> datetime:
    """Convert string to datetime.

    Args:
        date (str): datetime in string format.

    Returns:
        datetime: date formated.
    """
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')


def calculate_avg_time(dict_questions, dict_answ):
    """Get the average time between question and answers.

    Args:
        dict_questions (dict): dictionary with all the questions.
        dict_answ (dict): dictionary with all the answers.

    Returns:
        dict: dictionary with average time. Key: PostId, Value: AvgTime
    """
    dict_avg_time = {}  # Key: postId, Value: avg_time
    for id, dates in dict_answ.items():
        creation_time_question = convert_to_datetime(dict_questions[id])
        # Iterate through answer dates.
        first = True
        for date in dates:
            current_dif = convert_to_datetime(date) - creation_time_question
            if first:
                sum_days = current_dif
                first = False
            else:
                sum_days += current_dif
        dict_avg_time[id] = sum_days/len(dates)
    return dict_avg_time


if __name__ == "__main__":
    '''Average time answer in post'''
    start_time = time.time()
    # Main path where data is.
    root_path = '/home/lautaro/Cursos/Alkemy/Stack Overflow 11-2010/112010 Meta Stack Overflow'
    # Get root from xml file.
    root = parse(root_path, 'posts.xml')

    # Chunk data in batches.
    data_chunks = chunkify(root, 100)

    # Check avg negative.
    #l = []
    #type = []
    # for r in root:
    #
    #    if r.attrib.get('ParentId') == '18545':
    #        elem = r.attrib
    #        l.append(elem.get('CreationDate'))
    #        type.append(elem.get('PostTypeId'))
    # print(l)
    # print(type)

    # Map(function,data)
    mapped = list(map(mapper, data_chunks))
    # mapped is a list. each map in the list have 2 elements map[x][0] = question_dict, map[x][1] = answer_dict
    questions, answers = question_answer_list(mapped)
    # reduce questions.
    reduced_questions = reduce(reducer, questions)
    # reduce answers.
    reduced_answers = reduce(reducer, answers)

    # Calculate average time for each answer.
    avg_time = calculate_avg_time(reduced_questions, reduced_answers)

    # Just for test purpose spy on data (not required).
    # Sort dict by value.
    sorted_dict = sorted(avg_time.items(),
                         key=lambda x: x[1], reverse=True)

    i = 0
    for x in sorted_dict:
        if i == 10:
            break
        print(f'PostId: {x[0]} , AvgTime: {x[1]}')
        i += 1
   
    print('Final time: ' , round((time.time() - start_time), 2))

    # Warning. Some of the data is corrupted answer_date < question_date. (That is not possible)

    # PostId: 18545 *-------* Creation_Date: 2008-11-19T01:18:37.527  *-----* PostTypeId: 1 (Question)
    # Answers: All type 2 (checked). All parent id 18545 (checked)
    # Corrupted DATA. 3 Answers are before creation date.
    # ['2008-11-19T01:22:56.127', '2009-04-15T18:58:02.163', '2008-10-25T20:00:47.047',
    # '2008-10-25T20:01:10.637', '2008-10-25T20:01:33.257']

    # PostId: 25872 *-------* Creation_Date: 2009-10-14T18:41:02.230  *-----* PostTypeId: 1 (Question)
    # Answers: All type 2 (checked). All parent id 25872 (checked)
    # Corrupted DATA. 2 Answers are before creation date.
    # ['2009-09-18T17:09:44.303', '2009-09-18T20:22:29.543', '2009-10-14T18:42:29.287',
    # '2009-10-14T18:45:50.697', '2009-10-14T18:46:00.913', '2009-10-14T18:47:11.550',
    # '2009-10-14T19:32:29.207', '2009-10-15T00:57:10.663']


# Pseudocode
    # Por cada post de posts.xml ->
    # Si PostTypeId = 1 (Question) CreationDate
    #   Guardar en un map <postId, fecha de creación>
    # Si PostTypeId = 2 (Answer) CreationDate
    #   Guardar en un map <ParentID, list<CreationDate>
    #
    # Al finalizar el for, recorrer la lista de Creation date, calcular un promedio.
    # Map < promedio, 1>
    # Reduce
