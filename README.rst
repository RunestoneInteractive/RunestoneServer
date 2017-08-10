Runestone Interactive Server and API
====================================

.. image:: https://badge.waffle.io/RunestoneInteractive/RunestoneServer.png?label=ready&title=Ready
   :target: https://waffle.io/RunestoneInteractive/RunestoneServer
   :alt: 'Stories in Ready'

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/bnmnetp/runestone
   :target: https://gitter.im/bnmnetp/runestone?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge


.. |buildstatus| image:: https://drone.io/github.com/bnmnetp/runestone/status.png

Build Status |buildstatus|

Relationship to other Runestone components
------------------------------------------

If you just want to use Runestone's capabilities to build pre-existing books or to make your own books using Sphinx and directives like ActiveCode, then you won't need this repository at all.

This repository has the extra materials needed for running a web2py server with extra features for running courses using Runestone books and tools.


Installation
------------

#. Install python.

   First, make sure you have Python 2.7 installed.  Web2py has not yet been ported to Python3.  Even if you don't care about the web2py part of the install, the version of paverutils on pypi is still a Python 2.x package, although the development version is now at 3.x.

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
   
   **OS X**
   
   On an OS X installation You must install Xcode and the command line tools.  Free from the app store.  Then, I recommend you install homebrew (http://brew.sh)  then run the following commands:
   
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
   
   On Windows machines, install `PostgreSQL for Windows <https://www.postgresql.org/download/windows/>`_. (Tested with the EnterpriseDB interactive installer for PostgreSQL v 9.6).

#. Install web2py. The easiest way to do so is to download the **Source Code** distribution from http://www.web2py.com/init/default/download. `Here <http://www.web2py.com/examples/static/web2py_src.zip>`_ is a direct link to the zip archive. After you download it, extract the zip file to some folder on your hard drive. (web2py requires no real "installation").  I avoid the web2py.app installation on OS X as it messes with the Python path.  On Windows, the web2py.exe is also problematic because it won't find modules installed in a virtualenv.

#. Get familiar with the Runestone Components, which were installed with pip. They come from https://github.com/RunestoneInteractive/RunestoneComponents and there are good quick start instructions there.

#. Clone this repository **into the web2py/applications directory**. If you might be contributing to the project, please fork this repository first and then do a local clone onto your machine, in the web2py/applications. You will contribute back to the project by making pull requests from your fork to this one.  When you make the clone you should clone it into ``runestone`` rather than the default ``RunestoneServer`` .  All the web2py stuff is configured assuming that the application will be called **runestone**.

   There are a couple of prerequisites you need to satisfy before you can build and use this
   eBook. The easiest/recommended way is to use `pip <http://www.pip-installer.org/en/latest/>`_. You can simply install all dependencies by running the following command in main runestone directory:
   
   ::
   
       # cd /path/to/web2py/applications
       # git clone https://github.com/RunestoneInteractive/RunestoneServer runestone
       # cd runestone
       # pip install -r requirements.txt

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
       
     * For Windows, use the `-U postgres <https://www.postgresql.org/docs/9.6/static/app-createdb.html>`_ flag to run all commands in the ``postgres`` role, which is automatically created during installation.
     
       ::
     
           C:\> "C:\Program Files\PostgreSQL\9.6\bin\createuser" --interactive -U postgres -P
           Enter name of role to add: <your name here>
           Enter password for new role: <a password for this user>
           Enter it again: <again>
           Shall the new role be a superuser? (y/n) y
           Password: <password for the default, postgres user>
   
     * On both Mac and Ubuntu you can now do the following; for Windows, use ``"C:\Program Files\PostgreSQL\9.6\bin\createdb" --owner=<yournamehere> -U postgres runestone``. Enter the password for the default, postgres user (not for the newly-created user).
   
   ::
   
       $ createdb --owner=<yournamehere> runestone
   
       $ exit
   
       psql runestone
       psql (9.5.3)
       Type "help" for help.
   
       runestone=# \q
       $
   
   * Figure out your database connection string. It will be something like ``postgres://username:passwd@localhost/dbname``
   
   * Tell web2py to use that database:
   
     * Create a file ``applications/runestone/models/1.py``, with the following line: ``settings.database_uri = '<your_connection_string>'``. NOTE: Don't put this inside an if statement, like it shows in ``models/1.prototype``.
     * If you're running https, edit ``settings.server_type`` in ``models/0.py``.
     * Set and export environment variable for DBURL -- Note the url format for web2py is different from sqlalchemy.  use `postgres` for web2py and `postgresql` for sqlalchemy.  example:  `postgresql://username:pw@host/database` where pw may be empty.
      
#. Run web2py once, so that it will create all the tables.

   * cd web2py/
   * python web2py.py
   * Then you must access http://localhost:8000/runestone one time so that the models load and create the tables in the database.

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
  * cohort id should be "id"
  * Course name should be the course name from above (not a number)
  * Do *not* make up a registration key or a reset password key; leave them blank

* Make yourself the instructor for the course.

  * insert new course_instructor
  * Course is the *number* for the course (probably 5 if you just inserted one additional course)



Documentation
-------------

Documentation for the project is on our official `documentation site <http://runestoneinteractive.org/build/html/index.html>`_  This includes
the list of dependencies you need to install in order to build the books included in the repository, or to set up
a complete server environment.

The Runestone Tools are not only good for authoring the textbooks contained in this site, but can also be used for:

* Making your own lecture materials
* Making online quizzes for use in class
* Creating online polls for your course

What's New
----------

* We just recently updated the ``activecode`` directive to support two new languages: Javascript and HTML.

How to Contribute
-----------------

#. Get a github (free) account.
#. Make a fork of this project.  That will create a repository in your
   account for you to have read/write access to.  Very nice, complete
   instructions for making a fork are here:  ``https://help.github.com/articles/fork-a-repo``
#. Clone the repository under your account to your local machine.
#. Check the issues list, or add your own favorite feature.  commit and pull to your fork at will!
#. test
#. Make a Pull Request.  This will notify me that I should look at your changes and merge them into the main repository.
#. Repeat!


How to Contribute $$
--------------------

As our popularity has grown we have server costs.  We
were also able to make great progress during the Summer of 2013
thanks to a generous grant from ACM-SIGCSE that supported one of our
undergraduate students. It would be great if we could have a student
working on this all the time.

If this system or these books have helped you, please consider making a small
donation using `gittip <https://www.gittip.com/bnmnetp/>`_


More Documentation
------------------

I have begun a project to document the `Runestone Interactive <http://docs.runestoneinteractive.org/build/html/index.html>`_ tools

* All of the Runestone Interactive extensions to sphinx:

  * Activecode -- Interactive Python in the browser
  * Codelens  -- Step through code examples and see variables change
  * mchoicemf  -- multiple choice questions with feedback
  * mchoicema  -- multiple choice question with multiple answers and multiple feedback
  * fillintheblank  -- fill in the blank questiosn with regular expression matching answers
  * parsonsproblem  -- drag and drop blocks of code to complete a simple programming assignment
  * datafile -- create datafiles for activecode

* How to write your own extension for Runestone Interactive

Enable Bug Reporting on Github
------------------------------

The Runestone server now has a controller to allow users to enter bug reports without needing a github account.  But for this to work you will need to configure ``settings.github_token`` in ``models/1.py``

Creating Your Own Textbook
--------------------------

To find instructions on using the Runestone Tools to create your own interactive textbook, see the
file in this directory named README_new_book.rst.


Browser Notes
-------------

Note, because this interactive edition makes use of lots of HTML 5 and Javascript
I highly recommend either Chrome, or Safari.  Firefox 6+ works too, but has
proven to be less reliable than the first two.  I have no idea whether this works
at all under later versions of Internet Explorer.
