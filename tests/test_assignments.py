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

import unittest
import json
from gluon.globals import Request

# bring in the assignments controllers
execfile("applications/runestone/controllers/assignments.py", globals())

class TestGradingFunction(unittest.TestCase):
    def setUp(self):
        request = Request(globals()) # Use a clean Request object

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
                             "Failed for graded question {}".format(g))

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestGradingFunction))
unittest.TextTestRunner(verbosity=2).run(suite)
