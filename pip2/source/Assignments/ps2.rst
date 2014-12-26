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


Week 2: ends September 14
=========================


For this week, you have the following activities:

1. Do the mutliple choice questions and exercises in the textbook chapters, including the ones at the bottom of the chapters, below the glossary. Don't forget to click Save for each of the exercises, and always access the textbook by clicking on the link from cTools, so that you'll be logged in.
   
   * Before Tuesday's class: 
      * Last chance to provide some `info about you </runestone/default/bio>`_ or change the name you want to be called by in class.
      * Read :ref:`Object Instances and Turtle graphics<turtles_chap>`, and do the exercises in that chapter 
   
   * Before Thursday's class:
      * Read :ref:`Sequences <sequences_chap>`, and do the exercises in that chapter
      

#. Reading responses

   * By Monday night: 
      * Read from the beginning through the middle of page 7 of `Minds, Brains, and Programs <https://ctools.umich.edu/access/content/group/a98a2bac-51e6-472a-a68e-b43f85d1e8d1/SearleChineseRoom.pdf>`_, by Richard Searle. It's in the cTools Resources folder, if that link doesn't work. 
      * Answer :ref:`Reading Response 2 <reading_response_2>`.
   
   * By Wednesday night: 
      * Read chapter 2 of The Most Human Human. 
      * Answer :ref:`Reading Response 3 <reading_response_3>`. 

#. Save answers to the exercises in Problem Set 2 (by Sunday night):
   :ref:`Problem Set 2 <problem_set_2>` 

.. _reading_response_2:

Reading Response 2
------------------

What is the connection between the Turing Test and Searle's Chinese Room example?

.. activecode:: rr_2_1
   :nocanvas:

   # Fill in your answer on the lines between the triple quotes
   s = """
   """

What do you think of the "systems reply"? Does the room with you in it understand Chinese?

.. activecode:: rr_2_2
   :nocanvas:

   # Fill in your answer on the lines between the triple quotes
   s = """
   """
   
   
.. _reading_response_3:

Reading Response 3
------------------

If you had to convince someone you were *you*, not just any old human, via text only, what would you do? Relate your answer to something in Chapter 2 of The Most Human Human.

.. activecode:: rr_3_1
   :nocanvas:

   # Fill in your answer on the lines between the triple quotes
   s = """
   """

.. _problem_set_2:

Problem Set
-----------
**Due:** **Sunday, September 14th at 5 pm**

**Instructions:** Write the code you want to save in the provided boxes, and click **save** for each one. The last code you have saved for each one by the deadline is what will be graded.

1. Assign the variable ``fl`` the value of the first element of the string value in ``original_str``. Assign the variable ``last_l`` the value of the last element of the string value in ``original_str``.

.. tabbed:: ps2_pb1

  .. tab:: Problem

    .. activecode:: ps_2_1
       
       original_str = "The quick brown rhino jumped over the extremely lazy fox."

       # assign variables as specified below this line!

       ====
       
       import test
       print "\n\n---\n"
       test.testEqual(fl,original_str[0])
       test.testEqual(last_l, original_str[-1])

  .. tab:: Solution

    .. activecode:: ps_2_1s
       
       original_str = "The quick brown rhino jumped over the extremely lazy fox."

       # assign variables as specified below this line!
       fl = original_str[0]
       last_l = original_str[-1]


       ====
       
       import test
       print "\n\n---\n"
       test.testEqual(fl,original_str[0])
       test.testEqual(last_l, original_str[-1])


2. See comments for instructions.

.. tabbed:: ps2_pb2

  .. tab:: Problem

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
         test.testEqual(len_of_sent,len(sent))
         test.testEqual(short_len,len(short_sent))
         test.testEqual(index_of_v, sent.find('v'))

  .. tab:: Solution

    .. activecode:: ps_2_2s

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
           len_of_sent = len(sent)

           # How long is the string in the variable short_sent?
           # Write code to assign the length of that string to a variable called short_len.
           short_len = len(short_sent)

           # Print out the value of short_len (and len_of_sent, if you want!) so you can see it. 
           print short_len
           print len_of_sent

           # Write a comment below this line to explain why these values are larger than you might expect. Why is the length of short_sent longer than 15 characters?
           # There are characters that humans can't see that still count as part of the length of a string. For example, spaces count, and newlines count.

           # Assign the index of the first 'v' in the value of the variable sent TO a variable called index_of_v. (Hint: we saw a method of the string class that can help with this)
           index_of_v = sent.find('v')

           ====
           
           import test
           print "\n\n---\n"
           test.testEqual(len_of_sent,len(sent))
           test.testEqual(short_len,len(short_sent))
           test.testEqual(index_of_v, sent.find('v'))

3. See comments for instructions again. (Keep in mind: All ordinal numbers in *instructions*, like "third" or "fifth" refer to the way HUMANS count. How do you write code to find the right things?)

.. tabbed:: ps2_pb3

  .. tab:: Problem

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
         test.testEqual(third_elem, num_lst[2])
         test.testEqual(elem_sixth, num_lst[5])
         test.testEqual(num_lst_len,len(num_lst))
         test.testEqual(fifth_type,type(mixed_bag[4]))
         test.testEqual(another_type, type(mixed_bag[0]))

  .. tab:: Solution

    .. activecode:: ps_2_3s

         num_lst = [4,16,25,9,100,12,13]
         mixed_bag = ["hi", 4,6,8, 92.4, "see ya", "23", 23]

         # Assign the value of the third element of num_lst to a variable called third_elem
         third_elem = num_lst[2]

         # Assign the value of the sixth element of num_lst to a variable called elem_sixth
         elem_sixth = num_lst[5]

         # Assign the length of num_lst to a variable called num_lst_len
         num_lst_len = len(num_lst)

         # Write a comment explaining the difference between mixed_bag[-1] and mixed_bag[-2]
         # (you may want to print out those values so you can make sure you know what they are!)
         # They are different types. mixed_bag[-2] is a string literal, but mixed_bag[-1] is an integer.

         # Write code to print out the type of the third element of mixed_bag
         print type(mixed_bag[2])

         # Write code to assign the **type of the fifth element of mixed_bag** to a variable called fifth_type
         fifth_type = type(mixed_bag[4])

         # Write code to assign the **type of the first element of mixed_bag** to a variable called another_type
         another_type = type(mixed_bag[0])

         ====

         import test
         print "\n\n---\n"
         test.testEqual(third_elem, num_lst[2])
         test.testEqual(elem_sixth, num_lst[5])
         test.testEqual(num_lst_len,len(num_lst))
         test.testEqual(fifth_type,type(mixed_bag[4]))
         test.testEqual(another_type, type(mixed_bag[0]))

4. There is a function we are giving you for this problem set that takes two strings, and returns the length of both of those strings added together, called ``add_lengths``. We are also including the functions from Problem Set 1 called ``random_digit`` and ``square`` in this problem set. 

Now, take a look at the following code and related questions, in this code window.

.. tabbed:: ps2_pb4

  .. tab:: Problem

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

  .. tab:: Solution

    .. activecode:: ps_2_4s
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

         # (I haven't printed anything, but feel free if it helps you!)

         # The following questions are based on that code. All refer to the types of the 
         #variables and/or expressions after the above code is run.

         #####################   

         # Write a comment explaining each of the following, after each question.
         # Don't forget to save!

         # What is square? 
         # a function that takes one integer input and returns an integer

         # What type of object does the expression square(len(new_str)) evaluate to?
         # integer

         # What type is z?
         # integer

         # What type is l?
         # integer

         # What type is the expression z-l?
         # integer

         # What type is x?
         # integer

         # What is random_digit? How many inputs does it take?
         # a function, which takes no inputs (it returns an integer, any digit 0-9)

         # What type does the expression x * random_digit() evaluate to?
         # integer (this is an integer * another integer, so it will result in an integer)

         # Given all this information, what type will fin_value hold once all this code is run?
         # integer!

5. Here's another complicated expression, using the Turtle framework we talked about. Arrange these expressions in the order they are executed, like you did in an exercise in Chapter 2 of the textbook. **No solutions are provided for this problem -- we ultimately did not grade this for points. Because it will tell you how it's right or wrong -- keep tryin', play around with it, ask questions if you want!**

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
