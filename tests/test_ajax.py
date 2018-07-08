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
from gluon.globals import Request, Session
from gluon.tools import Auth
from dateutil.parser import parse
import sys

# This doesn't work -- ``__file__`` is ``applications\runestone\models\user_biography.py`` on my PC. ???
#sys.path.append(os.path.dirname(__file__))
sys.path.append('applications/runestone/tests')
from ci_utils import is_linux

# bring in the ajax controllers


# clean up the database
db(db.useinfo.div_id == 'unit_test_1').delete()
db.commit()

class TestAjaxEndpoints(unittest.TestCase):
    def setUp(self):
        global request, session, auth
        request = Request(globals()) # Use a clean Request object
        session = Session()
        auth = Auth(db, hmac_key=Auth.get_or_create_key())
        execfile("applications/runestone/controllers/ajax.py", globals())

    def tearDown(self):
        # In case of an error, roll back the last transaction to leave the
        # database in a working state.
        db.rollback()

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

        #mchoice
        auth.login_user(db.auth_user(11))
        request.vars.course = 'testcourse'
        request.vars.div_id = 'test_question2_4_1'
        request.vars.sid = 'user_1662'
        request.vars.event = 'mChoice'

        res = getAssessResults()
        res = json.loads(res)
        self.assertEqual(res['answer'], '1')
        self.assertEqual(res['correct'], True)

        request.vars["act"] = '3'
        request.vars.answer = '3'
        request.vars.correct = 'T'
        request.vars.event = 'mChoice'
        request.vars.course = 'testcourse'
        request.vars.div_id = 'testAddmchoice1'
        request.client = "foobar"
        res = hsblog()
        request.vars.sid = 'user_11'
        res = getAssessResults()
        res = json.loads(res)
        self.assertEqual(res['answer'], '3')
        self.assertEqual(res['correct'], True)

    def testGetParsonsResults(self):
        # Parsons
        auth.login_user(db.auth_user(11))
        request.vars.course = 'testcourse'
        request.vars.sid = 'user_1662'
        request.vars.event = 'parsons'
        request.vars.div_id = '3_8'
        res = json.loads(getAssessResults())
        self.assertEqual(res['answer'], '0_0-1_2_0-3_4_0-5_1-6_1-7_0', msg=None)
        # self.assertEqual(res['correct'], True) # TODO: why isn't correct returned?
        request.vars["act"] = '0_0-1_2_0-3_4_0-5_1-6_1-7_0'
        request.vars.answer = '0_0-1_2_0-3_4_0-5_1-6_1-7_0'
        request.vars.correct = 'F'
        request.vars.event = 'parsons'
        request.vars.course = 'testcourse'
        request.vars.div_id = 'testAddParsons1'
        request.client = "foobar"
        res = hsblog()
        request.vars.sid = 'user_11'
        res = getAssessResults()
        res = json.loads(res)
        self.assertEqual(res['answer'], '0_0-1_2_0-3_4_0-5_1-6_1-7_0')
        #self.assertEqual(res['correct'], False)


    def testGetClickableResults(self):
        # Parsons
        auth.login_user(db.auth_user(11))
        request.vars.course = 'testcourse'
        # clickable
        request.vars.event = 'clickableArea'
        request.vars.div_id = 'ca_id_str'
        request.vars.sid = 'user_1674'
        res = json.loads(getAssessResults())
        self.assertEqual(res['answer'], '0;1', msg=None)
        self.assertEqual(res['correct'], False)
        # timestamp 2017-09-04 00:56:34
        self.assertEqual("2017-09-04 00:56:34", res['timestamp'], msg=None)
        request.vars["act"] = '0;1'
        request.vars.answer = '0;1'
        request.vars.correct = 'F'
        request.vars.event = 'clickableArea'
        request.vars.course = 'testcourse'
        request.vars.div_id = 'testAddClickable1'
        request.client = "foobar"
        res = hsblog()
        request.vars.sid = 'user_11'
        res = getAssessResults()
        res = json.loads(res)
        self.assertEqual(res['answer'], '0;1')
        self.assertEqual(res['correct'], False)


    def testGetShortAnswerResults(self):
        auth.login_user(db.auth_user(11))
        request.vars.course = 'testcourse'
        request.vars.event = 'shortanswer'
        request.vars.div_id = 'turtle_reflect'
        request.vars.sid = 'user_1669'
        res = json.loads(getAssessResults())
        self.assertTrue("Moving the turtle" in res['answer'])
        request.vars["act"] = 'hello_test'
        request.vars.answer = 'hello_test'
        request.vars.correct = 'F'
        request.vars.event = 'shortanswer'
        request.vars.course = 'testcourse'
        request.vars.div_id = 'testAddShortanswer1'
        request.client = "foobar"
        res = hsblog()
        request.vars.sid = 'user_11'
        res = getAssessResults()
        res = json.loads(res)
        self.assertEqual(res['answer'], 'hello_test')


    # fitb
    def testGetFITBAnswerResults(self):
        auth.login_user(db.auth_user(11))
        request.vars.course = 'testcourse'
        request.vars.event = 'fillb'
        request.vars["act"] = '42'
        request.vars.answer = '42'
        request.vars.correct = 'T'
        request.vars.div_id = 'testAddFillb1'
        request.client = "foobar"
        res = hsblog()
        request.vars.sid = 'user_11'
        res = getAssessResults()
        res = json.loads(res)
        self.assertEqual(res['answer'], '42')
        self.assertTrue(res['correct'])



                # dragndrop
    def testGetDragNDropResults(self):
        auth.login_user(db.auth_user(11))
        request.vars.course = 'testcourse'
        auth.login_user(db.auth_user(11))
        request.vars["act"] = '0;1;2'
        request.vars.answer = '0;1;2'
        request.vars.correct = 'T'
        request.vars.event = 'dragNdrop'
        request.vars.course = 'testcourse'
        request.vars.div_id = 'demovideodnd'
        request.client = "foobar"
        request.vars.minHeight = '512'
        res = hsblog()
        request.vars.sid = 'user_11'
        res = json.loads(getAssessResults())
        self.assertTrue(res['correct'])


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
        request.vars.acid = 'unittest_div_111'
        prog = json.loads(getprog())
        self.assertEqual(prog[0]['source'], "this is a unittest")

    def testGetLastPage(self):
        auth.login_user(db.auth_user(11))
        request.vars.course = 'testcourse'
        res = json.loads(getlastpage())

        self.assertEqual('/runestone/static/testcourse/SimplePythonData/Exercises.html',
                         res[0]['lastPageUrl'])

        self.assertEqual('Simple Python Data', res[0]['lastPageChapter'])


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
        today = datetime.datetime.now()
        self.assertEqual(row.start_date.month, today.month)
        self.assertEqual(row.start_date.day, today.day)
        self.assertEqual(row.start_date.year, today.year)

        res = json.loads(getAllCompletionStatus())
        self.assertEqual(409, len(res))

    def test_GetNumOnline(self):
        # Put some users online and record that in the database.
        self.testGettop10Answers()
        db.commit()
        res = json.loads(getnumonline())
        # this is 6 because gettop10 adds data for 6 users to useinfo.
        self.assertEqual(6, res[0]['online'])

    def testGetUserLoggedIn(self):
        auth.login_user(db.auth_user(11))
        res = json.loads(getuser())
        self.assertEqual('user_11', res[0]['nick'])
        auth.logout_bare()

    def testGetUserNotLoggedIn(self):
        res = json.loads(getuser())[0]
        self.assertTrue('redirect' in res)


    def testGettop10Answers(self):
        # We don't have any fillb answers in our test database, so lets add some.
        db.questions.insert(base_course='thinkcspy', name='fillb1',
                            chapter='Exceptions',
                            subchapter='using-exceptions',
                            htmlsrc='<h2>Hello World</h2>', question_type='fillintheblank')

        for user in [11, 1662, 1663, 1665, 1667, 1670]:
            auth.login_user(db.auth_user(user))
            request.vars["act"] = 'run'
            request.vars.event = 'fillb'
            request.vars.course = 'testcourse'
            request.vars.div_id = 'fillb1'
            if user % 2 == 1:
                request.vars.act = '42'
                request.vars.answer = '42'
                request.vars.correct = 'T'
            else:
                request.vars.act = '41'
                request.vars.answer = '41'
                request.vars.correct = 'F'
            res = hsblog()

        auth.login_user(db.auth_user(11))
        request.vars.course = 'testcourse'
        request.vars.div_id = 'fillb1'
        res = json.loads(gettop10Answers())
        misc = res[1]
        res = res[0]
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0]['answer'], '42')
        self.assertEqual(res[0]['count'], 4)
        self.assertEqual(res[1]['answer'], '41')
        self.assertEqual(res[1]['count'], 2)
        self.assertEqual(misc['yourpct'], 100)

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

        now = datetime.datetime.now()

        self.assertEqual(res.status, 1)
        self.assertEqual(res.end_date.month, now.month)
        self.assertEqual(res.end_date.day, now.day)
        self.assertEqual(res.end_date.year, now.year)

    def test_donations(self):
        auth.login_user(db.auth_user(1667))
        res = save_donate()
        self.assertIsNone(res)
        res = json.loads(did_donate())
        self.assertTrue(res['donate'])

    def test_non_donor(self):
        auth.login_user(db.auth_user(11))
        res = json.loads(did_donate())
        self.assertFalse(res['donate'])

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






suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestAjaxEndpoints))
res = unittest.TextTestRunner(verbosity=2).run(suite)
if len(res.errors) == 0 and len(res.failures) == 0:
    sys.exit(0)
else:
    print("nonzero errors exiting with 1", res.errors, res.failures)
    sys.exit(1)


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
