..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Nested conditionals
-------------------

One conditional can also be **nested** within another. For example, assume we have two integer variables, ``x`` and ``y``.
The following pattern of selection shows how we might decide how they are related to each other.

.. sourcecode:: python

    if x < y:
        print "x is less than y"
    else:
        if x > y:
            print "x is greater than y"
        else:
            print "x and y must be equal"

The outer conditional contains two branches.
The second branch (the else from the outer) contains another ``if`` statement, which
has two branches of its own. Those two branches could contain
conditional statements as well.

The flow of control for this example can be seen in this flowchart illustration.

.. image:: Figures/flowchart_nested_conditional.png




Here is a complete program that defines values for ``x`` and ``y``.  Run the program and see the result.  Then change the values of the variables to change the flow of control.

.. activecode:: sel2

    x = 10
    y = 10

    if x < y:
        print "x is less than y"
    else:
        if x > y:
            print "x is greater than y"
        else:
            print "x and y must be equal"

.. note::

	In some programming languages, matching the if and the else is a problem.  However, in Python this is not the case.
	The indentation pattern tells us exactly which else
	belongs to which if.

If you are still a bit unsure, here is the same selection as part of a codelens example.  Step through it to see how the correct ``print`` is chosen.

.. codelens:: sel1
    :showoutput:

    x = 10
    y = 10

    if x < y:
        print "x is less than y"
    else:
        if x > y:
            print "x is greater than y"
        else:
            print "x and y must be equal"


**Check your understanding**

.. mchoicemf:: test_question6_6_1
   :answer_a: No
   :answer_b: Yes
   :correct: a
   :feedback_a: This is a legal nested if-else statement.  The inner if-else statement is contained completely within the body of the outer else-block.
   :feedback_b: This is a legal nested if-else statement.  The inner if-else statement is contained completely within the body of the outer else-block.

   Will the following code cause an error?

   .. code-block:: python

     x = -10
     if x < 0:
         print "The negative number ",  x, " is not valid here."
     else:
         if x > 0:
             print x, " is a positive number"
         else:
             print x," is 0"


.. index::
    single: chained conditional
    single: conditional; chained

