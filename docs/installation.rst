Manual Installation
====================

.. warning::

   Note: These are the instructions for installing Runestone Server by hand environment. There are also `simpler Docker based instructions <https://runestoneserver.readthedocs.io/en/latest/docker/README.html>`_ available.


#. Install python.

   First, make sure you have Python installed.  Web2py has  been ported to Python3, but we have not finished all of our Python 3 testing yet. If you are a developer feel free to jump in with Python 3.

#. Install and make a Python virtualenv

   Note, development works well with a Python ``virtualenv``  If  you don't have root privileges on your computer I strongly recommend you install ``virtualenv`` and install all of the dependencies there.

   * Documentation here:  https://virtualenv.pypa.io/en/stable/
   * Video here:  https://www.youtube.com/watch?v=IX-v6yvGYFg
   * For the impatient:

     ::

     $ sudo pip install virtualenv
     $ virtualenv /path/to/home/MyEnv
     $ source /path/to/home/MyEnv/bin/activate

   * You will need to do the last command every time you want to work on RunestoneServer.  If you have not used Python virtual environments before I strongly recommend reading the docs or watching the video

#. Install lots of other dependencies

   **Ubuntu**

   On a vanilla Ubuntu (16.04) installation you will need to do at least the following:

   ::

       sudo apt-get install python-pip
       sudo apt-get install libfreetype6-dev
       sudo apt-get install postgresql-common postgresql postgresql-contrib
       sudo apt-get install libpq-dev
       sudo apt-get install libxml2-dev libxslt1-dev

   **macOS**

   On an macOS installation You must install Xcode and the command line tools.  Free from the App Store.  Then, I recommend you install homebrew (http://brew.sh)  then run the following commands:

   ::

       xcode-select --install
       brew install postgresql
       brew install libpng
       brew install freetype


   When you install **postgresql** make sure you follow the instructions at the end of
   the install for getting the server started.  On a mac you can ignore the additional configuration
   instructions for postgres given below. For a recent homebrew just do ``brew services start postgresql``
   to start the postgres database server.  Your user will already be configured as an administrative
   user.

   **Windows**

   On Windows machines, install `PostgreSQL for Windows <https://www.postgresql.org/download/windows/>`_. (Tested with the EnterpriseDB interactive installer for PostgreSQL v 9.6). Optionally, you can add the PostgreSQL bin folder (e.g. C:\Program Files\PostgreSQL\9.6\bin) to Path to make later steps slightly simpler:
   
     * Access the Environment Variables window: Control Panel > System and Security > System > Advanced System Settings > Advanced tab > Environment Variables (or Windows Search for "edit environment variables")

     * Either in User Variables (if you would like this addition to Path to be local to the current Windows user) or in System Variables (if you would like this addition to Path to apply to all users on your machine), click the Path line, and then click ``Edit...``.

     * Click ``New`` and paste the PostgreSQL bin folder directory.

#. Install web2py. The easiest way to do so is to download the **Source Code** (NOT the binaries) distribution from http://www.web2py.com/init/default/download. `Here <http://www.web2py.com/examples/static/web2py_src.zip>`_ is a direct link to the zip archive. After you download it, extract the zip file to some folder on your hard drive. (web2py requires no real "installation").  I avoid the web2py.app installation on OS X as it messes with the Python path.  On Windows, the web2py.exe is also problematic because it won't find modules installed in a virtualenv.

#. Get familiar with the Runestone Components, which were installed with pip. They come from https://github.com/RunestoneInteractive/RunestoneComponents and there are good quick start instructions there. If you might be contributing to RunestoneComponents as well, then please fork this repository and then do a local clone onto your machine, but clone it into a different directory than where you will clone RunestoneServer in the next step. For additional information on installing RunestoneComponents, please refer to the documentation included in that repository. If you do not clone a local copy of RunestoneComponents onto your machine, then the master version on GitHub will be used during server setup.

#. Clone the https://github.com/RunestoneInteractive/RunestoneServer repository **into the web2py/applications directory**. If you might be contributing to the project, please fork this repository first and then do a local clone onto your machine, in the web2py/applications. You will contribute back to the project by making pull requests from your fork to this one.  When you make the clone you should clone it into ``runestone`` rather than the default ``RunestoneServer`` .  All the web2py stuff is configured assuming that the application will be called **runestone**.

   There are a couple of prerequisites you need to satisfy before you can build and use this
   eBook. The easiest/recommended way is to use `pip <http://www.pip-installer.org/en/latest/>`_. You can simply install all dependencies by running the following command in main runestone directory:

   ::

       # cd /path/to/web2py/applications
       # git clone https://github.com/RunestoneInteractive/RunestoneServer runestone
       # cd runestone
       # pip install -r requirements-dev.txt

#. Clone the book that you want to use, **into the web2py/applications/runestone/books** directory. You can see some of the available books at https://github.com/RunestoneInteractive. Again, if you might contribute back to the book, please fork the book repository first and then do a local clone onto your machine.

#. Set up your local database

   * Configure Postgresql (or you can try mySQL, but there may be some issues with field lengths with that.)

   * Create a database

     * For Ubuntu you will need to do the following first:

       ::

           $ sudo -i -u postgres
           $ postgres@ubuntu:~$ createuser --interactive -P
           Enter name of role to add: <your name here>
           Enter password for new role: <a password for this user>
           Enter it again: <again>
           Shall the new role be a superuser? (y/n) y
           Password: <password for the default, postgres user>

     * For Windows, the equivalent of the above is using the `-U postgres <https://www.postgresql.org/docs/9.6/static/app-createdb.html>`_ flag to run all commands in the ``postgres`` role, which is automatically created during installation.

       ::

           C:\> "C:\Program Files\PostgreSQL\9.6\bin\createuser" --interactive -U postgres -P
           Enter name of role to add: <your name here>
           Enter password for new role: <a password for this user>
           Enter it again: <again>
           Shall the new role be a superuser? (y/n) y
           Password: <password for the default, postgres user>

       If you added PostgreSQL to Path, then you can simplify the above command to ``createuser --interactive -U postgres -P``.

     * On both Mac and Ubuntu you can now do the following, and enter the password for the default, postgres user (not for the newly-created user). For Windows, the equivalent is to use ``"C:\Program Files\PostgreSQL\9.6\bin\createdb" --owner=<yournamehere> -U postgres runestone``. Again, if you added PostgreSQL to Path, then you can use the simplified command ``createdb --owner=<yournamehere> -U postgres runestone``.

   ::

       $ createdb --owner=<yournamehere> runestone

       $ exit

       psql runestone
       psql (9.5.3)
       Type "help" for help.

       runestone=# \q
       $

   * Figure out your database connection string. It will be something like ``postgresql://username:passwd@localhost/dbname``

   * Tell web2py to use that database:

     * If you're running https, edit ``settings.server_type`` in ``web2py/applications/runestone/models/0.py``.
     * Set and export environment variable for ``DBURL`` -- Note the url format for web2py is different from sqlalchemy.  use `postgres` for web2py and `postgresql` for sqlalchemy.  example:  `postgresql://username:pw@host/database` where pw may be empty, and `database` is the database you created above, `runestone`.
     * Set and export environment variable ``WEB2PY_CONFIG``. If set to production, it will get the database connection string from DBURL. If set to development, it will get the database connection string from DEV_DBURL. If set to test, it will get it from TEST_DBURL.
     * Set and export environment variable ``WEB2PY_MIGRATE``. If set to Yes, web2py will check on each page load whether any database migrations are needed and perform them. If set to No, web2py will just assume that models match the database. If set to Fake, web2py will try to update the metadata it maintains about the database tables to match the models, but will not make any changes to the database; use that setting only for repairs when something has gone wrong.
     * You can confirm that you have set the environment variable and database connection string correctly using ``psql %DBURL%``, and then to exit this command, use ``\q``.
     * If you want to customize other settings you can create a file ``applications/runestone/models/1.py`` using ``models/1.py.prototype`` as the template.  If you have your environment variables set up as explained above you probably won't need to worry about this for your initial setup.

   ::

       export WEB2PY_CONFIG=production # or development or test
       export WEB2PY_MIGRATE=Yes
       export DBURL=postgresql://username:pw@host/database
       export TEST_DBURL=postgresql://username:pw@host/database
       export DEV_DBURL=postgresql://username:pw@host/database
       # For Windows, use the 'set' command instead of 'export', e.g. 'set WEB2PY_CONFIG=production'

   ::

       C:\> "C:\Program Files\PostgreSQL\9.6\bin\psql" %DBURL%
       psql (9.6)
       Type "help" for help.
       runestone=# \q

#. run ``rsmanage initdb``  -- This will initialize the database so you can build your first book.  The rsmanage command was installed when you ran ``pip install -r requirements.txt`` in a previous step.  If you are upgrading you should run ``pip install -e rsmanage`` from the applications/runestone directory. If you are developing and wanting to test a change, then use ``rsmanage initdb --reset`` to close and reinitialize the database, incorporating recent changes.


   .. important:: Database errors

      If you get an error message that the session table already exists, you need to go into the database and drop the table.
      If you get other error messages about tables that either exist or do not exist when they should or should not, then your database is out of sync with the data in your databases folder created by web2py.  This is not a happy spot to be in.  `rsmanage initdb --reset` will definitely get things back in order for a new installation.

      If this is an old installation and you don't want to lose any data the you can try setting the ``WEB2PY_MIGRATE`` variable to 'Fake' But, this may cause cause even more problems, so only use it if you really know what changes you have made to the database schema and why.  You may need to study sql.log to figure out which tables need to be migrated by hand.



#. Build the book.

   ::

       $ cd web2py/applications/runestone/books/<your book>
       $ runestone build
       $ runestone deploy


   * At the end of the build step it should say ``trying alternative database access due to  No module named pydal`` and then, if things are working correctly, start outputting the names of the chapters.

#. Additional Steps for TextBook as a Service (Build your Own Course)

This step is somewhat optional even for developers, depending on what you are working on. But if you want to be able to click on the build a course button you'll need to do the following.

    ::

        $ cd web2py
        $ cp applications/runestone/scripts/start .
        $ cp applications/runestone/scripts/run_scheduler.py .

Now you will want to edit the start script according to your setup.  Then use the start script to start web2py and the scheduler together.  Do not just run `python web2py.py` directly.

More on Environment Variables
-----------------------------

There are a few environment variables that you can use to control the runestone server out of the box:

* ``WEB2PY_CONFIG`` You can set this to production, development, or test.  Each mode can have a corresponding database connection environment variable.  They are:
* for development use ``DEV_DBURL``
* for test use ``TEST_DBURL``
* for production use ``DBURL``   Yes, its not quite consistent, but its backward compatible for the way we have been doing things.


Create an account for yourself
------------------------------

There are two methods you can use here. If the book you built above is thinkcspy or pythonds then there is an easy method.  If you built some other custom book then it's a bit more work.

The Easy Way
````````````

* restart web2py if it's not running
* go to localhost:8000/runestone
* click on the register button

The Harder Way
``````````````

* restart web2py if it's not running
* go to  localhost:8000/runestone/appadmin

* create a course for the book

  * insert new courses
  * course_id can be blank
  * course name should be your book name, the directory name inside books/ (no spaces)

    * date is in format 2015-08-29
    * institution doesn't matter
    * base course should be same as course name

* create an account for yourself

  * insert new auth_user
  * Course name should be the course name from above (not a number)
  * Do *not* make up a registration key or a reset password key; leave them blank

* Make yourself the instructor for the course.

  * insert new course_instructor
  * Course is the *number* for the course (probably 5 if you just inserted one additional course)


