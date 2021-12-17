import datetime

#
# Unit Tests for DASHBOARD API endpoints
# Set up the environment variables
# WEB2PY_CONFIG=test
# TEST_DBURL=postgres://user:pw@host:port/dbname
#
#
# Run these from the main web2py directory with the command:
#
#
def test_student_report(test_client, runestone_db_tools, test_user, test_user_1):
    course_3 = runestone_db_tools.create_course("test_course_3")
    test_instructor_1 = test_user("test_instructor_1", "password_1", course_3)
    test_instructor_1.make_instructor()

    test_instructor_1.login()
    db = runestone_db_tools.db

    # Create an assignment -- using createAssignment
    # test_client.post('dashboard/studentreport',
    #     data=dict(id='test_user_1'))

    test_client.validate(
        "dashboard/studentreport", "Recent Activity", data=dict(id="test_instructor_1")
    )

    test_instructor_1.hsblog(
        event="mChoice",
        act="answer:1:correct",
        answer="1",
        correct="T",
        div_id="subc_b_1",
        course="test_course_3",
    )

    test_client.validate(
        "dashboard/studentreport", "subc_b_1", data=dict(id="test_instructor_1")
    )


def test_subchapteroverview(test_client, runestone_db_tools, test_user, test_user_1):
    course_3 = runestone_db_tools.create_course(
        "test_course_3", base_course="test_course_1"
    )
    test_instructor_1 = test_user("test_instructor_1", "password_1", course_3)
    test_instructor_1.make_instructor()

    test_instructor_1.login()
    db = runestone_db_tools.db

    test_client.validate("dashboard/subchapoverview", "Dashboard")
    test_client.validate(
        "dashboard/subchapoverview", "Dashboard", data=dict(tablekind="dividnum")
    )

    test_instructor_1.hsblog(
        event="mChoice",
        act="answer:1:correct",
        answer="1",
        correct="T",
        div_id="subc_b_1",
        course="test_course_3",
    )

    test_client.validate(
        "dashboard/subchapoverview", "subc_b_1", data=dict(tablekind="dividnum")
    )
    test_client.validate(
        "dashboard/subchapoverview", "div_id", data=dict(tablekind="dividmin")
    )
    test_client.validate(
        "dashboard/subchapoverview", "div_id", data=dict(tablekind="dividmax")
    )


def test_exercisemetrics(test_client, runestone_db_tools, test_user, test_user_1):
    course_3 = runestone_db_tools.create_course(
        "test_course_3", base_course="test_course_1"
    )
    test_instructor_1 = test_user("test_instructor_1", "password_1", course_3)
    test_instructor_1.make_instructor()

    test_instructor_1.login()
    test_instructor_1.hsblog(
        event="mChoice",
        act="answer:1:correct",
        correct="T",
        answer="answer:1:correct",
        div_id="subc_b_1",
        course="test_course_3",
    )

    res = test_instructor_1.test_client.validate(
        "dashboard/exercisemetrics",
        "Responses by Student",
        data=dict(chapter="test_chapter_1", id="subc_b_1"),
    )


def test_grades(test_client, runestone_db_tools, test_user):
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

    # set up practice - similar to test_instructor_practice_admin
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

    test_client.validate("dashboard/grades")

    assert "Gradebook" in test_client.text


def test_questiongrades_redirect(
    test_client, runestone_db_tools, test_user, test_user_1
):
    course_3 = runestone_db_tools.create_course(
        "test_course_3", base_course="test_course_1"
    )
    test_instructor_1 = test_user("test_instructor_1", "password_1", course_3)
    test_instructor_1.make_instructor()

    test_instructor_1.login()

    test_client.validate("dashboard/questiongrades")

    assert "Cannot call questiongrades directly" in test_client.text


def test_questiongrades(test_assignment, test_client, test_user, test_user_1):
    # make a dummy student to do work
    student1 = test_user("student1", "password", test_user_1.course)
    student1.logout()

    test_user_1.make_instructor()
    test_user_1.login()

    # make dummy assignment
    my_ass = test_assignment("test_assignment", test_user_1.course)
    assignment_id = my_ass.assignment_id
    my_ass.addq_to_assignment(question="subc_b_fitb", points=10)
    my_ass.save_assignment()

    # record a grade for that student on an assignment
    sid = student1.username
    acid = "subc_b_fitb"
    grade = 5
    comment = "OK job"
    res = test_client.validate(
        "assignments/record_grade",
        data=dict(sid=sid, acid=acid, grade=grade, comment=comment),
    )

    res = test_user_1.test_client.validate(
        "dashboard/questiongrades",
        "Click on the question name to display or update the grade for any question.",
        data=dict(sid=sid, assignment_id=assignment_id),
    )


# TODO:
# grades
# questiongrades
# better testing of index conten
