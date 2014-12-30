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


Activities through 2/8
======================


You have the following graded activities:

1. Class prep. Don't forget: always access the textbook by clicking on the Textbook link from cTools, so that you'll be logged in and get credit for doing the prep.
   
   * Before Monday's class: 
      * Read :ref:`Dictionaries<dictionaries_chap>`, and do the exercises in that chapter 
      * Read `External tutorial on unix <, >, and |  <http://www.ee.surrey.ac.uk/Teaching/Unix/unix3.html>`_
         * Note: If you're trying out the commands in the tutorial on your own machine, don't be alarmed by the *who* command that is used in one of the examples. It's not very intuitive what it's doing on a single-user computing system like a Mac, and it's not available all in git bash for Windows users.
         * Note: you might also like some of the other pages in the tutorial at that site. 
   
   * Before Wednesday's class:
       * Read :ref:`Accumulating results in dictionaries<dictionary_accum_chap>`, and do the exercises in that chapter
       * Read `External tutorial on unix grep  <http://www.uccs.edu/~ahitchco/grep/>`_
 
#. Reading responses

   * By Tuesday night: 
      * Read *The Most Human Human*, Chapter 5, "Getting out of Book"
      * Answer :ref:`Reading Response 4 <reading_response_4>`. 

#. Problem set **Due:** **Sunday, February 8 at 5 pm**

   * Do the Unix Problem part of the problem set: :ref:`Unix Problems (3) <unix_pset4>`
   
   * Save answers to the exercises in Problem Set 4: :ref:`Problem Set 4 <problem_set_4>` 

Reading Response
----------------

.. _reading_response_5:

Give an example of when you were interacting with someone where you used "book" responses. What's an example of a time when you or the person you were talking to got "out of book" unusually fast?

.. activecode:: rr_5_1
   :nocanvas:

   # Fill in your answer on the lines between the triple quotes
   s = """
   """
   print s

Quick check-in. How are things going for you in this class so far? Feeling overwhelmed? Inspired? Bored? 

.. activecode:: rr_5_2
   :nocanvas:
   
   # Fill in your answer on the lines between the triple quotes
   s = """
   """
   print s
   
   
Unix Problems
-------------

.. _unix_pset4:

Turn these in as screenshots via CTools in the Assignments tab!

#. In the `tutorial on unix <, >, and |  <http://www.ee.surrey.ac.uk/Teaching/Unix/unix3.html>`_,  there are instructions for creating two files called  ``list1`` and ``list2``. Write a single unix command that displays all lines in either file that contain the letter ``p``.

#. Save a file in the ``106`` folder you created a couple weeks ago called ``fun_with_unix.txt``. Now use ``ls``, ``|`` (pipe), and ``grep`` to find all filenames in your folder containing the string ``unix``. (For fun, try this with other substrings and other folders)



Problem Set
-----------

.. _problem_set_4:

.. datafile::  about_programming.txt
   :hide:

   Computer programming (often shortened to programming) is a process that leads from an
   original formulation of a computing problem to executable programs. It involves
   activities such as analysis, understanding, and generically solving such problems
   resulting in an algorithm, verification of requirements of the algorithm including its
   correctness and its resource consumption, implementation (or coding) of the algorithm in
   a target programming language, testing, debugging, and maintaining the source code,
   implementation of the build system and management of derived artefacts such as machine
   code of computer programs. The algorithm is often only represented in human-parseable
   form and reasoned about using logic. Source code is written in one or more programming
   languages (such as C++, C#, Java, Python, Smalltalk, JavaScript, etc.). The purpose of
   programming is to find a sequence of instructions that will automate performing a
   specific task or solve a given problem. The process of programming thus often requires
   expertise in many different subjects, including knowledge of the application domain,
   specialized algorithms and formal logic.
   Within software engineering, programming (the implementation) is regarded as one phase in a software development process. There is an on-going debate on the extent to which
   the writing of programs is an art form, a craft, or an engineering discipline. In
   general, good programming is considered to be the measured application of all three,
   with the goal of producing an efficient and evolvable software solution (the criteria
   for "efficient" and "evolvable" vary considerably). The discipline differs from many
   other technical professions in that programmers, in general, do not need to be licensed
   or pass any standardized (or governmentally regulated) certification tests in order to
   call themselves "programmers" or even "software engineers." Because the discipline
   covers many areas, which may or may not include critical applications, it is debatable
   whether licensing is required for the profession as a whole. In most cases, the
   discipline is self-governed by the entities which require the programming, and sometimes
   very strict environments are defined (e.g. United States Air Force use of AdaCore and
   security clearance). However, representing oneself as a "professional software engineer"
   without a license from an accredited institution is illegal in many parts of the world.

**Instructions:** Write the code you want to save in the provided boxes, and click **save** for each one. The last code you have saved for each one by the deadline is what will be graded.

**Note:** Passing tests for a problem (``Pass``) does not ensure that the problem is 100% correct -- we can only test some things, to provide a bit of feedback as you go.


1. Old McDonald had a farm. He records the animals on his farm in a dictionary called 'animals'. See comments for instructions...

.. activecode:: ps_4_1

   animals = {'cows': 2, 'chickens': 8, 'pigs': 4, 'mice': 72, 'cats': 9,'dogs': 1}

	# Write code to look up the number of chickens 
   # Old McDonald recorded and assign it to the 
   # variable num_chickens. 
   # (Do not hard-code values! num_chickens = 8 will not earn points.)

   # Write code to add the key-value pair "yak":3
   # to the dictionary stored in the variable called animals.

   # Write code to increase the value for the key 
   # "dogs" in the animals dictionary we've provided) by 1.

   ====
   
   import test
   try: 
      test.testEqual(num_chickens, animals['chickens'])
   except:
      print "either num_chickens or animal['chickens'] is undefined"

   try:
      test.testEqual(animals['yak'], 3)
   except:
      print "key 'yak' is not set in dictionary num_chickens"
      
   test.testEqual(animals['dogs'], 2)


2. See comments in code for instructions.

.. activecode:: ps_4_2

   lp = ["hello","arachnophobia","lamplighter","inspirations","ice","amalgamation","programming","Python"]

   # How many characters are in each element of list lp? 
   # Write code to print the length (number of characters)
   # of each element of the list on a separate line. 
   ## (Do not write 8+ lines of code to do this. Use a for loop.)

   # The output you get should be:
   # 5
   # 13
   # 11
   # 12
   # 3
   # 12
   # 11
   # 6

   # Now write code to print out each element of 
   # list lp IF the length of the element is 
   # an even number.

   ====

   print "\n---\n\n"
   print "There are no tests for this problem."


            ====

            print "\n---\n\n"
            print "There are no tests for this problem."


3. Write code to count the number of strings in list ``items`` that have the character ``w`` in it. Assign that number to the variable ``acc_num``. HINT 1: Use the accumulation pattern! HINT 2: the ``in`` operator checks whether a letter or substring is present in a string.

.. activecode:: ps_4_3

  	items = ["whirring", "calendar", "wry", "glass", "", "llama","tumultuous","owing"]


  	====

  	import test
  	print "\n---\n\n"
  	test.testEqual(acc_num,3)


4. Here's another dictionary. Write code to print out each key-value pair in it. Then follow the rest of the instructions in the comments.

.. activecode:: ps_4_4

     nd = {"autumn":"spring", "well":"spring","4":"seasons","23":345}
     
     # Print out each key-value pair. 
     # Remember that printing things with a comma, e.g.
     # print "hello", "everyone" 
     # will print out those things on the same 
     # line with a space in between them.
     
     # Your output should look SOMETHING LIKE 
     # (remember, the pairs could be in any order, 
     # because it's a dictionary):
     # autumn spring
     # 4 seasons
     # 23 345
     # well spring
     
     # Now, write code to increase the 
     # value of key "23" by 5
     
     # Now, write code to print the 
     # value of the key "well".
     
     ====
     
     import test
     test.testEqual(nd["23"],350)



5. We've included the same file in this problem set that we included in the last problem set -- ``about_programming.txt``. Write code to open the file and print out each line in the file that has a "program"-based word (any of the words ``program``, ``programs``, ``programming``, ``programmer``, or ``programmers``) in it.

.. activecode:: ps_4_5

  	# Write your code here!

 
