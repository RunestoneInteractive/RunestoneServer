..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Chained conditionals
--------------------

Python provides an alternative way to write nested selection such as the one shown in the previous section.
This is sometimes referred to as a **chained
conditional**

.. sourcecode:: python

    if x < y:
        print("x is less than y")
    elif x > y:
        print("x is greater than y")
    else:
        print("x and y must be equal")

The flow of control can be drawn in a different orientation but the resulting pattern is identical to the one shown above.

.. image:: Figures/flowchart_chained_conditional.png

``elif`` is an abbreviation of ``else if``. Again, exactly one branch will be
executed. There is no limit of the number of ``elif`` statements but only a
single (and optional) final ``else`` statement is allowed and it must be the last
branch in the statement.

Each condition is checked in order. If the first is false, the next is checked,
and so on. If one of them is true, the corresponding branch executes, and the
statement ends. Even if more than one condition is true, only the first true
branch executes.

Here is the same program using ``elif``.

.. activecode:: sel4

    x = 10
    y = 10

    if x < y:
        print("x is less than y")
    elif x > y:
        print("x is greater than y")
    else:
        print("x and y must be equal")




.. note::

  This workspace is provided for your convenience.  You can use this activecode window to try out anything you like.

  .. activecode:: scratch_06_02


**Check your understanding**

.. mchoicemf:: test_question6_7_1
   :answer_a: I only
   :answer_b: II only
   :answer_c: III only
   :answer_d: II and III
   :answer_e: I, II, and III
   :correct: b
   :feedback_a: You can not use a Boolean expression after an else.
   :feedback_b: Yes, II will give the same result.
   :feedback_c: No, III will not give the same result.  The first if statement will be true, but the second will be false, so the else part will execute.
   :feedback_d: No, Although II is correct III will not give the same result.  Try it.
   :feedback_e: No, in I you can not have a Boolean expression after an else.

   Which of I, II, and III below gives the same result as the following nested if?

   .. code-block:: python

     # nested if-else statement
     x = -10
     if x < 0:
         print("The negative number ",  x, " is not valid here.")
     else:
         if x > 0:
             print(x, " is a positive number")
         else:
             print(x, " is 0")


   .. code-block:: python

     I.
     
     if x < 0:
         print("The negative number ",  x, " is not valid here.")
     else (x > 0):
         print(x, " is a positive number")
     else:
         print(x, " is 0")


   .. code-block:: python

     II.
     
     if x < 0:
         print("The negative number ",  x, " is not valid here.")
     elif (x > 0):
         print(x, " is a positive number")
     else:
         print(x, " is 0")

   .. code-block:: python

     III.
     
     if x < 0:
         print("The negative number ",  x, " is not valid here.")
     if (x > 0):
         print(x, " is a positive number")
     else:
         print(x, " is 0")


.. mchoicemf:: test_question6_7_2
   :answer_a: a
   :answer_b: b
   :answer_c: c
   :correct: c
   :feedback_a: While the value in x is less than the value in y (3 is less than 5) it is not less than the value in z (3 is not less than 2).
   :feedback_b: The value in y is not less than the value in x (5 is not less than 3).
   :feedback_c: Since the first two Boolean expressions are false the else will be executed.

   What will the following code print if x = 3, y = 5, and z = 2?

   .. code-block:: python

     if x < y and x < z:
         print ("a")
     elif y < x and y < z:
         print ("b")
     else:
         print ("c")




