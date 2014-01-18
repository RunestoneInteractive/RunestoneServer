..  Copyright (C)  Paul Resnick, Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".
    
..  shortname:: Iteration
..  description:: Introduction to iteration over the items in lists and strings.

.. qnum::
   :prefix: iter-
   :start: 1

.. _iteration_chap:

Iteration
=========

A basic building block of all programs is to be able to repeat some code
over and over again.  In computing, we refer to this repetitive execution as **iteration**.  In this section, we will explore some mechanisms for basic iteration.

With collections (lists and strings), a lot of computations involve processing one item at a time.  
For strings this means that we would like to process one character at a time.
Often we start at the beginning, select each character in turn, do something
to it, and continue until the end. This pattern of processing is called a
**traversal**, or **iteration over the characters**. Similarly, we can process each of the items in a list, one at a time,
**iteration over the items in the list**.

.. index:: for loop

The **for** Loop
----------------

In Python, the **for** statement allows us to write programs that implement iteration.   As a simple example, let's say we have some friends, and
we'd like to send them each an email inviting them to our party.  We
don't quite know how to send email yet, so for the moment we'll just print a
message for each friend.

.. activecode:: ch03_4
    :nocanvas:
    :tour_1: "Overall Tour"; 1-2: Example04_Tour01_Line01; 2: Example04_Tour01_Line02; 1: Example04_Tour01_Line03;

    for name in ["Joe", "Amy", "Brad", "Angelina", "Zuki", "Thandi", "Paris"]:
        print("Hi", name, "Please come to my party on Saturday!")


Take a look at the output produced when you press the ``run`` button.  There is one line printed for each friend.  Here's how it works:


* **name** in this ``for`` statement is called the **loop variable**.
* The list of names in the square brackets is the sequence over which we will iterate.
* Line 2  is the **loop body**.  The loop body is always
  indented. The indentation determines exactly what statements are "in the
  loop".  The loop body is performed one time for each name in the list.
* On each *iteration* or *pass* of the loop, first a check is done to see if
  there are still more items to be processed.  If there are none left (this is
  called the **terminating condition** of the loop), the loop has finished.
  Program execution continues at the next statement after the loop body.
* If there are items still to be processed, the loop variable is updated to
  refer to the next item in the list.  This means, in this case, that the loop
  body is executed here 7 times, and each time `friendName` will refer to a different
  friend.
* At the end of each execution of the body of the loop, Python returns
  to the ``for`` statement, to see if there are more items to be handled.



.. index:: control flow, flow of execution


Flow of Execution of the for Loop
---------------------------------

As a program executes, the interpreter always keeps track of which statement is
about to be executed.  We call this the **control flow**, or the **flow of
execution** of the program.  When humans execute programs, they often use their
finger to point to each statement in turn.  So you could think of control flow
as "Python's moving finger".

Control flow until now has been strictly top to bottom, one statement at a
time.  We call this type of control **sequential**.  
Sequential flow of control is always assumed to be the default behavior for a computer program. 
The ``for`` statement changes this.

Flow of control is often easy to visualize and understand if we draw a flowchart.
This flowchart shows the exact steps and logic of how the ``for`` statement executes.


.. image:: Figures/new_flowchart_for.png
      :width: 300px

.. note::

    Not sure what a flowchart is? Check out this funny take on it, in `XKCD <http://xkcd.com/518/>`_. `And this one <http://xkcd.com/1195/>`_.


A codelens demonstration is a good way to help you visualize exactly how the flow of control
works with the for loop.  Try stepping forward and backward through the program by pressing
the buttons.  You can see the value of ``name`` change as the loop iterates thru the list of friends.

.. codelens:: vtest

    for name in ["Joe", "Amy", "Brad", "Angelina", "Zuki", "Thandi", "Paris"]:
        print("Hi ", name, "  Please come to my party on Saturday!")



Strings and ``for`` loops
-------------------------


Since a string is simply a sequence of characters, the ``for`` loop iterates over each character automatically. (As always, try
to predict what the output will be from this code before your run it.

.. activecode:: ch08_6
    :nocanvas:

    for achar in "Go Spot Go":
        print(achar)

The loop variable ``achar`` is automatically reassigned each character in the string "Go Spot Go".
We will refer to this type of sequence iteration as **iteration by item**.  
Note that the for loop processes the characters in a string or items in a sequence one at a time from left to right.

**Check your understanding**

.. mchoicemf:: test_question8_8_1
   :answer_a: 10
   :answer_b: 11
   :answer_c: 12
   :answer_d: Error, the for statement needs to use the range function.
   :correct: c
   :feedback_a: Iteration by item will process once for each item in the sequence.
   :feedback_b: The blank is part of the sequence.
   :feedback_c: Yes, there are 12 characters, including the blank.
   :feedback_d: The for statement can iterate over a sequence item by item.


   How many times is the word HELLO printed by the following statements?
   
   .. code-block:: python

      s = "python rocks"
      for ch in s:
         print("HELLO")

   
   
   
.. mchoicemf:: test_question8_8_2
   :answer_a: 4
   :answer_b: 5
   :answer_c: 6
   :answer_d: Error, the for statement cannot use slice.
   :correct: b
   :feedback_a: Slice returns a sequence that can be iterated over.
   :feedback_b: Yes, The blank is part of the sequence returned by slice
   :feedback_c: Check the result of s[3:8].  It does not include the item at index 8.
   :feedback_d: Slice returns a sequence.


   How many times is the word HELLO printed by the following statements?
   
   .. code-block:: python

      s = "python rocks"
      for ch in s[3:8]:
         print("HELLO")



Traversal and the ``for`` Loop: By Index
----------------------------------------

It is also possible to iterate through the *indexes* of a string or sequence. The ``for`` loop can then be used to iterate over these positions. 
These positions can be used together with the indexing operator to access the individual
characters in the string.

.. activecode:: ch08_7a

   fruit = "apple"
   for idx in [0, 1, 2, 3, 4]:
      currentChar = fruit[idx]
      print(currentChar)
   
   # after you run this, try changing the order of items in the list [0, 1, 2, 3, 4] and see what happens.
   # What happens if you put the number 6 into the list, or the word "hello"?       

Conveniently, we can use the ``range`` function to automatically generate the indices of the characters. 

.. activecode:: ch08_7a1

   x = range(5)
   print(type(x))
   print(x)
   

Consider the following codelens example.

.. codelens:: ch08_7

    fruit = "apple"
    x = range(5)
    for idx in x:
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
traversal by changing the sequence of index values.

.. codelens:: ch08_8

    fruit = "apple"
    for idx in [0, 2, 4, 3, 1]:
        print(fruit[idx])


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


The Accumulator Pattern with Strings
------------------------------------

We can also accumulate strings rather than accumulating numbers. The following "stuttering" program 
isn't very useful, but we will see more useful things later that accumulate strings.

.. activecode:: ch08_acc1
    
   s = raw_input("Enter some text")
   ac = ""
   for c in s:
      ac = ac + c + "-" + c + "-"
       
   print ac
 
Look carefully at line 4 in the above program (``ac = ac + c + "-" + c + "-"``).  
In words, it says that the new value of ``ac`` will be the old value of ``ac`` concatenated with the current character a dash, then the current character and a dash again.
We are building the result string character by character. 

Take a close look also at the initialization of ``ac``.  We start with an empty string and then begin adding
new characters to the end. Also note that I have given it a different name this time, ``ac`` instead of ``accum``. There's
nothing magical about these names. You could use any valid variable and it would work the same (try substituting x for ac
everywhere in the above code).


**Check your understanding**

.. mchoicemf:: test_question8_11_1
   :answer_a: Ball
   :answer_b: BALL
   :answer_c: LLAB
   :correct: c
   :feedback_a: Each item is converted to upper case before concatenation.
   :feedback_b: Each character is converted to upper case but the order is wrong.
   :feedback_c: Yes, the order is reversed due to the order of the concatenation.

   What is printed by the following statements:
   
   .. code-block:: python

      s = "ball"
      r = ""
      for item in s:
         r = item.upper() + r
      print(r)


.. note::

   This workspace is provided for your convenience.  You can use this activecode window to try out anything you like.

   .. activecode:: scratch_08_03




Summary 
------- 

This chapter introduced the central concept of **iteration**.  The following summary 
may prove helpful in remembering what you learned.

.. glossary::



Glossary
========

.. glossary::

    for loop traversal (``for``)
        *Traversing* a string or a list means accessing each character in the string or item in the list, one
        at a time.  For example, the following for loop:

        .. sourcecode:: python

            for ix in 'Example':
                ...

        executes the body of the loop 7 times with different values of `ix` each time.
        
    range
        A function that produces a list of numbers. For example, `range(5)`, produces a list of five 
        numbers, starting with 0, `[0, 1, 2, 3, 4]`. 

    pattern
        A sequence of statements, or a style of coding something that has
        general applicability in a number of different situations.  Part of
        becoming a mature programmer is to learn and establish the
        patterns and algorithms that form your toolkit.   

    index
        A variable or value used to select a member of an ordered collection, such as
        a character from a string, or an element from a list.

    traverse
        To iterate through the elements of a collection, performing a similar
        operation on each.

    accumulator pattern
         A pattern where the program initializes an accumulator variable and then changes it
         during each iteration, accumulating a final result.

Exercises
=========


#. (You'll work on this one in class. Feel free to start thinking about it.) Print out a neatly formatted multiplication table, up to 12 x 12.

   .. actex:: ex_8_4


#. (You'll work on on this one in class. Feel free to start thinking about it.) In Robert McCloskey's
   book *Make Way for Ducklings*, the names of the ducklings are Jack, Kack, Lack,
   Mack, Nack, Ouack, Pack, and Quack.  This loop tries to output these names in order.

   .. sourcecode:: python

      prefixes = "JKLMNOPQ"
      suffix = "ack"

      for p in prefixes:
          print(p + suffix)


   Of course, that's not quite right because Ouack and Quack are misspelled.
   Can you fix it?
   
    .. actex:: ex_8_2


#. Get the user to enter some text and print it out in reverse. (Hint: we did this as well as capitalizing
in one of the earlier exercises. But first see if you can generate the answer without looking back.)

   .. actex:: ex_8_5


#. Get the user to enter some text and print out True if it's a palindrome, False otherwise. (Hint: reuse
some of your code from the last question.)

   .. actex:: ex_8_6

