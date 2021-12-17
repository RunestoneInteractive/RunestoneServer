***************************************************************
rsmanage - command-line tools for managing the Runestone server
***************************************************************

The rsmanage command is designed to streamline many of the common tasks associated with running a Runestone Server.

::

    Usage: rsmanage [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

    Type subcommand --help for help on any subcommand

    Options:
    --verbose   More verbose output
    --if_clean  only run if database is uninitialized
    --help      Show this message and exit.

    Commands:
    addcourse                   Create a course in the database
    addeditor                   Add an existing user as an instructor for a...
    addinstructor               Add an existing user as an instructor for a...
    build                       Build the book for an existing course
    courseinfo                  List all information for a single course
    env                         Print out your configured environment If...
    fill-practice-log-missings  Only for one-time use to fill out the missing...
    findinstructor              Print the PII of the instructor for a given...
    grade                       Grade a problem set; hack for long-running...
    initdb                      Initialize and optionally reset the database
    inituser                    Add a user (or users from a csv file)
    instructors                 List instructor information for all courses
                                or...

    migrate                     Startup web2py and load the models with...
    resetpw                     Utility to change a users password.
    rmuser                      Utility to change a users password.
    run                         Starts up the runestone server and optionally...
    shutdown                    Shutdown the server and any schedulers


.. toctree::
    :maxdepth: 2
    :glob:

    *.py
