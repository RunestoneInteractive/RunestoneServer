..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

The `random` module
-----------------------------------

We often want to use **random numbers** in programs.  Here are a few typical uses:

* To play a game of chance where the computer needs to throw some dice, pick a number, or flip a coin,
* To shuffle a deck of playing cards randomly,
* To randomly allow a new enemy spaceship to appear and shoot at you,
* To simulate possible rainfall when we make a computerized model for
  estimating the environmental impact of building a dam,
* For encrypting your banking session on the Internet.

Python provides a module ``random`` that helps with tasks like this.  You can
take a look at it in the documentation.  Here are the key things we can do with it.

.. activecode:: chmodule_rand

    import random

    prob = random.random()
    print(prob)

    diceThrow = random.randrange(1,7)       # return an int, one of 1,2,3,4,5,6
    print(diceThrow)

Press the run button a number of times.  Note that the values change each time.  These are random numbers.

The ``randrange`` function generates an integer between its lower and upper
argument, using the same semantics as ``range`` --- so the lower bound is included, but
the upper bound is excluded.   All the values have an equal probability of occurring
(i.e. the results are *uniformly* distributed).

The ``random()`` function returns a floating point number in the range [0.0, 1.0) --- the
square bracket means "closed interval on the left" and the round parenthesis means
"open interval on the right".  In other words, 0.0 is possible, but all returned
numbers will be strictly less than 1.0.  It is usual to *scale* the results after
calling this method, to get them into a range suitable for your application.

In the
case shown here, we've converted the result of the method call to a number in
the range [0.0, 5.0).  Once more, these are uniformly distributed numbers --- numbers
close to 0 are just as likely to occur as numbers close to 0.5, or numbers close to 1.0.
If you continue to press the run button you will see random values between 0.0 and up to but not including 5.0.

.. activecode:: chmodule_rand2

    import random

    prob = random.random()
    result = prob * 5
    print(result)






.. index:: deterministic algorithm,  algorithm; deterministic, unit tests

It is important to note that
random number generators are based on a **deterministic** algorithm --- repeatable and predictable.
So they're called **pseudo-random** generators --- they are not genuinely random.
They start with a *seed* value. Each time you ask for another random number, you'll get
one based on the current seed attribute, and the state of the seed (which is one
of the attributes of the generator) will be updated.  The good news is that each time you run your program, the seed value
is likely to be different meaning that even though the random numbers are being created algorithmically, you will likely
get random behavior each time you execute.


.. admonition:: Lab

    * `Sine Wave <../Labs/sinlab.html>`_ In this guided lab exercise we will have the turtle plot a sine wave.

**Check your understanding**

.. mchoicemf:: question4_4_1
   :answer_a: math.pi
   :answer_b: math(pi)
   :answer_c: pi.math
   :answer_d: math->pi
   :correct: a
   :feedback_a: To invoke or reference something contained in a module you use the dot (.) notation.
   :feedback_b: This is the syntax for calling a function, not referencing an item in a module.
   :feedback_c: The module name must come first when accessing values and functions with a module.
   :feedback_d: The -> notation is not used in Python.

   Which of the following is the correct way to reference the value pi within the math module.   Assume you have already imported the math module.

.. mchoicemf:: question4_4_2
   :answer_a: the math module
   :answer_b: the random module
   :answer_c: the turtle module
   :answer_d: the game module
   :correct: b
   :feedback_a: While you might want to use the math module for other numerical computations in your program, it does not contain functions that are likely to help you simulate a dice roll.
   :feedback_b: You would likely call the function random.randrange.
   :feedback_c: The turtle module, while producing interesting graphics, is unlikely to help you here.
   :feedback_d: Python does not have a game module.

   Which module would you most likely use if you were writing a function to simulate rolling dice?


.. mchoicemf:: question4_4_3
   :answer_a: prob = random.randrange(1, 101)
   :answer_b: prob = random.randrange(1, 100)
   :answer_c: prob = random.randrange(0, 101)
   :answer_d: prob = random.randrange(0, 100)
   :correct: a
   :feedback_a: This will generate a number between 1 and 101, but does not include 101.
   :feedback_b: This will generate a number between 1 and 100, but does not include 100.  The highest value generated will be 99.
   :feedback_c: This will generate a number between 0 and 100.  The lowest value generated is 0.  The highest value generated will be 100.
   :feedback_d: This will generate a number between 0 and 100, but does not include 100.  The lowest value generated is 0 and the highest value generated will be 99.

   The correct code to generate a random number between 1 and 100 (inclusive) is:

.. mchoicemf:: question4_4_4
   :answer_a: There is no computer on the stage for the drawing.
   :answer_b: Because computers don’t really generate random numbers, they generate pseudo-random numbers.
   :answer_c: They would just generate the same numbers over and over again.
   :answer_d: The computer can’t tell what values were already selected, so it might generate all 5’s instead of 5 unique numbers.
   :correct: b
   :feedback_a: They could easily put one there.
   :feedback_b: Computers generate random numbers using a deterministic algorithm.  This means that if anyone ever found out the algorithm they could accurately predict the next value to be generated and would always win the lottery.
   :feedback_c: This might happen if the same seed value was used over and over again, but they could make sure this was not the case.
   :feedback_d: While a programmer would need to ensure the computer did not select the same number more than once, it is easy to ensure this.

   One reason that lotteries don’t use computers to generate random numbers is:


.. note::

   This workspace is provided for your convenience.  You can use this activecode window to try out anything you like.

   .. activecode:: scratch_04



