Testing The Runestone Server
============================

Testing the Runestone Server is a daunting task, especially since we did not write unit tests for the first several years of our development!  Recently (meaning 2019) we have begun to develop a decent test infrastructure that allows you to write tests with relatively little pain!  And thats what it needs to be in order to make it possible to write tests in an environment where we just want to get that new feature added!

If you just want to run the tests:

.. code-block::

    python run_tests.py


Or if you have a docker container set up:

.. code-block::

    docker exec -it runestoneserver_runestone_1 bash -c 'cd applications/runestone/tests; python run_tests.py'

But we really hope you will write some tests, so lets take a look at a sample of a test that simulates a user submitting a response to a poll.  We'll then check to see that their answer made it into the database, and then make sure that the api call to retrieve poll results works as expected

.. code-block:: python

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


The test above can be run as part of the entire suite of tests by running ``scripts/dtest -k test_poll`` from the Runestone main directory.  This assumes that you have a Docker environment set up for your developent work. If you are not using docker then from the tests folder run ``python run_tests.py -k test_poll`` The ``-k`` option matches any part of the test names, so you don't have to give it the full test name.  ``-k poll`` would run any test that has poll in its name.

The ``run_tests.py`` script ensures that the database is initialized, a test book/course is created (called test_course_1) and all of the testing framework is in place.  The pytest framework uses "fixtures" to help with all the gory details of setting up a test environment and creating various pieces of that environment.  The fixtures include:

* test_client - A client for interacting with the web2py Server

  * logout
  * validate - get a page, validate it and check for an expected string
  * logout

* test_user_1 - A pre-made user registered for test_course_1 . Every user supports the following methods:

  * login
  * logout
  * hsblog
  * make_instructor - turn this user into an instructor
  * update_profile
  * make_payment
  * test_client -- an attribute that gets the client the user is using (think of the client liket the browser)

* test_user - A function to create a test user
* runestone_db_tools - An object that allows you to get the db object
* web2py_server

When you want to make sure that a variable has a value all you need to do is use an ``assert`` statment.  If the assert fails the test fails.  Its that easy.

In the future we'll add new fixtures, such as an assignment, and we'll add more capabilities to the user and client as we learn what will help write tests more quickly and efficiently.

We can enhance the test above by adding the following code to simulate a second user responding:

.. code-block:: python

    # Now lets have a second user respond to the poll.
    user2 = test_user('test_user_2', 'password', 'test_course_1')
    test_user_1.logout()
    user2.login()
    user2.hsblog(event='poll', act='2', div_id="LearningZone_poll", course='test_course_1')
    test_client.post('ajax/getpollresults', data=dict(course='test_course_1', div_id='LearningZone_poll'))
    res = json.loads(test_client.text)
    assert res[1] == [0, 1, 2]
    assert res[2] == [0, 1, 1]
    assert res[-1] == "2"
    assert res[0] == 2

Load Testing
============

From the scripts folder, run the command:

```
locust -f locustfile.py
```

Then in your browser go to `http://127.0.0.1:8089` You an set up how many users you want and how fast they will come online.  The webpage will update every couple of seconds to show you statistics on load times for various kinds of pages.