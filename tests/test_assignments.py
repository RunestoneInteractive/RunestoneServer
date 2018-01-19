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

    def testReproduceScores(self):
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


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestGradingFunction))
unittest.TextTestRunner(verbosity=2).run(suite)
