..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. qnum::
   :prefix: iter-2-
   :start: 1

The ``for`` loop revisited
--------------------------

Recall that the ``for`` loop processes each item in a list.  Each item in
turn is (re-)assigned to the loop variable, and the body of the loop is executed.
We saw this example in an earlier chapter.

.. activecode:: ch07_for1

    for f in ["Joe", "Amy", "Brad", "Angelina", "Zuki", "Thandi", "Paris"]:
        print("Hi", f, "Please come to my party on Saturday")


We have also seen iteration paired with the update idea to form the accumulator pattern.  For example, to compute
the sum of the first n integers, we could create a for loop using the ``range`` to produce the numbers 1 through n.
Using the accumulator pattern, we can start with a running total variable initialized to 0 and on each iteration, add the current value of the loop
variable.  A function to compute this sum is shown below.

.. activecode:: ch07_summation

    def sumTo(aBound):
        theSum = 0
        for aNumber in range(1, aBound + 1):
            theSum = theSum + aNumber

        return theSum

    print(sumTo(4))

    print(sumTo(1000))

To review, the variable ``theSum`` is called the accumulator.  It is initialized to zero before we start the loop.  The loop variable, ``aNumber`` will take on the values produced by the ``range(1, aBound + 1)`` function call.  Note that this produces all the integers from 1 up to the value of ``aBound``.  If we had not added 1 to ``aBound``, the range would have stopped one value short since ``range`` does not include the upper bound.

The assignment statement, ``theSum = theSum + aNumber``, updates ``theSum`` each time through the loop.  This accumulates the running total.  Finally, we return the value of the accumulator.




