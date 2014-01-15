..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

List Values
-----------

There are several ways to create a new list.  The simplest is to enclose the
elements in square brackets ( ``[`` and ``]``).

.. sourcecode:: python
    
    [10, 20, 30, 40]
    ["spam", "bungee", "swallow"]

The first example is a list of four integers. The second is a list of three
strings. As we said above, the elements of a list don't have to be the same type.  The following
list contains a string, a float, an integer, and
another list.

.. sourcecode:: python
    
    ["hello", 2.0, 5, [10, 20]]

A list within another list is said to be **nested** and the inner list is often called a **sublist**.
Finally, there is a special list that contains no elements. It is called the
empty list and is denoted ``[]``.

As you would expect, we can also assign list values to variables and pass lists as parameters to functions.  

.. activecode:: chp09_01
    
    vocabulary = ["iteration", "selection", "control"]
    numbers = [17, 123]
    empty = []
    mixedlist = ["hello", 2.0, 5*2, [10, 20]]

    print(numbers)
    print(mixedlist)
    newlist = [ numbers, vocabulary ]
    print(newlist)

.. _accessing-elements:

**Check your understanding**

.. mchoicemf:: test_question9_1_1 
   :answer_a: False
   :answer_b: True
   :correct: a
   :feedback_a: Yes, unlike strings, lists can consist of any type of Python data.
   :feedback_b: Lists are heterogeneous, meaning they can have different types of data.

   A list can contain only integer items.

.. index:: list index, index, list traversal

