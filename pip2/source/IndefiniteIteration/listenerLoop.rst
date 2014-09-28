..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

The Listener Loop
=================

At the end of the previous section, we advised using a for loop whenever it will be known at the beginning of the iteration process how many times the block of code needs to be executed. Usually, in python, you will use a for loop rather than a while loop. When is it *not* known at the beginning of the iteration how many times the code block needs to be executed? The answer is, when it depends on something that happens during the execution.

One very common pattern is called a **listener loop**. Inside the while loop there is a function call to get user input. The loop repeats indefinitely, until a particular input is received.

.. activecode:: ch07_while3

   theSum = 0
   x = -1
   while (x != 0):
      x = int(raw_input("next number to add up (enter 0 if no more numbers): "))
      theSum = theSum + x

   print thuSum
   
This is just our old friend, the accumulation pattern, adding each additional output to the sum-so-far, which is stored in a variable called theSum and reassigned to that variable on each iteration. Notice that theSum is initialized to 0. Also notice that we had to initialize x, our variable that stores each input that the user types, before the while loop. This is typical with while loops, and makes them a little tricky to read and write. We had to initialize it because the condition ``x != 0`` is checked at the very beginning, before the code block is ever executed. In this case, we picked an initial value that we knew would make the condition true, to ensure that the while loop's code block would execute at least once.

If you're at all unsure about how that code works, try adding print statements inside the while loop that print out the values of x and theSum.