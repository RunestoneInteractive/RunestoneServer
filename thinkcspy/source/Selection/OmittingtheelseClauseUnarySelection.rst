..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. qnum::
   :prefix: select-5-
   :start: 1

Omitting the `else` Clause: Unary Selection
-------------------------------------------

.. video:: unaryselection
   :controls:
   :thumb: ../_static/unaryselection.png

   http://media.interactivepython.org/thinkcsVideos/unaryselection.mov
   http://media.interactivepython.org/thinkcsVideos/unaryselection.webm




.. sidebar::  Flowchart of an **if** with no **else**

   .. image:: Figures/flowchart_if_only.png

Another form of the ``if`` statement is one in which the ``else`` clause is omitted entirely.
This creates what is sometimes called **unary selection**.
In this case, when the condition evaluates to ``True``, the statements are
executed.  Otherwise the flow of execution continues to the statement after the body of the ``if``.


.. activecode:: ch05_unaryselection

    x = 10
    if x < 0:
        print("The negative number ",  x, " is not valid here.")
    print("This is always printed")


What would be printed if the value of ``x`` is negative?  Try it.


**Check your understanding**

.. mchoicemf:: test_question6_5_1
   :answer_a: Output a
   :answer_b: Output b
   :answer_c: Output c
   :answer_d: It will cause an error because every if must have an else clause.
   :correct: b
   :feedback_a: Because -10 is less than 0, Python will execute the body of the if-statement here.
   :feedback_b: Python executes the body of the if-block as well as the statement that follows the if-block.
   :feedback_c: Python will also execute the statement that follows the if-block (because it is not enclosed in an else-block, but rather just a normal statement).
   :feedback_d: It is valid to have an if-block without a corresponding else-block (though you cannot have an else-block without a corresponding if-block).

   What does the following code print?

   .. code-block:: python
     
     x = -10
     if x < 0:
         print("The negative number ",  x, " is not valid here.")
     print("This is always printed")

   ::

     a.
     This is always printed

     b.
     The negative number -10 is not valid here
     This is always printed

     c.
     The negative number -10 is not valid here


.. mchoicemf:: test_question6_5_2
   :answer_a: No
   :answer_b: Yes
   :correct: b
   :feedback_a: Every else-block must have exactly one corresponding if-block.  If you want to chain if-else statements together, you must use the else if construct, described in the chained conditionals section.
   :feedback_b: This will cause an error because the second else-block is not attached to a corresponding if-block.

   Will the following code cause an error?

   .. code-block:: python

     x = -10
     if x < 0:
         print("The negative number ",  x, " is not valid here.")
     else:
         print(x, " is a positive number")
     else:
         print("This is always printed")

.. index::
    single: nested conditionals
    single: conditionals; nested

