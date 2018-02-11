#
# Unit Tests for AJAX API endpoints
# Set up the environment variables
# WEB2PY_CONFIG=test
# TEST_DBURL=postgres://user:pw@host:port/dbname
#
#
# Run these from the main web2py directory with the command:
# python web2py.py -S runestone -M -R applications/runestone/tests/test_ajax.py
#

#         record_grade      11539 305.000   29372
#     calculate_totals      40596 325.000    6490
# record_assignment_score     129 169.000     545
#            undefined         42 362.000    3374
#          get_problem      26087 702.000    9464
#                index       3775 901.000   17725
#         doAssignment      36219 1435.000          57225
#            autograde       2306 5531.000         235419



import unittest
import json
from gluon.globals import Request

# bring in the assignments controllers


class TestGradingFunction(unittest.TestCase):
    def setUp(self):
        global request
        request = Request(globals()) # Use a clean Request object
        execfile("applications/runestone/controllers/assignments.py", globals())

    def test_reproduce_scores(self):
        # fetch all of the autograded questions_grades
        # with all the info about them
        graded = db((db.question_grades.comment == 'autograded') &
                    (db.question_grades.div_id == db.questions.name) &
                    (db.questions.id == db.assignment_questions.question_id) &
                    (db.assignment_questions.assignment_id == db.assignments.id)).select(
                        db.question_grades.id,
                        db.question_grades.course_name,
                        db.question_grades.sid,
                        db.question_grades.div_id,
                        db.question_grades.comment,
                        db.question_grades.deadline,
                        db.assignment_questions.id,
                        db.assignment_questions.points,
                        db.questions.id,
                        db.questions.question_type,
                        db.assignments.id,
                        db.assignments.duedate,
                        db.assignment_questions.autograde,
                        db.assignment_questions.which_to_grade,
                        db.question_grades.score)

        # for each one, see if the computed score matches the recorded one
        for g in graded:
            sc = _autograde_one_q(course_name=g.question_grades.course_name,
                                              sid=g.question_grades.sid,
                                              question_name=g.question_grades.div_id,
                                              points=g.assignment_questions.points,
                                              question_type=g.questions.question_type,
                                              deadline=g.question_grades.deadline,
                                              autograde=g.assignment_questions.autograde,
                                              which_to_grade=g.assignment_questions.which_to_grade,
                                              save_score=False)
            self.assertEqual(sc,
                             g.question_grades.score,
                             "Failed for graded question {} got a score of {}".format(g,sc))


    def testASlashInSubchapter(self):
        execfile("applications/runestone/controllers/admin.py", globals())
        auth.login_user(db.auth_user(11))
        bad_name = 'Exceptions/When to use try/except'

        chap_id = db((db.chapters.chapter_name == 'Exceptions') & (db.chapters.course_id == auth.user.course_name)).select(db.chapters.id).first()
        db.sub_chapters.insert(sub_chapter_name='When to use try/except', chapter_id=chap_id,
                               sub_chapter_length=0, sub_chapter_label='using-exceptions')

        db.questions.insert(base_course='thinkcspy', name=bad_name,
                            chapter='Exceptions',
                            subchapter='using-exceptions',
                            htmlsrc='<h2>Hello World</h2>', question_type='page')

        request.vars.due = '2018/12/12 17:30'  # TODO: finish PR to use dateutil to parse dates in createAssignment
        request.vars.name = 'badsubchapter_assignment'
        res = createAssignment()  # TODO: deprecated?? but still used in admin.js

        res = json.loads(res)
        assignment_id = int(res[request.vars.name])

        request.vars.assignment = assignment_id
        request.vars.question = bad_name
        request.vars.points = 5
        request.vars.autograde = 'interact'
        request.vars.which_to_grade = ''
        request.vars.reading_assignment = True
        request.vars.activities_required = 2

        res = add__or_update_assignment_question()
        res = json.loads(res)
        rows = db(db.assignment_questions.assignment_id == assignment_id).select()
        self.assertEqual(1, len(rows))
        self.assertEqual(res['total'], rows[0].points)
        self.assertEqual('interact', rows[0].autograde)
        self.assertEqual(2, rows[0].activities_required)
        # select * from assignment_questions where assignment_id = 1244;
        #   id   | assignment_id | question_id | points | timed | autograde | which_to_grade | reading_assignment | sorting_priority | activities_required
        # -------+---------------+-------------+--------+-------+-----------+----------------+--------------------+------------------+---------------------
        #  30325 |          1244 |       14561 |      5 |       | interact  |                | T                  |                0 |                   2

        request.vars.assignment_id=str(assignment_id)
        res = doAssignment()
        # TODO: verify results of doAssignment

    def test_index(self):
        # Try to reproduce crash
        auth.login_user(db.auth_user(11))
        request.vars.sid = 'user_1663'
        res = index()
        self.assertEqual('user_1663', res['student'].username)

    def test_doAssignment(self):
        auth.login_user(db.auth_user(1663))
        request.vars.assignment_id = '94'
        res = doAssignment()

        rlist = [['General Introduction', 'GeneralIntro/toctree.html', 'The Python Programming Language', 'GeneralIntro/ThePythonProgrammingLanguage.html', 'completed', 'completed'],
         ['General Introduction', 'GeneralIntro/toctree.html', 'More About Programs', 'GeneralIntro/MoreAboutPrograms.html', 'completed'],
         ['General Introduction', 'GeneralIntro/toctree.html', 'What is Debugging?', 'GeneralIntro/WhatisDebugging.html', 'completed'],
         ['General Introduction', 'GeneralIntro/toctree.html', 'Algorithms', 'GeneralIntro/Algorithms.html', 'completed'],
         ['General Introduction', 'GeneralIntro/toctree.html', 'Syntax errors', 'GeneralIntro/Syntaxerrors.html', 'completed'],
         ['General Introduction', 'GeneralIntro/toctree.html', 'The Way of the Program', 'GeneralIntro/intro-TheWayoftheProgram.html', 'completed'],
         ['General Introduction', 'GeneralIntro/toctree.html', 'Semantic Errors', 'GeneralIntro/SemanticErrors.html', 'completed'],
         ['General Introduction', 'GeneralIntro/toctree.html', 'Runtime Errors', 'GeneralIntro/RuntimeErrors.html', 'completed'],
         ['General Introduction', 'GeneralIntro/toctree.html', 'Executing Python in this Book', 'GeneralIntro/SpecialWaystoExecutePythoninthisBook.html', 'completed'],
         ['General Introduction', 'GeneralIntro/toctree.html', 'Formal and Natural Languages', 'GeneralIntro/FormalandNaturalLanguages.html', 'completed'],
         ['General Introduction', 'GeneralIntro/toctree.html', 'Experimental Debugging', 'GeneralIntro/ExperimentalDebugging.html', 'completed'],
         ['General Introduction', 'GeneralIntro/toctree.html', 'A Typical First Program', 'GeneralIntro/ATypicalFirstProgram.html', 'completed'],
         ['General Introduction', 'GeneralIntro/toctree.html', 'Comments', 'GeneralIntro/Comments.html', 'completed']]

        self.assertEqual(len(res['readings'][7116]),13)
        for i in res['readings'][7116]:
            self.assertEqual(i[-1], "completed")
            self.assertEqual(i[0], "General Introduction")

        for i, r in enumerate(res['readings'][7116]):
            self.assertEqual(r, rlist[i])

        self.assertEqual(len(res['questioninfo']),0)
        self.assertEqual('testcourse', res['course_name'])
        self.assertEqual('testcourse', res['course_id'])

        request.vars.assignment_id = '263'
        res = doAssignment()
        self.assertEqual(len(res['questioninfo']),2)
        self.assertEqual(res['questioninfo'][0][-1], 'ex_3_10')
        self.assertEqual(res['questioninfo'][0][-6], 5)

    def test_save_score(self):
        auth.login_user(db.auth_user(11))
        # the db contains a pre-existing answer of 0.0 percent correct
        db.useinfo.insert(sid='user_11', timestamp=datetime.datetime.now(),
                          event='unittest', course_id='testcourse',
                          div_id='ex_5_8', act='percent:0.5:passed:2:failed:2')

        sc = _autograde_one_q(course_name='testcourse',
                              sid='user_11',
                              question_name='ex_5_8',
                              points=10,
                              question_type='actex',
                              deadline=None,
                              autograde='pct_correct',
                              which_to_grade='first_answer',
                              save_score=True)
        self.assertEqual(sc, 0)
        res = db((db.question_grades.sid=='user_11') &
                 (db.question_grades.div_id == 'ex_5_8')).select().first()
        self.assertEqual(0.0, res.score)

        sc = _autograde_one_q(course_name='testcourse',
                              sid='user_11',
                              question_name='ex_5_8',
                              points=10,
                              question_type='actex',
                              deadline=None,
                              autograde='pct_correct',
                              which_to_grade='last_answer',
                              save_score=True)
        self.assertEqual(5,sc)
        sc = _autograde_one_q(course_name='testcourse',
                              sid='user_11',
                              question_name='ex_5_8',
                              points=10,
                              question_type='actex',
                              deadline=None,
                              autograde='pct_correct',
                              which_to_grade='best_answer',
                              save_score=True)
        self.assertEqual(5,sc)

        res = db((db.question_grades.sid=='user_11') &
                 (db.question_grades.div_id == 'ex_5_8')).select().first()
        self.assertEqual(5.0, res.score)

        sc = _autograde_one_q(course_name='testcourse',
                              sid='user_11',
                              question_name='ex_5_8',
                              points=10,
                              question_type='actex',
                              deadline=datetime.datetime.now() - datetime.timedelta(days=1),
                              autograde='pct_correct',
                              which_to_grade='best_answer',
                              save_score=True)
        self.assertEqual(0,sc)

    def test_chooseAssignment(self):
        auth.login_user(db.auth_user(1663))
        res = chooseAssignment()
        # note:  19 may be affected by earlier testsadding more
        alist = res['assignments']
        self.assertEqual(len(alist), 19)
        self.assertEqual(alist[0].name, 'Chapter 1 Reading')
        self.assertEqual(alist[0].points, 13)
        self.assertEqual(alist[0].released, True)
        self.assertEqual(alist[8].released, None)

    def test_calculate_totals(self):
        auth.login_user(db.auth_user(11))
        request.vars.assignment = 'Function Practice'
        request.vars.sid = 'user_1663'
        res = json.loads(calculate_totals())
        # res {"computed_score": 5.0, "manual_score": null, "message": "Total for user_1663 is 5.0", "success": true}
        self.assertEqual(res['computed_score'], 5.0)
        self.assertEqual(res['success'], True)
        self.assertTrue('user_1663' in res['message'])
        assign = db( (db.assignments.name == request.vars.assignment) &\
                     (db.assignments.course == auth.user.course_id)).select(db.assignments.id).first()
        score = db((db.grades.assignment == assign) & (db.grades.auth_user == 1663)).select(db.grades.score).first()
        self.assertEqual(res['computed_score'], score.score)

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestGradingFunction))
unittest.TextTestRunner(verbosity=2).run(suite)
