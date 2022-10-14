from utils.get_preg_3 import get_preg_3
import pytest

@pytest.mark.parametrize(
    #parameters to test
    "imput_test,expected",
    [(get_preg_3(),
     {'1': '6.48', 
     '115866': '2.21',
     '140171': '1.95',
     '130154': '1.82',
     '22164': '1.45',
     '17174': '1.43',
     '3043': '1.33', 
     '2915': '1.31',
     '130024': '1.31',
     '22656': '1.26'}),
     (len(get_preg_3()),10 )
     ]
    )

def test_preg_3 (imput_test,expected):
  """ Compare result top 10 most favorite
    Arguments:
        imput_test: dictionary of top 10 elem. and
        length of element list
        expected: test results of top 10 elem.
  """
  assert(imput_test == expected)