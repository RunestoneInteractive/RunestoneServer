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
import sys
from bs4 import BeautifulSoup

from gluon.globals import Request, Session
from gluon.tools import Auth
from six import StringIO

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
        exec(compile(open("applications/runestone/controllers/dashboard.py").read(), "applications/runestone/controllers/dashboard.py", 'exec'), globals())


    def testStudentReport(self):
        auth.login_user(db.auth_user(1674))
        session.auth = auth
        request.vars.id=auth.user.username

        res = studentreport()   #todo: if this is an endoint why does it not return json?

        #course_id=auth.user.course_name,  user=data_analyzer.user, chapters=chapters, activity=activity, assignments=data_analyzer.grades
        self.assertEqual(res['course_id'], 'testcourse')
        self.assertEqual(res['user'].username, 'user_1674')
        self.assertEqual(res['assignments']['List Practice']['score'], 13.0)
        self.assertEqual(res['assignments']['List Practice']['class_average'], '7.82') #todo: why a string?



    def test_subchapoverview(self):
        auth.login_user(db.auth_user(11))
        session.auth = auth
        request.vars.tablekind = 'sccount'

        res = subchapoverview()
        self.assertIsNotNone(res)
        soup = BeautifulSoup(res['summary'])
        thlist = soup.select('th')
        self.assertEqual(thlist[11].text, 'user_1671')
        rl = soup.select('tr')
        cl = rl[10].select('td')
        self.assertEqual(cl[5].text, '4.0')
        self.assertEqual(cl[17].text, '6.0')
        request.vars.action = 'tocsv'
        request.vars.tablekind = 'dividmin'
        res = subchapoverview()
        csvf = StringIO(res)
        rows = csvf.readlines()
        cols = rows[18].split(',')
        self.assertEqual(cols[0], 'Dictionaries')
        self.assertEqual(cols[2], 'ch12_dict11')
        self.assertEqual(cols[-1].strip(), '2017-10-26 22:25:38')
        cols = rows[122].split(',')
        self.assertEqual(cols[0], 'GeneralIntro')
        self.assertEqual(cols[3], '2017-08-30 22:29:30')


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestDashboardEndpoints))
res = unittest.TextTestRunner(verbosity=2).run(suite)
if len(res.errors) == 0 and len(res.failures) == 0:
    sys.exit(0)
else:
    print("nonzero errors exiting with 1", res.errors, res.failures)
    sys.exit(1)
