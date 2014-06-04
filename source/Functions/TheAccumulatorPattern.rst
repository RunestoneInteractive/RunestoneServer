..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

The Accumulator Pattern
-----------------------

.. video:: function_accumulator_pattern
   :controls:
   :thumb: ../_static/accumulatorpattern.png

   http://media.interactivepython.org/thinkcsVideos/accumulatorpattern.mov
   http://media.interactivepython.org/thinkcsVideos/accumulatorpattern.webm

In the previous example, we wrote a function that computes the square of a number.  The algorithm we used
in the function was simple: multiply the number by itself.
In this section we will reimplement the square function and use a different algorithm, one that relies on addition instead
of multiplication.

If you want to multiply two numbers together, the most basic approach is to think of it as repeating the process of
adding one number to itself.  The number of repetitions is where the second number comes into play.  For example, if we
wanted to multiply three and five, we could think about it as adding three to itself five times.  Three plus three is six, plus three is nine, plus three is 12, and finally plus three is 15.  Generalizing this, if we want to implement
the idea of squaring a number, call it `n`, we would add `n` to itself `n` times.

Do this by hand first and try to isolate exactly what steps you take.  You'll
find you need to keep some "running total" of the sum so far, either on a piece
of paper, or in your head.  Remembering things from one step to the next is
precisely why we have variables in a program.  This means that we will need some variable
to remember the "running total".  It should be initialized with a value of zero.  Then, we need to **update** the "running total" the correct number of times.  For each repetition, we'll want
to update the running total by adding the number to it.

In words we could say it this way.  To square the value of `n`, we will repeat the process of updating a running total `n` times.  To update the running total, we take the old value of the "running total" and add `n`.  That sum becomes the new
value of the "running total".

Here is the program in activecode.  Note that the function definition is the same as it was before.  All that has changed
is the details of how the squaring is done.  This is a great example of "black box" design.  We can change out the details inside of the box and still use the function exactly as we did before.


.. activecode:: sq_accum1

    def square(x):
        runningtotal = 0
        for counter in range(x):
            runningtotal = runningtotal + x

        return runningtotal

    toSquare = 10
    squareResult = square(toSquare)
    print("The result of", toSquare, "squared is", squareResult)





In the program above, notice that the variable ``runningtotal`` starts out with a value of 0.  Next, the iteration is performed ``x`` times.  Inside the for loop, the update occurs. ``runningtotal`` is reassigned a new value which is the old value plus the value of ``x``.


This pattern of iterating the updating of a variable is commonly
referred to as the **accumulator pattern**.  We refer to the variable as the **accumulator**.  This pattern will come up over and over again.  Remember that the key
to making it work successfully is to be sure to initialize the variable before you start the iteration.
Once inside the iteration, it is required that you update the accumulator.

.. note::

    What would happen if we put the assignment ``runningTotal = 0`` inside
    the for statement?  Not sure? Try it and find out.



Here is the same program in codelens.  Step through the function and watch the "running total" accumulate the result.

.. codelens:: sq_accum3

    def square(x):
        runningtotal = 0
        for counter in range(x):
            runningtotal = runningtotal + x

        return runningtotal

    toSquare = 10
    squareResult = square(toSquare)
    print("The result of", toSquare, "squared is", squareResult)





.. index::
    functional decomposition
    generalization
    abstraction


.. note::

   This workspace is provided for your convenience.  You can use this activecode window to try out anything you like.

   .. activecode:: scratch_05_04

**Check your understanding**

.. mchoicemf:: test_question5_4_1
   :answer_a: The square function will return x instead of x * x
   :answer_b: The square function will cause an error
   :answer_c: The square function will work as expected and return x * x
   :answer_d: The square function will return 0 instead of x * x
   :correct: a
   :feedback_a: The variable runningtotal will be reset to 0 each time through the loop.   However because this assignment happens as the first instruction, the next instruction in the loop will set it back to x.   When the loop finishes, it will have the value x, which is what is returned.
   :feedback_b: Assignment statements are perfectly legal inside loops and will not cause an error.
   :feedback_c: By putting the statement that sets runningtotal to 0 inside the loop, that statement gets executed every time through the loop, instead of once before the loop begins.  The result is that runningtotal is ìclearedî (reset to 0) each time through the loop.
   :feedback_d: The line runningtotal = 0 is the first line in the for loop, but immediately after this line, the line runningtotal = runningtotal + x will execute, giving runningtotal a non-zero value  (assuming x is non-zero).

   Consider the following code:

   .. code-block:: python

     def square(x):
         runningtotal = 0
         for counter in range(x):
             runningtotal = runningtotal + x
         return runningtotal

   What happens if you put the initialization of runningtotal (the
   line runningtotal = 0) inside the for loop as the first
   instruction in the loop?


.. parsonsprob:: question5_4_1p

   Rearrange the code statements so that the program will add up the first n odd numbers where n is provided by the user.
   -----
   n = int(input('How many odd numbers would
   you like to add together?'))
   thesum = 0
   oddnumber = 1
   =====
   for counter in range(n):
   =====
      thesum = thesum + oddnumber
      oddnumber = oddnumber + 2
   =====
   print(thesum)



