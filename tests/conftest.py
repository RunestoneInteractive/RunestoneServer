# ***************************************
# |docname| - pytest fixtures for testing
# ***************************************
# These fixtures start the web2py server then submit requests to it.
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
import time
import subprocess
from pprint import pprint
from contextlib import contextmanager
from io import open
import json
import re
from threading import Thread
import datetime
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
from six.moves.urllib.error import HTTPError, URLError
from six.moves.urllib.request import urlopen

# Local imports
# -------------
from .utils import COVER_DIRS, DictToObject


# Utilities
# =========
# A simple data-struct object.
class _object(object):
    pass


# Create a web2py controller environment. This is taken from pieces of ``gluon.shell.run``. It returns a ``dict`` containing the environment.
def web2py_controller_env(
        # _`application`: The name of the application to run in, as a string.
        application):

    env = gluon.shell.env(application, import_models=True)
    env.update(gluon.shell.exec_pythonrc())
    return env


# Create a web2py controller environment. Given ``ctl_env = web2py_controller('app_name')``, then  ``ctl_env.db`` refers to the usual DAL object for database access, ``ctl_env.request`` is an (empty) Request object, etc.
def web2py_controller(
        # See env_.
        env):

    return DictToObject(env)


# Fixtures
# ========
@pytest.fixture(scope='module')
def web2py_server_address():
    return 'http://127.0.0.1:8000'


# This fixture starts and shuts down the web2py server.
#
# Execute this `fixture <https://docs.pytest.org/en/latest/fixture.html>`_ once per `module <https://docs.pytest.org/en/latest/fixture.html#scope-sharing-a-fixture-instance-across-tests-in-a-class-module-or-session>`_.
@pytest.fixture(scope='module')
def web2py_server(runestone_name, web2py_server_address):
    password = 'pass'

    # For debug, uncomment the next three lines, then run web2py manually to see all debug messages. Use a command line like ``python web2py.py -a pass -X -K runestone,runestone &`` to also start the workers for the scheduler.
    ##import pdb; pdb.set_trace()
    ##yield DictToObject(dict(password=password))
    ##return

    # Start the web2py server and the `web2py scheduler <http://web2py.com/books/default/chapter/29/04/the-core#Scheduler-Deployment>`_.
    web2py_server = subprocess.Popen(
        [sys.executable, '-m', 'coverage', 'run', '--append',
         '--source=' + COVER_DIRS, 'web2py.py', '-a', password,
         '--nogui'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Wait for the webserver to come up.
    for tries in range(50):
        try:
            urlopen(web2py_server_address, timeout=2)
        except URLError:
            # Wait for the server to come up.
            time.sleep(0.1)
        else:
            # The server is up. We're done.
            break
    # Running two processes doesn't produce two active workers. Running with ``-K runestone,runestone`` means additional subprocesses are launched that we lack the PID necessary to kill. So, just use one worker.
    web2py_scheduler = subprocess.Popen(
        [sys.executable, '-m', 'coverage', 'run', '--append',
         '--source=' + COVER_DIRS, 'web2py.py', '-K', runestone_name],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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

    # After this comes the `teardown code <https://docs.pytest.org/en/latest/fixture.html#fixture-finalization-executing-teardown-code>`_.
    yield web2py_server

    # Terminate the server and schedulers to give web2py time to shut down gracefully.
    web2py_server.terminate()
    web2py_scheduler.terminate()
    echo_thread.join()


# The name of the Runestone controller. It must be module scoped to allow the ``web2py_server`` to use it.
@pytest.fixture(scope='module')
def runestone_name():
    return 'runestone'


# The environment of a web2py controller.
@pytest.fixture
def runestone_env(runestone_name):
    return web2py_controller_env(runestone_name)


# Create fixture providing a web2py controller environment for a Runestone application.
@pytest.fixture
def runestone_controller(runestone_env):
    return web2py_controller(runestone_env)


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
    def __init__(self, web2py_server, web2py_server_address, runestone_name):
        self.web2py_server = web2py_server
        self.web2py_server_address = web2py_server_address
        super(_TestClient, self).__init__('{}/{}/'.format(self.web2py_server_address, runestone_name),
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

            return self.text

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
                admin_client = WebClient('{}/admin/'.format(self.web2py_server_address),
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
def test_client(web2py_server, web2py_server_address, runestone_name):
    tc = _TestClient(web2py_server, web2py_server_address, runestone_name)
    yield tc
    tc.tearDown()


# This class allows creating a user inside a context manager.
class _TestUser(object):
    def __init__(self, test_client, runestone_db_tools, username, password, course_name,
        # True if the course is free (no payment required); False otherwise.
        is_free=True, first_name='test', last_name='user'):

        self.test_client = test_client
        self.runestone_db_tools = runestone_db_tools
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
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
        self.test_client.validate('default/user/login', data=dict(
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
        # Get the time, rounded down to a second, before posting to the server.
        ts = datetime.datetime.utcnow()
        ts -= datetime.timedelta(microseconds=ts.microsecond)

        # Post to the server.
        try:
            yield json.loads(self.test_client.validate('ajax/hsblog',
                                                       data=kwargs))
        finally:
            # Try to remove this hsblog entry.
            event = kwargs.get('event')
            div_id = kwargs.get('div_id')
            course = kwargs.get('course')
            answer = kwargs.get('answer')
            correct = kwargs.get('correct')
            act = kwargs.get('act', '')

            db = self.runestone_db_tools.db
            useinfo_row = db(
                (db.useinfo.sid == self.username) &
                (db.useinfo.act == act) &
                (db.useinfo.div_id == div_id) &
                (db.useinfo.event == event) &
                (db.useinfo.course_id == course) &
                (db.useinfo.timestamp >= ts)
            ).select(db.useinfo.id, orderby=db.useinfo.id).first()
            if useinfo_row:
                del db.useinfo[useinfo_row.id]

            # TODO: Add more cleanup for other question types.
            if event == 'lp_build':
                lp_answers_row = db(
                    (db.lp_answers.sid == self.username) &
                    (db.lp_answers.div_id == div_id) &
                    (db.lp_answers.course_name == course) &
                    (db.lp_answers.timestamp >= ts)
                ).select(db.lp_answers.id, orderby=db.lp_answers.id).first()
                if lp_answers_row:
                    del db.lp_answers[lp_answers_row.id]
            elif event == 'fillb':
                fitb_answers_row = db(
                    # Note: can't test the correct field, since it's ignored if server feedback is provided.
                    (db.fitb_answers.sid == self.username) &
                    (db.fitb_answers.div_id == div_id) &
                    (db.fitb_answers.course_name == course) &
                    (db.fitb_answers.timestamp >= ts) &
                    (db.fitb_answers.answer == answer)
                ).select(db.fitb_answers.id, orderby=db.fitb_answers.id).first()
                if fitb_answers_row:
                    del db.fitb_answers[fitb_answers_row.id]
            elif event == 'mChoice':
                mchoice_answers_row = db(
                    (db.mchoice_answers.sid == self.username) &
                    (db.mchoice_answers.div_id == div_id) &
                    (db.mchoice_answers.course_name == course) &
                    (db.mchoice_answers.timestamp >= ts) &
                    (db.mchoice_answers.answer == answer) &
                    (db.mchoice_answers.correct == correct)
                ).select(db.mchoice_answers.id, orderby=db.mchoice_answers.id).first()
                if mchoice_answers_row:
                    del db.mchoice_answers[mchoice_answers_row.id]
            elif event == 'shortanswer':
                shortanswer_answers_row = db(
                    (db.shortanswer_answers.sid == self.username) &
                    (db.shortanswer_answers.div_id == div_id) &
                    (db.shortanswer_answers.course_name == course) &
                    (db.shortanswer_answers.timestamp >= ts) &
                    (db.shortanswer_answers.answer == act)
                ).select(db.shortanswer_answers.id, orderby=db.shortanswer_answers.id).first()
                if shortanswer_answers_row:
                    del db.shortanswer_answers[shortanswer_answers_row.id]


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
