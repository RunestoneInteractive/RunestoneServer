
def test_build(test_client, test_user_1, runestone_db_tools):
    test_user_1.make_instructor()
    test_user_1.login()
    test_client.validate('designer/build', 'build_course_1',
        data=dict(
        coursetype=test_user_1.course.course_name,
        institution='Runestone',
        startdate='01/01/2019',
        python3='T',
        login_required='T',
        instructor='T',
        projectname='build_course_1',
        projectdescription='Build a course'
    ))

    db = runestone_db_tools.db
    res = db(db.courses.course_name == 'build_course_1').select().first()
    assert res.institution == 'Runestone'
    assert res.base_course == test_user_1.course.course_name

    # Now delete it

    test_client.validate('admin/deletecourse', 'About Runestone')
    res = db(db.courses.course_name == 'build_course_1').select().first()
    assert not res

    test_client.validate('designer/build', 'build_course_2',
        data=dict(
        coursetype=test_user_1.course.course_name,
        instructor='T',
        startdate='',
        projectname='build_course_2',
        projectdescription='Build a course'
    ))
