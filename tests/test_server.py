# <p>***************************************** |docname| - Tests using the
#     web2py server ***************************************** These tests start
#     the web2py server then submit requests to it. All the fixtures are
#     auto-imported by pytest from ``conftest.py``. .. contents:: Imports
#     ======= These are listed in the order prescribed by `PEP 8 `_. Standard
#     library ----------------</p>
from textwrap import dedent
import json
from threading import Thread
import datetime
import re
import sys
import time

# <p>Third-party imports -------------------</p>
import pytest
import six

# <p>Local imports -------------</p>
from utils import web2py_controller_import


# <p>Debugging notes =============== Invoke the debugger.</p>
import pdb; pdb.set_trace()
# <p>Put this in web2py code, then use the web-based debugger.</p>
from gluon.debug import dbg; dbg.set_trace()
# <p>This link will hopefully be of assistance to
#     https://web2py.readthedocs.io/en/latest/_modules/gluon/debug.html</p>

# <p>Tests ===== Use for easy manual te<a
#         href="https://web2py.readthedocs.io/en/latest/_modules/gluon/debug.html">https://web2py.readthedocs.io/en/latest/_modules/gluon/debug.html</a>sting
#     of the server, by setting up a user and class automatically. Comment out
#     the line below to enable it.</p>
#@pytest.mark.skip(reason="Only needed for manual testing.")
def test_manual(runestone_db_tools, test_user):
    # <p>Modify this as desired to create courses, users, etc. for manual
    #     testing.</p>
    course_1 = runestone_db_tools.create_course()
    test_user("bob", "bob", course_1)

    # <p>Pause in the debugger until manual testing is done.</p>
    import pdb

    pdb.set_trace()


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
    with pytest.raises(Exception) as excinfo:
        test_client.post("admin/killer")
        assert test_client.text == ""
    print(excinfo.value)
    assert "ticket" in str(excinfo.value) or "INTERNAL" in str(excinfo.value)


# <p>Validate the HTML produced by various web2py pages. NOTE -- this is the
#     start of a really really long decorator for test_1</p>
@pytest.mark.parametrize(
    "url, requires_login, expected_string, expected_errors",
    [
        # <p>**Admin** ---------- FIXME: Flashed messages don't seem to work.
        #     ('admin/index', False, 'You must be registered for a course to
        #     access this page', 1), ('admin/index', True, 'You must be an
        #     instructor to access this page', 1),</p>
        ("admin/doc", True, "Runestone Help and Documentation", 1),
        # <p>**Assignments** ----------------</p>
        ("assignments/chooseAssignment", True, "Assignments", 2),
        ("assignments/doAssignment", True, "Bad Assignment ID", 2),
        ("assignments/practice", True, "Practice", 1),
        ("assignments/practiceNotStartedYet", True, "test_course_1", 1),
        # <p>**Default** ------------ *User* The `authentication `_ section
        #     gives the URLs exposed by web2py. Check these.</p>
        ("default/user/login", False, "Login", 1),
        ("default/user/register", False, "Registration", 1),
        ("default/user/logout", True, "Logged out", 1),
        # <p>One validation error is a result of removing the input field for
        #     the e-mail, but web2py still tries to label it, which is an error.
        # </p>
        ("default/user/profile", True, "Profile", 2),
        ("default/user/change_password", True, "Change password", 1),
        # <p>Runestone doesn't support this.</p>
        #'default/user/verify_email', False, 'Verify email', 1),
        ("default/user/retrieve_username", False, "Our Mission", 1),
        ("default/user/request_reset_password", False, "Request reset password", 1),
        # <p>This doesn't display a webpage, but instead redirects to courses.
        #     ('default/user/reset_password, False, 'Reset password', 1),
        #     ("default/user/impersonate", True, "Impersonate", 1), FIXME: This
        #     produces an exception.</p>
        #'default/user/groups', True, 'Groups', 1),
        ("default/user/not_authorized", False, "Our Mission", 1),
        # <p>*Other pages* TODO: What is this for? ('default/call', False, 'Not
        #     found', 0),</p>
        ("default/index", True, "Course Selection", 1),
        ("default/about", False, "About Runestone", 1),
        ("default/error", False, "Error: the document does not exist", 1),
        ("default/ack", False, "Acknowledgements", 1),
        # <p>web2py generates invalid labels for the radio buttons in this form.
        # </p>
        ("default/bio", True, "Tell Us About Yourself", 3),
        ("default/courses", True, "Course Selection", 1),
        ("default/remove", True, "Remove a Course", 1),
        # <p>Should work in both cases.</p>
        ("default/reportabug", False, "Report a Bug", 1),
        ("default/reportabug", True, "Report a Bug", 1),
        # <p>('default/sendreport', True, 'Could not create issue', 1),</p>
        ("default/terms", False, "Terms and Conditions", 1),
        ("default/privacy", False, "Runestone Academy Privacy Policy", 1),
        ("default/donate", False, "Support Runestone Academy", 1),
        # <p>TODO: This doesn't really test much of the body of either of these.
        # </p>
        ("default/coursechooser", True, "Course Selection", 1),
        # <p>If we choose an invalid course, then we go to the profile to allow
        #     the user to add that course. The second validation failure seems
        #     to be about the ``for`` attribute of the ```<label
        #         id="auth_user_email__label" class="readonly"
        #         for="auth_user_email">`` tag, since the id ``auth_user_email``
        #         isn't defined elsewhere.</label></p>
        ("default/coursechooser/xxx", True, "Course IDs for open courses", 2),
        ("default/removecourse", True, "Course Selection", 1),
        ("default/removecourse/xxx", True, "Course Selection", 1),
        (
            "dashboard/studentreport",
            True,
            "Recent Activity",
            1,
        ),
        # <p>**Designer** -------------</p>
        (
            "designer/index",
            True,
            "This page allows you to select a book for your own class.",
            1,
        ),
        ("designer/build", True, "Build a Custom", 1),
        # <p>**OAuth** ----------</p>
        (
            "oauth/index",
            False,
            "This page is a utility for accepting redirects from external services like Spotify or LinkedIn that use oauth.",
            1,
        ),
        # <p>TODO: Many other views!</p>
    ],
)
def test_validate_user_pages(
    url, requires_login, expected_string, expected_errors, test_client, test_user_1
):
    if requires_login:
        test_user_1.login()
    else:
        test_client.logout()
    test_client.validate(url, expected_string, expected_errors)


# <p>Validate the HTML in instructor-only pages. NOTE -- this is the start of a
#     really really long decorator for test_2</p>
@pytest.mark.parametrize(
    "url, expected_string, expected_errors",
    [
        # <p>**Default** ------------ web2py-generated stuff produces two extra
        #     errors.</p>
        ("default/bios", "Bios", 3),
        # <p>FIXME: The element ``</p>
        # <form id="editIndexRST" action="">`` in ``views/admin/admin.html``
        #     produces the error ``Bad value \u201c\u201d for attribute
        #     \u201caction\u201d on element \u201cform\u201d: Must be
        #     non-empty.``. **Admin** ----------</form>
        ("admin/admin", "Course Settings", 1),
        # <p>This endpoint produces JSON, so don't check it.</p>
        ##("admin/course_students", '"test_user_1"', 2),
        ("admin/createAssignment", "ERROR", None),
        ("admin/grading", "assignment", 1),
        # <p>TODO: This produces an exception. ('admin/practice', 'Choose when
        #     students should start their practice.', 1), TODO: This deletes the
        #     course, making the test framework raise an exception. Need a
        #     separate case to catch this. ('admin/deletecourse', 'Manage
        #     Section', 2), FIXME: these raise an exception.
        #     ('admin/addinstructor', 'Trying to add non-user', 1), -- this is
        #     an api call ('admin/add_practice_items', 'xxx', 1), -- this is an
        #     api call</p>
        ("admin/assignments", "Assignment", 6),  # labels for hidden elements
        # <p>('admin/backup', 'xxx', 1),</p>
        ("admin/practice", "Choose when students should start", 1),
        # <p>('admin/removeassign', 'Cannot remove assignment with id of', 1),
        #     ('admin/removeinstructor', 'xxx', 1), ('admin/removeStudents',
        #     'xxx', 1),</p>
        ("admin/get_assignment", "Error: assignment ID", 1),
        ("admin/get_assignment?assignmentid=junk", "Error: assignment ID", 1),
        ("admin/get_assignment?assignmentid=100", "Error: assignment ID", 1),
        # <p>TODO: added to the ``createAssignment`` endpoint so far.
        #     **Dashboard** --------------</p>
        ("dashboard/index", "Instructor Dashboard", 1),
        ("dashboard/grades", "Gradebook", 1),
        # <p>TODO: This doesn't really test anything about either
        #     exercisemetrics or questiongrades other than properly handling a
        #     call with no information</p>
        ("dashboard/exercisemetrics", "Instructor Dashboard", 1),
        ("dashboard/questiongrades", "Instructor Dashboard", 1),
    ],
)
def test_validate_instructor_pages(
    url, expected_string, expected_errors, test_client, test_user, test_user_1
):
    test_instructor_1 = test_user("test_instructor_1", "password_1", test_user_1.course)
    test_instructor_1.make_instructor()
    # <p>Make sure that non-instructors are redirected.</p>
    test_client.logout()
    test_client.validate(url, "Login")
    test_user_1.login()
    test_client.validate(url, "Insufficient privileges")
    test_client.logout()

    # <p>Test the instructor results.</p>
    test_instructor_1.login()
    test_client.validate(url, expected_string, expected_errors)


# <p>Test the ``ajax/preview_question`` endpoint.</p>
def test_preview_question(test_client, test_user_1):
    preview_question = "ajax/preview_question"
    # <p>Passing no parameters should raise an error.</p>
    test_client.validate(preview_question, "Error: ")
    # <p>Passing something not JSON-encoded should raise an error.</p>
    test_client.validate(preview_question, "Error: ", data={"code": "xxx"})
    # <p>Passing invalid RST should produce a Sphinx warning.</p>
    test_client.validate(preview_question, "WARNING", data={"code": '"*hi"'})
    # <p>Passing valid RST with no Runestone component should produce an error.
    # </p>
    test_client.validate(preview_question, "Error: ", data={"code": '"*hi*"'})
    # <p>Passing a string with Unicode should work. Note that 0x0263 == 611; the
    #     JSON-encoded result will use this.</p>
    test_client.validate(
        preview_question,
        r"\u03c0",
        data={
            "code": json.dumps(
                dedent(
                    """\
        .. fillintheblank:: question_1

            Mary had a π.

            -   :x: Whatever.
    """
                )
            )
        },
    )
    # <p>Verify that ``question_1`` is not in the database. TODO: This passes
    #     even if the ``DBURL`` env variable in ``ajax.py`` fucntion
    #     ``preview_question`` isn't deleted. So, this test doesn't work.</p>
    db = test_user_1.runestone_db_tools.db
    assert len(db(db.fitb_answers.div_id == "question_1").select()) == 0
    # <p>TODO: Add a test case for when the runestone build produces a non-zero
    #     return code.</p>


# <p>Test the ``default/user/profile`` endpoint.</p>
def test_user_profile(test_client, test_user_1):
    test_user_1.login()
    runestone_db_tools = test_user_1.runestone_db_tools
    course_name = "test_course_2"
    test_course_2 = runestone_db_tools.create_course(course_name)
    # <p>Test a non-existant course.</p>
    test_user_1.update_profile(
        expected_string="Errors in form", course_name="does_not_exist"
    )

    # <p>Test an invalid e-mail address. TODO: This doesn't produce an error
    #     message.</p>
    ##test_user_1.update_profile(expected_string='Errors in form',
    ##                           email='not a valid e-mail address')

    # <p>Change the user's profile data; add a new course.</p>
    username = "a_different_username"
    first_name = "a different first"
    last_name = "a different last"
    email = "a_different_email@foo.com"
    test_user_1.update_profile(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        course_name=course_name,
        accept_tcp="",
        is_free=True,
    )

    # <p>Check the values.</p>
    db = runestone_db_tools.db
    user = db(db.auth_user.id == test_user_1.user_id).select().first()
    # <p>The username shouldn't be changable.</p>
    assert user.username == test_user_1.username
    assert user.first_name == first_name
    assert user.last_name == last_name
    # <p>TODO: The e-mail address isn't updated. assert user.email == email</p>
    assert user.course_id == test_course_2.course_id
    assert user.accept_tcp == False  # noqa: E712
    # <p>TODO: I'm not sure where the section is stored. assert user.section ==
    #     section</p>


# <p>Test that the course name is correctly preserved across registrations if
#     other fields are invalid.</p>
def test_registration(test_client, runestone_db_tools):
    # <p>Registration doesn't work unless we're logged out.</p>
    test_client.logout()
    course_name = "a_course_name"
    runestone_db_tools.create_course(course_name)
    # <p>Now, post the registration.</p>
    username = "username"
    first_name = "first"
    last_name = "last"
    email = "e@mail.com"
    password = "password"
    test_client.validate(
        "default/user/register",
        "Please fix the following errors in your registration",
        data=dict(
            username=username,
            first_name=first_name,
            last_name=last_name,
            # <p>The e-mail address must be unique.</p>
            email=email,
            password=password,
            password_two=password + "oops",
            # <p>Note that ``course_id`` is (on the form) actually a course
            #     name.</p>
            course_id=course_name,
            accept_tcp="on",
            donate="0",
            _next="/runestone/default/index",
            _formname="register",
        ),
    )


# <p>Check that the pricing system works correctly.</p>
def test_pricing(runestone_db_tools, runestone_env):
    # <p>Check the pricing.</p>
    default_controller = web2py_controller_import(runestone_env, "default")
    db = runestone_db_tools.db

    # <p>These course names rely on defaults in the ``runestone_db_tools``
    #     fixture.</p>
    base_course = runestone_db_tools.create_course("test_course_1")
    child_course_1 = runestone_db_tools.create_course()
    # <p>It would be nice to use the ``test_user`` fixture, but we're not using
    #     the web interface here -- it's direct database access instead. This is
    #     an alternative.</p>
    runestone_env["auth"].get_or_create_user(
        dict(
            username="test_user_1",
            course_id=child_course_1.course_id,
            course_name=child_course_1.course_name,
            # <p>Provide a non-null value for these required fields.</p>
            first_name="",
            last_name="",
            email="",
            password="",
            created_on="01-01-2000",
            modified_on="01-01-2000",
            registration_key="",
            reset_password_key="",
            registration_id="",
            active="T",
            donated="F",
            accept_tcp="T",
        )
    )

    # <p>First, test on a base course.</p>
    for expected_price, actual_price in [(0, None), (0, -100), (0, 0), (15, 15)]:
        db(db.courses.id == base_course.course_id).update(student_price=actual_price)
        assert default_controller._course_price(base_course.course_id) == expected_price

    # <p>Test in a child course as well. Create a matrix of all base course
    #     prices by all child course prices.</p>
    for expected_price, actual_base_price, actual_child_price in [
        (0, None, None),
        (0, None, 0),
        (0, None, -1),
        (2, None, 2),
        (0, 0, None),
        (0, 0, 0),
        (0, 0, -1),
        (2, 0, 2),
        (0, -2, None),
        (0, -2, 0),
        (0, -2, -1),
        (2, -2, 2),
        (3, 3, None),
        (0, 3, 0),
        (0, 3, -1),
        (2, 3, 2),
    ]:

        db(db.courses.id == base_course.course_id).update(
            student_price=actual_base_price
        )
        db(db.courses.id == child_course_1.course_id).update(
            student_price=actual_child_price
        )
        assert (
            default_controller._course_price(child_course_1.course_id) == expected_price
        )

    # <p>Make sure the book is free if the student already owns the base course.
    #     First, create another child course and add the current student to it.
    # </p>
    child_course_2 = runestone_db_tools.create_course("test_child_course_2")
    db.user_courses.insert(
        user_id=runestone_env["auth"].user.id, course_id=child_course_2.course_id
    )
    # <p>Now check the price of a different child course of the same base
    #     course.</p>
    assert default_controller._course_price(child_course_1.course_id) == 0


# <p>Check that setting the price causes redirects to the correct location
#     (payment vs. donation) when registering for a course or adding a new
#     course.</p>
def test_price_free(runestone_db_tools, test_user):
    db = runestone_db_tools.db
    course_1 = runestone_db_tools.create_course(student_price=0)
    course_2 = runestone_db_tools.create_course("test_course_2", student_price=0)

    # <p>Check registering for a free course.</p>
    test_user_1 = test_user("test_user_1", "password_1", course_1, is_free=True)
    # <p>Verify the user was added to the ``user_courses`` table.</p>
    assert (
        db(
            (db.user_courses.course_id == test_user_1.course.course_id)
            & (db.user_courses.user_id == test_user_1.user_id)
        )
        .select()
        .first()
    )

    # <p>Check adding a free course.</p>
    test_user_1.update_profile(course_name=course_2.course_name, is_free=True)
    # <p>Same as above.</p>
    assert (
        db(
            (db.user_courses.course_id == course_2.course_id)
            & (db.user_courses.user_id == test_user_1.user_id)
        )
        .select()
        .first()
    )


def test_price_paid(runestone_db_tools, test_user):
    db = runestone_db_tools.db
    # <p>Check registering for a paid course.</p>
    course_1 = runestone_db_tools.create_course(student_price=1)
    course_2 = runestone_db_tools.create_course("test_course_2", student_price=1)
    # <p>Check registering for a paid course.</p>
    test_user_1 = test_user("test_user_1", "password_1", course_1, is_free=False)

    # <p>Until payment is provided, the user shouldn't be added to the
    #     ``user_courses`` table. Ensure that refresh, login/logout, profile
    #     changes, adding another class, etc. don't allow access.</p>
    test_user_1.test_client.logout()
    test_user_1.login()
    test_user_1.test_client.validate("default/index")

    # <p>Check adding a paid course.</p>
    test_user_1.update_profile(course_name=course_2.course_name, is_free=False)

    # <p>Verify no access without payment.</p>
    assert (
        not db(
            (db.user_courses.course_id == course_1.course_id)
            & (db.user_courses.user_id == test_user_1.user_id)
        )
        .select()
        .first()
    )
    assert (
        not db(
            (db.user_courses.course_id == course_2.course_id)
            & (db.user_courses.user_id == test_user_1.user_id)
        )
        .select()
        .first()
    )


# <p>Check that payments are handled correctly.</p>
def test_payments(runestone_controller, runestone_db_tools, test_user):
    if not runestone_controller.settings.STRIPE_SECRET_KEY:
        pytest.skip("No Stripe keys provided.")

    db = runestone_db_tools.db
    course_1 = runestone_db_tools.create_course(student_price=100)
    test_user_1 = test_user("test_user_1", "password_1", course_1, is_free=False)

    def did_payment():
        return (
            db(
                (db.user_courses.course_id == course_1.course_id)
                & (db.user_courses.user_id == test_user_1.user_id)
            )
            .select()
            .first()
        )

    # <p>Test some failing tokens.</p>
    assert not did_payment()
    for token in ["tok_chargeCustomerFail", "tok_chargeDeclined"]:
        test_user_1.make_payment(token)
        assert not did_payment()

    test_user_1.make_payment("tok_visa")
    assert did_payment()
    # <p>Check that the payment record is correct.</p>
    payment = (
        db(
            (db.user_courses.user_id == test_user_1.user_id)
            & (db.user_courses.course_id == course_1.course_id)
            & (db.user_courses.id == db.payments.user_courses_id)
        )
        .select(db.payments.charge_id)
        .first()
    )
    assert payment.charge_id


# <p>Test dynamic book routing.</p>
@pytest.mark.skip(
    reason="Can't render new BookServer template using old server. TODO: Port to the BookServer."
)
def test_dynamic_book_routing_1(test_client, test_user_1):
    test_user_1.login()
    dbr_tester(test_client, test_user_1, True)

    # <p>Test that a draft is accessible only to instructors.</p>
    test_user_1.make_instructor()
    test_user_1.update_profile(course_name=test_user_1.course.course_name)
    test_client.validate(
        "books/draft/{}/index.html".format(test_user_1.course.base_course),
        "The red car drove away.",
    )


# <p>Test the no-login case.</p>
@pytest.mark.skip(
    reason="Can't render new BookServer template using old server. TODO: Port to the BookServer."
)
def test_dynamic_book_routing_2(test_client, test_user_1):
    test_client.logout()
    # <p>Test for a book that doesn't require a login. First, change the book to
    #     not require a login.</p>
    db = test_user_1.runestone_db_tools.db
    db(db.courses.course_name == test_user_1.course.base_course).update(
        login_required=False
    )
    db.commit()

    dbr_tester(test_client, test_user_1, False)


def dbr_tester(test_client, test_user_1, is_logged_in):
    # <p>Test error cases.</p>
    validate = test_client.validate
    base_course = test_user_1.course.base_course
    # <p>A non-existant course.</p>
    if is_logged_in:
        validate("books/published/xxx", "Course Selection")
    else:
        validate("books/published/xxx", expected_status=404)
    # <p>A non-existant page.</p>
    validate("books/published/{}/xxx".format(base_course), expected_status=404)
    # <p>A directory.</p>
    validate(
        "books/published/{}/test_chapter_1".format(base_course), expected_status=404
    )
    # <p>Attempt to access files outside a course.</p>
    validate("books/published/{}/../conf.py".format(base_course), expected_status=404)
    # <p>Attempt to access a course we're not registered for. TODO: Need to
    #     create another base course for this to work.</p>
    ##if is_logged_in:
    ##    #validate('books/published/{}/index.html'.format(base_course), [
    ##        'Sorry you are not registered for this course.'
    ##    ])

    # <p>A valid page. Check the book config as well.</p>
    validate(
        "books/published/{}/index.html".format(base_course),
        [
            "The red car drove away.",
            "eBookConfig.course = '{}';".format(
                test_user_1.course.course_name if is_logged_in else base_course
            ),
            "eBookConfig.basecourse = '{}';".format(base_course),
        ],
    )
    # <p>Drafts shouldn't be accessible by students.</p>
    validate(
        "books/draft/{}/index.html".format(base_course),
        "Insufficient privileges" if is_logged_in else "Username",
    )

    # <p>Check routing in a base course.</p>
    if is_logged_in:
        test_user_1.update_profile(
            course_name=test_user_1.course.base_course, is_free=True
        )
        validate(
            "books/published/{}/index.html".format(base_course),
            [
                "The red car drove away.",
                "eBookConfig.course = '{}';".format(base_course),
                "eBookConfig.basecourse = '{}';".format(base_course),
            ],
        )

    # <p>Test static content.</p>
    validate(
        "books/published/{}/_static/basic.css".format(base_course),
        "Sphinx stylesheet -- basic theme.",
    )


def test_assignments(test_client, runestone_db_tools, test_user):
    course_3 = runestone_db_tools.create_course("test_course_3")
    test_instructor_1 = test_user("test_instructor_1", "password_1", course_3)
    test_instructor_1.make_instructor()
    test_instructor_1.login()
    db = runestone_db_tools.db
    name_1 = "test_assignment_1"
    name_2 = "test_assignment_2"
    name_3 = "test_assignment_3"

    # <p>Create an assignment -- using createAssignment</p>
    test_client.post("admin/createAssignment", data=dict(name=name_1))

    assign1 = (
        db(
            (db.assignments.name == name_1)
            & (db.assignments.course == test_instructor_1.course.course_id)
        )
        .select()
        .first()
    )
    assert assign1

    # <p>Make sure you can't create two assignments with the same name</p>
    test_client.post("admin/createAssignment", data=dict(name=name_1))
    assert "EXISTS" in test_client.text

    # <p>Rename assignment</p>
    test_client.post("admin/createAssignment", data=dict(name=name_2))
    assign2 = (
        db(
            (db.assignments.name == name_2)
            & (db.assignments.course == test_instructor_1.course.course_id)
        )
        .select()
        .first()
    )
    assert assign2

    test_client.post(
        "admin/renameAssignment", data=dict(name=name_3, original=assign2.id)
    )
    assert db(db.assignments.name == name_3).select().first()
    assert not db(db.assignments.name == name_2).select().first()

    # <p>Make sure you can't rename an assignment to an already used assignment
    # </p>
    test_client.post(
        "admin/renameAssignment", data=dict(name=name_3, original=assign1.id)
    )
    assert "EXISTS" in test_client.text

    # <p>Delete an assignment -- using removeassignment</p>
    test_client.post("admin/removeassign", data=dict(assignid=assign1.id))
    assert not db(db.assignments.name == name_1).select().first()
    test_client.post("admin/removeassign", data=dict(assignid=assign2.id))
    assert not db(db.assignments.name == name_3).select().first()

    test_client.post("admin/removeassign", data=dict(assignid=9999999))
    assert "Error" in test_client.text


def test_instructor_practice_admin(test_client, runestone_db_tools, test_user):
    course_4 = runestone_db_tools.create_course("test_course_1")
    test_student_1 = test_user("test_student_1", "password_1", course_4)
    test_student_1.logout()
    test_instructor_1 = test_user("test_instructor_1", "password_1", course_4)
    test_instructor_1.make_instructor()
    test_instructor_1.login()
    db = runestone_db_tools.db

    course_start_date = datetime.datetime.strptime(
        course_4.term_start_date, "%Y-%m-%d"
    ).date()

    start_date = course_start_date + datetime.timedelta(days=13)
    end_date = datetime.datetime.today().date() + datetime.timedelta(days=30)
    max_practice_days = 40
    max_practice_questions = 400
    day_points = 1
    question_points = 0.2
    questions_to_complete_day = 5
    graded = 0

    # <p>Test the practice tool settings for the course.</p>
    flashcard_creation_method = 2
    test_client.post(
        "admin/practice",
        data={
            "StartDate": start_date,
            "EndDate": end_date,
            "graded": graded,
            "maxPracticeDays": max_practice_days,
            "maxPracticeQuestions": max_practice_questions,
            "pointsPerDay": day_points,
            "pointsPerQuestion": question_points,
            "questionsPerDay": questions_to_complete_day,
            "flashcardsCreationType": 2,
            "question_points": question_points,
        },
    )

    practice_settings_1 = (
        db(
            (db.course_practice.auth_user_id == test_instructor_1.user_id)
            & (db.course_practice.course_name == course_4.course_name)
            & (db.course_practice.start_date == start_date)
            & (db.course_practice.end_date == end_date)
            & (
                db.course_practice.flashcard_creation_method
                == flashcard_creation_method
            )
            & (db.course_practice.graded == graded)
        )
        .select()
        .first()
    )
    assert practice_settings_1
    if practice_settings_1.spacing == 1:
        assert practice_settings_1.max_practice_days == max_practice_days
        assert practice_settings_1.day_points == day_points
        assert (
            practice_settings_1.questions_to_complete_day == questions_to_complete_day
        )
    else:
        assert practice_settings_1.max_practice_questions == max_practice_questions
        assert practice_settings_1.question_points == question_points

    # <p>Test instructor adding a subchapter to the practice tool for students.
    # </p>

    # <p>I need to call set_tz_offset to set timezoneoffset in the session.</p>
    test_client.post("ajax/set_tz_offset", data={"timezoneoffset": 0})

    # <p>The reason I'm manually stringifying the list value is that
    #     test_client.post does something strange with compound objects instead
    #     of passing them to json.dumps.</p>
    test_client.post(
        "admin/add_practice_items",
        data={"data": '["1. Test chapter 1/1.2 Subchapter B"]'},
    )

    practice_settings_1 = (
        db(
            (db.user_topic_practice.user_id == test_student_1.user_id)
            & (db.user_topic_practice.course_name == course_4.course_name)
            & (db.user_topic_practice.chapter_label == "test_chapter_1")
            & (db.user_topic_practice.sub_chapter_label == "subchapter_b")
        )
        .select()
        .first()
    )
    assert practice_settings_1


@pytest.mark.skip(reason="Requires BookServer for testing -- TODO")
def test_deleteaccount(test_client, runestone_db_tools, test_user):
    course_3 = runestone_db_tools.create_course("test_course_3")
    the_user = test_user("user_to_delete", "password_1", course_3)
    the_user.login()
    validate = the_user.test_client.validate
    the_user.hsblog(
        event="mChoice",
        act="answer:1:correct",
        answer="1",
        correct="T",
        div_id="subc_b_1",
        course="test_course_3",
    )
    validate("default/delete", "About Runestone", data=dict(deleteaccount="checked"))
    db = runestone_db_tools.db
    res = db(db.auth_user.username == "user_to_delete").select().first()
    print(res)
    time.sleep(2)
    assert not db(db.useinfo.sid == "user_to_delete").select().first()
    assert not db(db.code.sid == "user_to_delete").select().first()
    for t in [
        "clickablearea",
        "codelens",
        "dragndrop",
        "fitb",
        "lp",
        "mchoice",
        "parsons",
        "shortanswer",
    ]:
        assert (
            not db(db["{}_answers".format(t)].sid == "user_to_delete").select().first()
        )


# <p>Test the grades report. When this test fails it is very very difficult to
#     figure out why. The data structures being compared are very large which
#     makes it very very difficult to pin down what is failing. In addition it
#     seems there is a dictionary in here somewhere where the order of things
#     shifts around. I think it is currenly broken because more components now
#     return a percent correct value.</p>
@pytest.mark.skip(reason="TODO: This test is unpredictable and needs to be updated.")
def test_grades_1(runestone_db_tools, test_user, tmp_path):
    # <p>Create test users.</p>
    course = runestone_db_tools.create_course()
    course_name = course.course_name

    # <p>**Create test data** ====================== Create test users.</p>
    test_user_array = [
        test_user(
            "test_user_{}".format(index), "x", course, last_name="user_{}".format(index)
        )
        for index in range(4)
    ]

    def assert_passing(index, *args, **kwargs):
        res = test_user_array[index].hsblog(*args, **kwargs)
        assert "errors" not in res

    # <p>Prepare common arguments for each question type.</p>
    shortanswer_kwargs = dict(
        event="shortanswer", div_id="test_short_answer_1", course=course_name
    )
    fitb_kwargs = dict(event="fillb", div_id="test_fitb_1", course=course_name)
    mchoice_kwargs = dict(event="mChoice", div_id="test_mchoice_1", course=course_name)
    lp_kwargs = dict(
        event="lp_build",
        div_id="test_lp_1",
        course=course_name,
        builder="unsafe-python",
    )
    unittest_kwargs = dict(event="unittest", div_id="units2", course=course_name)

    # <p>*User 0*: no data supplied</p>
    ##----------------------------

    # <p>*User 1*: correct answers</p>
    ##---------------------------
    # <p>It doesn't matter which user logs out, since all three users share the
    #     same client.</p>
    logout = test_user_array[2].test_client.logout
    logout()
    test_user_array[1].login()
    assert_passing(1, act=test_user_array[1].username, **shortanswer_kwargs)
    assert_passing(1, answer=json.dumps(["red", "away"]), **fitb_kwargs)
    assert_passing(1, answer="0", correct="T", **mchoice_kwargs)
    assert_passing(
        1, answer=json.dumps({"code_snippets": ["def one(): return 1"]}), **lp_kwargs
    )
    assert_passing(1, act="percent:100:passed:2:failed:0", **unittest_kwargs)

    # <p>*User 2*: incorrect answers</p>
    ##----------------------------
    logout()
    test_user_array[2].login()
    # <p>Add three shortanswer answers, to make sure the number of attempts is
    #     correctly recorded.</p>
    for x in range(3):
        assert_passing(2, act=test_user_array[2].username, **shortanswer_kwargs)
    assert_passing(2, answer=json.dumps(["xxx", "xxxx"]), **fitb_kwargs)
    assert_passing(2, answer="1", correct="F", **mchoice_kwargs)
    assert_passing(
        2, answer=json.dumps({"code_snippets": ["def one(): return 2"]}), **lp_kwargs
    )
    assert_passing(2, act="percent:50:passed:1:failed:1", **unittest_kwargs)

    # <p>*User 3*: no data supplied, and no longer in course.</p>
    ##----------------------------------------------------
    # <p>Wait until the autograder is run to remove the student, so they will
    #     have a grade but not have any submissions.</p>

    # <p>**Test the grades_report endpoint**</p>
    ##====================================
    tu = test_user_array[2]

    def grades_report(assignment, *args, **kwargs):
        return tu.test_client.validate(
            "assignments/grades_report",
            *args,
            data=dict(chap_or_assign=assignment, report_type="assignment"),
            **kwargs
        )

    # <p>Test not being an instructor.</p>
    grades_report("", "About Runestone")
    tu.make_instructor()
    # <p>Test an invalid assignment.</p>
    grades_report("", "Unknown assignment")

    # <p>Create an assignment.</p>
    assignment_name = "test_assignment"
    assignment_id = json.loads(
        tu.test_client.validate(
            "admin/createAssignment", data={"name": assignment_name}
        )
    )[assignment_name]
    assignment_kwargs = dict(
        assignment=assignment_id, autograde="pct_correct", which_to_grade="first_answer"
    )

    # <p>Add questions to the assignment.</p>
    def add_to_assignment(question_kwargs, points):
        assert tu.test_client.validate(
            "admin/add__or_update_assignment_question",
            data=dict(
                question=question_kwargs["div_id"], points=points, **assignment_kwargs
            ),
        ) != json.dumps("Error")

    # <p>Determine the order of the questions and the _`point values`.</p>
    add_to_assignment(shortanswer_kwargs, 0)
    add_to_assignment(fitb_kwargs, 1)
    add_to_assignment(mchoice_kwargs, 2)
    add_to_assignment(lp_kwargs, 3)
    add_to_assignment(unittest_kwargs, 4)

    # <p>Autograde the assignment.</p>
    assignment_kwargs = dict(data={"assignment": assignment_name})
    assert json.loads(
        tu.test_client.validate("assignments/autograde", **assignment_kwargs)
    )["message"].startswith("autograded")
    assert json.loads(
        tu.test_client.validate("assignments/calculate_totals", **assignment_kwargs)
    )["success"]

    # <p>Remove test user 3 from the course. They can't be removed from the
    #     current course, so create a new one then add this user to it.</p>
    logout()
    tu = test_user_array[3]
    tu.login()
    new_course = runestone_db_tools.create_course("random_course_name")
    tu.update_profile(course_name=new_course.course_name, is_free=True)
    tu.coursechooser(new_course.course_name)
    tu.removecourse(course_name)

    # <p>**Test this assignment.** =========================== Log back in as
    #     the instructor.</p>
    logout()
    tu = test_user_array[2]
    tu.login()
    # <p>Now, we can get the report.</p>
    grades = json.loads(grades_report(assignment_name))

    # <p>Define a regex string comparison.</p>
    class RegexEquals:
        def __init__(self, regex):
            self.regex = re.compile(regex)

        def __eq__(self, other):
            return bool(re.search(self.regex, other))

    # <p>See if a date in ISO format followed by a "Z" is close to the current
    #     time.</p>
    class AlmostNow:
        def __eq__(self, other):
            # <p>Parse the date string. Assume it ends with a Z and discard
            #     this.</p>
            assert other and other[-1] == "Z"
            # <p>Per the `docs `_, this function requires Python 3.7+.</p>
            if sys.version_info >= (3, 7):
                dt = datetime.datetime.fromisoformat(other[:-1])
                return datetime.datetime.utcnow() - dt < datetime.timedelta(minutes=1)
            else:
                # <p>Hope for the best on older Python.</p>
                return True

    # <p>These are based on the data input for each user earlier in this test.
    # </p>
    expected_grades = {
        "colHeaders": [
            "userid",
            "Family name",
            "Given name",
            "e-mail",
            "avg grade (%)",
            "1",
            "1",
            "1",
            "2.1",
            "2",
        ],
        "data": [
            [
                "div_id",
                "",
                "",
                "",
                "",
                "test_short_answer_1",
                "test_fitb_1",
                "test_mchoice_1",
                "test_lp_1",
                "units2",
            ],
            [
                "location",
                "",
                "",
                "",
                "",
                "index - ",
                "index - ",
                "index - ",
                "lp_demo.py - ",
                "index - ",
            ],
            [
                "type",
                "",
                "",
                "",
                "",
                "shortanswer",
                "fillintheblank",
                "mchoice",
                "lp_build",
                "activecode",
            ],
            # <p>See the `point values`_ assigned earlier.</p>
            ["points", "", "", "", "", 0, 1, 2, 3, 4],
            ["avg grade (%)", "", "", "", ""],
            ["avg attempts", "", "", "", ""],
            ["test_user_0", "user_0", "test", "test_user_0@foo.com", 0.0],
            ["test_user_1", "user_1", "test", "test_user_1@foo.com", 1.0],
            ["test_user_2", "user_2", "test", "test_user_2@foo.com", 0.2],
            ["test_user_3", "user_3", "test", "test_user_3@foo.com", 0.0],
        ],
        # <p>Correct since the first 3 questions are all on the index page.</p>
        "mergeCells": [{"col": 5, "colspan": 3, "row": 1, "rowspan": 1}],
        "orig_data": [
            # <p>User 0: not submitted.</p>
            [
                # <p>The format is: ``[timestamp, score, answer, correct,
                #     num_attempts]``.</p>
                [None, 0.0, None, None, None],  # shortanswer
                [None, 0.0, None, None, None],  # fillintheblank
                [None, 0.0, None, None, None],  # mchoice
                [None, 0.0, {}, None, None],  # lp_build
                [None, 0.0, "", None, None],  # activecode
            ],
            # <p>User 1: all correct.</p>
            [
                [AlmostNow(), 0.0, "test_user_1", None, 1],
                [AlmostNow(), 1.0, ["red", "away"], True, 1],
                [AlmostNow(), 2.0, [0], True, 1],
                [
                    AlmostNow(),
                    3.0,
                    {"code_snippets": ["def one(): return 1"], "resultString": ""},
                    100.0,
                    1,
                ],
                [AlmostNow(), 4.0, "percent:100:passed:2:failed:0", True, 1],
            ],
            # <p>User 2: all incorrect.</p>
            [
                [AlmostNow(), 0.0, "test_user_2", None, 3],
                [AlmostNow(), 0.0, ["xxx", "xxxx"], False, 1],
                [AlmostNow(), 0.0, [1], False, 1],
                [
                    AlmostNow(),
                    0.0,
                    {
                        "code_snippets": ["def one(): return 2"],
                        "resultString": RegexEquals(
                            "Traceback \\(most recent call last\\):\n"
                            "  File "
                            # <p>Use a regex for the file's path.</p>
                            '"\\S*lp_demo-test.py", '
                            "line 6, in <module>\n"
                            "    assert one\\(\\) == 1\n"
                            "AssertionError"
                        ),
                    },
                    0.0,
                    1,
                ],
                [AlmostNow(), 2.0, "percent:50:passed:1:failed:1", False, 1],
            ],
            # <p>User 3: not submitted.</p>
            [
                # <p>The format is:</p>
                [None, 0.0, None, None, None],
                [None, 0.0, None, None, None],
                [None, 0.0, None, None, None],
                [None, 0.0, {}, None, None],
                [None, 0.0, "", None, None],
            ],
        ],
    }

    # <p>Note: on test failure, pytest will report as incorrect all the
    #     ``AlmostNow()`` and ``RegexEquals`` items, even though they may have
    #     actually compared as equal. assert grades == expected_grades lets
    #     break this up a bit.</p>
    for k in expected_grades:
        assert grades[k] == expected_grades[k]

    logout()
    # <p>Test with no login.</p>
    grades_report("", "About Runestone")


# <p>Test the teaming report.</p>
@pytest.mark.skip(
    reason="Can't render new BookServer template using old server. TODO: Port to the BookServer."
)
def test_team_1(runestone_db_tools, test_user, runestone_name):
    # <p>Create test users.</p>
    course = runestone_db_tools.create_course()
    course_name = course.course_name

    # <p>**Create test data** ===================== Create test users.</p>
    test_user_array = [
        test_user(
            "test_user_{}".format(index), "x", course, last_name="user_{}".format(index)
        )
        for index in range(3)
    ]

    def assert_passing(index, *args, **kwargs):
        res = test_user_array[index].hsblog(*args, **kwargs)
        assert "errors" not in res

    # <p>Prepare common arguments for each question type.</p>
    shortanswer1_kwargs = dict(
        event="shortanswer", div_id="team_eval_role_0", course=course_name
    )
    shortanswer2_kwargs = dict(
        event="shortanswer", div_id="team_eval_communication", course=course_name
    )
    fitb_kwargs = dict(
        event="fillb", div_id="team_eval_ge_contributions_0", course=course_name
    )

    # <p>*User 0* ---------------------------</p>
    logout = test_user_array[2].test_client.logout
    logout()
    test_user_array[0].login()
    assert_passing(
        0, act=json.dumps(test_user_array[0].username), **shortanswer1_kwargs
    )
    assert_passing(0, act=json.dumps("comm 0"), **shortanswer2_kwargs)
    assert_passing(0, answer=json.dumps(["5"]), **fitb_kwargs)

    # <p>*User 1* -------------------------- It doesn't matter which user logs
    #     out, since all three users share the same client.</p>
    logout()
    test_user_array[1].login()
    assert_passing(
        1, act=json.dumps(test_user_array[1].username), **shortanswer1_kwargs
    )
    assert_passing(1, act=json.dumps("comm 1"), **shortanswer2_kwargs)
    assert_passing(1, answer=json.dumps(["25"]), **fitb_kwargs)

    # <p>*User 2* ----------------------------</p>
    logout()
    test_user_array[2].login()
    # <p>Add three shortanswer answers, to make sure the number of attempts is
    #     correctly recorded.</p>
    assert_passing(
        2, act=json.dumps(test_user_array[2].username), **shortanswer1_kwargs
    )
    assert_passing(2, act=json.dumps("comm 2"), **shortanswer2_kwargs)
    assert_passing(2, answer=json.dumps(["90"]), **fitb_kwargs)

    # <p>**Test the team report** =========================</p>
    with open(
        "applications/{}/books/{}/test_course_1.csv".format(
            runestone_name, course.base_course
        ),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(
            "user id,user name,team name\n"
            "test_user_0@foo.com,test user_0,team 1\n"
            "test_user_1@foo.com,test user_1,team 1\n"
            "test_user_2@foo.com,test user_2,team 1\n"
        )

    # <p>TODO: Test not being an instructor.</p>
    tu = test_user_array[2]
    tu.make_instructor()
    tu.test_client.validate(
        "books/published/{}/test_chapter_1/team_report_1.html".format(course_name)
    )

    logout()
    # <p>TODO: Test with no login.</p>


@pytest.mark.skip(
    reason="Can't render new BookServer template using old server. TODO: Port to the BookServer."
)
def test_pageprogress(test_client, runestone_db_tools, test_user_1):
    test_user_1.login()
    test_user_1.hsblog(
        event="mChoice",
        act="answer:1:correct",
        answer="1",
        correct="T",
        div_id="subc_b_1",
        course=test_user_1.course.course_name,
    )
    # <p>Since the user has answered the question the count for subc_b_1 should
    #     be 1 cannot test the totals on the client without javascript but that
    #     is covered in the selenium tests on the components side.</p>
    test_user_1.test_client.validate(
        "books/published/{}/test_chapter_1/subchapter_b.html".format(
            test_user_1.course.base_course
        ),
        '"subc_b_1": 1',
    )
    assert '"LearningZone_poll": 0' in test_user_1.test_client.text
    assert '"subc_b_fitb": 0' in test_user_1.test_client.text


@pytest.mark.skip(
    reason="Can't render new BookServer template using old server. What does this test do? Should it be ported?"
)
def test_lockdown(test_client, test_user_1):
    test_user_1.login()
    base_course = test_user_1.course.base_course

    res = test_client.validate("books/published/{}/index.html".format(base_course))
    assert "Runestone in social media:" in res
    assert ">Change Course</a></li>" in res
    assert 'id="profilelink">Edit' in res
    assert '<ul class="dropdown-menu user-menu">' in res
    assert "<span id='numuserspan'></span><span class='loggedinuser'></span>" in res
    assert '<script async src="https://hypothes.is/embed.js"></script>' in res
