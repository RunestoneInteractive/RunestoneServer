Runestone Academy Server and API
================================

.. image:: https://runestone.academy/static/images/logo_small.png
    :align: center
    :width: 300

.. image:: https://github.com/RunestoneInteractive/RunestoneServer/actions/workflows/python-app.yml/badge.svg

.. image:: https://coveralls.io/repos/github/RunestoneInteractive/RunestoneServer/badge.png?branch=master
   :target: https://coveralls.io/github/RunestoneInteractive/RunestoneServer?branch=master


.. image:: https://readthedocs.org/projects/runestoneserver/badge/?version=latest
    :target: https://runestoneserver.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status 

**Note:** This repository will be archived very soon.  All Runestone Development has moved to the ``RunestoneInteractive/rs`` monorepo.


Runestone Server Introduction
-----------------------------

The mission of Runestone Academy is to democratize textbooks for the 21st century. To accomplish that mission we make high quality interactive textbooks available for free to all **students.** In the 21st century it is silly to ignore the wonderful possibilities for interactivity in a web browser, so we make great interactive textbooks that engage students in learning. It would also be silly to ignore the rich data that an online textbook can provide to **teachers, authors** and **researchers.** To support these different stakeholders we have built a Learning Engineering and Analytics Portal (LEAP).

What is a LEAP?
***************

* **Learning Engineering** is the systematic application of evidence-based principles and methods from educational technology and the learning sciences to create engaging and effective learning experiences, support the difficulties and challenges of learners as they learn, and come to better understand learners and learning. Everything we do on `Runestone Academy <https://runestone.academy>`_ takes this engineering approach to continuous improvement.

* **Analytics** As an instructor it is key to understand which of your students is struggling, which of them are working hard, which of them are successful or not. Runestone lets you quickly look at a dashboard of student progress to help you decide how to spend your classroom time most effectively. As a researcher or author you want to know what parts of your book are read the most, which questions are effective and which are duds that should be replaced or fixed to make them better.

* **Portal:** Runestone Academy is a portal for online textbooks, students can interact with our books on any device for free. Runestone Academy is a portal for teachers who want to create a course, grade their students work, and monitor their progress all in one place. Runestone Acaademy is a portal for authors and researchers who want to invent new pedagogical strategies and try them out on lots of students while gaining access to anonymous information to help them better understand how students learn.

Our primary stakeholders are students, teachers, authors, and educational researchers.  You might think of what we are trying to accomplish in terms of a virtuous circle of improvement.   Educational Research makes good Open Educational Resources better, which in turn helps teachers teach more effectively, which improves student learning, which drives even more interesting educational research…

.. image:: https://blog.runestone.academy/_images/VirtuousCircle.png


We welcome contributions to all aspects of the Runestone ecosystem.  Our vision is big and our todo list is long.  If you are interested in finding out more about our community see `Our blog page <https://blog.runestone.academy>`_  We have recently received funding from the NSF to grow our community and ecosystem, see `The PROSE Project <https://prose.runestone.academy>`_ to learn more about that project and how you can participate.

We understand that privacy in student learning is paramount.  If you are uncomforable using a cloud based solution to host your courses, You are welcome to fork this source and run your own server.


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

I have begun a project to document the `Runestone Academy <https://runestone.academy/ns/books/published/authorguide/index.html>`_ tools

* All of the Runestone Academy extensions to sphinx:

  * Activecode -- Interactive Python in the browser
  * Codelens  -- Step through code examples and see variables change
  * mchoicemf  -- multiple choice questions with feedback
  * mchoicema  -- multiple choice question with multiple answers and multiple feedback
  * fillintheblank  -- fill in the blank questions with regular expression matching answers
  * parsonsproblem  -- drag and drop blocks of code to complete a simple programming assignment
  * datafile -- create datafiles for activecode

* How to write your own extension for Runestone Academy

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
