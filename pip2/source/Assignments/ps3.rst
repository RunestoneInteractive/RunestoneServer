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


Week 3: ends September 21
=========================

For this week, you have the following graded activities:

1. Do the multiple choice questions and exercises in the textbook chapters, including the ones at the bottom of the chapters, below the glossary. Don't forget to click Save for each of the exercises, and always access the textbook by clicking on the link from cTools, so that you'll be logged in.
   
   * Before Tuesday's class: 
        * Read :ref:`Iteration<iteration_chap>`, and do the exercises in that chapter 
   
   * Before Thursday's class:
      * :ref:`Conditionals <conditionals_chap>`
      * :ref:`File Input/Output <files_chap>` (read the Selection/Conditionals chapter first, or you won't be able to do the last exercise...)
      * If you have a Windows machine, install the git bash command line. :ref:`Installing Git <install_git_bash>`

#. Reading responses

   * By Wednesday night: 
      * Read chapter 3 of The Most Human Human. 
      * Answer :ref:`Reading Response 4 <reading_response_4>`. 

#. Problem set **Due:** **Sunday, September 21st at 5 pm**

   * Do the Unix Problems part of the problem set: :ref:`Unix Problems (1) <unix_pset3>`
   
   * Save answers to the exercises in Problem Set 1: :ref:`Problem Set 3 <problem_set_3>` 

.. _reading_response_4:

Reading Response
----------------

If you had to give up either your left-brain functions or your right-brain functions, which would you give up? Is the one you wouldn't give up the "soul" of who you really are? 

.. activecode:: rr_4_1
   :nocanvas:

   # Fill in your answer on the lines between the triple quotes
   s = """
   """
   print s


.. _unix_pset3:

Unix Problems
-------------

The following problems include instructions for you to follow in your Terminal application, if you have a Mac, or in Git Bash, if you have Windows (:ref:`instructions for installing git bash <install_git_bash>`). Each one requires you to take a screenshot of the result and upload all these screenshots to **Unix Problems (PS3)** on our course CTools page. (CTools > SI 106 002 > Assignments > Unix Problems (PS3))


To take a screenshot, 

**Mac:** Press ``Control`` + ``Shift`` + ``4`` and drag to create a screenshot of the part of your screen you drag the window over. It will be saved to your Desktop.

**Windows:** Launch the program ``Snipping tools`` and use it to take a screen shot of all or part of the screen. **Please save it as a .JPG or .PNG file!**

In the Mac Finder or Windows Explorer, create a folder called ``106``. You may create this folder on the Desktop, or anywhere in your directory system that you would like, following your usual way of organizing folders on your computer. Inside the 106 folder, create a subfolder called ``ps3``. Use a text editor to create a file called ``test.py``. It doesn't matter what text you put in the file.  

#. Use the Finder or Windows Explorer to figure out what the full path is for the 106/ps3 folder. In a Terminal window (Mac) or git bash command window (Windows), use the ``cd`` command to go to your 106/ps3 folder. Then use the ``ls`` command to list all of the files in this directory, presumably just test.py unless you also added some other file. Then use the ``cd ..`` command to connect to the parent directory, 106, and use ``ls`` again to show what's in that directory. Finally, use ``cd ps3`` to go back to the ps3 directory. Take a screenshot of the window, showing a transcript of everything you typed and the responses, save it as ``unix_ps3_1.png`` or ``unix_ps1.jpg``, and upload it to CTools.

#. Use the Unix commands you've learned in this chapter to go to your ``Desktop`` directory. Take a screenshot of the result that shows you've gotten to ``Desktop``, save it as ``unix_ps3_2.png`` or ``unix_ps3_2.jpg``, and upload it it to CTools.

(Remember that you can find a lot of familiar things in your home directory... that's where Desktop directories are usually found, in most people's file systems!)


.. _problem_set_3:

Problem Set
-----------

**Instructions:** Write the code you want to save in the provided boxes, and click **save** for each one. The last code you have saved for each one by the deadline is what will be graded.

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


3. Write code to print out each element of the list ``several_things``. Then, write code to print out the TYPE of each element of the list called ``several_things``.

.. tabbed:: ps3_pb3

  .. tab:: Problem

    .. activecode:: ps_3_3

       several_things = ["hello", 2, 4, 6.0, 7.5, 234352354, "the end", "", 99]
       
       ====
       import test
       print "\n\n---\n"
       print "(There are no tests for this problem.)"

  .. tab:: Solution

    .. activecode:: ps_3_3s

      several_things = ["hello", 2, 4, 6.0, 7.5, 234352354, "the end", "", 99]
     
      for x in several_things:
        print x

      print "--" # adding this extra print just prints another line with the string "--" in between
      # not necessary! this is only there so it's very clear for you to see if you run this

      for yzb in several_things:
        print type(yzb)

      ====
      import test
      print "\n\n---\n"
      print "(There are no tests for this problem.)"



4. See the comments for directions.

.. tabbed:: ps3_pb4

  .. tab:: Problem

    .. activecode:: ps_3_4

       sent = "The magical mystery tour is waiting to take you away."
       
       # Write a comment explaining how you would define what a word is for a computer.
       
       # Write code that assigns a variable word_list to hold a LIST of all the 
       # WORDS in the string sent. It's fine if words include punctuation.
       # Hint: use the split method
       
       ====
       
       import test
       print "\n\n---\n"
       test.testEqual(word_list,sent.split())

  .. tab:: Solution

    .. activecode:: ps_3_4s

       sent = "The magical mystery tour is waiting to take you away."
       
       # Write a comment explaining how you would define what a word is for a computer.
       # A word is basically any set of characters besides whitespace separated by whitespace

       # Write code that assigns a variable word_list to hold a LIST of all the 
       # WORDS in the string sent. It's fine if words include punctuation.
       # Hint: use the split method

       word_list = sent.split() # default use of .split() method breaks on any group of whitespace
       
       ====
       
       import test
       print "\n\n---\n"
       test.testEqual(word_list,sent.split())
   

5. Write code to print out each element of the list stored in ``excited_words``, BUT print out each element **without** its ending punctuation. You should see:

``hello``

``goodbye``

``wonderful``

``I love Python``

(Hint: remember string slicing!)


.. tabbed:: ps3_pb5

  .. tab:: Problem
      
    .. activecode:: ps_3_5

       excited_words = ["hello!", "goodbye!", "wonderful!", "I love Python?"]

       # Now, write code to print out each element of the list stored in excited_words,
       # BUT print out each element WITHOUT the ending punctuation.
       # Hint: remember string slicing? 
       
       ====
       
       import test
       print "\n\n---\n"
       print "(There are no tests for this problem.)"

  .. tab:: Solution

    .. activecode:: ps_3_5s

       excited_words = ["hello!", "goodbye!", "wonderful!", "I love Python?"]

       # Now, write code to print out each element of the list stored in excited_words,
       # BUT print out each element WITHOUT the ending punctuation.
       # Hint: remember string slicing? 

       for ib in excited_words:
          print ib[:-1]
       
       ====
       
       import test
       print "\n\n---\n"
       print "(There are no tests for this problem.)"




6. Follow the directions in the comments!

.. tabbed:: ps3_pb6

  .. tab:: Problem

    .. activecode:: ps_3_6

       rv = """Once upon a midnight dreary, while I pondered, weak and weary,  
         Over many a quaint and curious volume of forgotten lore,  
         While I nodded, nearly napping, suddenly there came a tapping,   
         As of some one gently rapping, rapping at my chamber door.   
         'Tis some visitor, I muttered, tapping at my chamber door;           5
         Only this and nothing more."""
       
       # Write code to assign the number of characters in the string rv to the variable num_chars.
       
       # Write code to assign the number of words in the string rv to the variable num_words. 
       ## Hint: use the .split() method 
       
       ====
       
       import test
       print "\n\n---\n"
       test.testEqual(num_chars,len(rv))
       test.testEqual(num_words,len(rv.split()))

  .. tab:: Solution

    .. activecode:: ps_3_6s

     rv = """Once upon a midnight dreary, while I pondered, weak and weary,  
       Over many a quaint and curious volume of forgotten lore,  
       While I nodded, nearly napping, suddenly there came a tapping,   
       As of some one gently rapping, rapping at my chamber door.   
       'Tis some visitor, I muttered, tapping at my chamber door;           5
       Only this and nothing more."""
     
     # Write code to assign the number of characters in the string rv to the variable num_chars.
     num_chars = len(rv)
     
     # Write code to assign the number of words in the string rv to the variable num_words. 
     ## Hint: use the .split() method 

     num_words = len(rv.split())
     
     ====
     
     import test
     print "\n\n---\n"
     test.testEqual(num_chars,len(rv))
     test.testEqual(num_words,len(rv.split()))  


7. Write code to open the file we've included in this problem set, ``about_programming.txt``, and print it out, line by line. (Don't worry about the blank lines that will appear.)

The first two lines should look like this:

   Computer programming (often shortened to programming) is a process that leads from a
  
   original formulation of a computing problem to executable programs. It involves

.. tabbed:: ps3_pb7

  .. tab:: Problem

    .. activecode:: ps_3_7

       # Write your code here.
       # Don't worry about extra blank lines between each of the lines
       # (but if you want to get rid of them, you can try out the .strip() method)

       ====

       import test
       print "\n\n---\n"
       print "There are no tests for this problem."

  .. tab:: Solution

    .. activecode:: ps_3_7s

     # Write your code here.
     # Don't worry about extra blank lines between each of the lines
     # (but if you want to get rid of them, you can try out the .strip() method)

     f = open("about_programming.txt", "r")
     fr = f.readlines() # this is a list of strings, each string is a line of the content in the file, including a newline character

     for lp in fr:
        print lp

     ====

     import test
     print "\n\n---\n"
     print "There are no tests for this problem."


8. Now write code to open the file ``about_programming.txt`` and assign the **number of lines** in the file to the variable ``file_lines_num``.

.. tabbed:: ps3_pb8

  .. tab:: Problem

    .. activecode:: ps_3_8

       # Write your code here.

       ====

       import test
       print "\n\n---\n"
       test.testEqual(file_lines_num,len(open("about_programming.txt","r").readlines()))

  .. tab:: Solution

    .. activecode:: ps_3_8s

     # Write your code here.

     f = open("about_programming.txt","r")
     oranges = f.readlines() # list of strings, each string is a line from that file
     file_lines_num = len(oranges)

     ====

     import test
     print "\n\n---\n"
     test.testEqual(file_lines_num,len(open("about_programming.txt","r").readlines()))


9. **Challenge problem (OPTIONAL, much harder):** write code to find the average (mean) number of words in each line of the file ``about_programming.txt``.

.. tabbed:: ps3_pb9

  .. tab:: Problem

    .. activecode:: ps_3_9

       # Write your code here.

  .. tab:: Solution

    .. activecode:: ps_3_9s

      # Write your code here.

      # There are a couple ways to do this problem. It's pretty hard. (Awesome if you tried it.)

      # Here's the way that uses the accumulation pattern we know, 
      # and does not use some file manipulation tricks we haven't learned. 
      # As almost always, there are multiple ways to solve this problem!

      f = open("about_programming.txt", "r")
      lns = f.readlines()
      num_lines = len(lns) # now we have the total number of lines in the file

      acc_total = 0 # here we initialize our accumulator
      for x in lns: # now let's go through each line of the file in the result of .readlines()
         sp = len(x.split()) # we want to find how many words, things separated by whitespace, are in each line string
         acc_total = acc_total + sp # each time, we want to add that number to our accumulator


      # now we have the total number of lines in the file AND the total number of words in the file, so we need to do some division for the average (the mean)
      avg_num_wrds = float(acc_total)/num_lines
      print avg_num_wrds # now let's print out the answer to see it

   
.. activecode:: addl_functions_3
   :nopre:
   :hidecode:

   def square(num):
      return num**2

   def greeting(st):
      #st = str(st) # just in case
      return "Hello, " + st

   def random_digit():
     import random
     return random.choice([0,1,2,3,4,5,6,7,8,9])
   