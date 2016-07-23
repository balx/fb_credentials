import fb_credentials
from nose.tools import assert_raises

def test_FogBugzErrorIfBothTokenAndPwd(unittest.TestCase):
    assert_raises(TypeError, FogBugz, '', '', token='a', password='a') 
