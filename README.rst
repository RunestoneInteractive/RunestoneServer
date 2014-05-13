Runestone Interactive Tools and Content
=======================================


.. |buildstatus| image:: https://drone.io/github.com/bnmnetp/runestone/status.png

Build Status |buildstatus|

Documentation
-------------
The database contains two tables ``chapters`` and ``sub_chapters`` which are populated using a script by scraping the ``toc.html`` page. In order to run the script, from the command line, navigate to ``runestone/thinkcspy`` and type the command ``python chapterNames.py``
In order to populate the chapter tables for other courses, create a copy of ``chapterNames.py`` file and modify the line
``os.chdir("..\\static\\thinkcspy")``

Documentation for the project is on our official `documentation site <http://docs.runestoneinteractive.org>`_  

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

