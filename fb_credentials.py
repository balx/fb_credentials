"""
==============================================
Extend login Interface for fogbugz
Parts of this code comes from the fborm project
==============================================
"""

from __future__ import print_function
import getpass
import contextlib
import os
import re
import urllib2

__version__ = (0,2,2)
__version_string__ = '.'.join(str(x) for x in __version__)

__author__ = 'Nicolas Morales'
__email__ = 'portu.github@gmail.com'

def getInput(prompt):
    '''Wrapper around builtin function raw_input in order to mock it in tests'''
    return raw_input(prompt)

def get_credentials(fogbugzrc=None, fogbugzPrefix='', interactive=True):
    """When credentials are not provided in the constructor, get them from fogbugzrc or prompt user
       fogbugzrc: Path to fogbugzrc file
       fogbugzPrefix: prefix for user and password. Useful if the fogbugzrc is used for multiple servers
                 with different credentials
       interactive: If credentials not found in fogbugzrc and this is set, prompt the user
    """
    #Search whether there is an fogbugzrc file. Default: ~/fogbugzrc
    username = None
    password = None
    if not fogbugzrc:
        fogbugzrc = os.path.join(os.path.expanduser("~"), '.fogbugzrc')
    if os.path.isfile(fogbugzrc):
        for line in open(fogbugzrc):
            line = line.split('#')[0]
            if fogbugzPrefix + 'username' in line:
                res = re.search(r'username\s*=\s*(\S+)', line)
                username = res.group(1)
            elif fogbugzPrefix + 'password' in line:
                res = re.search(r'password\s*=\s*(\S+)', line)
                password = res.group(1)
    if interactive:
        if not username:
            username = getInput('user: ')
        if not password:
            password = getpass.getpass('password: ')# Same as raw_input but hide what user types
    return username, password

def get_token(fogbugzrc=None, fogbugzPrefix=''):
    """When token is not provided in the constructor, get them from fogbugzrc
       fogbugzrc: Path to fogbugzrc file
       fogbugzPrefix: prefix for token.
    """
    # Search whether there is an fogbugzrc file. Default: ~/.fogbugzrc
    token = None
    if not fogbugzrc:
        fogbugzrc = os.path.join(os.path.expanduser("~"), '.fogbugzrc')
    if os.path.isfile(fogbugzrc):
        for line in open(fogbugzrc):
            line = line.split('#')[0]
            if fogbugzPrefix + 'token' in line:
                res = re.search(r'token\s*=\s*(\S+)', line)
                token = res.group(1)
    return token

def validate_token(hostname, token):
    """
    Validate the user token.

    Returns True for a successful validation.
    """
    url = hostname + "/api.asp?cmd=logon&token=" + token
    try:
        response = urllib2.urlopen(url)
        return token in response.read()
    except Exception as e:
        print(e)
    return False

def FogBugz(fbConstructor, hostname, token=None, username=None, password=None, fogbugzrc=None,
            fogbugzPrefix='', interactive=True, storeCredentials=False):
    """Calls the constructor specified by fbConstructor (hence, despite this being a function use
        CapWords naming convention)

       fbConstructor: Fogbugz constructor class. Typically fogbugz.FogBugz, fborm.FogBugzORM or
                       kiln.Kiln
       hostname: passed directly to the fbInterface
       token, username, password: input credentials
       fogbugzrc, fogbugzPrefix, interactive: Passed to method get_credentials
       storeCredentials: If active, create attributes token, username and password. This opens the
                          door to using it for login to other system, which is convenient, but the
                          programmer can also do what he wants with the password (which is bad).
       TODO: Support passing a list of args to fbConstructor
    """
    if token and (username or password):
        raise TypeError("If you supply 'token' you cannot supply 'username' or 'password'")
    if (username and not password) or (not username and password):
        raise TypeError("You must supply both 'username' and 'password'")
    if not username:
        if not token:
            token = get_token(fogbugzrc, fogbugzPrefix)
        if token and validate_token(hostname, token):
            return fbConstructor(hostname, token=token)
        else:
            username, password = get_credentials(fogbugzrc, fogbugzPrefix, interactive)
            if not username and password: # If still no credentials available, raise
                raise TypeError("You must provide either 'username' and 'password' or 'token'")

    fb = fbConstructor(hostname, token=token)
    if username:
        fb.logon(username, password)

    if storeCredentials:
        fb.token = token
        fb.username = username
        fb.password = password

    return fb

@contextlib.contextmanager
def FogBugz_cm(fbConstructor, hostname, logoff=False, **kwargs):
    '''Context manager with logOff functionality'''
    fb = FogBugz(fbConstructor, hostname, **kwargs)
    yield fb
    
    if logoff:
        fb.logoff()
    else:
        print("Save this token for later: token=%s" % fb._token)
