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


Activities through 2/1
======================
 

You have the following graded activities:

1. Class prep. Don't forget: always access the textbook by clicking on the Textbook link from cTools, so that you'll be logged in and get credit for doing the prep.
   
   * Before Monday's class: 
        * Read :ref:`Iteration<iteration_chap>`, and do the exercises in that chapter 
        * Read :ref:`unix cat and less<less_chap>` section of the Unix chapter
   
   * Before Wednesday's class:
      * :ref:`Conditionals <conditionals_chap>`
      * :ref:`File Input/Output <files_chap>` (read the Selection/Conditionals chapter first, or you won't be able to do the last exercise...)
      * :ref:`Understanding Code <understand_code_chap>`

2. Reading responses

   * By Tuesday night: 
      * Read chapter 3 of The Most Human Human. 
      * Answer :ref:`Reading Response 4 <reading_response_4>`. 

3. Problem set **Due:** **Sunday, February 1 at 5 pm**

   * Do the Unix Problem part of the problem set: :ref:`Unix Problems (2) <unix_pset3>`

   * Save answers to the exercises in :ref:`Problem Set 3 <problem_set_3>` 


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



.. _problem_set_3:

.. _unix_pset3:

Unix Problems
-------------

The following problems include instructions for you to follow in your Terminal application, if you have a Mac, or in Git Bash, if you have Windows (:ref:`instructions for installing git bash <install_git_bash>`). Each one requires you to take a screenshot of the result and upload all these screenshots to **Unix Problems (PS3)** on our course CTools page. (CTools > SI 106 002 > Assignments > Unix Problems (PS3))

#. Create a folder ps4 in your 106 directory. Download the file ``sample.txt`` from the cTools Resources>Code directory and save it in your ps4 directory.

#. Connect to the ps4 directory. Run the command ``less sample.txt``. Take a screenshot to show that the command worked for displaying the contents. Upload it to cTools.


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


3. Write code that uses iteration to print out each element of the list ``several_things``. Then, write code to print out the TYPE of each element of the list called ``several_things``.

.. activecode:: ps_3_3

   several_things = ["hello", 2, 4, 6.0, 7.5, 234352354, "the end", "", 99]
   
   ====
   import test
   print "\n\n---\n"
   print "(There are no tests for this problem.)"



4. See the comments for directions.

.. activecode:: ps_3_4

    sent = "The magical mystery tour is waiting to take you away."
    
    # Write a comment explaining how you would define what a word is for
    # a computer.
    
    # Write code that assigns a variable word_list to hold a LIST of all the 
    # WORDS in the string sent. It's fine if words include punctuation.
    # Hint: remember how to split strings?
    
    ====
    
    import test
    print "\n\n---\n"

    try:
        test.testEqual(word_list,sent.split())
    except:
        print "The variable word_list has not been defined"

5. Write code that uses iteration to print out each element of the list stored in ``excited_words``, BUT print out each element **without** its ending punctuation. You should see:

``hello``

``goodbye``

``wonderful``

``I love Python``

(Hint: remember string slicing?)


.. activecode:: ps_3_5

    excited_words = ["hello!", "goodbye!", "wonderful!", "I love Python?"]
   
    # Now, write code that uses iteration to print out each element of the
    # list stored in excited_words,
    # BUT print out each element WITHOUT the ending punctuation.
    # Hint: remember string slicing? 
    
    ====
    
    import test
    print "\n\n---\n"
    print "(There are no tests for this problem.)"


6. See the comments for directions.

.. activecode:: ps_3_6

    rv = """Once upon a midnight dreary, while I pondered, weak and weary,  
      Over many a quaint and curious volume of forgotten lore,  
      While I nodded, nearly napping, suddenly there came a tapping,   
      As of some one gently rapping, rapping at my chamber door.   
      'Tis some visitor, I muttered, tapping at my chamber door;
      Only this and nothing more."""
    
    # Write code to assign the number of characters in the string rv to
    # the variable num_chars.
    
    # Write code to assign the number of words in the string rv to the
    # variable num_words.
    ## Hint: remember how to split strings?
    
    ====
    
    import test
    print "\n\n---\n"
    try:
        test.testEqual(num_chars,len(rv))
    except:
        print "The variable num_chars has not been defined"
    try:
        test.testEqual(num_words,len(rv.split()))
    except:
        print "The variable num_words has not been defined"


7. Write code to open the file we've included in this problem set, ``about_programming.txt``, and print it out, line by line. (Don't worry about the blank lines that will appear.)

The first two lines should look like this:

   Computer programming (often shortened to programming) is a process that leads from an
  
   original formulation of a computing problem to executable programs. It involves

.. activecode:: ps_3_7
       :available_files: about_programming.txt

       # Write your code here.
       # Don't worry about extra blank lines between each of the lines
       # (but if you want to get rid of them, you can try out the .strip() method)

       ====

       import test
       print "\n\n---\n"
       print "There are no tests for this problem."


8. Now write code to open the file ``about_programming.txt`` and assign the **number of lines** in the file to the variable ``file_lines_num``.

.. activecode:: ps_3_8
       :available_files: about_programming.txt

       # Write your code here.

       ====

       import test
       print "\n\n---\n"

       try:
            test.testEqual(file_lines_num,len(open("about_programming.txt","r").readlines()))
       except:
            print "The variable file_lines_num has not been defined"

9. **Challenge problem (OPTIONAL, much harder):** write code to find the average (mean) number of words in each line of the file ``about_programming.txt``.

.. activecode:: ps_3_9
      :available_files: about_programming.txt

      # Write your code here.

       ====

       import test
       print "\n\n---\n"
       print "There are no tests for this problem."
