from datetime import datetime
import time
import logging
import xml.etree.ElementTree as ET
from mrjob.job import MRJob
from mrjob.step import MRStep


# Create logger and set name.
logger = logging.getLogger('debug_logger')
ch = logging.StreamHandler()
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)

current_date = datetime.now()


class MRJobAvgAnswerPost(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_qa, reducer=self.reducer_qa),
            MRStep(reducer=self.reduce),
            MRStep(mapper=self.avg, reducer=self.sort)
        ]

    def _get_question_answer(self, data):
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

    def _convert_to_datetime(self, date: str) -> datetime:
        """Convert string to datetime.

        Args:
            date (str): datetime in string format.

        Returns:
            datetime: date formated.
        """
        return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')

    def _timedelta_to_datetime(self, timedelta) -> str:
        """Create string date from timedelta object. Current date + timedelta.

        Args:
            timedelta (timedelta): date in timedelta obj.

        Returns:
            str: string date format.
        """
        date = current_date + timedelta
        #logger.debug(f'Now: {current_date}, Timedelta: {timedelta}, Result: {date} ,type {type(date)}')
        return date.strftime('%Y-%m-%dT%H:%M:%S.%f')

    def _get_timedelta(self, date: str):
        """Get timedelta from datetime.

        Args:
            date (str): string date format.

        Returns:
            timedelta: return the timedelta.
        """
        return self._convert_to_datetime(date) - current_date

    def _combine_dates(self, list):
        """Concatenate creation dates by id.

        Args:
            list (dict): list with post id and creation dates.

        Returns:
            dict: dictionary with post id and list of creation dates.
        """
        dict = {}
        for i in list:
            if i['id'] in dict.keys():
                dict[i['id']].append(i['creation_date'])
            else:
                dict[i['id']] = [i['creation_date']]
        return dict

    def mapper_qa(self, _, line):
        """Map posts by type.

        Args:
            _ (None):no key.
            line (str): raw of data.

        Yields:
            int, dict: return post_type as key, dict{id,creation_date}
        """
        try:
            parse_line = ET.fromstring(line)
            post_type, creation_date, id = self._get_question_answer(
                parse_line)
            if post_type and id:
                if post_type == '1':
                    # Key: postId, Value: Creation date. postId is unique.
                    yield post_type, {'id': id, 'creation_date': creation_date}
                else:
                    # Is answer
                    yield post_type, {'id': id, 'creation_date': creation_date}
        except:
            pass

    def reducer_qa(self, post_type, dict):
        """Concat post_type in one dictionary.

        Args:
            post_type (int): type of post (Q,A)
            dict (dict): dict{id,creation_date}

        Yields:
            dict: return a dictionary with post_type and a list of values.
        """
        # Reduce to a dictionary where KEY: Question,Answer, VALUES: [{id,creation_date}]
        yield None, {'key': post_type, 'values': list(dict)}

    def reduce(self, _, dict):
        """Combine both dictionaries (Q,A) in one.

        Args:
            _ (None): no key.
            dict (dict): dictionary with post_type and a list of values.

        Yields:
            list[dict]: list with 2 dictionaries.
        """
        # Combine both dictionaries
        yield None, list(dict)

    def avg(self, _, values):
        """Get the average time of answers by post. 

        Args:
            _ (None): no key.
            values (list): list of dictionaries.

        Yields:
            dict: return a dictionary with key:post_id and time:average_time.
        """
        questions = values[0]['values']
        answers = values[1]['values']
        question_dict = self._combine_dates(questions)
        answer_dict = self._combine_dates(answers)
        #logger.debug(f'Questions {question_dict}')
        #logger.debug(f'Answers {answer_dict}')
        dict_avg_time = {}  # Key: postId, Value: avg_time
        for id, dates in answer_dict.items():
            if id in question_dict.keys():
                creation_time_question = self._convert_to_datetime(
                    question_dict[id][0])
                # Iterate through answer dates.
                first = True
                for date in dates:
                    current_dif = self._convert_to_datetime(
                        date) - creation_time_question
                    if first:
                        sum_days = current_dif
                        first = False
                    else:
                        sum_days += current_dif
                dict_avg_time[id] = sum_days/len(dates)
                #logger.debug(f'id {id}, {dict_avg_time}')

                yield None, {'id': id, 'time': self._timedelta_to_datetime(dict_avg_time[id])}

    def sort(self, _, values):
        """Sort the values.

        Args:
            _ (None): no key.
            values (dict): dictionary with key:post_id and time:average_time.

        Yields:
            int,str: return the post_id as key, and post avg time answer as time.
        """
        # Create a list of dictionaries
        data = list(values)
        # Sort data by score

        for d in data:
            new_date = self._get_timedelta(d['time'])
            d['time'] = new_date

        data.sort(key=lambda x: x['time'], reverse=False)
        #logger.debug(f'Data sorted {data}')
        for i in data:
            # yield i['num_words'],i['score']
            yield i['id'], str(i['time'])


if __name__ == '__main__':
    # Run map and reduce.
    start_time = time.time()
    MRJobAvgAnswerPost.run()
    # print('Final time: ', round((time.time() - start_time), 2)) #On hadoop.
    print(f'\n Final time: {round((time.time() - start_time), 2)}. \n')
