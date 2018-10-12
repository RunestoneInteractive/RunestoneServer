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

# TODO:  Write these
# getpollresults
# timedAssess


import unittest
import json
import datetime
import sys
from functools import wraps

from gluon.globals import Request, Session
from gluon.tools import Auth
from mock import patch, Mock

# This doesn't work -- ``__file__`` is ``applications\runestone\models\user_biography.py`` on my PC. ???
#sys.path.append(os.path.dirname(__file__))
sys.path.append('applications/runestone/tests')
from ci_utils import is_linux


# ``hsblog`` workaround
# =====================
# The ``hsblog`` endpoint timestamps all entries with ``utcnow`` rounded to the nearest second. Results from ``getAssessResults`` are selected based on the most recent commit, again based on this rounded timestamp. If there are two calls to ``hsblog`` within the same second, ``getAssessResults`` will return the first call, not the expected second call, since the timestamps are identical. Therefore, this function uses a mocked ``datetime`` to sleep for 1 (simulated) second before calling ``hsblog``.
#
# **Important**: To use this function, the test routine which calls it must be decorated with ``mock_utcnow``.
def sleep_hsblog():
    mock_sleep(1)
    return hsblog()


# This decorator mocks ``datetime.datetime.utcnow`` such that calls to ``mock_sleep`` advance the reported time. This is faster than using ``time.sleep`` to insert actual delays.
def mock_utcnow(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Record the time when this test is run.
        utcnow = datetime.datetime.utcnow()
        # This is based on a `Stack Overflow post <https://stackoverflow.com/a/51213128>`_.
        with patch.object(datetime, 'datetime', Mock(wraps=datetime.datetime)):
            # Return this time, until it's updated by ``mock_sleep``.
            datetime.datetime.utcnow.return_value = utcnow
            return f(*args, **kwargs)

    return decorated_function


# Move the mocked timer forward to ``time_sec``. This only works if the datetime object has been mocked.
def mock_sleep(time_sec):
    datetime.datetime.utcnow.return_value += datetime.timedelta(seconds=time_sec)


# Test helper class
# =================
# Provide a class with utility functions for creating synthetic test data. Eventually, all test classes should derive from this. However, I can't figure out how to put this in a separate module due to web2py globals confusion.
class Web2pyTestCase(unittest.TestCase):
    def setUp(self):
        global request, session, auth
        request = Request(globals())  # Use a clean Request object
        request.application = 'runestone'
        session = Session()
        auth = Auth(db, hmac_key=Auth.get_or_create_key())
        # bring in the ajax controllers
        execfile("applications/runestone/controllers/ajax.py", globals())

        # Create a default user and course.
        self.course_name_1 = 'test_course_1'
        self.course_id_1 = self.createCourse(self.course_name_1)
        self.user_name_1 = 'test_user_1'
        self.user_id_1 = self.createUser(self.user_name_1, self.course_id_1)

    def tearDown(self):
        # In case of an error, roll back the last transaction to leave the
        # database in a working state. Also, attempt to leave the database in a
        # clean state for the next test.
        db.rollback()

    def createCourse(self, course_name='test_course_1', term_start_date='2000-01-01', login_required=True):
        return db.courses.insert(
            course_name=course_name, base_course=course_name,
            term_start_date=term_start_date,
            login_required=login_required,
        )

    def createUser(self, username, course_id):
        user_id = db.auth_user.insert(username=username, course_id=course_id)
        db.user_courses.insert(user_id=user_id, course_id=course_id)
        return user_id

    def makeInstructor(self, user_id, course_id):
        return db.course_instructor.insert(course=course_id, instructor=user_id)


# Test cases
# ==========
class TestAjaxEndpoints(Web2pyTestCase):
    def testHSBLog(self):
        # Set up the request object
        request.vars.act = 'run'
        request.vars.event = 'activecode'
        request.vars.course = self.course_name_1
        request.vars.div_id = 'unit_test_1'
        request.client = "foobar"

        # call the function
        res = json.loads(hsblog())
        self.assertEqual(len(res.keys()), 2)
        self.assertEqual(res['log'], True)
        time_delta = datetime.datetime.utcnow() - datetime.datetime.strptime(res['timestamp'], '%Y-%m-%d %H:%M:%S')
        self.assertLess(time_delta, datetime.timedelta(seconds=1))

        # make sure the basic db stuff was written
        dbres = db(db.useinfo.div_id == 'unit_test_1').select(db.useinfo.ALL)
        self.assertEqual(len(dbres), 1)
        self.assertEqual(dbres[0].course_id, self.course_name_1)

    def testInstructorStatus(self):
        self.makeInstructor(self.user_id_1, self.course_id_1)
        auth.login_user(db.auth_user(self.user_id_1))
        self.assertTrue(verifyInstructorStatus(self.course_name_1, auth.user.id))

        user_id_2 = self.createUser('test_user_2', self.course_id_1)
        auth.login_user(db.auth_user(user_id_2))
        self.assertFalse(verifyInstructorStatus(self.course_name_1, auth.user.id))


    @mock_utcnow
    def testGetAssessResults(self):
        """
        getAssessResults
        test_question2_4_1 | user_1662 correct answer is 1 on second try

        """
        # Create a mchoice answer.
        auth.login_user(db.auth_user(self.user_id_1))
        request.vars.div_id = 'test_mchoice_1'
        request.vars.sid = self.user_name_1
        request.vars.answer = '1'
        request.vars.act = request.vars.answer
        request.vars.correct = 'F'
        request.vars.event = 'mChoice'
        request.vars.course = self.course_name_1
        request.client = "foobar"
        sleep_hsblog()

        # Verify that it's incorrect.
        res = json.loads(getAssessResults())
        self.assertEqual(res['answer'], '1')
        self.assertEqual(res['correct'], False)

        # Now add a correct answer.
        request.vars.answer = '3'
        request.vars.act = request.vars.answer
        request.vars.correct = 'T'
        sleep_hsblog()
        res = json.loads(getAssessResults())
        self.assertEqual(res['answer'], '3')
        self.assertEqual(res['correct'], True)

    @mock_utcnow
    def testGetParsonsResults(self):
        # Create an entry.
        auth.login_user(db.auth_user(self.user_id_1))
        request.vars.answer = '0_0-1_2_0-3_4_0-5_1-6_1-7_0'
        request.vars.act = request.vars.answer
        request.vars.correct = 'F'
        request.vars.event = 'parsons'
        request.vars.course = self.course_name_1
        request.vars.div_id = 'test_parsons_1'
        request.vars.sid = self.user_name_1
        request.vars.source = 'test_source_1'
        request.client = "foobar"
        sleep_hsblog()

        # Check it.
        res = json.loads(getAssessResults())
        self.assertEqual(res['answer'], '0_0-1_2_0-3_4_0-5_1-6_1-7_0', msg=None)

    @mock_utcnow
    def testGetClickableResults(self):
        auth.login_user(db.auth_user(self.user_id_1))
        request.vars.event = 'clickableArea'
        request.vars.course = self.course_name_1
        request.vars.div_id = 'test_parsons_1'
        request.vars.sid = self.user_name_1
        request.client = "foobar"
        request.vars.answer = '0;1'
        request.vars.act = request.vars.answer
        request.vars.correct = 'F'
        sleep_hsblog()

        res = json.loads(getAssessResults())
        self.assertEqual(res['answer'], '0;1')
        self.assertEqual(res['correct'], False)

    @mock_utcnow
    def testGetShortAnswerResults(self):
        auth.login_user(db.auth_user(self.user_id_1))
        request.vars.course = self.course_name_1
        request.vars.event = 'shortanswer'
        request.vars.sid = self.user_name_1
        request.vars.div_id = 'test_short_anser_1'
        request.vars.answer = 'hello_test'
        request.vars.act = request.vars.answer
        request.vars.correct = 'F'
        request.client = "foobar"
        sleep_hsblog()

        res = json.loads(getAssessResults())
        self.assertEqual(res['answer'], 'hello_test')

    @mock_utcnow
    def testGetFITBAnswerResults(self):
        auth.login_user(db.auth_user(self.user_id_1))

        # Test client-side grading.
        request.vars.course = self.course_name_1
        request.vars.sid = self.user_name_1
        request.vars.event = 'fillb'
        request.vars.div_id = 'test_fitb_1'
        request.client = "foobar"
        request.vars.answer = '["blue","away"]'
        request.vars.act = request.vars.answer
        request.vars.correct = 'F'
        sleep_hsblog()
        res = json.loads(getAssessResults())
        self.assertEqual(res['answer'], request.vars.answer)

    @mock_utcnow
    def testGetDragNDropResults(self):
        auth.login_user(db.auth_user(self.user_id_1))
        request.vars.course = self.course_name_1
        request.vars.sid = self.user_name_1
        request.vars.answer = '0;1;2'
        request.vars.act = request.vars.answer
        request.vars.correct = 'T'
        request.vars.event = 'dragNdrop'
        request.vars.div_id = 'test_dnd_1'
        request.client = "foobar"
        request.vars.minHeight = '512'
        sleep_hsblog()

        res = json.loads(getAssessResults())
        self.assertTrue(res['correct'])

    def testGetHist(self):
        auth.login_user(db.auth_user(self.user_id_1))
        request.vars.course = self.course_name_1
        request.vars.sid = self.user_name_1
        request.vars.div_id = 'test_activecode_1'
        request.vars.error_info = 'success'
        request.vars.event = 'activecode'
        request.vars.to_save = 'true'
        for x in range(0, 10):
            request.vars.code = 'test_code_{}'.format(x)
            runlog()

        request.vars.acid = request.vars.div_id
        request.vars.sid = self.user_name_1
        res = json.loads(gethist())
        self.assertEqual(len(res['timestamps']), 10)
        self.assertEqual(len(res['history']), 10)
        time_delta = datetime.datetime.utcnow() - datetime.datetime.strptime(res['timestamps'][-1], '%Y-%m-%dT%H:%M:%S')
        self.assertLess(time_delta, datetime.timedelta(seconds=1))
        prog = json.loads(getprog())
        self.assertEqual(res['history'][-1],prog[0]['source'])

    def testRunLog(self):
        """
        runlog should add an entry into the useinfo table as well as the code and acerror_log tables...
        code and acerror_log seem pretty redundant... This ought to be cleaned up.
        """
        auth.login_user(db.auth_user(self.user_id_1))
        request.vars.course = self.course_name_1
        request.vars.sid = self.user_name_1
        request.vars.div_id = 'test_activecode_1'
        request.vars.code = "this is a unittest"
        request.vars.error_info = 'success'
        request.vars.event = 'activecode'
        request.vars.to_save = "True"
        runlog()

        request.vars.acid = request.vars.div_id
        prog = json.loads(getprog())
        self.assertEqual(prog[0]['source'], "this is a unittest")

    def testGetLastPage(self):
        auth.login_user(db.auth_user(self.user_id_1))
        request.vars.course = self.course_name_1
        request.vars.lastPageUrl = 'test_chapter_1/subchapter_a.html'
        request.vars.lastPageScrollLocation = 100
        request.vars.completionFlag = '1'
        # Call ``getlastpage`` first to insert a new record.
        getlastpage()
        # Then, we can update it with the required info.
        updatelastpage()

        # Now, test a query.
        res = json.loads(getlastpage())
        self.assertEqual(request.vars.lastPageUrl,
                         res[0]['lastPageUrl'])
        self.assertEqual('Test chapter 1', res[0]['lastPageChapter'])

    def test_GetNumOnline(self):
        # Put some users online and record that in the database.
        self.testGettop10Answers()
        res = json.loads(getnumonline())
        # this is 6 because gettop10 adds data for 6 users to useinfo.
        self.assertEqual(6, res[0]['online'])

    def testGettop10Answers(self):
        user_ids = []
        for index in range(0, 6):
            user_ids.append(self.createUser('test_user_{}'.format(index + 2),
                                            self.course_id_1))
            auth.login_user(db.auth_user(user_ids[-1]))
            request.vars.event = 'fillb'
            request.vars.course = self.course_name_1
            request.vars.div_id = 'test_fitb_1'
            if index % 2 == 1:
                request.vars.answer = '42'
                request.vars.act = request.vars.answer
                request.vars.correct = 'T'
            else:
                request.vars.answer = '41'
                request.vars.act = request.vars.answer
                request.vars.correct = 'F'
            # ``sleep_hsblog `` doesn't work here -- I assume more than just the
            # ``utcnow`` function gets called.
            hsblog()

        auth.login_user(db.auth_user(user_ids[0]))
        res, misc = json.loads(gettop10Answers())
        self.assertEqual(res[0]['answer'], '41')
        self.assertEqual(res[0]['count'], 3)
        self.assertEqual(res[1]['answer'], '42')
        self.assertEqual(res[1]['count'], 3)
        self.assertEqual(misc['yourpct'], 0)

    @unittest.skipIf(not is_linux, 'preview_question only runs under Linux.')
    def testPreviewQuestion(self):
        src = """
.. activecode:: preview_test1

   Hello World
   ~~~~
   print("Hello World")

"""
        request.vars.code = json.dumps(src)
        res = json.loads(preview_question())
        self.assertTrue('id="preview_test1"' in res)
        self.assertTrue('print("Hello World")' in res)
        self.assertTrue('</textarea>' in res)
        self.assertTrue('<textarea data-component="activecode"' in res)
        self.assertTrue('<div data-childcomponent="preview_test1"' in res)

    def testGetUserLoggedIn(self):
        auth.login_user(db.auth_user(self.user_id_1))
        res = json.loads(getuser())
        self.assertEqual(self.user_name_1, res[0]['nick'])
        auth.logout_bare()

    def testGetUserNotLoggedIn(self):
        res = json.loads(getuser())[0]
        self.assertTrue('redirect' in res)

    def test_donations(self):
        auth.login_user(db.auth_user(self.user_id_1))
        res = save_donate()
        self.assertIsNone(res)
        res = json.loads(did_donate())
        self.assertTrue(res['donate'])

    def test_non_donor(self):
        auth.login_user(db.auth_user(self.user_id_1))
        res = json.loads(did_donate())
        self.assertFalse(res['donate'])

        ## ========================================================================
        # All the following tests should eventually be ported to use synthetic data
        ## ========================================================================

# getaggregateresults
#    id   |      timestamp      |       div_id       |    sid    | course_name | correct | answer
# --------+---------------------+--------------------+-----------+-------------+---------+--------
#   46630 | 2017-09-04 19:24:36 | test_question2_4_1 | user_1662 | testcourse  | F       | 0
#   46631 | 2017-09-04 19:24:38 | test_question2_4_1 | user_1662 | testcourse  | T       | 1
#   46467 | 2017-09-04 18:39:44 | test_question2_4_1 | user_1663 | testcourse  | T       | 1
#   42189 | 2017-09-03 01:19:19 | test_question2_4_1 | user_1665 | testcourse  | T       | 1
#   44746 | 2017-09-04 01:40:22 | test_question2_4_1 | user_1667 | testcourse  | F       | 0
#   44748 | 2017-09-04 01:40:26 | test_question2_4_1 | user_1667 | testcourse  | T       | 1
#   41088 | 2017-09-02 13:57:49 | test_question2_4_1 | user_1668 | testcourse  | F       | 0
#   41089 | 2017-09-02 13:57:52 | test_question2_4_1 | user_1668 | testcourse  | T       | 1
#   40908 | 2017-09-02 02:44:59 | test_question2_4_1 | user_1669 | testcourse  | T       | 1
#  390419 | 2017-10-30 00:18:26 | test_question2_4_1 | user_1670 | testcourse  | T       | 1
#   43072 | 2017-09-03 17:31:03 | test_question2_4_1 | user_1671 | testcourse  | T       | 1
#   41422 | 2017-09-02 17:16:08 | test_question2_4_1 | user_1672 | testcourse  | F       | 0
#   41423 | 2017-09-02 17:16:10 | test_question2_4_1 | user_1672 | testcourse  | T       | 1
#   43349 | 2017-09-03 18:57:54 | test_question2_4_1 | user_1673 | testcourse  | F       | 0
#   43350 | 2017-09-03 18:58:02 | test_question2_4_1 | user_1673 | testcourse  | T       | 1
#   44514 | 2017-09-04 00:35:29 | test_question2_4_1 | user_1674 | testcourse  | T       | 1
#   43534 | 2017-09-03 19:35:08 | test_question2_4_1 | user_1675 | testcourse  | F       | 0
#   43535 | 2017-09-03 19:35:13 | test_question2_4_1 | user_1675 | testcourse  | T       | 1
#   49076 | 2017-09-05 02:05:02 | test_question2_4_1 | user_1676 | testcourse  | T       | 1
#   40767 | 2017-09-01 23:00:20 | test_question2_4_1 | user_1677 | testcourse  | T       | 1
#   40835 | 2017-09-02 00:49:28 | test_question2_4_1 | user_1751 | testcourse  | F       | 0
#   40836 | 2017-09-02 00:49:31 | test_question2_4_1 | user_1751 | testcourse  | T       | 1
#   76275 | 2017-09-08 00:55:02 | test_question2_4_1 | user_2521 | testcourse  | T       | 1

    def testGetAggregateResults(self):
        request.vars.course = 'testcourse'
        request.vars.div_id = 'test_question2_4_1'
        auth.login_user(db.auth_user(1675))

        res = json.loads(getaggregateresults())[0]
        # [{u'answerDict': {u'1': 72.0, u'0': 28.0}, u'misc': {u'course': u'testcourse', u'correct': u'1', u'yourpct': 76.0}}]
        self.assertEqual(res['answerDict']['1'], 72.0)
        self.assertEqual(res['answerDict']['0'], 28.0)
        self.assertEqual(res['misc']['yourpct'], 79.0)

        # TODO: this shows the old method of doing things using useinfo.  We should use mchoice_answers and then calculate
        # a sensible way of calculating class percentages. for example 16 1's and 7 0's 23 total would indicate 70% 1 and 30% 0
        # we should not count answers after they are correct
        # TODO: We can do away with the instructor view here as it is better in the dashboard

        # Now test for the instructor:
        auth.login_user(db.auth_user(11))
        res = json.loads(getaggregateresults())
        res = res[0]
        expect = {
        'user_1662': [u'0', u'1'],
        'user_1663': [u'1'],
        'user_1665': [u'1'],
        'user_1667': [u'0', u'1'],
        'user_1668': [u'0', u'1'],
        'user_1669': [u'1'],
        'user_1670': [u'1'],
        'user_1671': [u'1'],
        'user_1672': [u'0', u'1'],
        'user_1673': [u'0', u'1'],
        'user_1674': [u'1'],
        'user_1675': [u'0', u'1'],
        'user_1676': [u'1'],
        'user_1677': [u'1'],
        'user_1751': [u'0', u'1'],
        'user_2521': [u'1']        ,
        }
        for student in res['reslist']:
            self.assertEqual(student[1], expect[student[0]])

    def testGetCompletionStatus(self):
        auth.login_user(db.auth_user(11))
        request.vars.lastPageUrl = 'https://runestone.academy/runestone/static/testcourse/PythonTurtle/InstancesAHerdofTurtles.html'

        res = json.loads(getCompletionStatus())
        self.assertEqual(0, res[0]['completionStatus'])

        request.vars.lastPageUrl = 'https://runestone.academy/runestone/static/testcourse/SimplePythonData/ValuesandDataTypes.html'
        res = json.loads(getCompletionStatus())
        self.assertEqual(1, res[0]['completionStatus'])

        request.vars.lastPageUrl = 'https://runestone.academy/runestone/static/testcourse/Recursion/SierpinskiTriangle.html'
        res = json.loads(getCompletionStatus())
        self.assertEqual(-1, res[0]['completionStatus'])
        row = db((db.user_sub_chapter_progress.chapter_id == 'Recursion') & (db.user_sub_chapter_progress.sub_chapter_id == 'SierpinskiTriangle')).select().first()
        self.assertIsNotNone(row)
        self.assertIsNone(row.end_date)
        today = datetime.datetime.utcnow()
        self.assertEqual(row.start_date.month, today.month)
        self.assertEqual(row.start_date.day, today.day)
        self.assertEqual(row.start_date.year, today.year)

        res = json.loads(getAllCompletionStatus())
        self.assertEqual(409, len(res))

    # TODO: Cannot verify any questions other than activecodes and readings -- mchoice et al not stored??
    def test_getassignmentgrade(self):
        auth.login_user(db.auth_user(1667))
        request.vars.div_id = 'Functions/Functions'
        res = json.loads(getassignmentgrade())[0]
        self.assertEqual(res['grade'], 5)

    def test_getassignmentgrade_actex(self):
        auth.login_user(db.auth_user(1675))
        request.vars.div_id = 'ex_7_11'
        res = json.loads(getassignmentgrade())[0]
        self.assertEqual(res['grade'], 5)


    def test_updatelastpage(self):
        auth.login_user(db.auth_user(1667))
        request.vars.lastPageUrl = '/runestone.academy/runestone/static/testcourse/SimplePythonData/VariableNamesandKeywords.html'
        request.vars.lastPageScrollLocation = 0
        request.vars.course = 'testcourse'
        request.vars.completionFlag = 1
        res = updatelastpage()

        res = db((db.user_sub_chapter_progress.user_id == 1667) &
                (db.user_sub_chapter_progress.sub_chapter_id == 'VariableNamesandKeywords')).select().first()

        now = datetime.datetime.utcnow()

        self.assertEqual(res.status, 1)
        self.assertEqual(res.end_date.month, now.month)
        self.assertEqual(res.end_date.day, now.day)
        self.assertEqual(res.end_date.year, now.year)

    def test_datafile(self):
        db.source_code.insert(course_id='testcourse',
            acid='mystery.txt',
            main_code = 'hello world')

        auth.login_user(db.auth_user(11))
        request.vars.course_id = 'testcourse'
        request.vars.acid = 'mystery.txt'
        res = json.loads(get_datafile())
        print('res = ', res)
        self.assertEqual(res['data'], 'hello world')
        # non-existant
        request.vars.course_id = 'testcourse'
        request.vars.acid = 'nothere.txt'
        res = json.loads(get_datafile())
        self.assertIsNone(res['data'])


def runTests(cls_to_test):
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(cls_to_test))
    res = unittest.TextTestRunner(verbosity=2).run(suite)
    if len(res.errors) == 0 and len(res.failures) == 0:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    runTests(TestAjaxEndpoints)

# One month of AJAX on runestone.academy
#      endpoint           calls   avg time   max time
#               hsblog    1821749 249.369   40197
#     getAssessResults     732162 491.053   10311
#               runlog     723377 220.344   40371
#              getuser     579962 292.291   10217
#         getnumonline     579967 299.845   40147
#          getnumusers     580003 297.314   10345
#  getCompletionStatus     299650 347.226   10315
#       updatelastpage     228058 371.076   10359
# getAllCompletionStatus    93890 478.528    5844
#          getlastpage      93856 390.003    6591
#        set_tz_offset      46490 268.683    5175
#  getaggregateresults      16347 252.095    6018
#   getassignmentgrade       4610 215.614    4289
#     preview_question        796 1664.394  17134
#      gettop10Answers        644 213.599    2468
#       getpollresults        253 432.198    1972
#      checkTimedReset         78 265.128    1884
