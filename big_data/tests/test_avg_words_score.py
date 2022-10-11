import xml.etree.ElementTree as ET
import sys
import os
import pytest
from fixture import raw_data, header, post_tag_ini, post_tag_end, row_1, row_2, row_3

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from map_reduce.mrjob_avg_words_score import MRJobAvgWordsScore

@pytest.mark.parametrize(
    "body , expected",
    [("", ""), (" ", " "), ("&lt;&gt;Now that we have meta.stackoverflow.com",
                            " now that we have meta stackoverflow com")],
)
def test_clean_body(body, expected):
    """Test function clean body from raw.

    Args:
        body (str): body message.
        expected (str): result expected.
    """
    avg_words = MRJobAvgWordsScore()
    result = avg_words._clean_body(body)
    assert result == expected


def test_get_words_score(row_1, row_2, row_3):
    """Test function count words and score.

    Args:
        row_1 (raw): raw question from posts.xml
        row_2 (raw): raw answer from posts.xml
        row_3 (raw): raw custom.
    """
    avg_words = MRJobAvgWordsScore()
    row_1 = ET.fromstring(row_1)
    data = avg_words._get_words_score(row_1)
    assert data == [81, 57]
    row_2 = ET.fromstring(row_2)
    data = avg_words._get_words_score(row_2)
    assert data == [78, 23]
    # Custom. "This is a message" Score=4
    row_3 = ET.fromstring(row_3)
    data = avg_words._get_words_score(row_3)
    assert data == [4, 4]


def test_mapper(raw_data, row_3):
    """Test map funciton.

    Args:
        raw_data (raw): raw data with header and info.
        row_3 (raw): custom raw.
    """
    data = []
    avg_words = MRJobAvgWordsScore()
    for line in raw_data:
        mapper = avg_words.mapper_words(None, line)
        try:
            while True:
                data.append(next(mapper))
        except:
            pass
    data.append(next(avg_words.mapper_words(None, row_3)))
    assert data == [(81, 57), (78, 23), (4, 4)]


def test_avg():
    """Test average function.
    """
    avg_words = MRJobAvgWordsScore()
    values = [1, 3, 2]  # avg 2.
    result = next(avg_words.calculate_avg(1, values))
    assert result == (None, {'num_words': 1, 'score': 2.})
    values = []  # avg 0.
    result = next(avg_words.calculate_avg(1, values))
    assert result == (None, {'num_words': 1, 'score': 0.})


def test_sort():
    """Test sort (list of dict) by score.
    """
    sorted_list = [{'num_words': 3, 'score': 5.0}, {
        'num_words': 1, 'score': 3.5}, {'num_words': 2, 'score': 2.1}]
    data = [{'num_words': 1, 'score': 3.5}, {
        'num_words': 2, 'score': 2.1}, {'num_words': 3, 'score': 5.0}]
    # Sort data by score
    data.sort(key=lambda x: x.get("score"), reverse=True)
    assert sorted_list == data
