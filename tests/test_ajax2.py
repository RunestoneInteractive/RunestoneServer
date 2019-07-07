import json
import datetime

def test_poll(test_client, test_user_1, test_user, runestone_db_tools):
    """
    The parameters to test_poll are really pytest fixtures, you don't have to pass
    them explicitly as the framework takes care of it.  If you have your own parameters they
    shold come last.

    test_client -- A client that can communicate with web2py server
    test_user_1 -- A pre-registered user for test_course_1
    test_user -- a function to make more users
    runestone_db_tools -- a way to get manual access to the database

    All tests can assume that the database is present, but empty except for the essential data
    for the automtaically created users and courses.
    """

    # Make sure the user is logged in
    test_user_1.login()
    # Using hsblog have the user respond to a poll in the test_course_1 book
    # this is what you would do to simulate a user activity an any kind of runeston
    # component.
    test_user_1.hsblog(event='poll', act='1', div_id="LearningZone_poll", course='test_course_1')

    # Now lets get a handle on the database
    db = runestone_db_tools.db

    # Manually check that the response made it to the database
    res = db(db.useinfo.div_id=='LearningZone_poll').select().first()
    assert res
    assert res['act'] == "1"

    # Next we'll invoke the API call that returns the poll results. this is a list
    # [<num responses> [option list] [response list] divid myvote]
    test_client.post('ajax/getpollresults', data=dict(course='test_course_1', div_id='LearningZone_poll'))
    # print statements are useful for debugging and only shown in the Captured stdout call
    # section of the output from pytest if the test fails. Otherwise print output is
    # hidden
    print(test_client.text)
    res = json.loads(test_client.text)
    # expecting [1 [0, 1]  [0, 1] 'LearningZone_poll' '1']
    assert res[0] == 1
    assert res[-1] == "1"

    # Now lets have a second user respond to the poll.
    user2 = test_user('test_user_2', 'password', 'test_course_1')
    test_user_1.logout()
    user2.login()
    user2.hsblog(event='poll', act='2', div_id="LearningZone_poll", course='test_course_1')
    test_client.post('ajax/getpollresults', data=dict(course='test_course_1', div_id='LearningZone_poll'))
    res = json.loads(test_client.text)
    assert res[0] == 2
    assert res[1] == [0, 1, 2]
    assert res[2] == [0, 1, 1]
    assert res[-1] == "2"


def test_hsblog(test_client, test_user_1, test_user, runestone_db_tools):
    test_user_1.login()

    kwargs = dict( 
            act = 'run',
            event = 'acivecode',
            course = 'test_course_1',
            div_id = 'unit_test_1',
            )
    res = test_user_1.hsblog(**kwargs)
    print(res)
    assert len(res.keys()) == 2
    assert res['log'] == True
    time_delta = datetime.datetime.utcnow() - datetime.datetime.strptime(res['timestamp'], '%Y-%m-%d %H:%M:%S')
    assert time_delta < datetime.timedelta(seconds=1)

    db = runestone_db_tools.db
    dbres = db(db.useinfo.div_id == 'unit_test_1').select(db.useinfo.ALL)
    assert len(dbres) == 1
    assert dbres[0].course_id == 'test_course_1'


def ajaxCall(client, funcName, **kwargs):
    """
    Call the funcName using the client
    Returns json.loads(funcName())
    """
    client.post('ajax/' + funcName, data = kwargs)
    print(client.text)
    if client.text != 'None':
        return(json.loads(client.text))

def genericGetAssessResults(test_client, test_user, runestone_db_tools, **kwargs):
    """
    A generic function that calls the ajax/getAssessResults API for a variety of runestone events.
    It returns the result of the API call

    **kwargs -- the remaining arguments are the list of parameters for the hsblog() call
    """

    # Make sure the user is logged in
    test_user.login()

    # Using hsblog have the user respond to a event in the specified course
    # this is what you would do to simulate a user activity an any kind of runeston
    # component.
    test_user.hsblog(**kwargs)

    # Next we'll invoke the API call that returns the event results. 
    test_client.post('ajax/getAssessResults', data=dict(course=kwargs['course'], div_id=kwargs['div_id'], event=kwargs['event']))

    # print statements are useful for debugging and only shown in the Captured stdout call
    # section of the output from pytest if the test fails. Otherwise print output is
    # hidden
    print(test_client.text)
    res = json.loads(test_client.text)
    return res

# The following tests are a port from the test_ajax.py
def test_GetMChoiceResults(test_client, test_user_1, test_user, runestone_db_tools):

    # Generate a incorrect mChoice answer
    val = '1'
    res = genericGetAssessResults(test_client, test_user_1, runestone_db_tools, 
                            event = 'mChoice',
                            div_id = 'test_mchoice_1',
                            answer = val,
                            act = val,
                            correct = 'F',
                            course = 'test_course_1'
                           )
    assert res['answer'] == val
    assert not res['correct']

    # Generate a correct mChoice answer
    val = '3'
    res = genericGetAssessResults(test_client, test_user_1, runestone_db_tools, 
                            event = 'mChoice',
                            div_id = 'test_mchoice_1',
                            answer = val,
                            act = val,
                            correct = 'T',
                            course = 'test_course_1'
                           )
    assert res['answer'] == val
    assert res['correct']


def test_GetParsonsResults(test_client, test_user_1, test_user, runestone_db_tools):
    val = '0_0-1_2_0-3_4_0-5_1-6_1-7_0' 
    res = genericGetAssessResults(test_client, test_user_1, runestone_db_tools, 
                            event = 'parsons',
                            div_id = 'test_parsons_1',
                            answer = val,
                            act = val,
                            correct = 'F',
                            course = 'test_course_1',
                            source = 'test_source_1'
                           )
    assert res['answer'] == val

def test_GetClickableResults(test_client, test_user_1, test_user, runestone_db_tools):
    val = '0;1'
    res = genericGetAssessResults(test_client, test_user_1, runestone_db_tools, 
                            event = 'clickableArea',
                            div_id = 'test_clickable_1',
                            answer = val,
                            act = val,
                            correct = 'F',
                            course = 'test_course_1'
                           )
    assert res['answer'] == val
    assert not res['correct']

def test_GetShortAnswerResults(test_client, test_user_1, test_user, runestone_db_tools):
    val = 'hello_test'
    res = genericGetAssessResults(test_client, test_user_1, runestone_db_tools, 
                            event = 'shortanswer',
                            div_id = 'test_short_answer_1',
                            answer = val,
                            act = val,
                            correct = 'F',
                            course = 'test_course_1'
                           )
    assert res['answer'] == val

def test_GetFITBAnswerResults(test_client, test_user_1, test_user, runestone_db_tools):

    # Test old format, server-side grading
    ## -----------------------------------
    # A correct answer.
    val = 'red,away'
    res = genericGetAssessResults(test_client, test_user_1, runestone_db_tools, 
                            event = 'fillb',
                            div_id = 'test_fitb_1',
                            answer = val,
                            act = val,
                            course = 'test_course_1'
                           )
    assert res['answer'] == val
    assert res['correct']

    # An incorrect answer.
    val = 'blue,away'
    res = genericGetAssessResults(test_client, test_user_1, runestone_db_tools, 
                            event = 'fillb',
                            div_id = 'test_fitb_1',
                            answer = val,
                            act = val,
                            course = 'test_course_1'
                           )
    assert res['answer'] == val
    assert not res['correct']


    # Test new format, server-side grading
    ## -----------------------------------
    # A correct answer. Add spaces to verify these are ignored.
    val = '[" red ","away"]'
    res = genericGetAssessResults(test_client, test_user_1, runestone_db_tools, 
                            event = 'fillb',
                            div_id = 'test_fitb_1',
                            answer = val,
                            act = val,
                            course = 'test_course_1'
                           )
    assert res['answer'] == val
    assert res['correct']

    # An incorrect answer.
    val = '["blue","away"]'
    res = genericGetAssessResults(test_client, test_user_1, runestone_db_tools, 
                            event = 'fillb',
                            div_id = 'test_fitb_1',
                            answer = val,
                            act = val,
                            course = 'test_course_1'
                           )
    assert res['answer'] == val
    assert not res['correct']

    # Test server-side grading of a regex
    val = '["mARy"]'
    res = genericGetAssessResults(test_client, test_user_1, runestone_db_tools, 
                            event = 'fillb',
                            div_id = 'test_fitb_regex',
                            answer = val,
                            act = val,
                            course = 'test_course_1'
                           )
    assert res['correct']

    val = '["mairI"]'
    res = genericGetAssessResults(test_client, test_user_1, runestone_db_tools, 
                            event = 'fillb',
                            div_id = 'test_fitb_regex',
                            answer = val,
                            act = val,
                            course = 'test_course_1'
                           )
    assert res['correct']

    val = '["mairy"]'
    res = genericGetAssessResults(test_client, test_user_1, runestone_db_tools, 
                            event = 'fillb',
                            div_id = 'test_fitb_regex',
                            answer = val,
                            act = val,
                            course = 'test_course_1'
                           )
    assert not res['correct']

    # Test server-side grading of a range of numbers, using various bases.
    val = '["10"]'
    res = genericGetAssessResults(test_client, test_user_1, runestone_db_tools, 
                            event = 'fillb',
                            div_id = 'test_fitb_numeric',
                            answer = val,
                            act = val,
                            course = 'test_course_1'
                           )
    assert res['correct']
    # Sphinx 1.8.5 and Sphinx 2.0 render text a bit differently.
    assert res['displayFeed'] in (['Correct.'], ['<p>Correct.</p>\n'])

    val = '["0b1010"]'
    res = genericGetAssessResults(test_client, test_user_1, runestone_db_tools, 
                            event = 'fillb',
                            div_id = 'test_fitb_numeric',
                            answer = val,
                            act = val,
                            course = 'test_course_1'
                           )
    assert res['correct']

    val = '["0xA"]'
    res = genericGetAssessResults(test_client, test_user_1, runestone_db_tools, 
                            event = 'fillb',
                            div_id = 'test_fitb_numeric',
                            answer = val,
                            act = val,
                            course = 'test_course_1'
                           )
    assert res['correct']

    val = '["9"]'
    res = genericGetAssessResults(test_client, test_user_1, runestone_db_tools, 
                            event = 'fillb',
                            div_id = 'test_fitb_numeric',
                            answer = val,
                            act = val,
                            course = 'test_course_1'
                           )
    assert not res['correct']
    # Sphinx 1.8.5 and Sphinx 2.0 render text a bit differently.
    assert res['displayFeed'] in (['Close.'], ['<p>Close.</p>\n'])


    val = '["11"]'
    res = genericGetAssessResults(test_client, test_user_1, runestone_db_tools, 
                            event = 'fillb',
                            div_id = 'test_fitb_numeric',
                            answer = val,
                            act = val,
                            course = 'test_course_1'
                           )
    assert not res['correct']
    assert res['displayFeed'] in (['Close.'], ['<p>Close.</p>\n'])


    val = '["8"]'
    res = genericGetAssessResults(test_client, test_user_1, runestone_db_tools, 
                            event = 'fillb',
                            div_id = 'test_fitb_numeric',
                            answer = val,
                            act = val,
                            course = 'test_course_1'
                           )
    assert not res['correct']
    assert res['displayFeed'] in (['Nope.'], ['<p>Nope.</p>\n'])


    # Test client-side grading. 
    db = runestone_db_tools.db
    db(db.courses.course_name == 'test_course_1').update(login_required=False)
    val = '["blue","away"]'
    res = genericGetAssessResults(test_client, test_user_1, runestone_db_tools, 
                            event = 'fillb',
                            div_id = 'test_fitb_numeric',
                            answer = val,
                            act = val,
                            correct = 'F',
                            course = 'test_course_1'
                           )
    assert res['answer'] == val
    assert not res['correct']

def test_GetDragNDropResults(test_client, test_user_1, test_user, runestone_db_tools):

    val = '0;1;2'
    res = genericGetAssessResults(test_client, test_user_1, runestone_db_tools, 
                            event = 'dragNdrop',
                            div_id = 'test_dnd_1',
                            answer = val,
                            act = val,
                            correct = 'T',
                            minHeight = '512',
                            course = 'test_course_1'
                           )
    assert res['correct']

def test_GetHist(test_client, test_user_1, test_user, runestone_db_tools):

    test_user_1.login()

    kwargs = dict( 
            course = 'test_course_1',
            sid = 'test_user_1',
            div_id = 'test_activecode_1',
            error_info = 'success',
            event = 'acivecode',
            to_save = 'true'
            )
    for x in range(0, 10):
        kwargs['code'] = 'test_code_{}'.format(x)
        test_client.post('ajax/runlog', data = kwargs)


    kwargs = dict(
            acid = 'test_activecode_1',
            sid = 'test_user_1'
            )
    test_client.post('ajax/gethist', data = kwargs)
    print(test_client.text)
    res = json.loads(test_client.text)

    assert len(res['timestamps']) == 10
    assert len(res['history']) == 10

    time_delta = datetime.datetime.utcnow() - datetime.datetime.strptime(res['timestamps'][-1], '%Y-%m-%dT%H:%M:%S')
    assert time_delta < datetime.timedelta(seconds=2)

    test_client.post('ajax/getprog', data = kwargs)
    print(test_client.text)
    prog = json.loads(test_client.text)
    
    assert res['history'][-1] == prog[0]['source']

def test_RunLog(test_client, test_user_1, test_user, runestone_db_tools):

    """
    runlog should add an entry into the useinfo table as well as the code and acerror_log tables...
    code and acerror_log seem pretty redundant... This ought to be cleaned up.
    """
    test_user_1.login()

    kwargs = dict( 
            course = 'test_course_1',
            sid = 'test_user_1',
            div_id = 'test_activecode_1',
            code = "this is a unittest",
            error_info = 'success',
            event = 'acivecode',
            to_save = 'True'
            )
    test_client.post('ajax/runlog', data = kwargs)

    kwargs = dict(
            acid = 'test_activecode_1',
            sid = 'test_user_1'
            )
    test_client.post('ajax/getprog', data = kwargs)
    print(test_client.text)
    prog = json.loads(test_client.text)

    assert prog[0]['source'] == "this is a unittest"


def test_GetLastPage(test_client, test_user_1, test_user, runestone_db_tools):

    test_user_1.login()
    kwargs = dict(
            course = 'test_course_1',
            lastPageUrl = 'test_chapter_1/subchapter_a.html',
            lastPageScrollLocation = 100,
            completionFlag = '1'
            )
    # Call ``getlastpage`` first to insert a new record.
    test_client.post('ajax/getlastpage', data=kwargs)
    # Then, we can update it with the required info.
    test_client.post('ajax/updatelastpage', data=kwargs)

    # Now, test a query.
    res = ajaxCall(test_client, 'getlastpage', **kwargs)
    assert res[0]['lastPageUrl'] == 'test_chapter_1/subchapter_a.html'
    assert res[0]['lastPageChapter'] == 'Test chapter 1'

def test_GetNumOnline(test_client, test_user_1, test_user, runestone_db_tools):
    test_GetTop10Answers(test_client, test_user_1, test_user, runestone_db_tools)
    test_client.post('ajax/getnumonline')
    print(test_client.text)
    res = json.loads(test_client.text)
    assert res[0]['online'] == 6

def test_GetTop10Answers(test_client, test_user_1, test_user, runestone_db_tools):
    user_ids = []
    for index in range(0, 6):
        user = test_user('test_user_{}'.format(index+2), 'password', 'test_course_1')
        user_ids.append(user)
        user.login()

        kwargs = dict(
                event = 'fillb',
                course = 'test_course_1',
                div_id = 'test_fitb_1'
               )
        if index % 2 == 1:
            kwargs['answer'] = '42'
            kwargs['correct'] = 'T'
        else:
            kwargs['answer'] = '41'
            kwargs['correct'] = 'F'
        kwargs['act'] = kwargs['answer']

        test_client.post('ajax/hsblog', data=kwargs)
        user.logout()

    user_ids[0].login()
    test_client.post('ajax/gettop10Answers', data=kwargs)
    print(test_client.text)
    res, misc = json.loads(test_client.text)
    
    assert res[0]['answer'] == '41'
    assert res[0]['count'] == 3
    assert res[1]['answer'] == '42'
    assert res[1]['count'] == 3
    assert misc['yourpct'] == 0
    

# @unittest.skipIf(not is_linux, 'preview_question only runs under Linux.') FIXME
def testPreviewQuestion(test_client, test_user_1, test_user, runestone_db_tools):
    src = """
.. activecode:: preview_test1

   Hello World
   ~~~~
   print("Hello World")

"""
    test_user_1.login()

    kwargs = dict( 
            code = json.dumps(src)
            )
    test_client.post('ajax/preview_question', data = kwargs)
    print(test_client.text)
    res = json.loads(test_client.text)

    assert 'id="preview_test1"' in res
    assert 'print("Hello World")' in res
    assert 'textarea>' in res
    assert 'textarea data-component="activecode"' in res
    assert 'div data-childcomponent="preview_test1"' in res

def test_GetUserLoggedIn(test_client, test_user_1, test_user, runestone_db_tools):
    test_user_1.login()
    test_client.post('ajax/getuser')
    print(test_client.text)
    res = json.loads(test_client.text)
    
    assert res[0]['nick'] == test_user_1.username


def test_GetUserNotLoggedIn(test_client, test_user_1, test_user, runestone_db_tools):
    test_user_1.logout() # make sure user is logged off...
    test_client.post('ajax/getuser')
    print(test_client.text)
    res = json.loads(test_client.text)[0]
    
    assert 'redirect' in res

def test_Donations(test_client, test_user_1, test_user, runestone_db_tools):
    test_user_1.login()
    res = ajaxCall(test_client, 'save_donate')
    assert res == None

    res = ajaxCall(test_client, 'did_donate')
    assert res['donate'] == True

def test_NonDonor(test_client, test_user_1, test_user, runestone_db_tools):
    test_user_1.login()
    res = ajaxCall(test_client, 'did_donate')
    assert not res['donate']

def test_GetAgregateResults(test_client, test_user_1, test_user, runestone_db_tools):

    # creat a bunch of users and have each one answer a multiple choice questions according to this table
    table = [ # sid      correct answer
              ('user_1662', 'F', '0'),
              ('user_1662', 'T', '1'),
              ('user_1663', 'T', '1'),
              ('user_1665', 'T', '1'),
              ('user_1667', 'F', '0'),
              ('user_1667', 'T', '1'),
              ('user_1668', 'F', '0'),
              ('user_1668', 'T', '1'),
              ('user_1669', 'T', '1'),
              ('user_1670', 'T', '1'),
              ('user_1671', 'T', '1'),
              ('user_1672', 'F', '0'),
              ('user_1672', 'T', '1'),
              ('user_1673', 'F', '0'),
              ('user_1673', 'T', '1'),
              ('user_1674', 'T', '1'),
              ('user_1675', 'F', '0'),
              ('user_1675', 'T', '1'),
              ('user_1675', 'T', '1'),
              ('user_1676', 'T', '1'),
              ('user_1677', 'T', '1'),
              ('user_1751', 'F', '0'),
              ('user_1751', 'T', '1'),
              ('user_2521', 'T', '1')   
             ]
    users = {}
    for t in table:
        # create the user if user has not been created yet
        user_name = t[0]
        correct = t[1]
        answer = t[2]
        logAnswer = "answer:" + answer + ":" + ("correct" if (correct == "T") else "no")
        if user_name not in users.keys():
            user = test_user(user_name, 'password', 'test_course_1')
            users[user_name] = user
        # logon
        user = users[user_name]
        user.login()
        # enter mchoice answer
        user.hsblog(event='mChoice', div_id="test_mchoice_1", course='test_course_1',
                     correct = correct, act = logAnswer, answer = answer)
        # logout
        user.logout()
    
    # get a particular user
    user = users['user_1675']
    user.login()
    kwargs = dict(
            course = 'test_course_1',
            div_id = 'test_mchoice_1'
            )

    test_client.validate('ajax/getaggregateresults', data = kwargs)
    print(test_client.text)
    res = json.loads(test_client.text)
    res = res[0]
    assert res['misc']['yourpct'] == 67
    assert res['answerDict']['0'] == 29 
    assert res['answerDict']['1'] == 71 
    user.logout()

    # Now test for the instructor:
    user.make_instructor()
    user.login()
    test_client.validate('ajax/getaggregateresults', data = kwargs)
    print(test_client.text)
    res = json.loads(test_client.text)
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
    'user_1675': [u'0', u'1', u'1'],
    'user_1676': [u'1'],
    'user_1677': [u'1'],
    'user_1751': [u'0', u'1'],
    'user_2521': [u'1']        ,
    }
    for student in res['reslist']:
        assert student[1] == expect[student[0]]

def test_GetCompletionStatus(test_client, test_user_1, test_user, runestone_db_tools):
    test_user_1.login()

    # Check an unviewed page
    kwargs = dict(
            lastPageUrl = 'https://runestone.academy/runestone/static/test_course_1/test_chapter_1/toctree.html'
            )

    test_client.validate('ajax/getCompletionStatus', data = kwargs)
    print(test_client.text)
    res = json.loads(test_client.text)
    assert res[0]['completionStatus'] == -1

    # check that the unviewed page gets added into the database with a start_date of today
    db = runestone_db_tools.db
    row = db((db.user_sub_chapter_progress.chapter_id == 'test_chapter_1') & (db.user_sub_chapter_progress.sub_chapter_id == 'toctree')).select().first()
    print (row)
    assert row is not None
    assert row.end_date is None
    today = datetime.datetime.utcnow()
    assert row.start_date.month ==  today.month
    assert row.start_date.day ==  today.day
    assert row.start_date.year ==  today.year

    # Check a viewed page w/ completion status 0
    # 'View the page'
    kwargs = dict(
            lastPageUrl = 'https://runestone.academy/runestone/static/test_course_1/test_chapter_1/subchapter_a.html',
            lastPageScrollLocation = 0,
            course = 'test_course_1',
            completionFlag = 0
            )
    test_client.validate('ajax/updatelastpage', data = kwargs)

    # Check it
    test_client.validate('ajax/getCompletionStatus', data = kwargs)
    print(test_client.text)
    res = json.loads(test_client.text)
    assert res[0]['completionStatus'] == 0

    # Check a viewed page w/ completion status 1
    # 'View the page and check the completion button'
    kwargs = dict(
            lastPageUrl = 'https://runestone.academy/runestone/static/test_course_1/test_chapter_1/subchapter_a.html',
            lastPageScrollLocation = 0,
            course = 'test_course_1',
            completionFlag = 1
            )
    test_client.validate('ajax/updatelastpage', data = kwargs)

    # Check it
    test_client.validate('ajax/getCompletionStatus', data = kwargs)
    print(test_client.text)
    res = json.loads(test_client.text)
    assert res[0]['completionStatus'] == 1


    # Test getAllCompletionStatus()
    test_client.validate('ajax/getAllCompletionStatus')
    res = json.loads(test_client.text)
    print(res)
    assert len(res) == 3


def test_updatelastpage(test_client, test_user_1, test_user, runestone_db_tools):
    test_user_1.login()
    kwargs = dict(
            lastPageUrl = 'https://runestone.academy/runestone/static/test_course_1/test_chapter_1/subchapter_a.html',
            lastPageScrollLocation = 0,
            course = 'test_course_1',
            completionFlag = 1
            )
    test_client.validate('ajax/updatelastpage', data = kwargs)
    db = runestone_db_tools.db
    res = db((db.user_sub_chapter_progress.user_id == test_user_1.user_id) &
            (db.user_sub_chapter_progress.sub_chapter_id == 'subchapter_a')).select().first()
    print(res)

    now = datetime.datetime.utcnow()

    assert res.status == 1
    assert res.end_date.month == now.month
    assert res.end_date.day == now.day
    assert res.end_date.year == now.year


def test_getassignmentgrade(test_assignment, test_user_1, test_user, runestone_db_tools, test_client):
    # make a dummy student to do work
    student1 = test_user('student1', 'password', 'test_course_1')
    student1.logout()

    test_user_1.make_instructor()
    test_user_1.login()

    # make dummy assignment
    my_ass = test_assignment('test_assignment', 'test_course_1')
    my_ass.addq_to_assignment(question='subc_b_fitb',points=10)
    my_ass.save_assignment()

    # record a grade for that student on an assignment
    sid = student1.username
    acid = 'subc_b_fitb'
    grade = 5
    comment = 'OK job'
    res = test_client.validate('assignments/record_grade',
            data=dict(sid=sid,
                      acid = acid,
                      grade = grade,
                      comment = comment))

    test_user_1.logout()

    # check unreleased assignment grade
    student1.login()
    kwargs = dict(
            div_id = acid
            )
    test_client.validate('ajax/getassignmentgrade', data = kwargs)
    print(test_client.text)
    res = json.loads(test_client.text)
    assert res[0]['grade'] == 'Not graded yet'
    assert res[0]['comment'] == 'No Comments'
    assert res[0]['avg'] == 'None'
    assert res[0]['count'] == 'None'
    student1.logout()

    # release grade 
    test_user_1.login()
    my_ass.release_grades()
    test_user_1.logout()

    # check grade again
    student1.login()
    kwargs = dict(
            div_id = acid
            )
    test_client.validate('ajax/getassignmentgrade', data = kwargs)
    print(test_client.text)
    res = json.loads(test_client.text)
    assert res[0]['grade'] == 5
    assert res[0]['version'] == 2
    assert res[0]['max'] == 10
    assert res[0]['comment'] == comment
    

def test_get_datafile(test_client, test_user_1, test_user, runestone_db_tools):

    # Create some datafile into the db and then read it out using the ajax/get_datafile()
    db = runestone_db_tools.db
    db.source_code.insert(course_id='test_course_1',
        acid='mystery.txt',
        main_code = 'hello world')

    test_user_1.make_instructor()
    test_user_1.login()
    kwargs = dict(
            course_id = 'test_course_1',
            acid = 'mystery.txt'
            )
    test_client.validate('ajax/get_datafile', data = kwargs)
    print(test_client.text)
    res = json.loads(test_client.text)
    assert res['data'] == 'hello world'

    # non-existant datafile
    kwargs = dict(
            course_id = 'test_course_1',
            acid = 'thisWillNotBeThere.txt'
            )
    test_client.validate('ajax/get_datafile', data = kwargs)
    print(test_client.text)
    res = json.loads(test_client.text)
    assert res['data'] is None




