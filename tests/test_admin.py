import unittest
import json
import datetime
from gluon.globals import Request, Session
from gluon.tools import Auth
from dateutil.parser import parse

#     getGradeComments      24180 273.000    6281
# add__or_update_assignment_question        14059 678.000    7232
#         getChangeLog       6522 363.000    6399
#                index       6152 466.000    8119
#                admin       3924 442.000    5944
#       get_assignment       2751 356.000    4780
#      save_assignment       1127 297.000    4363
#              htmlsrc       1984 308.000    4456
#      course_students       1816 355.000    4155
#              grading       2096 620.000    9410
#          assignments       1954 1401.000          11919
#      sections_create        132 288.000    2924
#            startdate         10 309.000     877
# get_assignment_release_states      1170 312.000    4611
#        sections_list          5 319.000     591
#        rebuildcourse         18 213.000    1436
#       createquestion        153 320.000    3433
# reorder_assignment_questions        321 321.000    5279
#                  doc        297 326.000    2765
#        question_text        394 359.000    3480
#        edit_question        157 400.000    3448
#       removeStudents         96 411.000    2922
#         editindexrst         36 487.000    2960
#        releasegrades        173 508.000    4220
# delete_assignment_question          617 540.000    2724
#         questionBank         21 820.000    4890
#         deletecourse          5 1221.000           4476
#               backup          7 40584.000        101069


# clean up the database
db(db.useinfo.div_id == 'unit_test_1').delete()
db.commit()

class TestAdminEndpoints(unittest.TestCase):
    def setUp(self):
        global request, session, auth
        request = Request(globals()) # Use a clean Request object
        session = Session()
        auth = Auth(db, hmac_key=Auth.get_or_create_key())
        execfile("applications/runestone/controllers/admin.py", globals())

    def test_getChangeLog(self):
        # Set up the request object
        auth.login_user(db.auth_user(11))
        res = getChangeLog()
        self.assertTrue("August 19 2016" in res)

    def test_getGradeComments(self):
        # Set up the request object
        auth.login_user(db.auth_user(11))
        request.vars.acid = 'ex_7_11'
        request.vars.sid = 'user_1675'
        res = json.loads(getGradeComments())
        self.assertEqual(5, res['grade'])
        self.assertEqual('autograded', res['comments'])

    def test_addinstructor(self):
        auth.login_user(db.auth_user(11))
        request.args.append('1675')
        res = addinstructor()
        res = db(db.course_instructor.course == 65).select()
        self.assertEqual(2,len(res))
        for row in res:
            self.assertTrue(row.instructor in [11, 1675])
    def test_get_question_id(self):
        qid = _get_question_id('test-name-incorrect', 65)
        self.assertEqual(qid, None)
        qid = _get_question_id('lsh_comphist_1', 65)
        self.assertEqual(qid, 2093)

    def test_sections_list(self):
        auth.login_user(db.auth_user(11))
        sec_list = sections_list()
        # self.assertEqual(len(sec_list), 2)
        self.assertEqual(len(sec_list['sections']), 1)

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestAdminEndpoints))
unittest.TextTestRunner(verbosity=2).run(suite)



