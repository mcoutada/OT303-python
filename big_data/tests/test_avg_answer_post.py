import xml.etree.ElementTree as ET
import sys
import os
import pytest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from datetime import datetime
from map_reduce.mrjob_avg_answer_post import MRJobAvgAnswerPost
from fixture import raw_data, header, post_tag_ini, post_tag_end, row_1, row_2, row_3

def test_question_answer(row_1, row_2, row_3):
    """Test function question answer.

    Args:
        row_1 (raw): raw question from posts.xml
        row_2 (raw): raw answer from posts.xml
        row_3 (raw): raw custom.
    """
    avg_ans_post = MRJobAvgAnswerPost()
    data = ET.fromstring(row_1)
    assert avg_ans_post._get_question_answer(data) == (
        '1', '2009-06-28T07:14:29.363', '1')  # PostType-Creation_Date-Id
    data = ET.fromstring(row_2)
    assert avg_ans_post._get_question_answer(data) == (
        '2', '2009-06-28T08:14:46.627', '1')  # PostType-Creation_Date-ParentId
    data = ET.fromstring(row_3)
    assert avg_ans_post._get_question_answer(data) == (
        '2', None, None)  # PostType-Creation_Date-ParentId


@pytest.mark.parametrize(
    "date",
    ["2009-06-28T07:14:29.363", "2029-06-18T04:14:29.363"],
)
def test_get_timedelta(date):
    """Test function datetime to timedelta.

    Args:
        date (str): date in string format.
    """
    avg_ans_post = MRJobAvgAnswerPost()
    expected = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f') - datetime.now()
    timedelta = avg_ans_post._get_timedelta(date)
    assert timedelta.days == expected.days
    assert timedelta.seconds == expected.seconds


@pytest.mark.parametrize(
    "date",
    ["2009-06-28T07:14:29.363", "2029-06-18T04:14:29.363"],
)
def test_timedelta_to_datetime(date):
    """Test timedelta to datetime function.

    Args:
        date (str): date in string format.
    """
    avg_ans_post = MRJobAvgAnswerPost()
    # Create timedelta
    timedelta = datetime.strptime(
        date, '%Y-%m-%dT%H:%M:%S.%f') - datetime.now()
    # This is the datetime we want.
    expected_date = datetime.now() + timedelta
    # Get datetime.
    date_time = avg_ans_post._timedelta_to_datetime(timedelta)
    d1 = str(expected_date).split(" ")[0]
    d2 = date_time.split("T")[0]
    assert d1 == d2


@pytest.mark.parametrize(
    "date",
    [[{"id": "1", "creation_date": "2009-06-28T07:14:29.363"},
      {"id": "1", "creation_date": "2009-07-28T07:14:29.363"},
      {"id": "2", "creation_date": "2009-07-28T07:14:29.363"}]],
)
def test_combine_dates(date):
    """Test combine creations dates.

    Args:
        date (list): list of dict.
    """
    avg_ans_post = MRJobAvgAnswerPost()
    expected = {"1": ["2009-06-28T07:14:29.363", "2009-07-28T07:14:29.363"],
                "2": ["2009-07-28T07:14:29.363"]}
    result = avg_ans_post._combine_dates(date)
    assert result == expected


def test_mapper(raw_data):
    """Test map function.

    Args:
        raw_data (raw): raw data with header and info.
    """
    avg_ans_post = MRJobAvgAnswerPost()
    data = []
    for line in raw_data:
        mapper = avg_ans_post.mapper_qa(None, line)
        try:
            while True:
                data.append(next(mapper))
        except:
            pass
    assert data == [('1', {'id': '1', 'creation_date': '2009-06-28T07:14:29.363'}),
                    ('2', {'id': '1', 'creation_date': '2009-06-28T08:14:46.627'})]