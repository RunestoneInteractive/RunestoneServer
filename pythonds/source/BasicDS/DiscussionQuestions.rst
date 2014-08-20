..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Discussion Questions
--------------------

#. Convert the following values to binary using “divide by 2.” Show the
   stack of remainders.

   -  17

   -  45

   -  96

#. Convert the following infix expressions to prefix (use full
   parentheses):

   -  (A+B)\*(C+D)\*(E+F)

   -  A+((B+C)\*(D+E))

   -  A\*B\*C\*D+E+F

#. Convert the above infix expressions to postfix (use full
   parentheses).

#. Convert the above infix expressions to postfix using the direct
   conversion algorithm. Show the stack as the conversion takes place.

#. Evaluate the following postfix expressions. Show the stack as each
   operand and operator is processed.

   -  2 3 \* 4 +

   -  1 2 + 3 + 4 + 5 +

   -  1 2 3 4 5 \* + \* +

#. The alternative implementation of the ``Queue`` ADT is to use a list
   such that the rear of the queue is at the end of the list. What would
   this mean for Big-O performance?

#. What is the result of carrying out both steps of the linked list
   ``add`` method in reverse order? What kind of reference results? What
   types of problems may result?

#. Explain how the linked list ``remove`` method works when the item to
   be removed is in the last node.

#. Explain how the ``remove`` method works when the item is in the
   *only* node in the linked list.

