import json
import time
import pytest

# parameters:
# 1. question name
# 2. event
# 2. correct answer
# 3. bad answer
# 4. correct_scores
#
# Test fillb, mChoice, dragNdrop, clickableArea, parsons, unittest
WHICH_ANSWER = ['first_answer', 'last_answer', 'best_answer']
HOW_TO_SCORE = ['all_or_nothing', 'pct_correct', 'interact']
@pytest.mark.parametrize('div_id, event, good_answer, bad_answer, correct_scores, which_tg, grade_type',
[ ('test_fitb_1','fillb',['red','away'], ['blue','green'], [0, 0, 10], WHICH_ANSWER, HOW_TO_SCORE),
  ('subc_b_1', 'mChoice', 'answer:1:correct', 'answer:0:no', [0, 0, 10], WHICH_ANSWER, HOW_TO_SCORE),
  ('subc_b_dd', 'dragNdrop', '1;2;3', '3;2;1', [0,0,10], WHICH_ANSWER, HOW_TO_SCORE),
  ('click1', 'clickableArea', '1;2;3', '0', [0,0, 10], WHICH_ANSWER, HOW_TO_SCORE),
  ('parsons_ag1', 'parsons', 'correct|-|1_1-2_1-3_3', 'incorrect|-|1_2-2_3-3_1', [0, 0, 10], WHICH_ANSWER, HOW_TO_SCORE),
  ('units1', 'unittest', 'percent:100:passed:2:failed:0', 'percent:0:passed:0:failed:2', [0, 0, 10], WHICH_ANSWER, HOW_TO_SCORE),
  ('units1', 'unittest', 'percent:50:passed:1:failed:1', 'percent:0:passed:0:failed:2', [5,0], ['best_answer', 'last_answer'], ['pct_correct']),
  ('LearningZone_poll', 'poll', '1', '2', [10], ['first_answer'], ['interact']),
  ('yt_vid_ex1', 'video', 'play', 'play', [10], ['last_answer'], ['interact']),
  ('showEval_0', 'showeval', 'next', 'next', [10], ['last_answer'], ['interact']),
  ('shorta1', 'shortanswer', 'Hello world', 'Just as good', [0, 10], ['last_answer'], ['manual', 'interact'])
])
def test_grade_one_student(div_id, event, good_answer, bad_answer, correct_scores, which_tg, grade_type,\
    test_assignment, test_user_1, test_user, runestone_db_tools, test_client):

    test_user_1.make_instructor()
    test_user_1.login()
    # Should test all combinations of
    # which_to_grade = first_answer, last_answer, best_answer
    # autograde = all_or_nothing, manual, pct_correct, interact
    my_ass = test_assignment('test_assignment', 'test_course_1')
    my_ass.addq_to_assignment(question=div_id, points=10,
        which_to_grade='best_answer',
        autograde='all_or_nothing')
    find_id = dict([reversed(i) for i in my_ass.questions()])

    student1 = test_user('student1', 'password', 'test_course_1')
    student1.login()
    # unittest does not json encode its results
    if event != 'unittest':
        good_answer = json.dumps(good_answer)
        bad_answer = json.dumps(bad_answer)

    student1.hsblog(event=event, act=bad_answer, correct='F',
        answer=bad_answer,
        div_id=div_id,
        course='test_course_1')
    time.sleep(1.5)
    student1.hsblog(event=event, act=good_answer, correct='T',
        answer=good_answer,
        div_id=div_id,
        course='test_course_1')
    time.sleep(1.5)
    student1.hsblog(event=event, act=bad_answer, correct='F',
        answer=bad_answer,
        div_id=div_id,
        course='test_course_1')
    student1.logout()

    test_user_1.login()
    qid = find_id[div_id]
    db = runestone_db_tools.db

    for ix, grun in enumerate(which_tg):
        for gt in grade_type:
            up = db((db.assignment_questions.assignment_id == my_ass.assignment_id) &
                    (db.assignment_questions.question_id == qid)).update(which_to_grade=grun, autograde=gt)
            db.commit()
            assert up == 1
            mess = my_ass.autograde()
            print(mess)
            my_ass.calculate_totals()

            res = db( (db.question_grades.sid == student1.username) &
                    (db.question_grades.div_id == div_id) &
                    (db.question_grades.course_name == 'test_course_1')
                    ).select().first()

            if gt == 'manual':
                assert not res
            else:
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
                assert totres['score'] == correct_scores[ix]
            else:
                assert totres['score'] == 10
