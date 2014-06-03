..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Concatenation and Repetition
----------------------------

Again, as with strings, the ``+`` operator concatenates lists.  
Similarly, the ``*`` operator repeats the items in a list a given number of times.

.. activecode:: chp09_5

    fruit = ["apple","orange","banana","cherry"]
    print([1,2] + [3,4])
    print(fruit+[6,7,8,9])

    print([0] * 4)
    print([1,2,["hello","goodbye"]]*2)


It is important to see that these operators create new lists from the elements of the operand lists.  If you concatenate a list with 2 items and a list with 4 items, you will get a new list with 6 items (not a list with two sublists).  Similarly, repetition of a list of 2 items 4 times will give a list with 8 items.

One way for us to make this more clear is to run a part of this example in codelens.  As you step through the code, you will see the variables being created and the lists that they refer to.  Pay particular attention to the fact that when ``newlist`` is created by the statement ``newlist = fruit + numlist``, it refers to a completely new list formed by making copies of the items from ``fruit`` and ``numlist``.  You can see this very clearly in the codelens object diagram.  The objects are different.



.. codelens:: chp09_concatid

    fruit = ["apple","orange","banana","cherry"]
    numlist = [6,7]

    newlist = fruit + numlist

    zeros = [0] * 4





In Python, every object has a unique identification tag.  Likewise, there is a built-in function that can be called on any object to return its unique id.  The function is appropriately called ``id`` and takes a single parameter, the object that you are interested in knowing about.  You can see in the example below that a real id is usually a very large integer value (corresponding to an address in memory).

.. sourcecode:: python

    >>> alist = [4,5,6]
    >>> id(alist)
    4300840544
    >>> 

**Check your understanding**

.. mchoicemf:: test_question9_5_1
   :answer_a: 6
   :answer_b: [1,2,3,4,5,6]
   :answer_c: [1,3,5,2,4,6]
   :answer_d: [3,7,11]
   :correct: c
   :feedback_a: Concatenation does not add the lengths of the lists.
   :feedback_b: Concatenation does not reorder the items. 
   :feedback_c: Yes, a new list with all the items of the first list followed by all those from the second.
   :feedback_d: Concatenation does not add the individual items.
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [1,3,5]
     blist = [2,4,6]
     print(alist + blist)

   
   
.. mchoicemf:: test_question9_5_2
   :answer_a: 9
   :answer_b: [1,1,1,3,3,3,5,5,5]
   :answer_c: [1,3,5,1,3,5,1,3,5]
   :answer_d: [3,9,15]
   :correct: c
   :feedback_a: Repetition does not multiply the lengths of the lists.  It repeats the items.
   :feedback_b: Repetition does not repeat each item individually.
   :feedback_c: Yes, the items of the list are repeated 3 times, one after another.
   :feedback_d: Repetition does not multiply the individual items.
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [1,3,5]
     print(alist * 3)

   

