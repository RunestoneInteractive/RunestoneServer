Runestone Interactive Server and API
====================================

.. image:: https://github.com/RunestoneInteractive/RunestoneServer/workflows/Python%20application/badge.svg

.. image:: https://coveralls.io/repos/github/RunestoneInteractive/RunestoneServer/badge.png?branch=master
   :target: https://coveralls.io/github/RunestoneInteractive/RunestoneServer?branch=master


.. image:: https://readthedocs.org/projects/runestoneserver/badge/?version=latest
    :target: https://runestoneserver.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


Runestone Server Introduction
-----------------------------

The Runestone Server has evolved into a streamlined LMS to support interactive textbooks.  The features of the Runestone Server include:

* Serving one or more interactive textbooks
* Creating and Managing a class of students
* Creating Reading Assignments for students
* Creating Problem sets for students
* Grading assignments manually and automatically
* Authoring new questions for the question bank
* Analytics on your students activities
* Checking student progress through the book
* Enabling practice problems for your students based on "spaced repetition"

You are welcome to fork this source and run your own server, but you are also welcome to use the Runestone Server as a free service on `Runestone Academy <https://runestone.academy>`_


Installation
------------

With Docker
***********

The easiest way to deploy Runestone Server is to use `Docker <https://www.docker.com/>`_. Docker automates
installing many of the components needed to provide a functioning server.
Please see complete instructions on the `Docker Deployment ReadTheDocs page <https://runestoneserver.readthedocs.io/en/latest/docker/README.html>`_.


Manual Installation
*******************

It is also possible to manually install Runestone Server. This involves more work up front, but may make any custom modifications you do later a little more straightforward. For instructions, see these `Manual Installation instructions <https://runestoneserver.readthedocs.io/en/latest/docs/installation.html>`_.



Documentation
-------------

Links to documentation for the project are on `runestoneserver.readthedocs.org <http://runestoneserver.readthedocs.org>`_  This includes
the list of dependencies you need to install in order to build the books included in the repository, or to set up
a complete server environment.

The Runestone Tools are not only good for authoring the textbooks contained in this site, but can also be used for:

* Making your own lecture materials
* Making online quizzes for use in class
* Creating online polls for your course


How to Contribute
-----------------

#. See the file `CONTRIBUTING.md` in this directory
#. Get a Github (free) account.
#. Make a fork of this project.  That will create a repository in your
   account for you to have read/write access to.  Very nice, complete
   instructions for making a fork are here:  ``https://help.github.com/articles/fork-a-repo``
#. Clone the repository under your account to your local machine.
#. Check the issues list, or add your own favorite feature.  commit and pull to your fork at will!
#. Make a Pull Request.  This will notify me that I should look at your changes and merge them into the main repository.
#. Repeat!


How to Contribute $$
--------------------

As our popularity has grown we have server costs.
If this system or these books have helped you, please consider making a small
donation using any of the Support links at the top of this page.


More Documentation
------------------

I have begun a project to document the `Runestone Interactive <https://runestone.academy/runestone/static/authorguide/index.html>`_ tools

* All of the Runestone Interactive extensions to sphinx:

  * Activecode -- Interactive Python in the browser
  * Codelens  -- Step through code examples and see variables change
  * mchoicemf  -- multiple choice questions with feedback
  * mchoicema  -- multiple choice question with multiple answers and multiple feedback
  * fillintheblank  -- fill in the blank questions with regular expression matching answers
  * parsonsproblem  -- drag and drop blocks of code to complete a simple programming assignment
  * datafile -- create datafiles for activecode

* How to write your own extension for Runestone Interactive

Enable Bug Reporting on Github
------------------------------

The Runestone server now has a controller to allow users to enter bug reports without needing a Github account.  But for this to work you will need to configure ``settings.github_token`` in ``models/1.py``

Creating Your Own Textbook
--------------------------

To find instructions on using the Runestone Tools to create your own interactive textbook, see the
instructions in the `Runestone Components repository <https://github.com/RunestoneInteractive/RunestoneComponents>`_.

Browser Notes
-------------

Note, because this interactive edition makes use of lots of HTML 5 and Javascript
I highly recommend either Chrome, or Safari.  Firefox 67+ works too.  Reportedly Edge works fine as well.

Python Notes
------------

Python 2.7 reached the end of its life on January 1st, 2020. All of our development is now on Python 3.7 and 3.8.  With the release of docutils 0.15 sphinx no longer runs on 2.7 unless you install docutils 0.14. Sphinx 2.x only supports Python 3.x.  In July 2019 I removed testing for Python 2.7 as it is too much work to try to keep track of dependencies for 2.x and 3.x.  Please upgrade to Python 3.

Researchers
-----------

If you use Runestone in your Research or write about it, please reference ``https://runestone.academy`` and cite this paper:

::

   @inproceedings{Miller:2012:BPE:2325296.2325335,
    author = {Miller, Bradley N. and Ranum, David L.},
    title = {Beyond PDF and ePub: Toward an Interactive Textbook},
    booktitle = {Proceedings of the 17th ACM Annual Conference on Innovation and Technology in Computer Science Education},
    series = {ITiCSE '12},
    year = {2012},
    isbn = {978-1-4503-1246-2},
    location = {Haifa, Israel},
    pages = {150--155},
    numpages = {6},
    url = {http://doi.acm.org/10.1145/2325296.2325335},
    doi = {10.1145/2325296.2325335},
    acmid = {2325335},
    publisher = {ACM},
    address = {New York, NY, USA},
    keywords = {cs1, ebook, sphinx},
   }
