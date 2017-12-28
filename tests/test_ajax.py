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

# bring in the ajax controllers
execfile("applications/runestone/controllers/ajax.py", globals())
execfile("applications/runestone/controllers/assignments.py", globals())

# clean up the database
db(db.useinfo.div_id == 'unit_test_1').delete()
db.commit()


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
                                              deadline=g.assignments.duedate,
                                              autograde=g.assignment_questions.autograde,
                                              which_to_grade=g.assignment_questions.which_to_grade,
                                              save_score=False)
            print "~", sc
            self.assertEqual(sc,
                             g.question_grades.score,
                             "Failed for graded question {}".format(g))



class TestAjaxEndpoints(unittest.TestCase):
    def setUp(self):
        request = Request(globals()) # Use a clean Request object

    def testHSBLog(self):
        # Set up the request object
        request.vars["act"] = 'run'
        request.vars.event = 'activecode'
        request.vars.course = 'thinkcspy'
        request.vars.div_id = 'unit_test_1'
        request.client = "foobar"

        # call the function
        res = hsblog()
        res = json.loads(res)
        self.assertEqual(res, {'log':True})

        # make sure the basic db stuff was written
        dbres = db(db.useinfo.div_id == 'unit_test_1').select(db.useinfo.ALL)
        self.assertEqual(len(dbres), 1)
        self.assertEqual(dbres[0].course_id, 'thinkcspy')

    def testInstructorStatus(self):
        auth.login_user(db.auth_user(11))
        course = 'testcourse'
        verifyInstructorStatus(course, 11)
        self.assertTrue(verifyInstructorStatus(course,auth.user.id))
        auth.login_user(db.auth_user(1663))
        self.assertFalse(verifyInstructorStatus(course,auth.user.id))

    def testGetAssessResults(self):
        """
        getAssessResults
        test_question2_4_1 | user_1662 correct answer is 1 on second try
        """
        #globals auth, db
        # can login user with auth.login_user(db.auth_user(60)) then auth.user will be defined
        auth.login_user(db.auth_user(11))
        request.vars.course = 'testcourse'
        request.vars.div_id = 'test_question2_4_1'
        request.vars.sid = 'user_1662'
        request.vars.event = 'mChoice'

        res = getAssessResults()
        res = json.loads(res)
        self.assertEqual(res['answer'], '1')
        self.assertEqual(res['correct'], True)





suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestAjaxEndpoints))
suite.addTest(unittest.makeSuite(TestGradingFunction))
unittest.TextTestRunner(verbosity=2).run(suite)
