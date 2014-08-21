Runestone ChangeLog
===================

3.1 August 21, 2014
------------------

* Redo the organization of the books so we can automatically populate the database with div_ids for exercises
* Some cleanups to make code coach work a little more cleanly
* Add some links to vimeo videos on common instructor problems

3.0.0 August 16, 2014
---------------------

* **Progress tracking, and cohorts.**  This is one of the major visual changes to the books, thanks to some great work by `Vipul Thackur <http://www.ivipul.com>`_.  The "chapters" have been broken up into subchapters and you can now track your progress through each chapter/sub-chapter on the table of contents.  In addition, there is now the facility to create a study group and to negotiate reading deadlines and have discussions with members of your own cohort.

* **New and improved grading and assignments interface.**  Thanks to `Paul Resnick <http://presnick.people.si.umich.edu/>`_ and his students at the University of Michigan you can now group activities into assignments.  You can also provide comments to students on the programming problems.

* **Custom assignment page.**  As an instructor you can now easily edit an assignments page that is part of your custom course.  This page will allow you to make use of all of the features of the Runestone tools and restructured text to add your own assignments.  I think this feature has great potential to grow into additional custom content in the future so stay tuned.

* **Run in Codelens.**  Sometime earlier this summer `Philip Guo <http://www.pgbovine.net/>`_ added an iframe interface to the awesome Online Python Tutor.  This allowed me to add a button to most of the activecode examples that allow you to also run the example in the `Online Python Tutor <http://pythontutor.com>`_.  You can edit the examples and click the button to run another version.  This feature requires that you have internet access while reading, something I have resisted in the past, but it it seems increasingly difficult to be offline now anyway, so I'm not going to resist anymore.

* **Code Coach.**   Last spring at SIGCSE, Paul Resnick, David Ranum and I spent an afternoon hacking.  The idea was to provide an interface that would allow students to look at the history of any particular programming assignment, and see the differences from one try to the next.  Our hypothesis is that this would be a good teaching tool for an instructor to use with a student to review how they developed a solution and arrived at their current state.  I expanded on the concept a bit this summer by making use of pylint, which points out a number of potential problems that plague beginning programmers.  For example, pointing out "useless statements" when a student forgets their parenthesis on a function call.  My hope is that Code Coach will grow into a fully automated code tutor in the future.

* **Blockly directive.**   I think that blocks based programming languages like `Blockly <https://blockly-demo.appspot.com/static/apps/index.html>`_, and Scratch have great potential to help students develop a mental model or a picture in their mind of how various programming constructs work. So I created this new directive that will let you write blocks language examples and exercises.  My hope was to write a new introduction to How to Think Like a Computer Scientist using Blockly, but there are only so many hours in the summer.  Hopefully I'll make progress on this during the coming months.

* **Activecode support for Javascript and HTML.**  In preparation for a new course I'm teaching this fall, I wanted to be able to have students edit HTML and Javascript examples like we can do with Python.  Now you can.

* **New Book:**  `Programs, Information, People <http://interactivepython.org/runestone/static/pip/index.html>`_.  This book is a new mashup of the How to Think book that Paul Resnick uses in his course in the School of Information by the same title.  I think this is a great alternative to the How to Think book in that it avoids some of the "early math" problems and focuses on information processing using data from the internet.

* **AP Java Review:**  `This book  <http://interactivepython.org/runestone/static/JavaReview/index.html>`_ came on line last spring, but its worth mentioning in this summary.  `Barbara Ericson <http://www.cc.gatech.edu/people/barbara-ericson>`_ at Georgia Tech has put this together and although we can't run any Java examples in the browser the rest of the interactive resources are great for getting ready for the AP exam.

2.0.0  August 6, 2013
---------------------

* Move to Bootstrap for themeing and better mobile device support
* **Activecode**:  Using a <a href="http://skulpt.org">Javascript implementation</a> of Python you can run and modify the examples in the textbook right in the book.  No server connection is required since it is based on javascript and runs right in the browser.
* **Codelens**:  Using the amazing power of the <a href="http://www.pythontutor.com">pythontutor.com</a>  tools you can step through examples one line at a time, forward and backward.  While you are stepping through the code you can see variables and other data structures change values.
* **Parsons Problems: ** For beginning programmers Parson's problems are like refrigerator magnet poetry.  You can provide your students with the statements needed to write a program, but they must put the statements in the correct order.
* **Inline Quizzes: **Each section of the book contains some inline quizzes that allow students to check their understanding of the material.  The quizzes have different feedback for each correct or incorrect answer that try to point students in the right direction. 
* **Online Homework:**   At the end of each chapter are programming assignments.  In this new edition we have provided the answers to the odd numbered questions, and discussion forums for students to exchange ideas or ask questions about the homework problems.  As an instructor, you can grade your students programs on one convenient page.
* **Highlighting**  This is another much requested new feature.  Students can highlight text using the mouse and the highlights magically reappear on any supported browser.  In addition we will remember the students last location in the book and offer to return them to that position when they return.
* There are many other features but the best way to understand what we are doing is to actually have a look at our <a href="http://interactivepython.org/runestone/static/overview/overview.html">overview page</a>, which shows everything I have mentioned here and a lot more in action.

	* Instructors looking for a textbook to use in their own course
	* People who are interested in teaching themselves some computer science and have found our books through google 

Textbooks as a Service
~~~~~~~~~~~~~~~~~~~~~~

When we launched the site last year we decided to not only provide the books free and open for anyone who wanted to read them, but also as a service for instructors who wanted to have their own custom copy of the book where they could track their students progress, review their answers to quizzes, and grade their students homework.   If you want to use our books in your class you are welcome to do so.  You have two options:

* You can use a copy of either book as is with the order of the chapters just as they are on the books linked to above.
* You can try our custom interface where you can mix and match chapters from both books to create your own custom textbook.

Once you have created your own course then you will be able to see the assignments your students have completed right in the textbook.  I find this to be very valuable as an instructor.  For example if I have assigned the students to read and do the quizzes for a particular section, I can simply go to the quiz question and click on the 'Compare Me' button.  As an instructor I will see a summary of the answers my students gave, as well as the details of the answers that each student tried.

Supporting the Independent Learner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Perhaps the biggest surprise of this project is the number of people that have found one of the books through google, and are simply teaching themselves to program.  We are hopeful that some of the new features we have added will help foster a  community of learners so that people just learning to program can talk to others in the same situation.  Some things we hope are particularly helpful include:

* **Answers to odd numbered questions**.  This was probably the number one request I got through email all last year.  How do I know if I did it right?  We decided to risk it and provide the answers, but only to the odd numbered problems.  In addition a student must try to answer the problem at least once before the answer becomes "unlocked"
* **Discussion threads** for homework problems.  Again this may seem like a risky move where students can just publish their answer and others can copy.  But, what we are hoping for is that students will see that there are many ways to get to the "right answer"  There are different approaches and programming styles that can be used to solve the same problem.
* **Compare Me**  Although we aren't sure about the title on the button, the idea is that after answering one of the quiz questions a learner can check on their overall 'grade' for all quiz questions, and see how their answer compared to all the other learners.  We haven't gone so far as to give out badges, but we think this is a nice intermediate approach.

2.0.1  August 16, 2013
----------------------

* Add Version tracking to the instructors page
* Add instructors FAQ
* Bug fixes, especially in course building and rebuilding
* Added javascript validation to keep out course names with spaces
* Remove old references to Google App Engine in the preface


2.1.0 August 21, 2013
---------------------

* Many improvements and cleanups in the data structures text.  Many more examples are runnable now thanks to the many improvements in Skulpt.
* Update to bootstrap 3.0 final
* Update to turtle chapter with more parson's problems.
* Bug fixes


2.1.1 September 15, 2013
------------------------

* Fix use of randrange in lab03 #311
* Shell sort self check answer wrong

2.1.2 September 21, 2013
------------------------

* IMPORTANT:  Bug Fix - random.randrange(X) was not returning a properly constructed Python int.  If you are
using random numbers this is pretty important as it will unexpectedly manifest itself in goofy ways.

2.1.3 September 28, 2013
------------------------

* Add Feedback button to end of chapter homework problems.  This button will show the grade for this assignment, and the average of all assignments.
* Add the ability for instructors to type in comments when they grade assignments.

2.1.4 October 6, 2013
---------------------

* Fix to turtle problem
* Fixes to make audio tours work again


2.1.5 October 13, 2013
----------------------

* Modify max width of content area to improve overall readability
* Add a video preload attribute.   Do not preload videos to save bandwidth and decrease load times.
