Runestone Interactive Tools and Content

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

1. Install python.

First, make sure you have Python 2.7 installed.  Web2py has not yet been ported to Python3.  Even if you don't care about the web2py part of the install, the version of paverutils on pypi is still a Python 2.x package, although the development version is now at 3.x.

There are a couple of prerequisites you need to satisfy before you can build and use this
eBook. The easiest/recommended way is to use `pip <http://www.pip-installer.org/en/latest/>`_.

You can simply install all dependencies by running the following command in main runestone directory:

::

    # pip install -r requirements.txt

Note, development works well with a Python ``virtualenv``  If  you don't have root privileges on your computer I strongly recommend you install ``virtualenv`` and install all of the dependencies there.

On Windows machines, some of the installations may not go smoothly with pip.

* For dulwich, you will need a C++ compiler.
Install Microsoft Visual C++ Compiler for Python 2.7 from http://www.microsoft.com/en-us/download/details.aspx?id=44266.
I had to also run: pip install setuptools --upgrade

* For numpy, you can try the Windows installer from http://sourceforge.net/projects/numpy/postdownload?source=dlp If
that fails, you can try installing from a wheel file at http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy

2. Install web2py. The easiest way to do so is to download the **Source Code** distribution from http://www.web2py.com/init/default/download.
`Here <http://www.web2py.com/examples/static/web2py_src.zip>`_ is a direct link to the zip archive.
After you download it, extract the zip file to some folder on your hard drive. (web2py requires no real "installation").  I avoid the web2py.app installation on OS X as it messes with the Python path.  On Windows, the web2py.exe is also problematic because it won't find modules installed in a virtualenv.

3. Get familiar with the Runestone Components, which were installed with pip. The come from https://github.com/RunestoneInteractive/RunestoneComponents and there are good quick start instructions there.

4. Clone this repository **into the web2py/applications directory**. If you might be contributing to the project, please fork this repository first and then do a local clone onto your machine, in the web2py/applications. You will contribute back to the project by making pull requests from your fork to this one.

5. Clone the book that you want to use, **into the web2py/applications/runestone/books** directory. You can see some of the available books at https://github.com/RunestoneInteractive Again, if you might contribute back to the book, please fork the book repository first and then do a local clone onto your machine.

6. Set up your local database

* Install postgreSQL (or you can try mySQL, but there may be some issues with field lengths with that.)

* Create a database

* Figure out your database connection string. It will be something like ``postgres://username:passwd@localhost/dbname''

* Tell web2py to use that database
    * Create a file applications/runestone/models/1.py, with the following line: ``settings.database_uri = <your_connection_string>``
        * NOTE: Don't put this inside an if statement, like it shows in models/1.prototype
    * on windows, you will also need to edit models/0.py
        * remove the line ``from os import uname``
        * remove the section beginning ``if 'local' in uname()[1] or 'Darwin' in uname()[0]:``
    * You may also need to put the connection string somewhere else, TBD
    * You will need a customization to runestone/modules/chapternames.py
        * (Note: hopefully, this will be fixed in the future so that it automatically reads from models/1.py)
        * In chapternames.py, where it sets dburl = a connection string, put your connection string there.


* Edit /applications/runestone/books/<yourbook>/pavement.py
    * set the master_url variable for your server, if not localhost

# Run web2py once, so that it will create all the tables
    * cd web2py/
    * python web2py.py

# Build the book.


* cd web2py/applications/runestone/books/<your book>

* runestone build

  * At the end, it should say ``trying alternative database access due to  No module named pydal`` and then, if things are working correctly, start outputting the names of the chapters.

* runestone deploy
    * If you're on windows where rsync doesn't work, here's the alternative
        * rm -r applications/runestone/static/<your book name>
        * cd runestone/books/<your book name>
        * mv build/<your book name> ../static/

* Create an account for yourself
    * restart web2py if it's not running
    * go to runestone/appadmin
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
    * make yourself the instructor for the course
        * insert new course_instructor
        * Course is the *number* for the course (probably 5 if you just inserted one additional course)



Documentation
-------------

Documentation for the project is on our official `documentation site <http://docs.runestoneinteractive.org>`_  This includes
the list of dependencies you need to install in order to build the books included in the repository, or to set up 
a complete server environment.

The Runestone Tools are not only good for authoring the textbooks contained in this site, but can also be used for:

* Making your own lecture materials
* Making online quizzes for use in class
* Creating online polls for your course

Whats New
---------

* We just recently updated the ``activecode`` directive to support two new languages.  Javascript and HTML.

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

Notes on running under Windows
------------------------------

As I mentioned up front, I'm not a windows user, But, others have figured out how to get the whole works running under windows anyway.  Here are some tips:

1.  In models.0 you will want to add this:

::

    try:
        from os import uname
    except:
        def uname():
            return ['0', 'windows']


   Now you can add a test for windows, and set your database settings accordingly.

2.  In the pavement.py file we use cp to copy some files into place.  I *think* the equivalent on Windows is copy or copy.exe.

