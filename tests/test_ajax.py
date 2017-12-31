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
from gluon.globals import Request, Session
from dateutil.parser import parse

# bring in the ajax controllers
execfile("applications/runestone/controllers/ajax.py", globals())

# clean up the database
db(db.useinfo.div_id == 'unit_test_1').delete()
db.commit()

class TestAjaxEndpoints(unittest.TestCase):
    def setUp(self):
        request = Request(globals()) # Use a clean Request object
        session = Session()

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
        print("RESULTS = ", res)
        res = json.loads(res)
        self.assertEqual(res['answer'], '1')
        self.assertEqual(res['correct'], True)

    def testGetHist(self):
        """
        user_1662 | 2017-09-22 20:29:19 | bnm_fruitco_selection
        user_1662 | 2017-09-22 20:29:34 | bnm_fruitco_selection
        user_1662 | 2017-09-22 20:29:43 | bnm_fruitco_selection
        user_1662 | 2017-09-22 20:30:16 | bnm_fruitco_selection
        user_1662 | 2017-09-22 20:30:28 | bnm_fruitco_selection
        user_1662 | 2017-09-22 20:31:24 | bnm_fruitco_selection
        user_1662 | 2017-09-22 20:31:54 | bnm_fruitco_selection
        user_1662 | 2017-09-22 20:33:15 | bnm_fruitco_selection
        user_1662 | 2017-09-22 20:33:32 | bnm_fruitco_selection
        user_1662 | 2017-09-22 20:43:58 | bnm_fruitco_selection
        """
        request.vars.acid = 'bnm_fruitco_selection'
        request.vars.sid = 'user_1662'

        res = gethist()
        res = json.loads(res)
        self.assertEqual(len(res['timestamps']), 10)
        self.assertEqual(len(res['history']), 10)
        self.assertEqual(parse(res['timestamps'][-1]), parse('2017-09-22 20:43:58'))
        self.assertEqual(parse(res['timestamps'][0]), parse('2017-09-22 20:29:19'))
        prog = json.loads(getprog())
        self.assertEqual(res['history'][-1],prog[0]['source'])

    def testRunLog(self):
        """
        runlog should add an entry into the useinfo table as well as the code and acerror_log tables...
        code and acerror_log seem pretty redundant... This ought to be cleaned up.
        """
        auth.login_user(db.auth_user(11))
        request.vars.course = 'testcourse'
        request.vars.div_id = "unittest_div_111"
        request.vars.code = "this is a unittest"
        error_info = "succes"
        request.vars.event = 'activecode'
        request.vars.to_save = "True"

        runlog()
        request.vars.sid = None
        request.vars.acid = 'unittest_div_111'
        prog = json.loads(getprog())
        self.assertEqual(prog[0]['source'], "this is a unittest")


    # getCompletionStatus
    # getAllCompletionStatus
    # getlastpage
    # getCorrectStats
    # getStudentResults ??
    # getaggregateresults
    # getpollresults
    # gettop10Answers
    # getassignmentgrade
    # getAssessResults
    # preview_question
    # getlastanswer

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestAjaxEndpoints))
unittest.TextTestRunner(verbosity=2).run(suite)
