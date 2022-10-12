from operator import itemgetter
import time
import logging
import re
import xml.etree.ElementTree as ET
from mrjob.job import MRJob
from mrjob.step import MRStep


# Create logger and set name.
logger = logging.getLogger('debug_logger')
ch = logging.StreamHandler()
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)


class MRJobTop10PositiveTags(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_tags, reducer=self.reducer_tags),
            MRStep(reducer=self.sort)
        ]

    def _clean_tags(self, tags: str) -> list[str]:
        """Clean tags, delete html format <>
        Args:
            tags (str): str tags concatenated.
        Returns:
            list[str]: list of tags.
        """
        list_tags = re.sub('[<>]', ' ', tags).split()
        return list_tags

    def _get_tags(self, data):
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
            return self._clean_tags(tags)

    def mapper_tags(self, _, line):
        """Get each line from posts.xml and return tags.
        Args:
            _ (None): no key.
            line (str): raw of data.
        Yields:
            Tag,1: return tag appearences.
        """
        #logger.debug(f'MESAAGE {line}')
        try:
            parse_line = ET.fromstring(line)
            result = self._get_tags(parse_line)
            #logger.debug(f'result: {result}')
            for tag in result:
                yield tag, 1
        except:
            pass

    def reducer_tags(self, tag, value):
        """Sum all the tag appearances.
        Args:
            tag (str): tag from post.
            value (int): number appearances (1)
        Yields:
            tuple: return a tuple with tag and sum appearances.
        """
        yield None, (tag, sum(value))

    def sort(self, _, values):
        """Sort values by appearances.
        Args:
            _ (None): no key.
            values (tuple): tuple with tag and sum appearances.
        Yields:
            tuple: tag - appearances
        """
        sort = []
        for value in values:
            sort.append(value)

        sort = sorted(sort, key=itemgetter(1))

        for i in sort[-10:]:
            yield i


if __name__ == '__main__':
    # Run map and reduce.
    start_time = time.time()
    MRJobTop10PositiveTags.run()
    # print('Final time: ', round((time.time() - start_time), 2)) #On hadoop.
    print(f'\n Final time: {round((time.time() - start_time), 2)}. \n')
