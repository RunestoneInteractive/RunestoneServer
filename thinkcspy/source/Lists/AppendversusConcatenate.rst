..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Append versus Concatenate
-------------------------

The ``append`` method adds a new item to the end of a list.  It is also possible to add a new item to the end of a list by using the concatenation operator.  However, you need to be careful.

Consider the following example.  The original list has 3 integers.  We want to add the word "cat" to the end of the list.

.. codelens:: appcon1

    origlist = [45, 32, 88]

    origlist.append("cat")



Here we have used ``append`` which simply modifies the list.  In order to use concatenation, we need to write an assignment statement that uses the accumulator pattern::

    origlist = origlist + ["cat"]

Note that the word "cat" needs to be placed in a list since the concatenation operator needs two lists to do its work.

.. codelens:: appcon2

    origlist = [45, 32, 88]

    origlist = origlist + ["cat"]


It is also important to realize that with append, the original list is simply modified.  
On the other hand, with concatenation, an entirely new list is created.  This can be seen in the following codelens example where
``newlist`` refers to a list which is a copy of the original list, ``origlist``, with the new item "cat" added to the end.  ``origlist`` still contains the three values it did before the concatenation.  This is why the assignment operation is necessary as part of the
accumulator pattern.

.. codelens:: appcon3

    origlist = [45, 32, 88]

    newlist = origlist + ["cat"]


**Check you understanding**

.. mchoicemf:: test_question9_15_1
   :answer_a: [4, 2, 8, 6, 5, 999]
   :answer_b: Error, you cannot concatenate a list with an integer.
   :correct: b
   :feedback_a: You cannot concatenate a list with an integer.
   :feedback_b: Yes, in order to perform concatenation you would need to write alist+[999].  You must have two lists.
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [4, 2, 8, 6, 5]
     alist = alist + 999
     print(alist)


.. index:: for loop, enumerate

.. index:: for loop

