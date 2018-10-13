# *****************************************
# |docname| - Tests using the web2py server
# *****************************************
import sys
import time
from subprocess import Popen
import unittest
from pprint import pprint

from gluon.contrib.webclient import WebClient
from py_w3c.validators.html.validator import HTMLValidator

from run_tests import COVER_DIRS
from ci_utils import flush_print


def setUpModule():
    # Start the web2py server.
    global web2py_server
    web2py_server = Popen(
        [sys.executable, '-m', 'coverage', 'run', '--append',
         '--source=' + COVER_DIRS, 'web2py.py', '-a', 'junk_password',
         '--nogui'])
    # Wait for the server to come up. The delay varies; this is a guess.
    time.sleep(1.5)
    flush_print('')


def tearDownModule():
    # Terminate the server to give web2py time to shut down gracefully.
    web2py_server.terminate()


class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = WebClient('http://127.0.0.1:8000/runestone/',
                               postbacks=True)
        # Create a user. First, get the form to read the CSRF key.
        cls.client.get('default/user/register')
        cls.client.post('default/user/register', data=dict(
            username='test_user_2',
            first_name='test',
            last_name='user_2',
            email='test_user_2@foo.com',
            password='password_2',
            password_two='password_2',
            # If this user is only enrolled in one course, ``models.default.index`` will redirect to it after registration, which (unless that book is built) will cause a bizarre web2py error, ``invalid file``. Using the ``boguscourse`` avoids this redirect.
            course_id='boguscourse',
            accept_tcp='on',
            donate='0',
            _next='/runestone/default/index',
            _formname='register',
        ))

    def logout(self):
        self.client.get('default/user/logout')
        self.assertEquals(self.client.status, 200)

    # Validate the HTML produced by various web2py pages.
    def test_1(self):
        for url, expected_values in {
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
            # This produces an exception.
            #'user/groups'=(True, 'Groups', 1),
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
            requires_login, expected_string, expected_errors = expected_values
            if requires_login:
                self.client.post('default/user/login', data=dict(
                    username='test_user_2',
                    password='password_2',
                    _formname='login',
                ))
            else:
                self.logout()
            self.validate('default/' + url, expected_string, expected_errors)

    # Use the W3C validator to check the HTML at the given URL.
    def validate(self,
        # The relative URL to validate.
        url,
        # An optional string that, if provided, must be in the text returned by the server
        expected_string='',
        # The number of validation errors expected
        expected_errors=0):

        self.client.get(url)
        self.assertEqual(self.client.status, 200)
        with open(url.replace('/', '-') + '.html', 'w') as f:
            f.write(self.client.text.replace('\r\n', '\n'))
        if expected_string:
            self.assertIn(expected_string, self.client.text)

        vld = HTMLValidator()
        vld.validate_fragment(self.client.text)
        if len(vld.errors) != expected_errors:
            print('Errors for {}: {}'.format(url, len(vld.errors)))
            pprint(vld.errors)
            # Save the HTML to make fixing the errors easier.
            with open(url.replace('/', '-') + '.html', 'w') as f:
                f.write(self.client.text.replace('\r\n', '\n'))
            self.assertTrue(False)
        if vld.warnings:
            print('Warnings for {}: {}'.format(url, len(vld.warnings)))
            pprint(vld.warnings)
