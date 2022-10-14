import pytest
import xml.etree.ElementTree as ET
from top10_sin_respuest import unanswered_responses, reducer, chunkify, mapper


@pytest.fixture
def tree_node():
    xml = """<?xml version="1.0" encoding="utf-8"?>
<row Id="6" PostTypeId="1" CreationDate="2009-06-28T08:40:18.673" Score="5" ViewCount="249" Body="&lt;p&gt;When using Google for your OpenId provider, it generates a different openid url for each website you use with it.  This means that for stackoverflow.com, meta.stackoverflow.com, superuser.com and serverfault.com you will have 4 different openids.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;Currently you can have an main and an alternate openid - should the system support as moany openids as there are sites in the stackoverflow family?&lt;/p&gt;&#xA;" OwnerUserId="41673" LastEditorUserId="23354" LastEditorDisplayName="" LastEditDate="2009-07-10T13:49:41.953" LastActivityDate="2010-04-14T06:58:25.480" Title="Should StackOverflow support more than 2 openids per account?" Tags="&lt;feature-request&gt;&lt;status-declined&gt;&lt;openid&gt;&lt;login&gt;&lt;google&gt;" AnswerCount="4" CommentCount="3" FavoriteCount="0" />
  """
    return ET.fromstring(xml)


@pytest.fixture
def tree_node_postid2():
    xml = """<?xml version="1.0" encoding="utf-8"?>

  """
    return ET.fromstring(xml)


@pytest.fixture
def tree_node_chunks():
    xml = """<?xml version="1.0" encoding="utf-8"?>
    <posts>

"""
    rows = ET.fromstring(xml)
    data_chunks = chunkify(rows, 100)
    return data_chunks


def test_reducer():
    """test reducer """
    d1 = {"a": 1, "b": 1, "c": 1}
    d2 = {"b": 2, "c": 3, "d": 1}
    r = reducer(d1, d2)

    assert r == {"a": 1, "b": 3, "c": 4, "d": 1}


def test_reducer_empty_dict():
    """test reducer con dicc vacio"""
    d1 = {"a": 1, "b": 1, "c": 1}
    d2 = {}
    r = reducer(d1, d2)

    assert r == {"a": 1, "b": 1, "c": 1}


def test_reducer_no_common():
   
    d1 = {"a": 1, "b": 1, "c": 1}
    d2 = {"h": 1}
    r = reducer(d1, d2)

    assert r == {"a": 1, "b": 1, "c": 1, "h": 1}


def test_unanswered_responses(tree_node_postid2):
    """test unanswered responses """

    r = unanswered_responses(tree_node_postid2)

    assert r is None


def test_unanswered_responses_1(tree_node):
    """test unanswered responses function"""
    r = unanswered_responses(tree_node)

    assert r == ["feature-request", "status-declined", "openid", "login", "google"]


def test_mapper(tree_node_chunks):
    """Test mapper """
    r = list(map(mapper, tree_node_chunks))
    assert r == [
        {"feature-request": 2, "google": 1, "login": 1, "openid": 2, "search": 1, "status-declined": 1},
    ]