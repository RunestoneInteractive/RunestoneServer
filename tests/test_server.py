# *****************************************
# |docname| - Tests using the web2py server
# *****************************************
# These tests start the web2py server then submit requests to it.
#
# .. contents::
#
# Imports
# =======
# These are listed in the order prescribed by `PEP 8
# <http://www.python.org/dev/peps/pep-0008/#imports>`_.
#
# Standard library
# ----------------
import sys
import time
from subprocess import Popen
from pprint import pprint

# Third-party imports
# -------------------
import pytest
from gluon.contrib.webclient import WebClient
from py_w3c.validators.html.validator import HTMLValidator

# Local imports
# -------------
from run_tests import COVER_DIRS
from ci_utils import flush_print


# Fixtures
# ========
# This fixture starts and shuts down the web2py server.
#
# Execute this `fixture <https://docs.pytest.org/en/latest/fixture.html>`_ once per `module <https://docs.pytest.org/en/latest/fixture.html#scope-sharing-a-fixture-instance-across-tests-in-a-class-module-or-session>`_.
@pytest.fixture(scope='module')
def web2py_server():
    # Start the web2py server.
    web2py_server = Popen(
        [sys.executable, '-m', 'coverage', 'run', '--append',
         '--source=' + COVER_DIRS, 'web2py.py', '-a', 'junk_password',
         '--nogui'])
    # Wait for the server to come up. The delay varies; this is a guess.
    time.sleep(1.5)
    flush_print('')

    # After this comes the `teardown code <https://docs.pytest.org/en/latest/fixture.html#fixture-finalization-executing-teardown-code>`_.
    yield web2py_server

    # Terminate the server to give web2py time to shut down gracefully.
    web2py_server.terminate()


# This class implements the ``test_client`` fixture.
class _TestClient(WebClient):
    def __init__(self):
        super(_TestClient, self).__init__('http://127.0.0.1:8000/runestone/',
                                          postbacks=True)

    # Use the W3C validator to check the HTML at the given URL.
    def validate(self,
        # The relative URL to validate.
        url,
        # An optional string that, if provided, must be in the text returned by the server
        expected_string='',
        # The number of validation errors expected
        expected_errors=0):

        self.get(url)
        assert self.status == 200
        if expected_string:
            assert expected_string in self.text

        vld = HTMLValidator()
        vld.validate_fragment(self.text)
        if len(vld.errors) != expected_errors:
            print('Errors for {}: {}'.format(url, len(vld.errors)))
            pprint(vld.errors)
            # Save the HTML to make fixing the errors easier.
            with open(url.replace('/', '-') + '.html', 'w') as f:
                f.write(self.text.replace('\r\n', '\n'))
            assert False
        if vld.warnings:
            print('Warnings for {}: {}'.format(url, len(vld.warnings)))
            pprint(vld.warnings)


# A fixture to create a client for accessing the server.
@pytest.fixture(scope='class')
def test_client(web2py_server):
    return _TestClient()


# Tests
# =====
# This class implements the ``test_user`` fixture.
class _TestUser(object):
    def __init__(self, test_client):
        self.username = 'test_user_2'
        self.password = 'password_2'
        self.test_client = test_client
        # Create a user. First, get the form to read the CSRF key.
        self.test_client.get('default/user/register')
        ret = dict(
            username=self.username,
            first_name='test',
            last_name='user_2',
            email='test_user_2@foo.com',
            password=self.password,
            password_two=self.password,
            # If this user is only enrolled in one course, ``models.default.index`` will redirect to it after registration, which (unless that book is built) will cause a bizarre web2py error, ``invalid file``. Using the ``boguscourse`` avoids this redirect.
            course_id='boguscourse',
            accept_tcp='on',
            donate='0',
            _next='/runestone/default/index',
            _formname='register',
        )
        self.test_client.post('default/user/register', data=ret)

    def login(self):
        self.test_client.post('default/user/login', data=dict(
            username=self.username,
            password=self.password,
            _formname='login',
        ))

    def logout(self):
        self.test_client.get('default/user/logout')
        assert self.test_client.status == 200


# This fixture creates a user for use with testing. Do it once per class to save time.
@pytest.fixture(scope='class')
def test_user(test_client):
    yield _TestUser(test_client)
    # TODO: Delete the user from the database.


class TestServer(object):
    # Validate the HTML produced by various web2py pages.
    def test_1(self, test_client, test_user):
        for url, (requires_login, expected_string, expected_errors) in {
            # The `authentication <http://web2py.com/books/default/chapter/29/09/access-control#Authentication>`_ section gives the URLs exposed by web2py. Check these.
            'user/login': (False, 'Login', 1),
            'user/register': (False, 'Registration', 1),
            'user/logout': (True, 'Logged out', 1),
            # One profile error is a result of removing the input field for the e-mail, but web2py still tries to label it, which is an error.
            'user/profile': (True, 'Profile', 2),
            'user/change_password': (True, 'Change password', 1),
            # Runestone doesn't support this.
            #'user/verify_email': (False, 'Verify email', 1),
            'user/retrieve_username': (False, 'Retrieve username', 1),
            'user/request_reset_password': (False, 'Request reset password', 1),
            # This doesn't display a webpage, but instead redirects to courses.
            #'user/reset_password=(False, 'Reset password', 1),
            'user/impersonate': (True, 'Impersonate', 1),
            # FIXME: This produces an exception.
            #'user/groups': (True, 'Groups', 1),
            'user/not_authorized': (False, 'Not authorized', 1),
            # Returns a 404.
            #'user/navbar'=(False, 'xxx', 1),

            # Other pages in ``default``.
            'about': (False, 'About Us', 1),
            'error': (False, 'Error: the document does not exist', 1),
            'ack': (False, 'Acknowledgements', 1),
            # web2py generates invalid labels for the radio buttons in this form.
            'bio': (True, 'Tell Us About Yourself', 3),
            'courses': (True, 'Course Selection', 1),
            'remove': (True, 'Remove a Course', 1),
            'reportabug': (False, 'Report a Bug', 1),
            'privacy': (False, 'Runestone Academy Privacy Policy', 1),
            'donate': (False, 'Support Runestone Interactive', 1),
        }.iteritems():
            if requires_login:
                test_user.login()
            else:
                test_user.logout()
            test_client.validate('default/' + url, expected_string,
                                 expected_errors)
