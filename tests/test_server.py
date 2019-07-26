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
from textwrap import dedent
import json
from threading import Thread

# Third-party imports
# -------------------
import pytest
import six

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
    test_user('bob', 'bob', course_1)

    # Pause in the debugginer until manual testing is done.
    import pdb; pdb.set_trace()

def test_killer(test_assignment, test_client, test_user_1, runestone_db_tools):
    """
    This test ensures that we have the routing set up for testing properly.
    This test will fail if routes.py is set up as follows.
    routes_onerror = [
        ('runestone/static/404', '/runestone/static/fail.html'),
        ('runestone/500', '/runestone/default/reportabug.html'),
        ]
    for testing purposes we don't want web2py to capture 500 errors.
    """
    with pytest.raises(RuntimeError) as excinfo:
        test_client.post('admin/killer')
        assert test_client.text == ""
    assert "ticket" in str(excinfo.value)

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
    ('admin/assignments', 'Assignment', 3), # labels for hidden elements
    #('admin/backup', 'xxx', 1),
    ('admin/practice', 'Choose when students should start', 1),
    #('admin/removeassign', 'Cannot remove assignment with id of', 1),
    #('admin/removeinstructor', 'xxx', 1),
    #('admin/removeStudents', 'xxx', 1),
    # TODO: added to the ``createAssignment`` endpoint so far.
])
def test_validate_instructor_pages(url, expected_string, expected_errors,
                                   test_client, test_user, test_user_1):
    test_instructor_1 = test_user('test_instructor_1', 'password_1',
                                  test_user_1.course)
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
def test_preview_question(test_client, test_user_1):
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
def test_user_profile(test_client, test_user_1):
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
def test_registration(test_client, runestone_db_tools):
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
def test_pricing(runestone_db_tools, runestone_env):
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
    test_user_1 = test_user('test_user_1', 'password_1', course_1, is_free=True)
    # Verify the user was added to the ``user_courses`` table.
    assert db(( db.user_courses.course_id == test_user_1.course.course_id) & (db.user_courses.user_id == test_user_1.user_id) ).select().first()

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
    test_user_1 = test_user('test_user_1', 'password_1', course_1,
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
def test_payments(runestone_controller, runestone_db_tools, test_user):
    if not runestone_controller.settings.STRIPE_SECRET_KEY:
        pytest.skip('No Stripe keys provided.')

    db = runestone_db_tools.db
    course_1 = runestone_db_tools.create_course(student_price=100)
    test_user_1 = test_user('test_user_1', 'password_1', course_1,
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
def test_lp(test_user_1):
    test_user_1.login()

    # Check that omitting parameters produces an error.
    ret = test_user_1.hsblog(event='lp_build')
    assert 'No feedback provided' in ret['errors'][0]

    # Check that database entries are validated.
    ret = test_user_1.hsblog(
        event='lp_build',
        # This div_id is too long. Everything else is OK.
        div_id='X'*1000,
        course=test_user_1.course.course_name,
        builder='unsafe-python',
        answer=json.dumps({"code_snippets": ["def one(): return 1"]}),
    )
    assert 'div_id' in ret['errors'][0]

    # Check a passing case
    def assert_passing():
        ret = test_user_1.hsblog(
            event='lp_build',
            div_id='lp_demo_1',
            course=test_user_1.course.course_name,
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
def test_dynamic_book_routing_1(test_client, test_user_1):
    test_user_1.login()
    dbr_tester(test_client, test_user_1, True)

    # Test that a draft is accessible only to instructors.
    test_user_1.make_instructor()
    test_user_1.update_profile(course_name=test_user_1.course.course_name)
    test_client.validate('books/draft/{}/index.html'.format(test_user_1.course.base_course),
                         'The red car drove away.')


# Test the no-login case.
def test_dynamic_book_routing_2(test_client, test_user_1):
    test_client.logout()
    # Test for a book that doesn't require a login. First, change the book to not require a login.
    db = test_user_1.runestone_db_tools.db
    db(db.courses.id == test_user_1.course.course_id).update(login_required=False)
    db.commit()

    dbr_tester(test_client, test_user_1, False)


def dbr_tester(test_client, test_user_1, is_logged_in):
    # Test error cases.
    validate = test_client.validate
    base_course = test_user_1.course.base_course
    # A non-existant course.
    if is_logged_in:
        validate('books/published/xxx', 'Course Selection')
    else:
        validate('books/published/xxx', expected_status=404)
    # A non-existant page.
    validate('books/published/{}/xxx'.format(base_course),
             expected_status=404)
    # A directory.
    validate('books/published/{}/test_chapter_1'.format(base_course),
             expected_status=404)
    # Attempt to access files outside a course.
    validate('books/published/{}/../conf.py'.format(base_course),
             expected_status=404)
    # Attempt to access a course we're not registered for.
    if is_logged_in:
        runestone_db_tools = test_user_1.runestone_db_tools
        child_course = runestone_db_tools.create_course('child_course_1', base_course=test_user_1.course.base_course)
        validate('books/published/{}/index.html'.format(child_course.course_name), [
            # TODO: this flashed message doesn't appear. ???
            #'Sorry you are not registered for this course.',
            'Choose your course',
        ])

    # A valid page. Check the book config as well.
    validate('books/published/{}/index.html'.format(base_course), [
        'The red car drove away.',
        "eBookConfig.course = '{}';".format(base_course),
        "eBookConfig.basecourse = '{}';".format(base_course),
    ])
    # Drafts shouldn't be accessible by students.
    validate('books/draft/{}/index.html'.format(base_course),
             'Insufficient privileges' if is_logged_in else 'Username')

    # Check routing in a child book.
    if is_logged_in:
        test_user_1.update_profile(course_name=child_course.course_name,
                                   is_free=True)
        validate('books/published/{}/index.html'.format(base_course), [
            'The red car drove away.',
            "eBookConfig.course = '{}';".format(child_course.course_name),
            "eBookConfig.basecourse = '{}';".format(base_course),
        ])

    # Test static content.
    validate('books/published/{}/_static/runestone-custom-sphinx-bootstrap.css'.format(base_course),
             'background-color: #fafafa;')


def test_assignments(test_client, runestone_db_tools, test_user):
    course_3 = runestone_db_tools.create_course('test_course_3')
    test_instructor_1 = test_user('test_instructor_1', 'password_1', course_3)
    test_instructor_1.make_instructor()
    test_instructor_1.login()
    db = runestone_db_tools.db
    name_1 = 'test_assignment_1'
    name_2 = 'test_assignment_2'
    name_3 = 'test_assignment_3'
    
    # Create an assignment -- using createAssignment
    test_client.post('admin/createAssignment',
        data=dict(name=name_1))

    assign1 = db(
        (db.assignments.name == name_1) &
        (db.assignments.course == test_instructor_1.course.course_id)
    ).select().first()
    assert assign1

    # Make sure you can't create two assignments with the same name
    test_client.post('admin/createAssignment',
                     data=dict(name=name_1))
    assert "EXISTS" in test_client.text

    # Rename assignment
    test_client.post('admin/createAssignment',
                     data=dict(name=name_2))
    assign2 = db(
        (db.assignments.name == name_2) &
        (db.assignments.course == test_instructor_1.course.course_id)
    ).select().first()
    assert assign2
    
    test_client.post('admin/renameAssignment',
                     data=dict(name=name_3,original=assign2.id))
    assert db(db.assignments.name == name_3).select().first()
    assert not db(db.assignments.name == name_2).select().first()

    # Make sure you can't rename an assignment to an already used assignment
    test_client.post('admin/renameAssignment',
                     data=dict(name=name_3,original=assign1.id))
    assert "EXISTS" in test_client.text
    
    # Delete an assignment -- using removeassignment
    test_client.post('admin/removeassign', data=dict(assignid=assign1.id))
    assert not db(db.assignments.name == name_1).select().first()
    test_client.post('admin/removeassign', data=dict(assignid=assign2.id))
    assert not db(db.assignments.name == name_3).select().first()
    
    test_client.post('admin/removeassign', data=dict(assignid=9999999))
    assert "Error" in test_client.text


def test_deleteaccount(test_client, runestone_db_tools, test_user):
    course_3 = runestone_db_tools.create_course('test_course_3')
    the_user = test_user('user_to_delete', 'password_1', course_3)
    the_user.login()
    validate = the_user.test_client.validate
    the_user.hsblog(event="mChoice",
            act="answer:1:correct",answer="1",correct="T",div_id="subc_b_1",
            course="test_course_3")
    validate('default/delete', 'About Runestone', data=dict(deleteaccount='checked'))
    db = runestone_db_tools.db
    res = db(db.auth_user.username == 'user_to_delete').select().first()
    print(res)
    assert not db(db.useinfo.sid == 'user_to_delete').select().first()
    assert not db(db.code.sid == 'user_to_delete').select().first()
    assert not db(db.acerror_log.sid == 'user_to_delete').select().first()
    for t in ['clickablearea','codelens','dragndrop','fitb','lp','mchoice','parsons','shortanswer']:
        assert not db(db['{}_answers'.format(t)].sid == 'user_to_delete').select().first()

def test_pageprogress(test_client, runestone_db_tools, test_user_1):
    test_user_1.login()
    test_user_1.hsblog(event="mChoice",
            act="answer:1:correct",answer="1",correct="T",div_id="subc_b_1",
            course="test_course_1")
    # Since the user has answered the question the count for subc_b_1 should be 1
    # cannot test the totals on the client without javascript but that is covered in the
    # selenium tests on the components side.
    test_user_1.test_client.validate('books/published/test_course_1/test_chapter_1/subchapter_b.html',
        '"subc_b_1": 1')
    assert '"LearningZone_poll": 0' in test_user_1.test_client.text
    assert '"subc_b_fitb": 0' in test_user_1.test_client.text
