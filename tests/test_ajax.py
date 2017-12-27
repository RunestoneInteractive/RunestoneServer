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

# clean up the database
db(db.useinfo.div_id == 'unit_test_1').delete()
db.commit()

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





suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestAjaxEndpoints))
unittest.TextTestRunner(verbosity=2).run(suite)
