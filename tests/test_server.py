# *****************************************
# |docname| - Tests using the web2py server
# *****************************************
# These tests start the web2py server then submit requests to it.
#
# The overall testing approach is functional: rather than test a function, this file primarily tests endpoints on the web server. To accomplish this:
#
# - This file includes the `web2py_server` fixture to start a web2py server, and a fixture (`test_client`) to make requests of it. To make debug easier, the `test_client` class saves the HTML of a failing test to a file, and also saves any web2py tracebacks in the HTML form to a file.
# - The `runestone_db` and related classes provide the ability to access the web2py database directory, in order to set up and tear down test. In order to leave the database unchanged after a test, almost all routines that modify the database are wrapped in a context manager; on exit, then delete any modifications.
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
import os
import time
import subprocess
from pprint import pprint
from contextlib import contextmanager
from io import open
from textwrap import dedent
import json
import re
from threading import Thread
try:
    from contextlib import ExitStack
except:
    from contextlib2 import ExitStack

# Third-party imports
# -------------------
import pytest
from gluon.contrib.webclient import WebClient
import gluon.shell
from py_w3c.validators.html.validator import HTMLValidator
import six
from six.moves.urllib.error import HTTPError

# Local imports
# -------------
sys.path.append(os.path.dirname(__file__))
from run_tests import COVER_DIRS


# Utilities
# =========
# Invoke the debugger.
##import pdb; pdb.set_trace()
# Put this in web2py code, then use the web-based debugger.
##from gluon.debug import dbg; dbg.set_trace()


# A simple data-struct object.
class _object(object):
    pass


# Given a dictionary, convert it to an object. For example, if ``d['one'] == 1``, then after ``do = DictToObject(d)``, ``do.one == 1``.
class DictToObject(object):
    def __init__(self, _dict):
        self.__dict__.update(_dict)


# Create a web2py controller environment. This is taken from pieces of ``gluon.shell.run``. It returns a ``dict`` containing the environment.
def web2py_controller_env(
        # _`application`: The name of the application to run in, as a string.
        application):

    env = gluon.shell.env(application, import_models=True)
    env.update(gluon.shell.exec_pythonrc())
    return env


# Import from a web2py controller. It returns a object of imported names, which also included standard web2py names (``request``, etc.). For example, ``d = web2py_controller_import('application', 'controller')`` then allows ``d.foo()``, assuming ``controller`` defined a ``foo()`` function.
def web2py_controller_import(
        # _`env`: A web2py environment returned by ``web2py_controller_env``. **This will be modified** by adding imported names to it.
        env,
        # The controller, as a string.
        controller):

    exec_file = 'applications/{}/controllers/{}.py'.format(env['request'].application, controller)
    exec(compile(open(exec_file, 'r' if six.PY3 else 'rb').read(), exec_file, 'exec'), env)
    return DictToObject(env)


# Create a web2py controller environment. Given ``ctl_env = web2py_controller('app_name')``, then  ``ctl_env.db`` refers to the usual DAL object for database access, ``ctl_env.request`` is an (empty) Request object, etc.
def web2py_controller(
        # See env_.
        env):

    return DictToObject(env)


# Fixtures
# ========
# This fixture starts and shuts down the web2py server.
#
# Execute this `fixture <https://docs.pytest.org/en/latest/fixture.html>`_ once per `module <https://docs.pytest.org/en/latest/fixture.html#scope-sharing-a-fixture-instance-across-tests-in-a-class-module-or-session>`_.
@pytest.fixture(scope='module')
def web2py_server():
    password = 'pass'

    # For debug, uncomment the next two lines, then run web2py manually to see all debug messages.
    ##yield DictToObject(dict(password=password))
    ##return

    # Start the web2py server.
    web2py_server = subprocess.Popen(
        [sys.executable, '-m', 'coverage', 'run', '--append',
         '--source=' + COVER_DIRS, 'web2py.py', '-a', password,
         '--nogui'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Start a thread to read web2py output and echo it.
    def echo():
        stdout, stderr = web2py_server.communicate()
        print('\n'
              'web2py server stdout\n'
              '--------------------\n')
        print(stdout)
        print('\n'
              'web2py server stderr\n'
              '--------------------\n')
        print(stderr)
    echo_thread = Thread(target=echo)
    echo_thread.start()

    # Save the password used.
    web2py_server.password = password
    # Wait for the server to come up. The delay varies; this is a guess.
    time.sleep(1)

    # After this comes the `teardown code <https://docs.pytest.org/en/latest/fixture.html#fixture-finalization-executing-teardown-code>`_.
    yield web2py_server

    # Terminate the server to give web2py time to shut down gracefully.
    web2py_server.terminate()
    echo_thread.join()


# The name of the Runestone controller.
RUNESTONE_CONTROLLER = 'runestone'


# The environment of a web2py controller.
RUNESTONE_ENV = web2py_controller_env(RUNESTONE_CONTROLLER)


# Create fixture providing a web2py controller environment for a Runestone application.
@pytest.fixture
def runestone_controller():
    return web2py_controller(RUNESTONE_ENV)


# Provide acess the the Runestone database through a fixture.
@pytest.fixture
def runestone_db(runestone_controller):
    db = runestone_controller.db
    yield db
    # In case of an error, roll back the last transaction to leave the
    # database in a working state. Also, attempt to leave the database in a
    # clean state for the next test.
    db.rollback()


# Provide context managers for manipulating the Runestone database.
class _RunestoneDbTools(object):
    def __init__(self, runestone_db):
        self.db = runestone_db

    # Create a new course. It returns an object with information about the created course.
    @contextmanager
    def create_course(self,
        # The name of the course to create, as a string.
        course_name='test_course_1',
        # The start date of the course, as a string.
        term_start_date='2000-01-01',
        # The value of the ``login_required`` flag for the course.
        login_required=True,
        # The base course for this course. If ``None``, it will use ``course_name``.
        base_course=None,
        # The student price for this course.
        student_price=None):

        # Sanity check: this class shouldn't exist.
        assert not self.db(self.db.courses.course_name == course_name).select().first()

        # Store these values in an object for convenient access.
        obj = _object()
        obj.course_name = course_name
        obj.term_start_date = term_start_date
        obj.login_required = login_required
        obj.base_course = base_course or course_name
        obj.student_price = student_price

        # Keep this in a local variable, in case the test bench changes the value stored in this object. This guarantees the deletion will work.
        course_id = self.db.courses.insert(
            course_name=course_name, base_course=obj.base_course,
            term_start_date=term_start_date,
            login_required=login_required,
            student_price=student_price,
        )
        obj.course_id = course_id
        self.db.commit()
        try:
            yield obj
        finally:
            # Remove this from the database.
            del self.db.courses[course_id]
            self.db.commit()


    @contextmanager
    def make_instructor(self,
        # The ID of the user to make an instructor.
        user_id,
        # The ID of the course in which the user will be an instructor.
        course_id):

        course_instructor_id =  self.db.course_instructor.insert(course=course_id, instructor=user_id)
        self.db.commit()
        db = self.db
        try:
            yield course_instructor_id
        finally:
            # Remove this from the database.
            del self.db.course_instructor[course_instructor_id]
            self.db.commit()


# Present ``_RunestoneDbTools`` as a fixture.
@pytest.fixture
def runestone_db_tools(runestone_db):
    return _RunestoneDbTools(runestone_db)


# Given the ``test_client.text``, prepare to write it to a file.
def _html_prep(text_str):
    _str = text_str.replace('\r\n', '\n')
    # Deal with fun Python 2 encoding quirk.
    return _str if six.PY2 else _str.encode('utf-8')


# Create a client for accessing the Runestone server.
class _TestClient(WebClient):
    def __init__(self, web2py_server):
        self.web2py_server = web2py_server
        super(_TestClient, self).__init__('http://127.0.0.1:8000/{}/'.format(RUNESTONE_CONTROLLER),
                                          postbacks=True)

    # Use the W3C validator to check the HTML at the given URL.
    def validate(self,
        # The relative URL to validate.
        url,
        # An optional string that, if provided, must be in the text returned by the server. If this is a list of strings, at least one of the provided strings but be in the text returned by the server.
        expected_string='',
        # The number of validation errors expected. If None, no validation is performed.
        expected_errors=None,
        # The expected status code from the request.
        expected_status=200,
        # All additional keyword arguments are passed to the ``post`` method.
        **kwargs):

        try:
            try:
                self.post(url, **kwargs)
            except HTTPError as e:
                # If this was the expected result, return.
                if e.code == expected_status:
                    # Since this is an error of some type, these paramets must be empty, since they can't be checked.
                    assert not expected_string
                    assert not expected_errors
                    return ''
                else:
                    raise
            assert self.status == expected_status
            if expected_string:
                if isinstance(expected_string, str):
                    assert expected_string in self.text
                else:
                    # Assume ``expected_string`` is a list of strings.
                    assert all(string in self.text for string in expected_string)

            if expected_errors is not None:
                vld = HTMLValidator()
                vld.validate_fragment(self.text)
                if len(vld.errors) != expected_errors:
                    print('Errors for {}: {}'.format(url, len(vld.errors)))
                    pprint(vld.errors)
                    assert False
                if vld.warnings:
                    print('Warnings for {}: {}'.format(url, len(vld.warnings)))
                    pprint(vld.warnings)

            return self.text if six.PY3 else self.text.decode('utf-8')

        except AssertionError:
            # Save the HTML to make fixing the errors easier. Note that ``self.text`` is already encoded as utf-8.
            validation_file = url.replace('/', '-') + '.html'
            with open(validation_file, 'wb') as f:
                f.write(_html_prep(self.text))
            print('Validation failure saved to {}.'.format(validation_file))
            raise

        except RuntimeError as e:
            # Provide special handling for web2py exceptions by saving the
            # resulting traceback.
            if e.args[0].startswith('ticket '):
                # Create a client to access the admin interface.
                admin_client = WebClient('http://127.0.0.1:8000/admin/',
                                         postbacks=True)
                # Log in.
                admin_client.post('', data={'password':
                                            self.web2py_server.password})
                assert admin_client.status == 200
                # Get the error.
                error_code = e.args[0][len('ticket '):]
                admin_client.get('default/ticket/' + error_code)
                assert admin_client.status == 200
                # Save it to a file.
                traceback_file = url.replace('/', '-') + '_traceback.html'
                with open(traceback_file, 'wb') as f:
                    f.write(_html_prep(admin_client.text))
                print('Traceback saved to {}.'.format(traceback_file))
            raise

    def logout(self):
        self.validate('default/user/logout', 'Logged out')

    # Always logout after a test finishes.
    def tearDown(self):
        self.logout()


# Present ``_TestClient`` as a fixure.
@pytest.fixture
def test_client(web2py_server):
    tc = _TestClient(web2py_server)
    yield tc
    tc.tearDown()


# This class allows creating a user inside a context manager.
class _TestUser(object):
    def __init__(self, test_client, runestone_db_tools, username, password, course_name,
        # True if the course is free (no payment required); False otherwise.
        is_free=True):

        self.test_client = test_client
        self.runestone_db_tools = runestone_db_tools
        self.username = username
        self.first_name = 'test'
        self.last_name = 'user'
        self.email = self.username + '@foo.com'
        self.password = password
        self.course_name = course_name
        self.is_free = is_free

    def __enter__(self):
        # Registration doesn't work unless we're logged out.
        self.test_client.logout()
        # Now, post the registration.
        self.test_client.validate('default/user/register',
            'Support Runestone Interactive' if self.is_free else 'Payment Amount',
            data=dict(
                username=self.username,
                first_name=self.first_name,
                last_name=self.last_name,
                # The e-mail address must be unique.
                email=self.email,
                password=self.password,
                password_two=self.password,
                # Note that ``course_id`` is (on the form) actually a course name.
                course_id=self.course_name,
                accept_tcp='on',
                donate='0',
                _next='/runestone/default/index',
                _formname='register',
            )
        )

        # Schedule this user for deletion.
        self.exit_stack_object = ExitStack()
        self.exit_stack = self.exit_stack_object.__enter__()
        self.exit_stack.callback(self._delete_user)

        # Record IDs
        db = self.runestone_db_tools.db
        self.course_id = db(db.courses.course_name == self.course_name).select(db.courses.id).first().id
        self.user_id = db(db.auth_user.username == self.username).select(db.auth_user.id).first().id

        return self

    # Clean up on exit by invoking all ``__exit__`` methods.
    def __exit__(self, exc_type, exc_value, traceback):
        self.exit_stack_object.__exit__(exc_type, exc_value, traceback)

    # Delete the user created by entering this context manager. TODO: This doesn't delete all the chapter progress tracking stuff.
    def _delete_user(self):
        db = self.runestone_db_tools.db
        # Delete the course this user registered for.
        db(( db.user_courses.course_id == self.course_id) & (db.user_courses.user_id == self.user_id) ).delete()
        # Delete the user.
        db(db.auth_user.username == self.username).delete()
        db.commit()

    def login(self):
        self.test_client.post('default/user/login', data=dict(
            username=self.username,
            password=self.password,
            _formname='login',
        ))

    def make_instructor(self, course_id=None):
        # If ``course_id`` isn't specified, use this user's ``course_id``.
        course_id = course_id or self.course_id
        return self.runestone_db_tools.make_instructor(self.user_id, course_id)

    # A context manager to update this user's profile. If a course was added, it returns that course's ID; otherwise, it returns None.
    @contextmanager
    def update_profile(self,
        # This parameter is passed to ``test_client.validate``.
        expected_string=None,
        # An updated username, or ``None`` to use ``self.username``.
        username=None,
        # An updated first name, or ``None`` to use ``self.first_name``.
        first_name=None,
        # An updated last name, or ``None`` to use ``self.last_name``.
        last_name=None,
        # An updated email, or ``None`` to use ``self.email``.
        email=None,
        # An updated last name, or ``None`` to use ``self.course_name``.
        course_name=None,
        section='',
        # A shortcut for specifying the ``expected_string``, which only applies if ``expected_string`` is not set. Use ``None`` if a course will not be added, ``True`` if the added course is free, or ``False`` if the added course is paid.
        is_free=None,
        # The value of the ``accept_tcp`` checkbox; provide an empty string to leave unchecked. The default value leaves it checked.
        accept_tcp='on'):

        if expected_string is None:
            if is_free is None:
                expected_string = 'Course Selection'
            else:
                expected_string = 'Support Runestone Interactive' \
                    if is_free else 'Payment Amount'
        username = username or self.username
        first_name = first_name or self.first_name
        last_name = last_name or self.last_name
        email = email or self.email
        course_name = course_name or self.course_name

        db = self.runestone_db_tools.db
        # Determine if we're adding a course. If so, delete it at the end of the test. To determine if a course is being added, the course must exist, but not be in the user's list of courses.
        course = db(db.courses.course_name == course_name).select(db.courses.id).first()
        delete_at_end = course and not db((db.user_courses.user_id == self.user_id) & (db.user_courses.course_id == course.id)).select(db.user_courses.id).first()

        # Perform the update.
        try:
            self.test_client.validate('default/user/profile',
                expected_string,
                data=dict(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    # Though the field is ``course_id``, it's really the course name.
                    course_id=course_name,
                    accept_tcp=accept_tcp,
                    section=section,
                    _next='/runestone/default/index',
                    id=str(self.user_id),
                    _formname='auth_user/' + str(self.user_id),
                )
            )

            yield course.id if delete_at_end else None
        finally:
            if delete_at_end:
                db = self.runestone_db_tools.db
                db((db.user_courses.user_id == self.user_id) & (db.user_courses.course_id == course.id)).delete()
                db.commit()

    # Call this after registering for a new course or adding a new course via ``update_profile`` to pay for the course.
    @contextmanager
    def make_payment(self,
        # The `Stripe test tokens <https://stripe.com/docs/testing#cards>`_ to use for payment.
        stripe_token,
        # The course ID of the course to pay for. None specifies ``self.course_id``.
        course_id=None):

        course_id = course_id or self.course_id

        # Get the signature from the HTML of the payment page.
        self.test_client.validate('default/payment')
        match = re.search('<input type="hidden" name="signature" value="([^ ]*)" />',
                          self.test_client.text)
        signature = match.group(1)

        try:
            html = self.test_client.validate('default/payment',
                data=dict(stripeToken=stripe_token, signature=signature)
            )
            assert ('Thank you for your payment' in html) or ('Payment failed' in html)

            yield None

        finally:
            db = self.runestone_db_tools.db
            db((db.user_courses.course_id == course_id) &
               (db.user_courses.user_id == self.user_id) ).delete()
            # Try to delete the payment
            try:
                db((db.user_courses.user_id == self.user_id) &
                   (db.user_courses.course_id == course_id) &
                   (db.user_courses.id == db.payments.user_courses_id)) \
                   .delete()
            except:
                pass
            db.commit()

    @contextmanager
    def hsblog(self, **kwargs):
        try:
            yield json.loads(self.test_client.validate('ajax/hsblog',
                                                       data=kwargs))
        finally:
            # Try to remove this hsblog entry.
            event = kwargs.get('event')
            div_id = kwargs.get('div_id')
            course = kwargs.get('course')
            db = self.runestone_db_tools.db
            criteria = ((db.useinfo.sid == self.username) &
                        (db.useinfo.act == kwargs.get('act', '')) &
                        (db.useinfo.div_id == div_id) &
                        (db.useinfo.event == event) &
                        (db.useinfo.course_id == course) )
            useinfo_row = db(criteria).select(db.useinfo.id, orderby=db.useinfo.id).last()
            if useinfo_row:
                del db.useinfo[useinfo_row.id]


# Present ``_TestUser`` as a fixture.
@pytest.fixture
def test_user(test_client, runestone_db_tools):
    return lambda *args, **kwargs: _TestUser(test_client, runestone_db_tools, *args, **kwargs)


# Provide easy access to a test user and course.
@pytest.fixture
def test_user_1(runestone_db_tools, test_user):
    with runestone_db_tools.create_course('test_course_1'), \
        test_user('test_user_1', 'password_1', 'test_course_1') as test_user_1:

        yield test_user_1


# Tests
# =====
# Use for easy manual testing of the server, by setting up a user and class automatically. Comment out the line below to enable it.
@pytest.mark.skip(reason='Only needed for manual testing.')
def test_manual(runestone_db_tools, test_user):
    # Modify this as desired to create courses, users, etc. for manual testing.
    with runestone_db_tools.create_course() as course_1, \
         test_user('bob', 'bob', course_1.course_name) as test_user_1:

        # Pause in the debugginer until manual testing is done.
        import pdb; pdb.set_trace()


# Validate the HTML produced by various web2py pages.
@pytest.mark.parametrize('url, requires_login, expected_string, expected_errors',
[
    # **Admin**
    #
    # FIXME: Flashed messages don't seem to work.
    #('admin/index', False, 'You must be registered for a course to access this page', 1),
    #('admin/index', True, 'You must be an instructor to access this page', 1),
    ('admin/doc', True, 'Runestone Help and Documentation', 1),

    # **Assignments**
    ('assignments/chooseAssignment', True, 'Assignments', 1),
    ('assignments/doAssignment', True, 'Bad Assignment ID', 1),
    ('assignments/index', True, 'Student Progress for', 1),
    # TODO: Why 2 errors here? Was just 1.
    ('assignments/practice', True, 'Practice tool is not set up for this course yet.', 2),
    ('assignments/practiceNotStartedYet', True, 'test_course_1', 2),

    # **Default**
    #
    # *User*
    #
    # The `authentication <http://web2py.com/books/default/chapter/29/09/access-control#Authentication>`_ section gives the URLs exposed by web2py. Check these.
    ('default/user/login', False, 'Login', 1),
    ('default/user/register', False, 'Registration', 1),
    ('default/user/logout', True, 'Logged out', 1),
    # One profile error is a result of removing the input field for the e-mail, but web2py still tries to label it, which is an error.
    ('default/user/profile', True, 'Profile', 2),
    ('default/user/change_password', True, 'Change password', 1),
    # Runestone doesn't support this.
    #'default/user/verify_email', False, 'Verify email', 1),
    ('default/user/retrieve_username', False, 'Retrieve username', 1),
    ('default/user/request_reset_password', False, 'Request reset password', 1),
    # This doesn't display a webpage, but instead redirects to courses.
    #('default/user/reset_password, False, 'Reset password', 1),
    ('default/user/impersonate', True, 'Impersonate', 1),
    # FIXME: This produces an exception.
    #'default/user/groups', True, 'Groups', 1),
    ('default/user/not_authorized', False, 'Not authorized', 1),
    # Returns a 404.
    #('default/user/navbar'=(False, 'xxx', 1),
    #
    # *Other pages*
    #
    # TODO: What is this for?
    #('default/call', False, 'Not found', 0),
    # TODO: weird returned HTML. ???
    #('default/index', True, 'Course Selection', 1),
    ('default/about', False, 'About Us', 1),
    ('default/error', False, 'Error: the document does not exist', 1),
    ('default/ack', False, 'Acknowledgements', 1),
    # web2py generates invalid labels for the radio buttons in this form.
    ('default/bio', True, 'Tell Us About Yourself', 3),
    ('default/courses', True, 'Course Selection', 1),
    ('default/remove', True, 'Remove a Course', 1),
    # Should work in both cases.
    ('default/reportabug', False, 'Report a Bug', 1),
    ('default/reportabug', True, 'Report a Bug', 1),
    # TODO: weird returned HTML. ???
    #('default/sendreport', True, 'Could not create issue', 1),
    ('default/terms', False, 'Terms and Conditions', 1),
    ('default/privacy', False, 'Runestone Academy Privacy Policy', 1),
    ('default/donate', False, 'Support Runestone Interactive', 1),
    # FIXME: This produces an exception.
    #('default/coursechooser', True, 'xxx', 1),
    #('default/removecourse', True, 'xxx', 1),


    # Assignments
    ('assignments/index', True, 'Student Progress for', 1),
    ('assignments/practice', True, 'Practice tool is not set up for this course yet.', 2),
    ('assignments/chooseAssignment', True, 'Assignments', 1),

    # **Misc**
    ('oauth/index', False, 'This page is a utility for accepting redirects from external services like Spotify or LinkedIn that use oauth.', 1),
    ('dashboard/index', True, 'Instructor Dashboard', 1),
    ('dashboard/grades', True, 'Gradebook', 1),
    ('dashboard/studentreport', True, 'Please make sure you are in the correct course', 1),
    # FIXME: This produces an exception.
    #('dashboard/exercisemetrics', True, 'xxx', 1),
    #('dashboard/questiongrades', True, 'Gradebook', 1),

    # TODO: Many other views!
])
def test_1(url, requires_login, expected_string, expected_errors, test_client,
           test_user_1):
    if requires_login:
        test_user_1.login()
    else:
        test_client.logout()
    test_client.validate(url, expected_string,
                         expected_errors)


# Validate the HTML in instructor-only pages.
@pytest.mark.parametrize('url, expected_string, expected_errors',
[
    # **Default**
    #
    # web2py-generated stuff produces two extra errors.
    ('default/bios', 'Bios', 3),

    # **Admin**
    ('admin/admin', 'Manage Section', 1),
    ('admin/course_students', '"test_user_1"', 2),
    ('admin/grading', 'assignment', 1),
    # TODO: This produces an exception.
    #('admin/practice', 'Choose when students should start their practice.', 1),
    ('admin/sections_list', 'db tables', 1),
    ('admin/sections_create', 'Create New Section', 1),
    ('admin/sections_delete', 'db tables', 1),
    ('admin/sections_update', 'db tables', 1),
    # TODO: This deletes the course, making the test framework raise an exception. Need a separate case to catch this.
    #('admin/deletecourse', 'Manage Section', 2),
    # FIXME: these raise an exception.
    #('admin/addinstructor', 'Trying to add non-user', 1), -- this is an api call
    #('admin/add_practice_items', 'xxx', 1), -- this is an api call
    #('admin/assignments', 'Assignment', 1),
    #('admin/backup', 'xxx', 1),
    #('admin/practice', 'Choose the sections taught, so that students can practice them.', 1),
    #('admin/removeinstructor', 'xxx', 1),
    #('admin/removeStudents', 'xxx', 1),
])
def test_2(url, expected_string, expected_errors, test_client,
           test_user, test_user_1):
    with test_user('test_instructor_1', 'password_1', 'test_course_1') as test_instructor_1, \
        test_instructor_1.make_instructor():

        # Make sure that non-instructors are redirected.
        test_client.logout()
        test_client.validate(url, 'Login')
        test_user_1.login()
        test_client.validate(url, 'Insufficient privileges')
        test_client.logout()

        # Test the instructor results.
        test_instructor_1.login()
        test_client.validate(url, expected_string,
                             expected_errors)


# Test the ``ajax/preview_question`` endpoint.
def test_3(test_client, test_user_1):
    preview_question = 'ajax/preview_question'
    # Passing no parameters should raise an error.
    test_client.validate(preview_question, 'Error: ')
    # Passing something not JSON-encoded should raise an error.
    test_client.validate(preview_question, 'Error: ', data={'code': 'xxx'})
    # Passing invalid RST should produce a Sphinx warning.
    test_client.validate(preview_question, 'WARNING', data={'code': '"*hi"'})
    # Passing valid RST with no Runestone component should produce an error.
    test_client.validate(preview_question, 'Error: ', data={'code': '"*hi*"'})
    # Passing a string with Unicode should work. Note that 0x0263 == 611; the JSON-encoded result will use this.
    test_client.validate(preview_question, '&#611;', data={'code': json.dumps(dedent(u'''\
        .. fillintheblank:: question_1

            Mary had a \u0263.

            -   :x: Whatever.
    '''))})
    # Verify that ``question_1`` is not in the database. TODO: This passes even if the ``DBURL`` env variable in ``ajax.py`` fucntion ``preview_question`` isn't deleted. So, this test doesn't work.
    db = test_user_1.runestone_db_tools.db
    assert len(db(db.fitb_answers.div_id == 'question_1').select()) == 0
    # TODO: Add a test case for when the runestone build produces a non-zero return code.


# Test the ``default/user/profile`` endpoint.
def test_4(test_client, test_user_1):
    test_user_1.login()
    runestone_db_tools = test_user_1.runestone_db_tools
    course_name = 'test_course_2'
    with runestone_db_tools.create_course(course_name) as test_course_2:
        # Test a non-existant course.
        with test_user_1.update_profile(expected_string='Errors in form',
                                   course_name='does_not_exist'):
            pass

        # Test an invalid e-mail address. TODO: This doesn't produce an error message.
        ##test_user_1.update_profile(expected_string='Errors in form',
        ##                           email='not a valid e-mail address')

        # Change the user's profile data; add a new course.
        username = 'a_different_username'
        first_name = 'a different first'
        last_name = 'a different last'
        email = 'a_different_email@foo.com'
        section = 'a_different_section'
        with test_user_1.update_profile(username=username, first_name=first_name,
           last_name=last_name, email=email, section=section,
           course_name=course_name, accept_tcp='', is_free=True):

            # Check the values.
            db = runestone_db_tools.db
            user = db(db.auth_user.id == test_user_1.user_id).select().first()
            # The username shouldn't be changable.
            assert user.username == test_user_1.username
            assert user.first_name == first_name
            assert user.last_name == last_name
            # TODO: The e-mail address isn't updated.
            #assert user.email == email
            assert user.course_id == test_course_2.course_id
            assert user.accept_tcp == False
            # TODO: I'm not sure where the section is stored.
            #assert user.section == section


# Test that the course name is correctly preserved across registrations if other fields are invalid.
def test_5(test_client, runestone_db_tools):
    # Registration doesn't work unless we're logged out.
    test_client.logout()
    course_name = 'a_course_name'
    with runestone_db_tools.create_course(course_name):
        # Now, post the registration.
        username = 'username'
        first_name = 'first'
        last_name = 'last'
        email = 'e@mail.com'
        password = 'password'
        test_client.validate('default/user/register', 'Please fix the following errors in your registration', data=dict(
            username=username,
            first_name=first_name,
            last_name=last_name,
            # The e-mail address must be unique.
            email=email,
            password=password,
            password_two=password + 'oops',
            # Note that ``course_id`` is (on the form) actually a course name.
            course_id=course_name,
            accept_tcp='on',
            donate='0',
            _next='/runestone/default/index',
            _formname='register',
        ))


# Check that the pricing system works correctly.
def test_6(runestone_db_tools):
    # Check the pricing.
    default_controller = web2py_controller_import(RUNESTONE_ENV, 'default')
    db = runestone_db_tools.db

    with runestone_db_tools.create_course() as base_course, \
        runestone_db_tools.create_course('test_child_course', base_course=base_course.course_name) as child_course:
        # First, test on a base course.
        for expected_price, actual_price in [(0, None), (0, -100), (0, 0), (15, 15)]:
            db(db.courses.id == base_course.course_id).update(student_price=actual_price)
            assert default_controller._course_price(base_course.course_id) == expected_price

        # Test in a child course as well. Create a matrix of all base course prices by all child course prices.
        for expected_price, actual_base_price, actual_child_price in [
            (0, None, None), (0, None, 0), (0, None, -1), (2, None, 2),
            (0,    0, None), (0,    0, 0), (0,    0, -1), (2,    0, 2),
            (0,   -2, None), (0,   -2, 0), (0,   -2, -1), (2,   -2, 2),
            (3,    3, None), (0,    3, 0), (0,    3, -1), (2,    3, 2)]:

            db(db.courses.id == base_course.course_id).update(student_price=actual_base_price)
            db(db.courses.id == child_course.course_id).update(student_price=actual_child_price)
            assert default_controller._course_price(child_course.course_id) == expected_price


# Check that setting the price causes redirects to the correct location (payment vs. donation) when registering for a course or adding a new course.
def test_7(runestone_db_tools, test_user):
    db = runestone_db_tools.db
    with runestone_db_tools.create_course(student_price=0) as course_1, \
        runestone_db_tools.create_course('test_course_2', student_price=0) as course_2:

        # Check registering for a free course.
        with test_user('test_user_1', 'password_1', course_1.course_name,
                       is_free=True) as test_user_1:
            # Verify the user was added to the ``user_courses`` table.
            assert db(( db.user_courses.course_id == test_user_1.course_id) & (db.user_courses.user_id == test_user_1.user_id) ).select().first()

            # Check adding a free course.
            with test_user_1.update_profile(course_name=course_2.course_name,
                                            is_free=True):
                # Same as above.
                assert db(( db.user_courses.course_id == course_2.course_id) & (db.user_courses.user_id == test_user_1.user_id) ).select().first()

    # Check registering for a paid course.
    with runestone_db_tools.create_course(student_price=1) as course_1, \
        runestone_db_tools.create_course('test_course_2', student_price=1) as course_2:
        # Check registering for a paid course.
        with test_user('test_user_1', 'password_1', course_1.course_name,
                       is_free=False) as test_user_1:

            # Until payment is provided, the user shouldn't be added to the ``user_courses`` table. Ensure that refresh, login/logout, profile changes, adding another class, etc. don't allow access.
            test_user_1.test_client.logout()
            test_user_1.login()
            test_user_1.test_client.validate('default/index')

            # Check adding a paid course.
            with test_user_1.update_profile(course_name=course_2.course_name,
                                            is_free=False):

                # Verify no access without payment.
                assert not db(( db.user_courses.course_id == course_1.course_id) & (db.user_courses.user_id == test_user_1.user_id) ).select().first()
                assert not db(( db.user_courses.course_id == course_2.course_id) & (db.user_courses.user_id == test_user_1.user_id) ).select().first()


# Check that payments are handled correctly.
def test_8(runestone_controller, runestone_db_tools, test_user):
    if not runestone_controller.settings.STRIPE_SECRET_KEY:
        pytest.skip('No Stripe keys provided.')

    db = runestone_db_tools.db
    with runestone_db_tools.create_course(student_price=100) as course_1, \
         test_user('test_user_1', 'password_1', course_1.course_name,
                   is_free=False) as test_user_1:

        def did_payment():
            return db(( db.user_courses.course_id == course_1.course_id) & (db.user_courses.user_id == test_user_1.user_id) ).select().first()
        assert not did_payment()

        with test_user_1.make_payment('tok_visa'):
            assert did_payment()
            # Check that the payment record is correct.
            payment = db((db.user_courses.user_id == test_user_1.user_id) &
                         (db.user_courses.course_id == course_1.course_id) &
                         (db.user_courses.id == db.payments.user_courses_id)) \
                         .select(db.payments.charge_id).first()
            assert payment.charge_id

        # Test some failing tokens.
        for token in ['tok_chargeCustomerFail', 'tok_chargeDeclined']:
            with test_user_1.make_payment(token):
                assert not did_payment()

        # TODO: Test with more tokens, test failures.


# Test dynamic book routing.
def test_10(test_client, test_user_1):
    test_user_1.login()

    # Test error cases.
    validate = test_user_1.test_client.validate
    test_course_1 = test_user_1.course_name
    course_selection = 'Course Selection'
    # A non-existant course.
    validate('books/published/xxx', course_selection)
    # A non-existant page.
    validate('books/published/{}/xxx'.format(test_course_1),
             expected_status=404)
    # A directory.
    validate('books/published/{}/test_chapter_1'.format(test_course_1),
             expected_status=404)
    # Attempt to access files outside a course.
    validate('books/published/{}/../conf.py'.format(test_course_1),
             expected_status=404)

    # A valid page. Check the book config as well.
    validate('books/published/{}/index.html'.format(test_course_1), [
        'The red car drove away.',
        "eBookConfig.course = '{}';".format(test_course_1),
        "eBookConfig.basecourse = '{}';".format(test_course_1),
    ])

    # Drafts shouldn't be accessible by students.
    validate('books/draft/{}/index.html'.format(test_course_1),
             'Insufficient privileges')
    with test_user_1.make_instructor():
        # But should be instructors.
        validate('books/draft/{}/index.html'.format(test_course_1),
                 'The red car drove away.')

    # Check routing in a child book.
    with test_user_1.runestone_db_tools.create_course('child_course_1', base_course=test_user_1.course_name) as child_course:
        child_course_1 = child_course.course_name
        # Routes if they do.
        with test_user_1.update_profile(course_name=child_course_1, is_free=True):
            validate('books/published/{}/index.html'.format(test_course_1), [
                'The red car drove away.',
                "eBookConfig.course = '{}';".format(child_course_1),
                "eBookConfig.basecourse = '{}';".format(test_course_1),
            ])

    # Test static content
    validate('books/published/{}/_static/runestone-custom-sphinx-bootstrap.css'.format(test_course_1),
             'background-color: #fafafa;')


def test_11(test_client, runestone_db_tools, test_user):
    with runestone_db_tools.create_course('test_course_3') as course_3:
        with test_user('test_instructor_1', 'password_1', course_3.course_name) as test_instructor_1, \
            test_instructor_1.make_instructor():

            test_instructor_1.login()
            db = runestone_db_tools.db

            # Create an assignment -- using createAssignment
            test_client.post('admin/createAssignment',
                data=dict(name='test_assignment_1'))

            assign = db((db.assignments.name == 'test_assignment_1') &
                        (db.assignments.course == test_instructor_1.course_id)).select().first()

            assert assign

            # Delete an assignment -- using removeassignment
            test_client.post('admin/removeassign', data=dict(assignid=assign.id))
            assert not db(db.assignments.name == 'test_assignment_1').select().first()

            test_client.post('admin/removeassign', data=dict(assignid=9999999))
            assert "Error" in test_client.text

            test_client.post('admin/removeassign', data=dict(assignid=""))
            assert "Error" in test_client.text
