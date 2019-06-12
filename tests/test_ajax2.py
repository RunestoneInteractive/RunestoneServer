import json

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

