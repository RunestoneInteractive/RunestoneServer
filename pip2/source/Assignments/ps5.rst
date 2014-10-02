:orphan:

..  Copyright (C) Paul Resnick.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. highlight:: python
    :linenothreshold: 500


Week 5: ends October 5
======================

1. Do the multiple choice questions and exercises in the textbook chapters, including the ones at the bottom of the chapters, below the glossary. Don't forget to click Save for each of the exercises, and always access the textbook by clicking on the link from cTools, so that you'll be logged in.
   
   * Before Tuesday's class: 
      * Read :ref:`Defining Functions<functions_chap>`, and do the exercises in that chapter
      * Read `External tutorial on unix <, >, and |  <http://www.ee.surrey.ac.uk/Teaching/Unix/unix3.html>`_
         * Note: If you're trying out the commands in the tutorial on your own machine, don't be alarmed by the *who* command that is used in one of the examples. It's not very intuitive what it's doing on a single-user computing system like a Mac, and it's not available all in git bash for Windows users.
         * Note: you might also like some of the other pages in the tutorial at that site. 
           
   
   * Before Thursday's class:
       * Read :ref:`While loops<while_chap>`, and do the exercises in that chapter
       * Read :ref:`Debugging tips<debugging_chap>`, and do the exercises in that chapter
       * Read `External tutorial on unix grep  <http://www.uccs.edu/~ahitchco/grep/>`_
       
       
 
#. Reading responses

   * By Monday midnight: 
      * Read *The Most Human Human*, Chapter 10, p.219-237 only (you'll read the rest of the chapter next week). Note: we are skipping some of the other chapters.
      * Answer :ref:`Reading Response 6 <reading_response_6>`. 

#. Problem set **Due:** **Sunday, October 5 at 5 pm**

   * Do the Unix Problem part of the problem set: :ref:`Unix Problems (3) <unix_pset5>`
   
   * Save answers to the exercises in Problem Set 5: :ref:`Problem Set 5 <problem_set_5>` 



Reading Response
----------------

.. _reading_response_6:

Compare a conversation that "stays in book" to one that doesn't. Which has more surprisal? Which would be easier to compress?

.. activecode:: rr_6_1

   # Fill in your response in between the triple quotes
   s = """

   """
   print s

Give an example of compression other than the ones Christian addresses. Explain. Why? In what situations does this occur?

.. activecode:: rr_6_2

   # Fill in your response in between the triple quotes
   s = """

   """
   print s


Unix Problems
-------------

.. _unix_pset5:

Turn these in as screenshots via CTools in the Assignments tab!

#. In the `tutorial on unix <, >, and |  <http://www.ee.surrey.ac.uk/Teaching/Unix/unix3.html>`_,  there are instructions for creating two files called  ``list1`` and ``list2``. Write a single unix command that displays all lines in either file that contain the letter ``p``.

#. Save a file in the ``106`` folder you created a couple weeks ago called ``fun_with_unix.txt``. Now use ``ls``, ``|`` (pipe), and ``grep`` to find all filenames in your folder containing the string ``unix``. (For fun, try this with other substrings and other folders)


Problem Set
-----------

.. _problem_set_5:

.. datafile:: timely_file.txt
	:hide:

	Autumn is interchangeably known as fall in the US and Canada, and is one of the four temperate seasons. Autumn marks the transition from summer into winter.
	Some cultures regard the autumn equinox as mid autumn while others, with a longer temperature lag, treat it as the start of autumn then. 
	In North America, autumn starts with the September equinox, while it ends with the winter solstice. 
	(Wikipedia)


3. Define a function called add_three, which takes one integer as input and returns that integer + 3.

.. activecode:: ps_5_3

   # Write your code here.
   # (The tests for this problem are going to try to CALL the function that you write!)

   ====

   import test
   print "testing if add_three(2) equals 5"
   test.testEqual(add_three(2),5)
   print "testing if add_three(33) equals 36"
   test.testEqual(add_three(33),36)


4. Write code **that will keep printing what the user inputs over and over until the user enters the string "quit".**

.. activecode:: ps_5_4

   # Write code here

   ====
   print "\n---\n\n"
   print "There are no tests for this problem"


5. Take a look at the code below. You'll get an error if you run it as is. Change it so it works!

.. activecode:: ps_5_5

   def subtract_five(inp)
      print inp - 5
      return None
   
   y = subtract_five(9) - 6
   
   
   ====
   
   print "\n---\n\n"
   import test
   print "testing if y is -2"
   test.testEqual(y, -2)


6. Here's another bit of code with a problem. Fix it so it calls change_amounts on some input and prints out the results. Also, add comments about what's going on with the current code that causes a problem.

.. activecode:: ps_5_6

   def change_amounts(yp):
      n = yp - 4
      return n * 7
   
   print yp
   
   ====
   
   print "\n---\n\n"
   print "There are no tests for this problem"


7. Define a function called change_amounts that takes one integer as input. If the input is larger than 10, it should return the input + 5. If the input is smaller than or equal to 10, it should return the input + 2.

.. activecode:: ps_5_7

   # We've started you off with the first line...
   def change_amounts(num_here):
      pass # delete this line and put in your own code for the body of the function.
   
   ====
   
   print "\n---\n\n"
   import test
   print "testing if change_amounts(9) equals 11"
   test.testEqual(change_amounts(9),11)
   print "testing if change_amounts(12) equals 17"
   test.testEqual(change_amounts(12),17)


8. Given the string in the code below, write code to figure out what the most common word in the string is and assign that to the variable ``abc``. (Do not hard-code the right answer.) Hint: dictionaries will be useful here.

.. activecode:: ps_5_8

   s = "Will there really be such a thing as morning in the morning"
   # Write your code here...
   
   ====
   
   print "\n---\n\n"
   import test
   print "testing whether abc is set correctly"
   test.testEqual(abc, 'morning')

9. We've given you another data file in this problem. It's called ``timely_file.txt``. Write code to figure out which is the most common word in the file. Again, save it in the variable abc.

.. activecode:: ps_5_9

   # Write code here!
   
   ====
   
   print "\n---\n\n"
   import test
   print "testing whether abc is set correctly"
   test.testEqual(abc, 'the')


