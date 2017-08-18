.. image:: https://travis-ci.org/portusato/fb_credentials.svg?branch=master
   :target: https://travis-ci.org/portusato/fb_credentials
   :alt: Build status of the master branch on Linux

fb_credentials
==============

An extension to logging functionality for FogBugz module and for extensions to it like fborm. 

Function fb_credentials.FogBugz is a layer on top of the constructor fogbugz.Fogbugz or similar constructors (for example fborm.FogBugzORM) that provides a convenient parsing of credentials (token, username or password) in a configuration file (by default ~/.fogbugzrc), or prompts the user for valid credentials.

Sample usage
============

import fb_credentials
fb = fb_credentials.FogBugz('https://YourRepository.com/')
fb.search(q='53410', cols='ixBug')

Installation
============

You can download and install using:

*pip install fb_credentials*

The PyPI URL for this project is: `https://pypi.python.org/pypi/fb-credentials <https://pypi.python.org/pypi/fb-credentials>`_.

Tests
=====

In order to run the tests you need to install the test dependencies indicated in setup.py.

Tests are stored in folder test and run with *nosetests*.  `Travis <https://travis-ci.org/portusato/fb_credentials>`_ is used for Continous Integration and is connected to the github repository; every new push to the repository triggers the set of tests in Travis. At the top of this README there is a link to Travis that indicates the status of the tests.

Tests need to pass for the different versions of python supported. This is setup in the .travis.yml configuration file. You can do the same locally using tox and the tox.ini file in this repository.

E-mail me
=========

portu.github@gmail.com

Release Notes
=============

0.3.0
~~~~~

New features
------------

    * Added support for searching for token in configuration file.

API changes
-----------

    * FogBugz_cm() has option logoff (default False) to turn on log-off when exiting the context manager.

Behavior changes
----------------

    * Simplified the sequence of credential validation steps (provided token, provided username, get token, get username).
    * Default configuration file changed from ~/.hgrc to ~/.fogbugzrc.
