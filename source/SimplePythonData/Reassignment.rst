..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Reassignment
------------

.. video:: reassignmentvid
    :controls:
    :thumb: ../_static/reassignmentthumb.png

    http://media.interactivepython.org/thinkcsVideos/reassignment.mov
    http://media.interactivepython.org/thinkcsVideos/reassignment.webm


As we have mentioned previously, it is legal to make more than one assignment to the
same variable. A new assignment makes an existing variable refer to a new value
(and stop referring to the old value).

.. activecode:: ch07_reassign1

    bruce = 5
    print(bruce)
    bruce = 7
    print(bruce)


The first time ``bruce`` is
printed, its value is 5, and the second time, its value is 7.  The assignment statement changes
the value (the object) that ``bruce`` refers to.

Here is what **reassignment** looks like in a reference diagram:

.. image:: Figures/reassign1.png
   :alt: reassignment



It is important to note that in mathematics, a statement of equality is always true.  If ``a is equal to b``
now, then ``a will always equal to b``. In Python, an assignment statement can make
two variables refer to the same object and therefore have the same value.  They appear to be equal.  However, because of the possibility of reassignment,
they don't have to stay that way:

.. activecode:: ch07_reassign2

    a = 5
    b = a    # after executing this line, a and b are now equal
    print(a,b)
    a = 3    # after executing this line, a and b are no longer equal
    print(a,b)

Line 4 changes the value of ``a`` but does not change the value of
``b``, so they are no longer equal. We will have much more to say about equality in a later chapter.

.. note::

	In some programming languages, a different
	symbol is used for assignment, such as ``<-`` or ``:=``.  The intent is
	that this will help to avoid confusion.  Python
	chose to use the tokens ``=`` for assignment, and ``==`` for equality.  This is a popular
	choice also found in languages like C, C++, Java, and C#.

**Check your understanding**

.. mchoicemf:: test_question2_9_1
   :answer_a: x is 15 and y is 15
   :answer_b: x is 22 and y is 22
   :answer_c: x is 15 and y is 22
   :answer_d: x is 22 and y is 15
   :correct: d
   :feedback_a: Look at the last assignment statement which gives x a different value.
   :feedback_b: No, x and y are two separate variables.  Just because x changes in the last assignment statement, it does not change the value that was copied into y in the second statement.
   :feedback_c: Look at the last assignment statement, which reassigns x, and not y.
   :feedback_d: Yes, x has the value 22 and y the value 15.


   After the following statements, what are the values of x and y?

   .. code-block:: python

     x = 15
     y = x
     x = 22


