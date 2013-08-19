:orphan:

Help for Instructors
====================

If you are an instructor who is wondering what this interactive textbook is all about you may want to take a look at the :doc:`overview`.  This shows you the various features that are incorporated into our interactive textbooks.

If you are thinking about using this book for your course but have some questions then this is a good place to start.  The rest of this help document is structured like a FAQ so you can quickly find the question you may have from the Page menu and hopefully it will be answered here.

Can I build my own course and host it here?
-------------------------------------------

Yes, we are currently hosting many courses for many different institutions around the world.  In fact in 2013 one large institution had 800 students using one of the books.

The best approach is to use our system to build your own textbook.  This gives you several advantages as an instructor including:

* a simple grading interface for homework problems at the end of each chapter
* some simple reports on your students activities within the textbook.
* at a glance information about the multiple choice and fill in the blank questions embedded in the text.


How do I build my own course?
-----------------------------

1.  First you should register yourself as a user on this site.  When you register you must pick a course.  Just use thinkcspy or pythonds, it doesn't matter as that will change when you build your own.
2.  Then go to the `instructors page <http://interactivepython.org/runestone/admin/index>`_.
3.  On this page you will see the links for listing and grading assignments and lots of other things.  Right now those won't show you anything, so move along to the `Create a Custom Course <http://interactivepython.org/runestone/designer>`_ link.
4. Fill in the Project Name.  This should be a short one word description of your course like `luther150a.`  When your students register for the course this is the name they will have to type in to join your particular course.   No Spaces allwed in this name.
5. The description can say a bit more about the course.
6. The big choice is whether to use a ready-made book or to pick and choose sections from the repository of sections.  Most people just choose one of the pre-made books.
7.  Its probably just fine to leave this at today's date.  If you set it into the future and then do some experimenting with assignments and quizzes today you won't be able to see your results because you are only shown things that come after the start date.


Is this site reliable enough to use in class?
---------------------------------------------

Yes.  All of the important parts of the book are served as static pages.  Everything else that happens either uses Javascript right in the browser, or background ajax calls that won't have any impact on the primary text.  We host this on a very reliable service and we monitor our traffic constantly.  In summer 2013 we increased our capacity in anticipation of higher traffic for Fall 2013.


Why doesn't List and Grade Assignments doesn't show anything?
-------------------------------------------------------------

There could be two reasons.

1.  You only see assignments or quiz questions that your students have attempted.  If you or your students haven't attempted any assignments yet then this report will be empty.

2.  Check your course starting date.  If the starting date is in the future you won't see anything.  You can change your course start date `here <http://interactivepython.org/runestone/admin/startdate>`_.


I want to reuse my course from last year, what should I do?
-----------------------------------------------------------

You can either just change your course start date, see above, or you can rebuild your course.   We recommend that you rebuild your course every so often to get the latest bug fixes etc.  Here is the link to `rebuild your course <http://interactivepython.org/runestone/admin/rebuildcourse>`_.

All the data from past terms is still saved in the database so students that want to go back and look at things from their past terms will be able to access their information, but nothing prior to your latest course start date will show up in any of your reports.


How do I update my course to get the latest bug fixes?
------------------------------------------------------

Here is the link to `rebuild your course <http://interactivepython.org/runestone/admin/rebuildcourse>`_.   We recommend that you do this every so often.  The instructors page will show you the current version of our software used to build the thinkcspy and pythonds books.  It will also show you the version for your own course.   If you course is out of date you will also get a flash message in the upper right corner of your browser window.


I was just experimenting and I want to delete my course
-------------------------------------------------------

We are working on an automatic way to delete a course, but its still in testing.  Until then send an email to me bmiller at luther dot edu and I'll remove the course.

What if I want to add a new section or chapter?
-----------------------------------------------

That would be awesome.  This whole book is open source.  You can grab a copy of the source on `github <http://github.com/bnmnetp/runestone>`_.  The source for thinkcspy and pythonds is in the source folder and there is a subfolder for each chapter.  If you want to make a whole new chapter then create a folder and follow the conventions of one of the other chapters.  There is full documentation for the markup language at `docs.runestoneinteractive.org <http://docs.runestoneinteractive.org>`_.  When you are finished make a pull request and we'll review your material and incorporate them into the book.

What if I want to add my own exercises?
---------------------------------------

New exercises are always welcome and we would love to expand the number of exercises.  The simplest way is to go to the `github issues <http://github.com/bnmnetp/runestone/issues>`_ page and file a new issue.  In the description simply include the text for the exercise and which chapter you think it should go in.  We'll take it from there.  After we've added the exercise you can rebuild your book and it will be there.

What version of Python does your book use?
------------------------------------------

Ok, this is a question that has the potential to start nasty religious wars.  The technical answer is that this book uses a version of Python called `Skulpt <http://skulpt.org>`_.  It is entirely written in Javascript so that it runs right in the browser.  We think this is very cool.  Now some poeple get all crazy about whether they should teach Python 3 or Python 2.  The truth is that for CS1 and CS2 it really doesn't matter.  Skulpt can do print with or without parenthesis, and lets face it for CS1 thats really all that matters.   Sure, there are differences, but are you really going to start out by teaching your students about `dict_keys` and how they are different from a `list`.  If so, I think you are cruel and you should teach your students APL.  If you want to slant your teaching toward Python 3, you can do that with this book.  If you want to lean towards 2, you can do that too.


I think there is a bug in your book what should I do?
-----------------------------------------------------

Please let us know!  You can file bug reports on our `github issues page <http://github.com/bnmnetp/runestone/issues>`_.  Thanks!  If you don't have a github account then you can tweet me at iRunestone   or visit our `google.groups discussion <https://groups.google.com/forum/#!forum/runestoneinteractive>`_


I have a question that is not covered here!
-------------------------------------------

1.  Tweet me @iRunestone  
2.  Post the question on our google group
3.  Send me a private email.  bmiller at luther dot edu

