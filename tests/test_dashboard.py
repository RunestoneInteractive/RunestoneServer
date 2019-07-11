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
    course_3 = runestone_db_tools.create_course('test_course_3')
    test_instructor_1 = test_user('test_instructor_1', 'password_1', course_3.course_name)
    test_instructor_1.make_instructor()

    test_instructor_1.login()
    db = runestone_db_tools.db

    # Create an assignment -- using createAssignment
    #test_client.post('dashboard/studentreport',
    #     data=dict(id='test_user_1'))

    test_client.validate('dashboard/studentreport','Recent Activity', data=dict(id='test_instructor_1'))

    test_instructor_1.hsblog(event="mChoice",
            act="answer:1:correct",answer="1",correct="T",div_id="subc_b_1",
            course="test_course_3")

    test_client.validate('dashboard/studentreport','subc_b_1', data=dict(id='test_instructor_1'))


def test_subchapteroverview(test_client, runestone_db_tools, test_user, test_user_1):
    course_3 = runestone_db_tools.create_course('test_course_3', base_course='test_course_1')
    test_instructor_1 = test_user('test_instructor_1', 'password_1', course_3.course_name)
    test_instructor_1.make_instructor()

    test_instructor_1.login()
    db = runestone_db_tools.db

    test_client.validate('dashboard/subchapoverview','chapter_num')
    test_client.validate('dashboard/subchapoverview','div_id', data=dict(tablekind='dividnum'))

    test_instructor_1.hsblog(event="mChoice",
            act="answer:1:correct",answer="1",correct="T",div_id="subc_b_1",
            course="test_course_3")

    test_client.validate('dashboard/subchapoverview','subc_b_1', data=dict(tablekind='dividnum'))
    test_client.validate('dashboard/subchapoverview','div_id', data=dict(tablekind='dividmin'))
    test_client.validate('dashboard/subchapoverview','div_id', data=dict(tablekind='dividmax'))

def test_exercisemetrics(test_client, runestone_db_tools, test_user, test_user_1):
    course_3 = runestone_db_tools.create_course('test_course_3', base_course='test_course_1')
    test_instructor_1 = test_user('test_instructor_1', 'password_1', course_3.course_name)
    test_instructor_1.make_instructor()

    test_instructor_1.login()
    test_instructor_1.hsblog(event='mChoice', act='answer:1:correct', correct='T',
        answer='answer:1:correct',
        div_id='subc_b_1',
        course='test_course_3')

    res = test_instructor_1.test_client.validate('dashboard/exercisemetrics', 'Responses by Student',
            data=dict(chapter='test_chapter_1', id='subc_b_1'))



# TODO:
# grades
# questiongrades
# better testing of index conten
