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


Week 1: ends September 7
========================


For this week, you have the following graded activities:

1. Do the mutliple choice questions and exercises in the textbook chapters, including the ones at the bottom of the chapters, below the glossary. Don't forget to click Save for each of the exercises, and always access the textbook by clicking on the link from cTools, so that you'll be logged in.
   
   * Before Tuesday's class: 
   
   * Before Thursday's class:
      * Fill in a little `info about you </runestone/default/bio>`_ and, optionally, upload a picture that looks like how you look in class, so I can start to learn your names.`
      * Sign up for the `Facebook group <https://www.facebook.com/groups/269032479960344/>`_
      * :ref:`General Intro <the_way_of_the_program>`
      * :ref:`Simple Python Data <simple_python_data>` (except for the last section, on getting input from the user, which you can delay until next week)

#. Reading responses
      * For Thursday, read the intro and chapter 1 of "The Most Human Human".

#. Save answers to the exercises in Problem Set 1:
   :ref:`Problem Set 1 <problem_set_1>` 

.. _response_1:

Reading Response
----------------

If you had to convince someone you were human and not a bot, via text only, what would you do?

.. activecode:: rr_1_1
   :nocanvas:

   # Fill in your answer on the lines between the triple quotes
   s = """
   """



.. _problem_set_1:

Problem Set
-----------
**Due:** **Sunday, September 7th at 5 pm**

**Instructions:** Write the code you want to save in the provided boxes, and click **save** for each one. The last code you have saved for each one by the deadline is what will be graded.

.. tabbed:: ps1_pb1

  .. tab:: Problem

    1. The variable ``tpa`` currently has the value ``0``. Assign the variable ``tpa`` the value ``6`` .

    .. activecode:: ps_1_1

       tpa = 0
       
       ====
       import test
       print "\n\n---\n"
       test.testEqual(tpa, 6)

  .. tab:: Solution

    .. activecode:: ps_1_1s

       tpa = 0 # just reassigning this to 6 is also fine
       tpa = 6

       ====
       import test
       print "\n\n---\n"
       test.testEqual(tpa, 6)


2. Write code to assign the variable ``yb`` to have the same value that variable ``cw`` has. Do not change the first line of code (``cw = "Hello"``), but write code that would work no matter what the current value of ``cw`` is.


.. tabbed:: ps1_pb2

  .. tab:: Problem

    .. activecode:: ps_1_2

       cw = "Hello"
       yb = 0

       ====
       import test
       print "\n\n---\n"
       test.testEqual(cw, yb)

  .. tab:: Solution

    .. activecode:: ps_1_2s

       cw = "Hello"
       yb = 0
       yb = cw

       ====
       import test
       print "\n\n---\n"
       test.testEqual(cw, yb)


3. Write code to print out the type of the variable ``apples_and_oranges``, the type of the variable ``abc``, and the type of the variable ``new_var``.

.. tabbed:: ps1_pb3

  .. tab:: Problem

    .. activecode:: ps_1_3
       
       apples_and_oranges = """hello, everybody
                                 how're you?"""

       abc = 6.75483

       new_var = 824

       ====
       print "\n\n---\n(There are no tests for this problem.)"

  .. tab:: Solution

    .. activecode:: ps_1_3s
       
       apples_and_oranges = """hello, everybody
                                 how're you?"""

       abc = 6.75483

       new_var = 824

       print type(apples_and_oranges)
       print type(abc)
       print type(new_var)

       ====
       print "\n\n---\n(There are no tests for this problem.)"


4. There is a function we are giving you called ``square``. It takes one integer and returns the square of that integer value. Write code to assign a variable callex ``xyz`` the value ``5*5`` (five squared). Use the square function, rather than just multiplying with ``*``.

.. tabbed:: ps1_pb4

  .. tab:: Problem

    .. activecode:: ps_1_4
       :include: addl_functions

       # Want to make sure there really is a function called square? Uncomment the following line and press run.

       #print type(square)

       xyz = ""
       
       ====
       import test
       print "\n\n---\n"
       try:
          test.testEqual(type(xyz), type(3))
          test.testEqual(xyz,25)
       except:
          print "variable xyz doesn't have a value at all!"

  .. tab:: Solution

    .. activecode:: ps_1_4s
       :include: addl_functions

       # Want to make sure there really is a function called square? Uncomment the following line and press run.

       #print type(square)

       xyz = square(5)
       
       ====
       import test
       print "\n\n---\n"
       try:
          test.testEqual(type(xyz), type(3))
          test.testEqual(xyz,25)
       except:
          print "variable xyz doesn't have a value at all!"
      

5. Write code to assign the return value of the function call ``square(3)`` to the variable ``new_number``.

.. tabbed:: ps1_pb5

  .. tab:: Problem

    .. activecode:: ps_1_5
        :include: addl_functions

        ====
        print "\n\n---\n"
        import test
        try:
           test.testEqual(new_number, 9)
        except:
           print "Failed test: the variable new_number does not exist yet"

  .. tab:: Solution

    .. activecode:: ps_1_5s
        :include: addl_functions

        new_number = square(3)

        ====
        print "\n\n---\n"
        import test
        try:
           test.testEqual(new_number, 9)
        except:
           print "Failed test: the variable new_number does not exist yet"


6. Write in a comment what each line of this code does. 

.. tabbed:: ps1_pb6

  .. tab:: Problem

    .. activecode:: ps_1_6
        :include: addl_functions

        # Here's an example.
        xyz = 12 # The variable xyz is being assigned the value 12, which is an integer

        # Now do the same for these!
        a = 6

        b = a

        # make sure to be very clear and detailed about the following line of code
        orange = square(b)

        print a

        print b

        print orange

        pear = square

        print pear

  .. tab:: Solution

    .. activecode:: ps_1_6s
      :include: addl_functions

      # Here's an example.
      xyz = 12 # The variable xyz is being assigned the value 12, which is an integer

      # Now do the same for these!
      a = 6 # the variable a is being assigned the integer value 6

      b = a # the variable b is being assigned the value that the variable a holds

      # make sure to be very clear and detailed about the following line of code
      orange = square(b) # the variable orange is being assigned the value of the 
      ## evaluated expression square(b), which, if b is an integer, will be another integer

      print a # the (integer) value bound to/held by the variable a is printed

      print b # the (integer) value bound to the variable b is printed

      print orange # the (integer) value bound to the variable orange is printed

      pear = square # the variable pear is being assigned the value of the variable name square(which is a function)

      print pear # the value bound to the variable pear (now a function) is beign printed out 

      ## remember, print is for people! printing out is for the programmer/user to see, not the computer or the program!

7. There are a couple more functions we're giving you in this problem set. One is a function called ``greeting``, which takes any string and adds ``"Hello, "`` in front of it. (You can see examples in the code.) Another one is a function called ``random_digit``, which returns a value of any random integer between 0 and 9 (inclusive). (You can also see examples in the code.)

Write code that assigns to the variable ``func_var`` the **function** ``greeting`` (without executing the function). 

Then, write code that assigns to the variable ``new_digit`` the **return value** from executing the function ``random_digit``.

Then, write code that assigns to the variable ``digit_func`` the **function** ``random_digit`` (without executing the function).

.. tabbed:: ps1_pb7

  .. tab:: Problem

    .. activecode:: ps_1_7
       :include: addl_functions

       # For example
       print greeting("Jackie")
       print greeting("everybody")
       print greeting("sdgadgsal")
       
       # Try running all this code more than once, so you can see how calling the function
       # random_digit works.
       print random_digit()
       print random_digit()

       # Write code that assigns the variables as mentioned in the instructions.

       ====
       import test
       print "\n\n---\n"
       test.testEqual(type(func_var), type(greeting))
       test.testEqual(type(new_digit), type(1))
       test.testEqual(type(digit_func), type(random_digit))

  .. tab:: Solution

    .. activecode:: ps_1_7s
       :include: addl_functions

       # For example
       print greeting("Jackie")
       print greeting("everybody")
       print greeting("sdgadgsal")
       
       # Try running all this code more than once, so you can see how calling the function
       # random_digit works.
       print random_digit()
       print random_digit()

       # Write code that assigns the variables as mentioned in the instructions.
       func_var = greeting
       new_digit = random_digit()
       digit_func = random_digit

       ====
       import test
       print "\n\n---\n"
       test.testEqual(type(func_var), type(greeting))
       test.testEqual(type(new_digit), type(1))
       test.testEqual(type(digit_func), type(random_digit))


8. Now write code that assigns the variable ``newval`` to hold the **return value** of ``greeting("everyone in class")``.

.. tabbed:: ps1_pb8

  .. tab:: Problem

    .. activecode:: ps_1_8
       :include: addl_functions

       ====   
       import test
       print "\n\n---\n"
       test.testEqual(newval, greeting("everyone in class"))

  .. tab:: Solution

    .. activecode:: ps_1_8s
       :include: addl_functions

       newval = greeting("everyone in class")

       ====   
       import test
       print "\n\n---\n"
       test.testEqual(newval, greeting("everyone in class"))
    

9. This code causes an error. Why? Write a comment explaining.

.. tabbed:: ps1_pb9

  .. tab:: Problem

    .. activecode:: ps_1_9

       another_variable = "?!"
       b = another_variable()

  .. tab:: Solution

    .. activecode:: ps_1_9s

       another_variable = "?!"
       b = another_variable()
       # this code is trying to call a non-callable object
       # another_value holds a string value, not a function value, so that cannot be called like a function can be!

   
.. activecode:: addl_functions
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
   