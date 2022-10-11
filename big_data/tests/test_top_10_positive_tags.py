import xml.etree.ElementTree as ET
import sys
import os
import pytest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from map_reduce.mrjob_top10_positive_tags import MRJobTop10PositiveTags
from fixture import raw_data, header, post_tag_ini, post_tag_end, row_1, row_2, row_3


@pytest.fixture
def tags_extract():
    """Parameters for clean tags function.

    Returns:
        list: list of strings to test.
    """
    return ["<tag1>", "<<tag2>>", ">tag3<"]


@pytest.mark.parametrize(
    "tag",
    ["", " ", "<>"],
)
def test_no_tags(tag):
    """Test case no tags.

    Args:
        tag (str): empty or bad tag.
    """
    top_10 = MRJobTop10PositiveTags()
    assert top_10._clean_tags(tags=tag) == []


@pytest.mark.parametrize(
    "tag",
    ["<tag>", "<<tag>>", ">tag<"],
)
def test_tags(tag):
    """Test clean tag function.

    Args:
        tag (str): tag to test.
    """
    top_10 = MRJobTop10PositiveTags()
    assert top_10._clean_tags(tags=tag) == ["tag"]


def test_get_tags(row_1, row_2):
    """Test function get tags.

    Args:
        row_1 (raw): raw question from posts.xml
        row_2 (raw): raw answer from posts.xml
    """
    top_10 = MRJobTop10PositiveTags()
    data = ET.fromstring(row_1)
    assert top_10._get_tags(
        data) == ["discussion", "status-completed", "uservoice"]
    data = ET.fromstring(row_2)
    assert top_10._get_tags(data) == None
    
    
def test_mapper(raw_data,row_1):
    """Test map function.

    Args:
        raw_data (raw): raw data with header and info.
        row_1 (raw): raw question from posts.xml
    """
    data = []
    top_10 = MRJobTop10PositiveTags()
    for line in raw_data:
        mapper = top_10.mapper_tags(None,line)
        try:
            while True:
                data.append(next(mapper))
        except:
            pass
    assert data == [('discussion', 1), ('status-completed', 1), ('uservoice', 1)]
    data = [next(top_10.mapper_tags(None,row_1))]
    data.append(next(top_10.mapper_tags(None,row_1)))
    assert data == [('discussion', 1), ('discussion', 1)]
    

def test_sort():
    """Test sort list of tuples by appearances.
    """
    sorted_list = []
    data = [('discussion', 1), ('status-completed', 2), ('uservoice', 1)]
    sorted_data = [('discussion', 1), ('uservoice', 1), ('status-completed', 2)]
    top_10 = MRJobTop10PositiveTags()
    sort = top_10.sort(None,data)
    try:
        while True:
            sorted_list.append(next(sort))
    except:
        pass
    assert sorted_list == sorted_data
    
