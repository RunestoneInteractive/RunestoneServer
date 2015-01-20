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


Activities through 1/25
=======================

You have the following graded activities:

1. Class prep. Don't forget: always access the textbook by clicking on the Textbook link from cTools, so that you'll be logged in and get credit for doing the prep.
   
   * No class Monday: MLK holiday
   
   * Before Wednesday's class:
      * Read :ref:`Sequences <sequences_chap>`, and do the exercises in that chapter.
      * If you have a Windows machine, install the git bash command line. :ref:`Installing Git <install_git_bash>`
      * Read :ref:`Command Prompt <command_prompt_sect>` section of the Unix chapter.
      * Read :ref:`Folders and Paths <folders_and_paths_sect>` section of the Unix chapter and do the exercises in it.
      

2. Reading responses

   * By Tuesday night, 1/20: 
      * Read chapter 2 of The Most Human Human. 
      * Answer :ref:`Reading Response 3 <reading_response_3>`. 

.. _reading_response_3:

3. Problem set **Due:** **Sunday, January 25 at 5 pm**
 
   * Do the Unix Problems part of the problem set: :ref:`Unix Problems (1) <unix_pset2>`       
   * Save answers to each of the exercises in :ref:`Problem Set 2 <problem_set_2>` 
   
Reading Response 3
------------------

If you had to convince someone you were *you*, not just any old human, via text only, what would you do? Relate your answer to something in Chapter 2 of The Most Human Human.

.. activecode:: rr_3_1
   :nocanvas:

   # Fill in your answer on the lines between the triple quotes
   s = """
   """
   
.. _unix_pset2:

Unix Problems
-------------

The following problems include instructions for you to follow in your Terminal application, if you have a Mac, or in Git Bash, if you have Windows (:ref:`instructions for installing git bash <install_git_bash>`). Each one requires you to take a screenshot of the result and upload all these screenshots to **Unix Problems (PS2)** on our course CTools page. (CTools > SI 106 002 > Assignments > Unix Problems (PS2))

To take a screenshot, 

**Mac:** Press ``Control`` + ``Shift`` + ``4`` and drag to create a screenshot of the part of your screen you drag the window over. It will be saved to your Desktop.

**Windows:** Launch the program ``Snipping tools`` and use it to take a screen shot of all or part of the screen. **Please save it as a .JPG or .PNG file!**

In the Mac Finder or Windows Explorer, create a folder called ``106``. You may create this folder on the Desktop, or anywhere in your directory system that you would like, following your usual way of organizing folders on your computer. Inside the 106 folder, create a subfolder called ``ps3``. Use a text editor to create a file called ``test.py``. It doesn't matter what text you put in the file.  

#. Use the Finder or Windows Explorer to figure out what the full path is for the 106/ps3 folder. In a Terminal window (Mac) or git bash command window (Windows), use the ``cd`` command to go to your 106/ps3 folder. Then use the ``ls`` command to list all of the files in this directory, presumably just test.py unless you also added some other file. Then use the ``cd ..`` command to connect to the parent directory, 106, and use ``ls`` again to show what's in that directory. Finally, use ``cd ps3`` to go back to the ps3 directory. Take a screenshot of the window, showing a transcript of everything you typed and the responses, save it as ``unix_ps3_1.png`` or ``unix_ps1.jpg``, and upload it to CTools.

#. Use the Unix commands you've learned in this chapter to go to your ``Desktop`` directory. Take a screenshot of the result that shows you've gotten to ``Desktop``, save it as ``unix_ps3_2.png`` or ``unix_ps3_2.jpg``, and upload it it to CTools.

(Remember that you can find a lot of familiar things in your home directory... that's where Desktop directories are usually found, in most people's file systems!)
   

.. _problem_set_2:

Problem Set
-----------
**Due:** **Sunday, Jnauary 25 at 5 pm**

**Instructions:** Write the code you want to save in the provided boxes, and click **save** for each one. The last code you have saved for each one by the deadline is what will be graded.

1. Assign the variable ``fl`` the value of the first element of the string value in ``original_str``. Use string indexing to assign the variable ``last_l`` the value of the last element of the string value in ``original_str``.

.. activecode:: ps_2_1
 
   original_str = "The quick brown rhino jumped over the extremely lazy fox."
   
   # assign variables as specified below this line!
   
   ====
   
   import test
   print "\n\n---\n"
   try:
      test.testEqual(fl,original_str[0])
   except:
      print "The variable fl has not been defined yet"
   try:
      test.testEqual(last_l, original_str[-1])
   except:
      print "The variable last_l has not been defined yet"

2. See comments for instructions.

.. activecode:: ps_2_2

   sent = """
   He took his vorpal sword in hand:
   Long time the manxome foe he sought
   So rested he by the Tumtum tree,
   And stood awhile in thought.
   - Jabberwocky, Lewis Carroll (1832-1898)"""

   short_sent = """
   So much depends
   on
   """

   # How long (how many characters) is the string in the variable sent?
   # Write code to assign the length of the string to a variable called len_of_sent.


   # How long is the string in the variable short_sent?
   # Write code to assign the length of that string to a variable called short_len.


   # Print out the value of short_len (and len_of_sent, if you want!) so you can see it. 


   # Write a comment below this line to explain why these values are larger than you might expect. Why is the length of short_sent longer than 15 characters?


   # Assign the index of the first 'v' in the value of the variable sent TO a variable called index_of_v. (Hint: we saw a method of the string class that can help with this)

   ====
   
   import test
   print "\n\n---\n"
   try:
      test.testEqual(len_of_sent,len(sent))
   except:
      print "The variable len_of_sent has not been defined yet"
   try:
      test.testEqual(short_len,len(short_sent))
   except:
      print "The variable short_len has not been defined yet"
   try:
      test.testEqual(index_of_v, sent.find('v'))
   except:
      print "The variable index_of_v has not been defined yet"


3. See comments for instructions again. (Keep in mind: All ordinal numbers in *instructions*, like "third" or "fifth" refer to the way HUMANS count. How do you write code to find the right things?)

.. activecode:: ps_2_3

   num_lst = [4,16,25,9,100,12,13]
   mixed_bag = ["hi", 4,6,8, 92.4, "see ya", "23", 23]

   # Assign the value of the third element of num_lst to a variable called third_elem

   # Assign the value of the sixth element of num_lst to a variable called elem_sixth

   # Assign the length of num_lst to a variable called num_lst_len

   # Write a comment explaining the difference between mixed_bag[-1] and mixed_bag[-2]
   # (you may want to print out those values so you can make sure you know what they are!)

   # Write code to print out the type of the third element of mixed_bag

   # Write code to assign the **type of the fifth element of mixed_bag** to a variable called fifth_type

   # Write code to assign the **type of the first element of mixed_bag** to a variable called another_type

   ====

   import test
   print "\n\n---\n"
   try:
      test.testEqual(third_elem, num_lst[2])
   except:
      print "The variable third_elem has not been defined"
   try:
      test.testEqual(elem_sixth, num_lst[5])
   except:
      print "The variable elem_sixth has not been defined"
   try:
      test.testEqual(num_lst_len,len(num_lst))
   except:
      print "The variable num_lst_len has not been defined"
   try:
      test.testEqual(fifth_type,type(mixed_bag[4]))
   except:
      print "The variable fifth_type has not been defined"
   try:
      test.testEqual(another_type, type(mixed_bag[0]))
   except:
      print "The variable another_type has not been defined"


4. There is a function we are giving you for this problem set that takes two strings, and returns the length of both of those strings added together, called ``add_lengths``. We are also including the functions from Problem Set 1 called ``random_digit`` and ``square`` in this problem set. 

Now, take a look at the following code and related questions, in this code window.

.. activecode:: ps_2_4
   :include: addl_functions_2
   
   new_str = "'Twas brillig"
   
   y = add_lengths("receipt","receive")
   
   x = random_digit()
   
   z = new_str.find('b')
   
   l = new_str.find("'")
   
   # notice that this line of code is made up of a lot of different expressions
   fin_value = square(len(new_str)) + (z - l) + (x * random_digit())
   
   # DO NOT CHANGE ANY CODE ABOVE THIS LINE
   # But below here, putting print statements and running the code may help you!
   
   # The following questions are based on that code. All refer to the types of the 
   #variables and/or expressions after the above code is run.
   
   #####################   
   
   # Write a comment explaining each of the following, after each question.
   # Don't forget to save!
   
   # What is square? 
   
   # What type of object does the expression square(len(new_str)) evaluate to?
   
   # What type is z?
   
   # What type is l?
   
   # What type is the expression z-l?
   
   # What type is x?
   
   # What is random_digit? How many inputs does it take?
   
   # What type does the expression x * random_digit() evaluate to?
   
   # Given all this information, what type will fin_value hold once all this code is run?

   ====

   print "\n\nThere are no tests for this problem"
 
5. Here's another complicated expression, using the Turtle framework we talked about. Arrange these expressions in the order they are executed, like you did in an exercise in Chapter 2 of the textbook. 

.. sourcecode:: python
   
   import turtle

   ella = turtle.Turtle()
   x = "hello class".find("o") - 1
   ella.speed = 3

  
   ella.move(square(x*ella.speed))

.. parsonsprob:: ps_2_5

   Order the code fragments in the order in which the Python interpreter would evaluate them, when evaluating that last line of code, ``ella.move(square(x*ella.speed))`` (It may help to think about what specifically is happening in the first four lines of code as well.)
   -----
   Look up the variable ella and find that it is an instance of a Turtle object
   =====
   Look up the attribute move of the Turtle ella and find that it's a method object
   =====
   Look up the function square
   =====
   Look up the value of the variable x and find that it is an integer
   =====
   Look up the value of the attribute speed of the instance ella and find that it is an integer
   =====
   Evaluate the expression x * ella.speed to one integer
   =====
   Call the function square on an integer value
   =====
   Call the method .move of the Turtle ella on its input integer
	 
6. Write a program that uses the turtle module to draw something interesting. It doesn't have to be complicated, but draw something different than we did in the textbook or in class. (Optional but encouraged: post a screenshot of the artistic outcome to the Facebook group, or a short video of the drawing as it is created.)

.. activecode:: ps_2_6

   import turtle


.. activecode:: addl_functions_2
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
      
   def add_lengths(str1, str2):
      return len(str1) + len(str2)

   
   