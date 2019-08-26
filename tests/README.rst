Testing The Runestone Server
============================

Testing the Runestone Server is a daunting task, especially since we did not write unit tests for the first several years of our development!  Recently (meaning 2019) we have begun to develop a decent test infrastructure that allows you to write tests with relatively little pain!  And thats what it needs to be in order to make it possible to write tests in an environment where we just want to get that new feature added!

If you just want to run the tests:

- There are some extra modules needed, so install them

  .. code-block::

      cd runestone
      pip install -r requirements-test.txt


- Next, switch to the test directory (``runestone/tests``)
- **Make sure that you don't have a runestone server running.** If you do, that server will handle the web page requests that occur during the tests instead of letting the test server respond to them, and it will be accessing the wrong database.
- Run the tests. From the shell:

  .. code-block::

      pytest


  Or if you have a docker container set up:

  .. code-block::

      docker exec -it runestoneserver_runestone_1 bash -c 'cd applications/runestone/tests; pytest'

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


The test above can be run as part of the entire suite of tests by running ``scripts/dtest -k test_poll`` from the Runestone main directory.  This assumes that you have a Docker environment set up for your developent work. If you are not using docker then from the tests folder run ``pytest -k test_poll`` The ``-k`` option matches any part of the test names, so you don't have to give it the full test name.  ``-k poll`` would run any test that has poll in its name.

The pytest framework uses "fixtures" to help with all the gory details of setting up a test environment and creating various pieces of that environment. When you define a test_function that has one of these as a parameter name, when the test runner executes the function, the parameter will be bound to the fixture object.  The fixtures include:

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

* test_user - A function to create additional users
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

When Tests Fail
===============

When you see a line like this:

::

    applications/runestone/tests/test_ajax2.py::test_poll FAILED                            [100%]

A test has failed.  There is an enormous amount of output that will follow so its easy to get lost and miss the important data.

First, there is a block that shows you the test that failed, and the code of that test, and exactly what line of the test failed.

.. code-block::

    _________________________________________ test_poll __________________________________________

    test_client = <applications.runestone.tests.conftest._TestClient object at 0x7f5f062b0f60>
    test_user_1 = <applications.runestone.tests.conftest._TestUser object at 0x7f5f0738eb38>
    test_user = <function test_user.<locals>.<lambda> at 0x7f5f05613e18>
    runestone_db_tools = <applications.runestone.tests.conftest._RunestoneDbTools object at 0x7f5f0625c0f0>

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
    >       assert res[0] == 4
    E       assert 2 == 4
    E         -2
    E         +4

applications/runestone/tests/test_ajax2.py:52: AssertionError

The error here is showing that we were expecting res[0] == 4 when it was really 2.

Next, there is standard output from the test setup.

.. code-block::

    ------------------------------------ Captured stdout setup ------------------------------------
    Changed session ID runestone

That is followed by the standard output from the call to the test itself.

::

    ------------------------------------ Captured stdout call -------------------------------------
    [1, [0, 1], [0, 1], "LearningZone_poll", "1"]
    Changed session ID runestone
    Changed session ID runestone
    Changed session ID runestone
    Changed session ID runestone

And then the standard output from the teardown
::

    ---------------------------------- Captured stdout teardown -----------------------------------
    Changed session ID runestone

The output from the web2py server and any logger.xxx() messages that have been generated will be found in the next two sections:
::

    web2py server stdout
    --------------------

    b'web2py Web Framework\nCreated by Massimo Di Pierro, Copyright 2007-2019\nVersion 2.18.5-stable+timestamp.2019.04.07.21.13.59\nDatabase drivers available: sqlite3, psycopg2, imaplib, pymysql\n\nplease visit:\n\thttp://127.0.0.1:8000/\nuse "kill -SIGTERM 2811" to shutdown the web2py server\n\n\n'

    web2py server stderr
    --------------------

    b'web2py.py: warning: --nogui is deprecated, use --no_gui instead\n'

If you are making use of the ``validate`` call, and there are web page validation errors there will be a section describing the validation errors.  In addition, if a page does not validate its source is saved for you in the home directory of web2py.  That is the folder where you installed web2py.py or on Docker it is the default directory you end up in when you shell in to the container.


Load Testing
============

From the scripts folder, run the command:

::

    locust -f locustfile.py


Then in your browser go to `http://127.0.0.1:8089` You an set up how many users you want and how fast they will come online.  The webpage will update every couple of seconds to show you statistics on load times for various kinds of pages.
