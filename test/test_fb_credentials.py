import fb_credentials
from nose.tools import assert_raises

def test_FogBugzErrorIfBothTokenAndPwd():
    assert_raises(TypeError, fb_credentials.FogBugz, '', '', token='a', password='a') 
