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
    print x
    x = x + 1    # update x
    print x


If you try to update a variable that doesn't exist, you get an error because
Python evaluates the expression on the right side of the assignment operator
before it assigns the resulting value to the name on the left.
Before you can update a variable, you have to **initialize** it, usually with a
simple assignment.  In the above example, ``x`` was initialized to 6.

Updating a variable by adding something to it is called an **increment**; subtracting is
called a **decrement**.  Sometimes programmers talk about incrementing or decrementing without specifying by how much; when they do they usually mean by 1. Sometimes programmers also talk about **bumping** a variable, which means the same as incrementing it by 1.

Incrementing and decrementing are such common operations that programming languages often include special syntax for it. In python ``+=`` is used for incrementing, and ``-=`` for decrementing. In some other languages, there is even a special syntax ``++`` and ``--`` for incrementing or decrementing by 1. Python does not have such a special syntax. To increment x by 1 you have to write ``x += 1`` or ``x = x + 1``.

.. activecode:: ch07_update2

    x = 6        # initialize x
    print x
    x += 3       # increment x by 3; same as x = x + 3
    print x
    x -= 1       # decrement x by 1
    print x



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
     print x

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
     print x

.. parsonsprob:: question2_10_3

   Construct the code that will result in the value 134 being printed.
   -----
   mybankbalance = 100
   mybankbalance = mybankbalance + 34
   print mybankbalance

.. mchoicema:: test_question2_10_3
   :answer_a: x = x + y
   :answer_b: y += x
   :answer_c: x += x + y
   :answer_d: x += y
   :answer_e: x++ y
   :correct: a,d
   :feedback_a: x is updated to be the old value of x plus the value of y.
   :feedback_b: y is updated to be the old value of y plus the value of x.
   :feedback_c: This updates x to be its old value (because of the +=) plus its old value again (because of the x on the right side) plus the value of y, so it's equivalent to x = x + x + y
   :feedback_d: x is updated to be the old value of x plus the value of y.
   :feedback_e: ++ is not a syntax that means anything in python


   Which of the following statements are equivalent?
 