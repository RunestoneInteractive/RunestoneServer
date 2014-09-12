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

It is also possible to iterate through the *indexes* of a string or sequence. The ``for`` loop can then be used to iterate over these positions. 
These positions can be used together with the indexing operator to access the individual
characters in the string.

.. activecode:: ch08_7a

   fruit = "apple"
   for idx in [0, 1, 2, 3, 4]:
      currentChar = fruit[idx]
      print currentChar
   
   # after you run this, try changing the order of items in the list [0, 1, 2, 3, 4] and see what happens.
   # What happens if you put the number 6 into the list, or the word "hello"?       

Conveniently, we can use the ``range`` function to automatically generate the indices of the characters. 

.. activecode:: ch08_7a1

   x = range(5)
   print type(x)
   print x
   

Consider the following codelens example.

.. codelens:: ch08_7

    fruit = "apple"
    x = range(5)
    for idx in x:
        currentChar = fruit[idx]
        print currentChar

The index positions in "apple" are 0,1,2,3 and 4.  This is exactly the same sequence of integers returned by ``range(5)``.  The first time through the for loop, ``idx`` will be 0 and the "a" will be printed.  Then, ``idx`` will be reassigned to 1 and "p" will be displayed.  This will repeat for all the range values up to but not including 5.  Since "e" has index 4, this will be exactly right to show all 
of the characters.

In order to make the iteration more general, we can use the ``len`` function to provide the bound for ``range``.  This is a very common pattern for traversing any sequence by position.	Make sure you understand why the range function behaves
correctly when using ``len`` of the string as its parameter value.

.. activecode:: ch08_7b
    :nocanvas:


    fruit = "apple"
    for idx in range(len(fruit)):
        print fruit[idx]


You may also note that iteration by position allows the programmer to control the direction of the
traversal by changing the sequence of index values.

.. codelens:: ch08_8

    fruit = "apple"
    for idx in [0, 2, 4, 3, 1]:
        print fruit[idx]


**Check your understanding**

.. mchoicemf:: test_question8_9_1
   :answer_a: 0
   :answer_b: 1
   :answer_c: 2
   :answer_d: 3
   :answer_e: 6
   :correct: d
   :feedback_a: idx % 2 is 0 whenever idx is even
   :feedback_b: idx % 2 is 0 whenever idx is even
   :feedback_c: idx % 2 is 0 whenever idx is even
   :feedback_d: idx % 2 is 0 whenever idx is even
   :feedback_e: idx % 2 is 0 whenever idx is even

   How many times is the letter p printed by the following statements?
   
   .. code-block:: python

      s = "python"
      for idx in range(len(s)):
         print s[idx % 2]


