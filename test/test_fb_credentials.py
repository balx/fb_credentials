import unittest
import nose.tools
from nose_parameterized import parameterized
import mock

import shutil, tempfile
from os import path

import fb_credentials

@parameterized([ # token, username, password
    ('a', 'a', ''), # token and username
    ('a', '', 'a'), # token and password
    ('', 'a', ''), # username and no password
    ('', '', 'a'), # password and no username
])

def test_FogBugz_raiseIfWrongCredentialOptionsProvided(token, username, password):
    nose.tools.assert_raises(TypeError, fb_credentials.FogBugz, '', '', token=token,
                             username=username, password=password)

@mock.patch('fb_credentials.get_credentials')
def test_FogBugzNoUserNameNorToken(mock_get_credentials):
    mock_fogbugz = mock.Mock()
    mock_get_credentials.return_value = ['username', 'pwd']
    ret = fb_credentials.FogBugz(mock_fogbugz, 'hostname', storeCredentials=True)
    mock_get_credentials.assert_called_once()
    mock_fogbugz.assert_called_once_with('hostname', token=None)
    ret.logon.assert_called_once_with('username', 'pwd')
    # Also test storeCredentials
    nose.tools.assert_equals(ret.username, 'username')
    nose.tools.assert_equals(ret.password, 'pwd')

def test_FogBugzWithUsernameNoToken():
    mock_fogbugz = mock.Mock()
    ret = fb_credentials.FogBugz(mock_fogbugz, 'hostname', username='uUsername', password='uPassword')
    ret.logon.assert_called_once_with('uUsername', 'uPassword')

@mock.patch('fb_credentials.validate_token')
def test_FogBugzWithTokenNoUsername(mock_validate_token):
    mock_fogbugz = mock.Mock()
    mock_validate_token.return_value = True
    ret = fb_credentials.FogBugz(mock_fogbugz, 'hostname', token='uToken')
    mock_fogbugz.assert_called_once_with('hostname', token='uToken')

@mock.patch('fb_credentials.validate_token')
@mock.patch('fb_credentials.get_credentials')
def test_FogBugzWithTokenNoUsername(mock_validate_token, mock_get_credentials):
    mock_fogbugz = mock.Mock()
    mock_validate_token.return_value = False
    ret = fb_credentials.FogBugz(mock_fogbugz, 'hostname', token='uToken')
    mock_get_credentials.assert_called_once()
	
@mock.patch('fb_credentials.FogBugz')
def test_FogBugz_cm(mock_FogBugz):
    with fb_credentials.FogBugz_cm('a', 'b') as cm:
        pass
    mock_FogBugz.assert_called_once_with('a', 'b')
    nose.tools.assert_equals(cm.logoff.call_count, 0)

    with fb_credentials.FogBugz_cm('a', 'b', logoff=True) as cm:
        pass
    nose.tools.assert_equals(cm.logoff.call_count, 1)

class test_get_credentials(unittest.TestCase):
    '''Tests for get_credentials'''

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        with open(path.join(self.test_dir, '.fogbugzrc'), 'w') as f:
            f.write('pref.username = uName\ndummyLine\npref.password = pwd')

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_credentials_NoArgsNoFogbugzrcNoInteractive(self):
        fb_credentials.os.path.expanduser = mock.Mock(return_value='/FolderThatDoesNotExist')
        ret = fb_credentials.get_credentials(interactive=False)
        self.assertFalse(ret[0]) #username
        self.assertFalse(ret[1]) #password
        self.assertEquals(fb_credentials.os.path.expanduser.call_count, 1)

    def test_get_credentials_NoArgsNoFogbugzrc(self):
        fb_credentials.os.path.expanduser = mock.Mock(return_value='/FolderThatDoesNotExist')
        fb_credentials.getInput = mock.Mock(return_value='myName')
        fb_credentials.getpass.getpass = mock.Mock(return_value='myPwd')
        ret = fb_credentials.get_credentials()
        self.assertEquals(ret[0], 'myName') #username
        self.assertEquals(ret[1], 'myPwd') #password
    
    def test_read_fogbugzrc_file(self):
        ret = fb_credentials.get_credentials(path.join(self.test_dir, '.fogbugzrc'))
        self.assertEquals(ret[0], 'uName')
        self.assertEquals(ret[1], 'pwd')

class test_get_token(unittest.TestCase):
    '''Tests for get_token'''

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        with open(path.join(self.test_dir, '.fogbugzrc'), 'w') as f:
            f.write('pref.token = uToken\ndummyLine')

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_token_NoArgs(self):
        fb_credentials.os.path.expanduser = mock.Mock(return_value='/FolderThatDoesNotExist')
        ret = fb_credentials.get_token()
        self.assertFalse(ret)
        self.assertEquals(fb_credentials.os.path.expanduser.call_count, 1)

    def test_read_fogbugzrc_file(self):
        ret = fb_credentials.get_token(path.join(self.test_dir, '.fogbugzrc'))
        self.assertEquals(ret, 'uToken')