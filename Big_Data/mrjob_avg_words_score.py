import re
import time
from bs4 import BeautifulSoup
from mrjob.job import MRJob
from mrjob.step import MRStep
import logging
import xml.etree.ElementTree as ET


# Create logger and set name.
logger = logging.getLogger('debug_logger')
ch = logging.StreamHandler()
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)


class MRJobAvgWordsScore(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_words, reducer=self.reducer_words),
            MRStep(mapper=self.calculate_avg, reducer=self.sort)
        ]

    def _clean_body(self, body: str) -> str:
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

    def _get_words_score(self, data):
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
            body = self._clean_body(dict_atrib.get("Body"))
            # Get score post.
            score = dict_atrib.get("Score")
            # Count the number of words.
            body_count = len(body.split())
            if str(body) != "None":
                return [int(body_count), int(score)]

    def mapper_words(self, _, line):
        """Get each line from posts.xml and return count_words and score.
        Args:
            _ (None): no key.
            line (str): raw of data.
        Yields:
            Count_Words,Score: return number of words and score from post.
        """
        #logger.debug(f'MESAAGE {line}')
        try:
            parse_line = ET.fromstring(line)
            result = self._get_words_score(parse_line)
            #logger.debug(f'Key: {result[0]}, Value: {result[1]}')
            yield result[0], result[1]
        except:
            pass

    def reducer_words(self, key, value):
        """Reduce function, group score values for each number words.
        Args:
            key (int): count of words in a post.
            value (int): score.
        Yields:
            count_words, list[score]: return the count of words as key
            and list of scores as value.
        """
        yield key, list(value)

    def calculate_avg(self, key, values):
        """Calculate the average score for each words count.
        Args:
            key (int): count of words.
            values (list[int]): list of scores.
        Yields:
            dict: return a dictionary with number of words and average score.
        """
        sum = 0.
        avg = 0.
        if len(values) > 0:
            for v in values:
                sum += v
            avg = sum / len(values)
        yield None, {'num_words': key, 'score': avg}

    def sort(self, _, values):
        """Sort dictionary.
        Args:
            _ (None): no key.
            values (dict): dictionary with number of words and average score.
        Yields:
            dict: ordered dict by scores.
        """
        # Create a list of dictionaries
        data = list(values)
        # Sort data by score
        data.sort(key=lambda x: x.get("score"), reverse=True)

        for i in data:
            # yield i['num_words'],i['score']
            yield i.values()


if __name__ == '__main__':
    # Run map and reduce.
    start_time = time.time()
    MRJobAvgWordsScore.run()
    # print('Final time: ', round((time.time() - start_time), 2)) #On hadoop.
    print(f'\n Final time: {round((time.time() - start_time), 2)}. \n')
