#
# Unit Tests for AJAX API endpoints
# Set up the environment variables
# WEB2PY_CONFIG=test
# TEST_DBURL=postgres://user:pw@host:port/dbname
#
#
# Run these from the main web2py directory with the command:
# python web2py.py -S runestone -M -R applications/runestone/tests/test_dashboard.py
#

import unittest
import json
import datetime
from gluon.globals import Request, Session
from gluon.tools import Auth
from dateutil.parser import parse

# bring in the ajax controllers


# clean up the database
db(db.useinfo.div_id == 'unit_test_1').delete()
db.commit()

class TestDashboardEndpoints(unittest.TestCase):
    def setUp(self):
        global request, session, auth
        request = Request(globals()) # Use a clean Request object
        session = Session()
        auth = Auth(db, hmac_key=Auth.get_or_create_key())
        execfile("applications/runestone/controllers/dashboard.py", globals())


    def testStudentReport(self):
        auth.login_user(db.auth_user(1674))
        session.auth = auth
        request.vars.id=auth.user.username

        # TODO: this does not appear to populate the session object

        print "SESSION = ", session
        res = studentreport()
        #course_id=auth.user.course_name,  user=data_analyzer.user, chapters=chapters, activity=activity, assignments=data_analyzer.grades
        self.assertEqual(res['course_id'], 'testcourse')
        self.assertEqual(res['user'].username, 'user_1674')
        print res['assignments']



suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestDashboardEndpoints))
unittest.TextTestRunner(verbosity=2).run(suite)
