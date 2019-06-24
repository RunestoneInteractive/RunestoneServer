import json
import time

def test_grade_one_student(test_assignment, test_user_1, test_user, runestone_db_tools, test_client):
    test_user_1.make_instructor()
    test_user_1.login()
    # Should test all combinations of
    # which_to_grade = first_answer, last_answer, best_answer
    # autograde = all_or_nothing, manual, pct_correct, interact
    which_tg = ['first_answer', 'last_answer', 'best_answer']
    my_ass = test_assignment('test_assignment', 'test_course_1')
    my_ass.addq_to_assignment(question='test_fitb_1', points=10,
        which_to_grade='best_answer',
        autograde='all_or_nothing')
    find_id = dict([reversed(i) for i in my_ass.questions()])

    student1 = test_user('student1', 'password', 'test_course_1')
    student1.login()
    answer = json.dumps(['red','away']),
    bad_answer = json.dumps(['blue','green']),
    student1.hsblog(event='fillb', act=bad_answer, correct='F',
        answer=bad_answer,
        div_id="test_fitb_1",
        course='test_course_1')
    time.sleep(1.5)
    student1.hsblog(event='fillb', act=answer, correct='T',
        answer=answer,
        div_id="test_fitb_1",
        course='test_course_1')
    time.sleep(1.5)
    student1.hsblog(event='fillb', act=bad_answer, correct='F',
        answer=bad_answer,
        div_id="test_fitb_1",
        course='test_course_1')
    student1.logout()

    test_user_1.login()
    qid = find_id['test_fitb_1']
    db = runestone_db_tools.db
    correct_scores = [0, 0, 10]

    for ix, grun in enumerate(which_tg):
        for gt in ['all_or_nothing', 'pct_correct', 'interact']:
            up = db((db.assignment_questions.assignment_id == my_ass.assignment_id) &
                    (db.assignment_questions.question_id == qid)).update(which_to_grade=grun, autograde=gt)
            db.commit()
            assert up == 1
            mess = my_ass.autograde()
            print(mess)
            my_ass.calculate_totals()

            res = db( (db.question_grades.sid == student1.username) &
                    (db.question_grades.div_id == 'test_fitb_1') &
                    (db.question_grades.course_name == 'test_course_1')
                    ).select().first()

            assert res
            if gt != 'interact':
                assert res['score'] == correct_scores[ix]
            else:
                assert res['score'] == 10

            totres = db( (db.grades.assignment == my_ass.assignment_id) &
                         (db.grades.auth_user == student1.user_id)
            ).select().first()
            assert totres
            if gt != 'interact':
                assert res['score'] == correct_scores[ix]
            else:
                assert res['score'] == 10
