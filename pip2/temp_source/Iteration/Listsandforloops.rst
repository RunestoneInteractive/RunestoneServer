..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Lists and ``for`` loops
-----------------------

It is also possible to perform **list traversal** using iteration by item as well as iteration by index.


.. activecode:: chp09_03a

    fruits = ["apple","orange","banana","cherry"]

    for afruit in fruits:     # by item
        print(afruit)

It almost reads like natural language: For (every) fruit in (the list of) fruits,
print (the name of the) fruit.

We can also use the indices to access the items in an iterative fashion.

.. activecode:: chp09_03b

    fruits = ["apple","orange","banana","cherry"]

    for position in range(len(fruits)):     # by index
        print(fruits[position])


In this example, each time through the loop, the variable ``position`` is used as an index into the
list, printing the ``position``-eth element. Note that we used ``len`` as the upper bound on the range
so that we can iterate correctly no matter how many items are in the list.

Since lists are mutable, it is often desirable to traverse a list, modifying
each of its elements as you go. The following code squares all the numbers from ``1`` to
``5`` using iteration by position.

.. activecode:: chp09_for4

    numbers = [10, 20, 30, 40, 50]
    print(numbers)

    for i in range(len(numbers)):
        numbers[i] = numbers[i]**2

    print(numbers)

Take a moment to think about ``range(len(numbers))`` until you understand how
it works. In this case, since ``len(numbers)`` is 5, it's the same as saying ``range(5)``.
We are interested here in both the *value* (10, 20, 30, etc.) and its *index* within the
list (0, 1, 2, etc.), so that we can assign a new value to the position in the list.


    

**Check your understanding**

.. mchoicemf:: test_question9_16_1
   :answer_a: [4,2,8,6,5]
   :answer_b: [4,2,8,6,5,5]
   :answer_c: [9,7,13,11,10]
   :answer_d: Error, you cannot concatenate inside an append.
   :correct: c
   :feedback_a: 5 is added to each item before the append is peformed.
   :feedback_b: There are too many items in this list.  Only 5 append operations are performed.
   :feedback_c: Yes, the for loop processes each item of the list.  5 is added before it is appended to blist.
   :feedback_d: 5 is added to each item before the append is performed.
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [4,2,8,6,5]
     blist = [ ]
     for item in alist:
        blist.append(item+5)
     print(blist)

.. _accum_pattern:
      
The Accumulator Pattern
=======================

One common programming "pattern" is to traverse a sequence, **accumulating** a value as we go, 
such as the sum-so-far or the maximum-so-far. That way, at the end of the traversal we have accumulated a single
value, such as the sum total of all the items or the largest item.

The anatomy of the accumulation pattern includes:
   - **initializing** an "acccumulator" variable to an initial value (such as 0 if accumulating a sum)
   - **iterating** (e.g., traversing the items in a sequence)
   - **updating** the accumulator variable on each iteration (i.e., when processing each item in the sequence)
   
For example, consider the following code, which computes the sum of the numbers in a list.

.. activecode:: iter_accum1

   nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
   accum = 0
   for w in nums:
      accum = accum + w
   print accum

In the program above, notice that the variable ``accum`` starts out with a value of 0.  
Next, the iteration is performed 10 times.  Inside the for loop, the update occurs. 
``w`` has the value of current item (1 the first time, then 2, then 3, etc.). 
``accum`` is reassigned a new value which is the old value plus the current value of ``w``.

This pattern of iterating the updating of a variable is commonly
referred to as the **accumulator pattern**.  We refer to the variable as the **accumulator**.  This pattern will come up over and over again.  Remember that the key
to making it work successfully is to be sure to initialize the variable before you start the iteration.
Once inside the iteration, it is required that you update the accumulator.


Here is the same program in codelens.  Step thru the function and watch the "running total" accumulate the result.

.. codelens:: iter_accum2

   nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
   accum = 0
   for w in nums:
      accum = accum + w
   print accum


.. note::

    What would happen if we indented the print accum statement? Not sure? Make a prediction, then try it and find out.


**Check your understanding**

.. mchoicemf:: test_question5_4_1
   :answer_a: It will print out 10 instead of 55
   :answer_b: It will cause a run-time error
   :answer_c: It will print out 0 instead of 55
   :correct: a
   :feedback_a: The variable accum will be reset to 0 each time through the loop. Then it will add the current item. Only the last item will count.  
   :feedback_b: Assignment statements are perfectly legal inside loops and will not cause an error.
   :feedback_c: Good thought: the variable accum will be reset to 0 each time through the loop. But then it adds the current item. 

   Consider the following code:

   .. code-block:: python

      nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
      for w in nums:
         accum = 0
         accum = accum + w
      print accum
   
   What happens if you put the initialization of accum inside the for loop as the first
   instruction in the loop?


.. parsonsprob:: question5_4_1p

   Rearrange the code statements so that the program will add up the first n odd numbers where n is provided by the user.
   -----
   n = int(input('How many even numbers would you like to add together?'))
   thesum = 0
   oddnumber = 1
   =====
   for counter in range(n):
   =====
      thesum = thesum + oddnumber
      oddnumber = oddnumber + 2
   =====
   print(thesum)


