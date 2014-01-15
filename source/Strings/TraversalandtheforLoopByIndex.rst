..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Traversal and the ``for`` Loop: By Index
----------------------------------------

It is also possible to use the ``range`` function to systematically generate the indices of the characters.  The ``for`` loop can then be used to iterate over these positions. 
These positions can be used together with the indexing operator to access the individual
characters in the string.

Consider the following codelens example.

.. codelens:: ch08_7

    fruit = "apple"
    for idx in range(5):
        currentChar = fruit[idx]
        print(currentChar)

The index positions in "apple" are 0,1,2,3 and 4.  This is exactly the same sequence of integers returned by ``range(5)``.  The first time through the for loop, ``idx`` will be 0 and the "a" will be printed.  Then, ``idx`` will be reassigned to 1 and "p" will be displayed.  This will repeat for all the range values up to but not including 5.  Since "e" has index 4, this will be exactly right to show all 
of the characters.

In order to make the iteration more general, we can use the ``len`` function to provide the bound for ``range``.  This is a very common pattern for traversing any sequence by position.	Make sure you understand why the range function behaves
correctly when using ``len`` of the string as its parameter value.

.. activecode:: ch08_7b
    :nocanvas:


    fruit = "apple"
    for idx in range(len(fruit)):
        print(fruit[idx])


You may also note that iteration by position allows the programmer to control the direction of the
traversal by changing the sequence of index values.  Recall that we can create ranges that count down as 
well as up so the following code will print the characters from right to left.

.. codelens:: ch08_8

    fruit = "apple"
    for idx in range(len(fruit)-1, -1, -1):
        print(fruit[idx])

Trace the values of ``idx`` and satisfy yourself that they are correct.  In particular, note the start and end of the range.

**Check your understanding**

.. mchoicemf:: test_question8_9_1
   :answer_a: 0
   :answer_b: 1
   :answer_c: 2
   :answer_d: Error, the for statement cannot have an if inside.
   :correct: c
   :feedback_a: The for loop visits each index but the selection only prints some of them.
   :feedback_b: o is at positions 4 and 8
   :feedback_c: Yes, it will print all the characters in even index positions and the o character appears both times in an even location.
   :feedback_d: The for statement can have any statements inside, including if as well as for.


   How many times is the letter o printed by the following statements?
   
   .. code-block:: python

      s = "python rocks"
      for idx in range(len(s)):
         if idx % 2 == 0:
            print(s[idx])
      



