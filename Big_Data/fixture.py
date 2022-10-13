import pytest


@pytest.fixture
def header():
    return '<?xml version="1.0" encoding="utf-8"?>'


@pytest.fixture
def post_tag_ini():
    return '<posts>'


@pytest.fixture
def post_tag_end():
    return '</posts>'


@pytest.fixture
def row_1():
    return """<row Id="1" PostTypeId="1" AcceptedAnswerId="3" CreationDate="2009-06-28T07:14:29.363" Score="57" ViewCount="1836" Body="&lt;p&gt;Now that we have meta.stackoverflow.com, should we continue using uservoice.com?&lt;/p&gt;&#xA;&#xA;&lt;p&gt;The only requirement for participation here is that you have an existing stackoverflow / serverfault / superuser account -- but you can be a brand new user, so anonymous participation is allowed.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;It seems that questions tagged &quot;bug&quot; or &quot;feature&quot; could be voted on and commented in a fashion very similar to what uservoice already offers.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;Some people wanted to &lt;a href=&quot;http://stackoverflow.uservoice.com/pages/1722-general/suggestions/193243-move-from-uv-to-getsatisfaction&quot; rel=&quot;nofollow&quot;&gt;move to GetSatisfaction&lt;/a&gt;, but I wasn't happy with that service.&lt;/p&gt;&#xA;" OwnerUserId="1" LastEditorUserId="56285" LastEditorDisplayName="" LastEditDate="2009-08-30T09:13:00.970" LastActivityDate="2009-08-30T09:13:00.970" Title="Should meta.stackoverflow.com replace uservoice.com?" Tags="&lt;discussion&gt;&lt;status-completed&gt;&lt;uservoice&gt;" AnswerCount="13" CommentCount="5" FavoriteCount="3" />"""


@pytest.fixture
def row_2():
    return """<row Id="3" PostTypeId="2" ParentId="1" CreationDate="2009-06-28T08:14:46.627" Score="23" ViewCount="0" Body="&lt;p&gt;As much as UV annoys me (and believe me it does), this doesn't do the job of UV.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;The key part of UV is the issue tracking component. Where is the part on here to say what's been declined, started, completed, etc?&lt;/p&gt;&#xA;&#xA;&lt;p&gt;This could easily be the place for questions like about SO and how it works though (ie things that don't necessarily result in site changes but are just issues people want to discuss).&lt;/p&gt;&#xA;" OwnerUserId="18393" LastActivityDate="2009-06-28T08:14:46.627" CommentCount="8" />"""


@pytest.fixture
def row_3():
    return """<row Id="1" PostTypeId="2" Score="4" Body="This is a message" />"""


@pytest.fixture
def raw_data(header, post_tag_ini, row_1, row_2, post_tag_end):
    """Header + 2  Data Rows."""
    return [header, post_tag_ini, row_1, row_2, post_tag_end]