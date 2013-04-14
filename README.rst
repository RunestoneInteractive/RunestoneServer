Runestone Interactive Tools and Content
=======================================

Important Notice
----------------

This is the consolidated repository for all work related to our interactive textbook project.  If you were using the
thinkcspy repository and the eBookExtensions repository you will find all of that work here.  Thanks.

Dependencies
------------

There are a couple of prerequisites you need to satisfy before you
can build and use this eBook.

First get Sphinx, Version 1.1.x is current as of this writing.

http://sphinx.pocoo.org

Follow the instructions there to download and install Sphinx.

Next install paver, version 1.2.0 is current as of this writing.  If you have ``pip`` installed its as easy as ``pip install paver`` if not, then follow the instructions `On the paver github page <http://paver.github.com/paver/#installation>`_

Once paver is installed you will also need to install sphincontrib-paverutils, again the easiest route is to use ``pip install sphinxcontrib-paverutils``

**Warning**  The current sphinxcontrib-paverutils is not compatible with Paver 1.2.  either install paver 1.1.4 or clone the repository:  https://bitbucket.org/bnmnetp/sphinx-contrib and run  ``python setup.py install`` in the paverutils directory.


If you want to run a full blown server -- so you can save activecode assignments etc. then you will need to download and install web2py.  http://web2py.com

After you install web2py go to the applications folder and check out this repository.  This will be installed as a web2py application automatically.

Cloning The Runestone Project and its submodules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This project consists of the main repository, plus *submodules* for codelens, parsons-problems, and skulpt.  In order to get all of the source you need you will need to do the following:

::

    $ git clone https://github.com/bnmnetp/runestone.git
    $ cd runestone
    $ git submodule init
    $ git submodule update

If you are using a GUI git client you may simply get prompted to update the submodules and all will be taken care of for you.  Newer versions of git also support::

    $ git clone --recursive https://github.com/bnmnetp/runestone.git


Building the Book
-----------------

Once you the above installed, you can type ``paver allbooks`` from the command
line and that will build the following targets:

* How to Think Like a Computer Scientist
* Problem Solving with algorithms and Data Structures using Python
* A development version of everything combined (devcourse)

You can quickly check the build by opening the file ``static/devcourse/index.html`` in your browser.

Now before you start web2py its convenient to make runestone the default application.  In the top level web2py directory copy routes.example.py to routes.py and Modify the three lines that contain the word runestone to look like this::

	default_application = 'runestone'    # ordinarily set in base routes.py
	default_controller = 'default'  # ordinarily set in app-specific routes.py
	default_function = 'index'      # ordinarily set in app-specific routes.py

	# routes_app is a tuple of tuples.  The first item in each is a regexp that will
	# be used to match the incoming request URL. The second item in the tuple is
	# an applicationname.  This mechanism allows you to specify the use of an
	# app-specific routes.py. This entry is meaningful only in the base routes.py.
	#
	# Example: support welcome, admin, app and myapp, with myapp the default:


	routes_app = ((r'/(?P<app>welcome|admin|app)\b.*', r'\g<app>'),
	              (r'(.*)', r'runestone'),
	              (r'/?(.*)', r'runestone'))


Running the Server
------------------

Once you've built the book using the steps above.  You can start the web2py development server by simply running ::

	python web2py.py.

This will bring up a little gui where you can make up an admin password and click start server.  When the server is running your browswer will open to the welcome application. Unless you've changed the default application as described above.  To see this app simply use the url:  http://127.0.0.1/courselib    -- From there you can register yourself as a user for dev course, which will redirect you to the index for devcourse.  Or if you have built them, you can click on the link for How to think..., or Problem Solving...

If you get an error at this point the most likely reason is that the settings file isn't recognizing your host and is not setting the database correctly.  These lines in models/0.py are important::

	if 'local' in uname()[1] or 'Darwin' in uname()[0]:
        settings.database_uri = 'sqlite://storage.sqlite'
	elif 'webfaction' in uname()[1]:  # production is on webfaction
	        settings.database_uri = 'postgres://production_db:secret@production_server.com/production_db'
	elif 'luther' in uname()[1]:   # this is my beta machine
	        settings.database_uri = 'sqlite://storage.sqlite'
	else:
	        raise RuntimeError('Host unknown, senttings not configured')

For  your own personal development, you want the first clause of the if statment to match.

Final Configuration
-------------------

To use the admin functionalities you are going to want to do one more bit of configuration.  Using the appadmin functionality of web2py.  Open ``http://127.0.0.1:8000/runestone/appadmin``  Login using the password you supplied.  click on the link for ``insert new auth_group`` and add instructor as a role.  Description can be whatever you want.

Now go back to the appadmin/index page and click on ``insert new auth_membership``  seleect yourself, and instructor as the two values and click submit.  You are now an instructor.


How to Contribute
-----------------

#. Get a github (free) account.
#. Make a fork of this project.  That will create a repository in your
   account for you to have read/write access to.  Very nice, complete
   instructions for making a Fork are here:  ``https://help.github.com/articles/fork-a-repo``
#. Clone the repository under your account to your local machine.
#. Check the issues list, or add your own favorite feature.  commit and pull to your fork at will!
#. test
#. Make a Pull Request.  This will notify me that I should look at your changes and merge them into the main repository.
#. Repeat!


More Documentation
------------------

I have begun a project to document the `Runestone Interactive <http://docs.runestoneinteractive.org/build/html/index.html>`_ tools

* All of the runestone interactive extensions to sphinx:

    * Activecode -- Interactive Python in the browser
    * Codelens  -- Step through code examples and see variables change
    * mchoicemf  -- multiple choice questions with feedback
    * mchoicema  -- multiple choice question with multiple answers and multiple feedback
    * fillintheblank  -- fill in the blank questiosn with regular expression matching answers
    * parsonsproblem  -- drag and drop blocks of code to complete a simple programming assignment
    * datafile -- create datafiles for activecode

* How to write your own extension for runestone interactive


Browser Notes
-------------

Note, because this interactive edition makes use of lots of HTML 5 and Javascript
I highly recommend either Chrome, or Safari.  Firefox 6+ works too, but has
proven to be less reliable than the first two.  I have no idea whether this works
at all under later versions of Internet Explorer.

