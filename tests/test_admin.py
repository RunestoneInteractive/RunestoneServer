import json


def test_add_assignment(test_assignment, test_client, test_user_1, runestone_db_tools):
    my_ass = test_assignment('test_assignment', 'test_course_1')
    # Should provide the following to addq_to_assignment
    # -- assignment (an integer)
    # -- question == div_id
    # -- points
    # -- autograde  one of ['manual', 'all_or_nothing', 'pct_correct', 'interact']
    # -- which_to_grade one of ['first_answer', 'last_answer', 'best_answer']
    # -- reading_assignment (boolean, true if it's a page to visit rather than a directive to interact with)
    my_ass.addq_to_assignment(question='subc_b_fitb',points=10)
    print(my_ass.questions())
    db = runestone_db_tools.db
    my_ass.save_assignment()
    res = db(db.assignments.name == 'test_assignment').select().first()
    assert res.description == my_ass.description
    assert str(res.duedate.date()) == str(my_ass.due.date())
    my_ass.autograde()
    my_ass.calculate_totals()
    my_ass.release_grades()
    res = db(db.assignments.id == my_ass.assignment_id).select().first()
    assert res.released == True


def test_choose_assignment(test_assignment, test_client, test_user_1, runestone_db_tools):
    my_ass = test_assignment('test_assignment', 'test_course_1')
    my_ass.addq_to_assignment(question='subc_b_fitb',points=10)
    my_ass.description = 'Test Assignment Description'
    my_ass.make_visible()
    test_user_1.login()
    test_client.validate('assignments/chooseAssignment.html','Test Assignment Description')

def test_do_assignment(test_assignment, test_client, test_user_1, runestone_db_tools):
    my_ass = test_assignment('test_assignment', 'test_course_1')
    my_ass.addq_to_assignment(question='subc_b_fitb',points=10)
    my_ass.description = 'Test Assignment Description'
    my_ass.make_visible()
    test_user_1.login()
    # This assignment has the fill in the blank for may had a |blank| lamb
    test_client.validate('assignments/doAssignment.html', 'Mary had a',
        data=dict(assignment_id=my_ass.assignment_id))

def test_question_text(test_assignment, test_client, test_user_1, runestone_db_tools):
    test_user_1.make_instructor()
    test_user_1.login()
    test_client.validate('admin/question_text', 'Mary had a',
            data=dict(question_name='subc_b_fitb'))
    test_client.validate('admin/question_text', 'Error: ',
            data=dict(question_name='non_existant_question'))

def test_removeinstructor(test_user, test_client, test_user_1, runestone_db_tools):
    my_inst = test_user('new_instructor', 'password', 'test_course_1')
    my_inst.make_instructor()
    my_inst.login()
    res = test_client.validate('admin/addinstructor/{}'.format(test_user_1.user_id))
    assert json.loads(res) == 'Success'
    res = test_client.validate('admin/removeinstructor/{}'.format(test_user_1.user_id))
    assert json.loads(res) == [True]
    res = test_client.validate('admin/removeinstructor/{}'.format(my_inst.user_id))
    assert json.loads(res) == [False]
    res = test_client.validate('admin/addinstructor/{}'.format(9999999))
    assert 'Cannot add non-existent user ' in json.loads(res)

def test_removestudents(test_user, test_client, test_user_1, runestone_db_tools):
    my_inst = test_user('new_instructor', 'password', 'test_course_1')
    my_inst.make_instructor()
    my_inst.login()
    res = test_client.validate('admin/removeStudents', 'Assignments',
        data=dict(studentList=test_user_1.user_id))

    db = runestone_db_tools.db
    res = db(db.auth_user.id == test_user_1.user_id).select().first()
    assert res.active == False


def test_htmlsrc(test_assignment, test_client, test_user_1, runestone_db_tools):
    test_user_1.make_instructor()
    test_user_1.login()
    test_client.validate('admin/htmlsrc', 'Mary had a',
            data=dict(acid='subc_b_fitb'))
    test_client.validate('admin/htmlsrc', 'No preview Available',
            data=dict(acid='non_existant_question'))


def test_qbank(test_client, test_user_1, runestone_db_tools):
    test_user_1.make_instructor()
    test_user_1.login()
    qname = 'subc_b_fitb'
    res = test_client.validate('admin/questionBank',
            data=dict(term=qname
            ))
    res = json.loads(res)
    assert qname in res
    res = test_client.validate('admin/questionBank',
            data=dict(chapter='test_chapter_1'
            ))
    res = json.loads(res)
    assert qname in res
    assert len(res) >= 4
    res = test_client.validate('admin/questionBank',
            data=dict(author='test_author'
            ))
    res = json.loads(res)
    assert qname in res
    assert len(res) == 2


def test_gettemplate(test_user_1, runestone_db_tools, test_client):
    test_user_1.make_instructor()
    test_user_1.login()
    dirlist = ['activecode', 'mchoice', 'fillintheblank']
    for d in dirlist:
        res = test_client.validate('admin/gettemplate/{}'.format(d))
        res = json.loads(res)
        assert res
        assert d in res['template']


def test_question_info(test_assignment, test_user_1, runestone_db_tools, test_client):
    test_user_1.make_instructor()
    test_user_1.login()
    my_ass = test_assignment('test_assignment', 'test_course_1')
    my_ass.addq_to_assignment(question='subc_b_fitb',points=10)
    res = test_client.validate('admin/getQuestionInfo', data=dict(
            assignment=my_ass.assignment_id,
            question='subc_b_fitb',
    ))
    res = json.loads(res)
    assert res
    assert res['code']
    assert res['htmlsrc']


def test_create_question(test_assignment, test_user_1, runestone_db_tools, test_client):
    test_user_1.make_instructor()
    test_user_1.login()
    my_ass = test_assignment('test_assignment', 'test_course_1')
    data = {
        'template': 'mchoice',
        'name': 'test_question_1',
        'question': "This is fake text for a fake question",
        'difficulty': 0,
        'tags': None,
        'chapter': 'test_chapter_1',
        'subchapter': 'Exercises',
        'isprivate': False,
        'assignmentid': my_ass.assignment_id,
        'points': 10,
        'timed': False,
        'htmlsrc': "<p>Hello World</p>"
    }
    res = test_client.validate('admin/createquestion', data=data)
    res = json.loads(res)
    assert res
    assert res['test_question_1']

    db = runestone_db_tools.db
    row = db(db.questions.id == res['test_question_1']).select().first()

    assert row['question'] == "This is fake text for a fake question"


def test_get_assignment(test_assignment, test_user_1, runestone_db_tools, test_client):
    test_user_1.make_instructor()
    test_user_1.login()
    my_ass = test_assignment('test_assignment', 'test_course_1')
    my_ass.addq_to_assignment(question='subc_b_fitb',points=10)

    res = test_client.validate('admin/get_assignment', data=dict(
        assignmentid=my_ass.assignment_id
    ))

    res = json.loads(res)
    assert res
    assert res['questions_data']