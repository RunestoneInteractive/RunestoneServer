..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Updating Variables
------------------

.. video:: updatevid
    :controls:
    :thumb: ../_static/updatethumb.png

    http://media.interactivepython.org/thinkcsVideos/update.mov
    http://media.interactivepython.org/thinkcsVideos/update.webm

One of the most common forms of reassignment is an **update** where the new
value of the variable depends on the old.  For example,

.. sourcecode:: python

    x = x + 1

This means get the current value of x, add one, and then update x with the new
value.  The new value of x is the old value of x plus 1.  Although this assignment statement may
look a bit strange, remember that executing assignment is a two-step process.  First, evaluate the
right-hand side expression.  Second, let the variable name on the left-hand side refer to this new
resulting object.  The fact that ``x`` appears on both sides does not matter.  The semantics of the assignment
statement makes sure that there is no confusion as to the result.

.. activecode:: ch07_update1

    x = 6        # initialize x
    print(x)
    x = x + 1    # update x
    print(x)


If you try to update a variable that doesn't exist, you get an error because
Python evaluates the expression on the right side of the assignment operator
before it assigns the resulting value to the name on the left.
Before you can update a variable, you have to **initialize** it, usually with a
simple assignment.  In the above example, ``x`` was initialized to 6.

Updating a variable by adding 1 is called an **increment**; subtracting 1 is
called a **decrement**.  Sometimes programmers also talk about **bumping**
a variable, which means the same as incrementing it by 1.




.. admonition:: Advanced Topics

   * `Topic 1: <at_1_1.html>`_ Python Beyond the Browser.  This is a gentle
     introduction to using Python from the command line.  We'll cover this
     later, but if you are curious about what Python looks like outside of this
     eBook, you can have a look here.  There are also instructions for
     installing Python on your computer here.

   * `Topic 2: <http://interactivepython.org/courselib/static/diveintopython3/index.html>`_ Dive Into Python 3,
     this is an online textbook by Mark Pilgrim.  If you have already had some
     programming experience, this book takes you off the deep end with
     both feet.

**Check your understanding**

.. mchoicemf:: test_question2_10_1
   :answer_a: 12
   :answer_b: -1
   :answer_c: 11
   :answer_d: Nothing.  An error occurs because x can never be equal to x - 1.
   :correct: c
   :feedback_a: The value of x changes in the second statement.
   :feedback_b: In the second statement, substitute the current value of x before subtracting 1.
   :feedback_c: Yes, this statement sets the value of x equal to the current value minus 1.
   :feedback_d: Remember that variables in Python are different from variables in math in that they (temporarily) hold values, but can be reassigned.


   What is printed when the following statements execute?

   .. code-block:: python

     x = 12
     x = x - 1
     print (x)

.. mchoicemf:: test_question2_10_2
   :answer_a: 12
   :answer_b: 9
   :answer_c: 15
   :answer_d: Nothing.  An error occurs because x cannot be used that many times in assignment statements.
   :correct: c
   :feedback_a: The value of x changes in the second statement.
   :feedback_b: Each statement changes the value of x, so 9 is not the final result.
   :feedback_c: Yes, starting with 12, subtract 3, than add 5, and finally add 1.
   :feedback_d: Remember that variables in Python are different from variables in math in that they (temporarily) hold values, but can be reassigned.


   What is printed when the following statements execute?

   .. code-block:: python

     x = 12
     x = x - 3
     x = x + 5
     x = x + 1
     print (x)

.. parsonsprob:: question2_10_3

   Construct the code that will result in the value 134 being printed.
   -----
   mybankbalance = 100
   mybankbalance = mybankbalance + 34
   print(mybankbalance)


.. note::

   This workspace is provided for your convenience.  You can use this activecode window to try out anything you like.

   .. activecode:: scratch_02



