# *****************************************
# |docname| - Tests using the web2py server
# *****************************************
# These tests start the web2py server then submit requests to it. All the fixtures are auto-imported by pytest from ``conftest.py``.
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
from io import open
from textwrap import dedent
import json
from threading import Thread
import datetime

# Third-party imports
# -------------------
import pytest
import six
import xlrd

# Local imports
# -------------
from .utils import web2py_controller_import


# Debugging notes
# ===============
# Invoke the debugger.
##import pdb; pdb.set_trace()
# Put this in web2py code, then use the web-based debugger.
##from gluon.debug import dbg; dbg.set_trace()

# Tests
# =====
# Use for easy manual testing of the server, by setting up a user and class automatically. Comment out the line below to enable it.
@pytest.mark.skip(reason='Only needed for manual testing.')
def test_manual(runestone_db_tools, test_user):
    # Modify this as desired to create courses, users, etc. for manual testing.
    course_1 = runestone_db_tools.create_course()
    test_user('bob', 'bob', course_1.course_name)

    # Pause in the debugginer until manual testing is done.
    import pdb; pdb.set_trace()


# Validate the HTML produced by various web2py pages.
# NOTE -- this is the start of a really really long decorator for test_1
@pytest.mark.parametrize('url, requires_login, expected_string, expected_errors',
[
    # **Admin**
    #----------
    # FIXME: Flashed messages don't seem to work.
    #('admin/index', False, 'You must be registered for a course to access this page', 1),
    #('admin/index', True, 'You must be an instructor to access this page', 1),
    ('admin/doc', True, 'Runestone Help and Documentation', 1),

    # **Assignments**
    #----------------
    ('assignments/chooseAssignment', True, 'Assignments', 1),
    ('assignments/doAssignment', True, 'Bad Assignment ID', 1),
    ('assignments/index', True, 'Student Progress for', 1),
    # TODO: Why 2 errors here? Was just 1.
    ('assignments/practice', True, 'Practice tool is not set up for this course yet.', 2),
    ('assignments/practiceNotStartedYet', True, 'test_course_1', 2),

    # **Default**
    #------------
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
    # TODO: This soesn't really test the body of either of these
    ('default/coursechooser', True, 'Course Selection', 1),
    ('default/removecourse', True, 'Course Selection', 1),

    # **Dashboard**
    #--------------
    ('dashboard/index', True, 'Instructor Dashboard', 1),
    ('dashboard/grades', True, 'Gradebook', 1),
    ('dashboard/studentreport', True, 'Please make sure you are in the correct course', 1),
    # TODO: This doesn't really test anything about either
    # exercisemetrics or questiongrades other than properly handling a call with no information
    ('dashboard/exercisemetrics', True, 'Instructor Dashboard', 1),
    ('dashboard/questiongrades', True, 'Instructor Dashboard', 1),

    # **Designer**
    #-------------
    ('designer/index', True, 'This page allows you to select a book for your own class.', 1),

    # **OAuth**
    #----------
    ('oauth/index', False, 'This page is a utility for accepting redirects from external services like Spotify or LinkedIn that use oauth.', 1),

    # TODO: Many other views!
])
def test_validate_user_pages(url, requires_login, expected_string,
                             expected_errors, test_client, test_user_1):
    if requires_login:
        test_user_1.login()
    else:
        test_client.logout()
    test_client.validate(url, expected_string,
                         expected_errors)


# Validate the HTML in instructor-only pages.
# NOTE -- this is the start of a really really long decorator for test_2
@pytest.mark.parametrize('url, expected_string, expected_errors',
[
    # **Default**
    #------------
    # web2py-generated stuff produces two extra errors.
    ('default/bios', 'Bios', 3),
    # FIXME: The element ``<form id="editIndexRST" action="">`` in ``views/admin/admin.html`` produces the error ``Bad value \u201c\u201d for attribute \u201caction\u201d on element \u201cform\u201d: Must be non-empty.``.
    #
    # **Admin**
    #----------
    ('admin/admin', 'Manage Section', 1),
    ('admin/course_students', '"test_user_1"', 2),
    # TODO: A response of ``null`` is obviously wrong.
    ('admin/createAssignment', 'null', None),
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
    #('admin/removeassign', 'Cannot remove assignment with id of', 1),
    #('admin/removeinstructor', 'xxx', 1),
    #('admin/removeStudents', 'xxx', 1),
    # TODO: added to the ``createAssignment`` endpoint so far.
])
def test_validate_instructor_pages(url, expected_string, expected_errors,
                                   test_client, test_user, test_user_1):
    test_instructor_1 = test_user('test_instructor_1', 'password_1', 'test_course_1')
    test_instructor_1.make_instructor()
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
    test_course_2 = runestone_db_tools.create_course(course_name)
    # Test a non-existant course.
    test_user_1.update_profile(expected_string='Errors in form',
                               course_name='does_not_exist')

    # Test an invalid e-mail address. TODO: This doesn't produce an error message.
    ##test_user_1.update_profile(expected_string='Errors in form',
    ##                           email='not a valid e-mail address')

    # Change the user's profile data; add a new course.
    username = 'a_different_username'
    first_name = 'a different first'
    last_name = 'a different last'
    email = 'a_different_email@foo.com'
    section = 'a_different_section'
    test_user_1.update_profile(username=username, first_name=first_name,
       last_name=last_name, email=email, section=section,
       course_name=course_name, accept_tcp='', is_free=True)

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
    runestone_db_tools.create_course(course_name)
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
def test_6(runestone_db_tools, runestone_env):
    # Check the pricing.
    default_controller = web2py_controller_import(runestone_env, 'default')
    db = runestone_db_tools.db

    base_course = runestone_db_tools.create_course()
    child_course = runestone_db_tools.create_course('test_child_course', base_course=base_course.course_name)
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
def test_price_free(runestone_db_tools, test_user):
    db = runestone_db_tools.db
    course_1 = runestone_db_tools.create_course(student_price=0)
    course_2 = runestone_db_tools.create_course('test_course_2', student_price=0)

    # Check registering for a free course.
    test_user_1 = test_user('test_user_1', 'password_1', course_1.course_name,
                            is_free=True)
    # Verify the user was added to the ``user_courses`` table.
    assert db(( db.user_courses.course_id == test_user_1.course_id) & (db.user_courses.user_id == test_user_1.user_id) ).select().first()

    # Check adding a free course.
    test_user_1.update_profile(course_name=course_2.course_name, is_free=True)
    # Same as above.
    assert db(( db.user_courses.course_id == course_2.course_id) & (db.user_courses.user_id == test_user_1.user_id) ).select().first()


def test_price_paid(runestone_db_tools, test_user):
    db = runestone_db_tools.db
    # Check registering for a paid course.
    course_1 = runestone_db_tools.create_course(student_price=1)
    course_2 = runestone_db_tools.create_course('test_course_2', student_price=1)
    # Check registering for a paid course.
    test_user_1 = test_user('test_user_1', 'password_1', course_1.course_name,
                           is_free=False)

    # Until payment is provided, the user shouldn't be added to the ``user_courses`` table. Ensure that refresh, login/logout, profile changes, adding another class, etc. don't allow access.
    test_user_1.test_client.logout()
    test_user_1.login()
    test_user_1.test_client.validate('default/index')

    # Check adding a paid course.
    test_user_1.update_profile(course_name=course_2.course_name, is_free=False)

    # Verify no access without payment.
    assert not db(( db.user_courses.course_id == course_1.course_id) & (db.user_courses.user_id == test_user_1.user_id) ).select().first()
    assert not db(( db.user_courses.course_id == course_2.course_id) & (db.user_courses.user_id == test_user_1.user_id) ).select().first()


# Check that payments are handled correctly.
def test_8(runestone_controller, runestone_db_tools, test_user):
    if not runestone_controller.settings.STRIPE_SECRET_KEY:
        pytest.skip('No Stripe keys provided.')

    db = runestone_db_tools.db
    course_1 = runestone_db_tools.create_course(student_price=100)
    test_user_1 = test_user('test_user_1', 'password_1', course_1.course_name,
                            is_free=False)

    def did_payment():
        return db(( db.user_courses.course_id == course_1.course_id) & (db.user_courses.user_id == test_user_1.user_id) ).select().first()

    # Test some failing tokens.
    assert not did_payment()
    for token in ['tok_chargeCustomerFail', 'tok_chargeDeclined']:
        test_user_1.make_payment(token)
        assert not did_payment()

    test_user_1.make_payment('tok_visa')
    assert did_payment()
    # Check that the payment record is correct.
    payment = db((db.user_courses.user_id == test_user_1.user_id) &
                 (db.user_courses.course_id == course_1.course_id) &
                 (db.user_courses.id == db.payments.user_courses_id)) \
                 .select(db.payments.charge_id).first()
    assert payment.charge_id


# Test the LP endpoint.
@pytest.mark.skipif(six.PY2, reason='Requires Python 3.')
def test_lp_1(test_user_1):
    test_user_1.login()

    # Check that omitting parameters produces an error.
    ret = test_user_1.hsblog(event='lp_build')
    assert 'No feedback provided' in ret['errors'][0]

    # Check that database entries are validated.
    ret = test_user_1.hsblog(
        event='lp_build',
        # This div_id is too long. Everything else is OK.
        div_id='X'*1000,
        course=test_user_1.course_name,
        builder='unsafe-python',
        answer=json.dumps({"code_snippets": ["def one(): return 1"]}),
    )
    assert 'div_id' in ret['errors'][0]

    # Check a passing case
    def assert_passing():
        ret = test_user_1.hsblog(
            event='lp_build',
            div_id='lp_demo_1',
            course=test_user_1.course_name,
            builder='unsafe-python',
            answer=json.dumps({"code_snippets": ["def one(): return 1"]}),
        )
        assert 'errors' not in ret
        assert ret['correct'] == 100
    assert_passing()

    # Send lots of jobs to test out the queue. Skip this for now -- not all the useinfo entries get deleted, which causes ``test_getNumOnline`` to fail.
    if False:
        threads = [Thread(target=assert_passing) for x in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()


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
    test_user_1.make_instructor()
    # But should be instructors.
    validate('books/draft/{}/index.html'.format(test_course_1),
             'The red car drove away.')

    # Check routing in a child book.
    child_course = test_user_1.runestone_db_tools.create_course('child_course_1', base_course=test_user_1.course_name)
    child_course_1 = child_course.course_name
    # Routes if they do.
    test_user_1.update_profile(course_name=child_course_1, is_free=True)
    validate('books/published/{}/index.html'.format(test_course_1), [
        'The red car drove away.',
        "eBookConfig.course = '{}';".format(child_course_1),
        "eBookConfig.basecourse = '{}';".format(test_course_1),
    ])

    # Test static content
    validate('books/published/{}/_static/runestone-custom-sphinx-bootstrap.css'.format(test_course_1),
             'background-color: #fafafa;')


def test_11(test_client, runestone_db_tools, test_user):
    course_3 = runestone_db_tools.create_course('test_course_3')
    test_instructor_1 = test_user('test_instructor_1', 'password_1', course_3.course_name)
    test_instructor_1.make_instructor()
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


# Test the grades report.
def test_grades_1(runestone_db_tools, test_user, tmp_path):
    course_name = 'test_course_1'

    # Create test users.
    runestone_db_tools.create_course(course_name)

    # **Create test data**
    #=====================
    # Create test users.
    test_user_array = [
        test_user('test_user_{}'.format(index), 'x', course_name, last_name='user_{}'.format(index))
        for index in range(3)
    ]

    def assert_passing(index, *args, **kwargs):
        res = test_user_array[index].hsblog(*args, **kwargs)
        assert 'errors' not in res

    # Prepare common arguments for each question type.
    shortanswer_kwargs = dict(
        event='shortanswer',
        div_id='team_eval_role_1',
        course=course_name,
    )
    fitb_kwargs = dict(event='fillb', div_id='test_fitb_1', course=course_name)
    mchoice_kwargs = dict(event='mChoice', div_id='test_mchoice_1', course=course_name)
    lp_kwargs = dict(event='lp_build', div_id='lp_demo_1',
                     course=course_name, builder='unsafe-python')

    # *User 0*: no data supplied
    #---------------------------

    # *User 1*: correct answers
    #--------------------------
    # It doesn't matter which user logs out, since all three users share the same client.
    logout = test_user_array[2].test_client.logout
    logout()
    test_user_array[1].login()
    assert_passing(1, act=json.dumps(test_user_array[1].username), **shortanswer_kwargs)
    assert_passing(1, answer=json.dumps(['red', 'away']), **fitb_kwargs)
    assert_passing(1, answer='0', correct='T', **mchoice_kwargs)
    assert_passing(1,
        answer=json.dumps({"code_snippets": ["def one(): return 1"]}),
        **lp_kwargs
    )

    # *User 2*: incorrect answers
    #----------------------------
    logout()
    test_user_array[2].login()
    # Add three shortanswer answers, to make sure the number of attempts is correctly recorded.
    for x in range(3):
        assert_passing(2, act=json.dumps(test_user_array[2].username), **shortanswer_kwargs)
    assert_passing(2, answer=json.dumps(['xxx', 'xxxx']), **fitb_kwargs)
    assert_passing(2, answer='1', correct='F', **mchoice_kwargs)
    assert_passing(2,
        answer=json.dumps({"code_snippets": ["def one(): return 2"]}),
        **lp_kwargs
    )

    # **Test the grades_report endpoint**
    #====================================
    tu = test_user_array[2]
    def grades_report(assignment, *args, **kwargs):
        return tu.test_client.validate('assignments/grades_report', *args, data={'assignment': assignment}, **kwargs)

    # Test not being an instructor.
    grades_report('', 'About Runestone')
    tu.make_instructor()
    # Test an invalid assignment.
    grades_report('', 'Unknown assignment')

    # Create an assignment.
    assignment_name = 'test_assignment'
    assignment_id = json.loads(
        tu.test_client.validate('admin/createAssignment',
                                data={'name': assignment_name})
    )[assignment_name]
    assignment_kwargs = dict(
        assignment=assignment_id,
        autograde='pct_correct',
        which_to_grade='first_answer',
    )

    # Add questions to the assignment.
    def add_to_assignment(question_kwargs, points):
        assert tu.test_client.validate(
            'admin/add__or_update_assignment_question', data=dict(
                question=question_kwargs['div_id'],
                points=points,
                **assignment_kwargs
            )
        ) != json.dumps('Error')
    add_to_assignment(shortanswer_kwargs, 0)
    add_to_assignment(fitb_kwargs, 1)
    add_to_assignment(mchoice_kwargs, 2)
    add_to_assignment(lp_kwargs, 3)

    # Autograde the assignment.
    assignment_kwargs = dict(data={'assignment': assignment_name})
    assert json.loads(
        tu.test_client.validate('assignments/autograde',
                                **assignment_kwargs)
    )['message'].startswith('autograded')
    assert json.loads(
        tu.test_client.validate('assignments/calculate_totals',
                                **assignment_kwargs)
    )['success']

    # Test this assignment.
    # Encoding problems in web2py test framework with py3.
    if six.PY3:
        return
    xlsx_path = str(tmp_path / 'grades.xlsx')
    with open(xlsx_path, 'wb') as f:
        text = grades_report(assignment_name)
        f.write(text if six.PY2 else text.encode('utf-8'))
        # If an error occurred, print it.
        try:
            print(json.loads(text)['errors'][0])
        except:
            pass

    # Debug: uncomment this on Windows to manually inspect the resulting file.
    ##os.system(xlsx_path)

    # Open and check a few values.
    wb = xlrd.open_workbook(xlsx_path)

    # Check timestamps.
    timestamps_sheet = wb.sheet_by_name('timestamps')
    # I can't quite get these to line up. Excel's number is days since 1900 + hours/24. In Python that's:
    td = datetime.datetime.utcnow() - datetime.datetime(1900, 1, 1)
    excel_val = td.days + td.seconds/24.0/3600.0
    # However, what I'm getting is 2 days off. TODO: understand then fix this.
    for row in range(7, 9):
        for col in range(5, 9):
            assert timestamps_sheet.cell(row, col).value == pytest.approx(excel_val, 3)

    # Check the scores of test_user_1 and _2.
    scores_sheet = wb.sheet_by_name('scores')
    assert [scores_sheet.cell(7, col).value for col in range(6, 9)] == [1.0, 2.0, 3.0]
    assert [scores_sheet.cell(8, col).value for col in range(6, 9)] == [0.0, 0.0, 0.0]

    # Check the answers.
    answers_sheet = wb.sheet_by_name('answers')
    assert [answers_sheet.cell(7, col).value for col in range(5, 9)] == [u'test_user_1', "[u'red', u'away']", u'0', "{u'resultString': u'', u'code_snippets': [u'def one(): return 1']}"]
    assert [answers_sheet.cell(8, col).value for col in range(5, 8)] == [u'test_user_2', "[u'xxx', u'xxxx']", u'1']

    # Check the attempts.
    attempts_sheet = wb.sheet_by_name('attempts')
    assert [attempts_sheet.cell(7, col).value for col in range(5, 9)] == [1, 1, 1, 1]
    assert [attempts_sheet.cell(8, col).value for col in range(5, 9)] == [3, 1, 1, 1]

    logout()
    # Test with no login.
    grades_report('', 'About Runestone')


# Test the teaming report.
def test_team_1(runestone_db_tools, test_user, runestone_name):
    course_name = 'test_course_1'

    # Create test users.
    runestone_db_tools.create_course(course_name)

    # **Create test data**
    #=====================
    # Create test users.
    test_user_array = [
        test_user('test_user_{}'.format(index), 'x', course_name, last_name='user_{}'.format(index))
        for index in range(3)
    ]

    def assert_passing(index, *args, **kwargs):
        res = test_user_array[index].hsblog(*args, **kwargs)
        assert 'errors' not in res

    # Prepare common arguments for each question type.
    shortanswer1_kwargs = dict(
        event='shortanswer',
        div_id='team_eval_role_0',
        course=course_name,
    )
    shortanswer2_kwargs = dict(
        event='shortanswer',
        div_id='team_eval_communication',
        course=course_name,
    )
    fitb_kwargs = dict(event='fillb', div_id='team_eval_ge_contributions_0', course=course_name)

    # *User 0*
    #---------------------------
    logout = test_user_array[2].test_client.logout
    logout()
    test_user_array[0].login()
    assert_passing(0, act=json.dumps(test_user_array[0].username), **shortanswer1_kwargs)
    assert_passing(0, act=json.dumps('comm 0'), **shortanswer2_kwargs)
    assert_passing(0, answer=json.dumps(['5']), **fitb_kwargs)

    # *User 1*
    #--------------------------
    # It doesn't matter which user logs out, since all three users share the same client.
    logout()
    test_user_array[1].login()
    assert_passing(1, act=json.dumps(test_user_array[1].username), **shortanswer1_kwargs)
    assert_passing(1, act=json.dumps('comm 1'), **shortanswer2_kwargs)
    assert_passing(1, answer=json.dumps(['25']), **fitb_kwargs)

    # *User 2*
    #----------------------------
    logout()
    test_user_array[2].login()
    # Add three shortanswer answers, to make sure the number of attempts is correctly recorded.
    assert_passing(2, act=json.dumps(test_user_array[2].username), **shortanswer1_kwargs)
    assert_passing(2, act=json.dumps('comm 2'), **shortanswer2_kwargs)
    assert_passing(2, answer=json.dumps(['90']), **fitb_kwargs)

    # **Test the team report**
    #=========================
    with open('applications/{}/books/test_course_1/test_course_1.csv'.format(runestone_name), 'w', encoding='utf-8') as f:
        f.write(
            u'user id,user name,team name\n'
            'test_user_0@foo.com,test user_0,team 1\n'
            'test_user_1@foo.com,test user_1,team 1\n'
            'test_user_2@foo.com,test user_2,team 1\n'
        )

    # TODO: Test not being an instructor.
    tu = test_user_array[2]
    tu.make_instructor()
    tu.test_client.validate('books/published/test_course_1/test_chapter_1/team_report_1.html')

    logout()
    # TODO: Test with no login.
