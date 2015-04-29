..  Copyright (C)  Paul Resnick, Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

..  shortname:: MoreAboutIteration
..  description:: This module has more information about iteration and while loops

.. qnum::
   :prefix: itr-
   :start: 1
   
.. _while_loop:
 

Iteration Revisited
===================

.. index:: iteration, assignment, assignment statement, reassignment

.. index::
    single: statement; assignment


Computers are often used to automate repetitive tasks. Repeating identical or
similar tasks without making errors is something that computers do well and
people do poorly.

Repeated execution of a sequence of statements is called **iteration**.  Because
iteration is so common, Python provides several language features to make it
easier. We've already seen the ``for`` statement in a previous chapter.  This is a very common
form of iteration in Python. In this chapter
we are going to look at the ``while`` statement --- another way to have your
program do iteration.


.. index:: for loop

The ``for`` loop revisited
--------------------------

Recall that the ``for`` loop processes each item in a list.  Each item in
turn is (re-)assigned to the loop variable, and the body of the loop is executed.
We saw this example in an earlier chapter.

.. activecode:: ch07_for1

    for f in ["Joe", "Amy", "Brad", "Angelina", "Zuki", "Thandi", "Paris"]:
        print("Hi", f, "Please come to my party on Saturday")


We have also seen iteration paired with the update idea to form the accumulator pattern.  For example, to compute
the sum of the first n integers, we could create a for loop using the ``range`` to produce the numbers 1 thru n.
Using the accumulator pattern, we can start with a running total variable initialized to 0 and on each iteration, add the current value of the loop
variable.  A function to compute this sum is shown below.

.. activecode:: ch07_summation

    def sumTo(aBound):
        theSum = 0
        for aNumber in range(1, aBound+1):
            theSum = theSum + aNumber

        return theSum

    print(sumTo(4))

    print(sumTo(1000))

To review, the variable ``theSum`` is called the accumulator.  It is initialized to zero before we start the loop.  The loop variable, ``aNumber`` will take on the values produced by the ``range(1,aBound+1)`` function call.  Note that this produces all the integers from 1 up to the value of ``aBound``.  If we had not added 1 to ``aBound``, the range would have stopped one value short since ``range`` does not include the upper bound.

The assignment statement, ``theSum = theSum + aNumber``, updates ``theSum`` each time thru the loop.  This accumulates the running total.  Finally, we return the value of the accumulator.




The ``while`` Statement
-----------------------

.. video:: whileloop
   :controls:
   :thumb: ../_static/whileloop.png

   http://media.interactivepython.org/thinkcsVideos/whileloop.mov
   http://media.interactivepython.org/thinkcsVideos/whileloop.webm

There is another Python statement that can also be used to build an iteration.  It is called the ``while`` statement.
The ``while`` statement provides a much more general mechanism for iterating.  Similar to the ``if`` statement, it uses
a boolean expression to control the flow of execution.  The body of while will be repeated as long as the controlling boolean expression evaluates to ``True``.

The following figure shows the flow of control.

.. image:: Figures/while_flow.png

We can use the ``while`` loop to create any type of iteration we wish, including anything that we have previously done with a ``for`` loop.  For example, the program in the previous section could be rewritten using ``while``.
Instead of relying on the ``range`` function to produce the numbers for our summation, we will need to produce them ourselves.  To to this, we will create a variable called ``aNumber`` and initialize it to 1, the first number in the summation.  Every iteration will add ``aNumber`` to the running total until all the values have been used.
In order to control the iteration, we must create a boolean expression that evaluates to ``True`` as long as we want to keep adding values to our running total.  In this case, as long as ``aNumber`` is less than or equal to the bound, we should keep going.



Here is a new version of the summation program that uses a while statement.

.. activecode:: ch07_while1

    def sumTo(aBound):
        """ Return the sum of 1+2+3 ... n """

        theSum  = 0
        aNumber = 1
        while aNumber <= aBound:
            theSum = theSum + aNumber
            aNumber = aNumber + 1
        return theSum

    print(sumTo(4))

    print(sumTo(1000))



You can almost read the ``while`` statement as if it were in natural language. It means,
while ``aNumber`` is less than or equal to ``aBound``, continue executing the body of the loop. Within
the body, each time, update ``theSum`` using the accumulator pattern and increment ``aNumber``. After the body of the loop, we go back up to the condition of the ``while`` and reevaluate it.  When ``aNumber`` becomes greater than ``aBound``, the condition fails and flow of control continues to the ``return`` statement.

The same program in codelens will allow you to observe the flow of execution.

.. codelens:: ch07_while2

    def sumTo(aBound):
        """ Return the sum of 1+2+3 ... n """

        theSum  = 0
        aNumber = 1
        while aNumber <= aBound:
            theSum = theSum + aNumber
            aNumber = aNumber + 1
        return theSum

    print(sumTo(4))



.. note:: The names of the variables have been chosen to help readability.

More formally, here is the flow of execution for a ``while`` statement:

#. Evaluate the condition, yielding ``False`` or ``True``.
#. If the condition is ``False``, exit the ``while`` statement and continue
   execution at the next statement.
#. If the condition is ``True``, execute each of the statements in the body and
   then go back to step 1.

The body consists of all of the statements below the header with the same
indentation.

This type of flow is called a **loop** because the third step loops back around
to the top. Notice that if the condition is ``False`` the first time through the
loop, the statements inside the loop are never executed.

The body of the loop should change the value of one or more variables so that
eventually the condition becomes ``False`` and the loop terminates. Otherwise the
loop will repeat forever. This is called an **infinite loop**.
An endless
source of amusement for computer scientists is the observation that the
directions written on the back of the shampoo bottle (lather, rinse, repeat) create an infinite loop.

In the case shown above, we can prove that the loop terminates because we
know that the value of ``aBound`` is finite, and we can see that the value of ``aNumber``
increments each time through the loop, so eventually it will have to exceed ``aBound``. In
other cases, it is not so easy to tell.

.. note::

    Introduction of the while statement causes us to think about the types of iteration we have seen.  The ``for`` statement will always iterate through a sequence of values like the list of names for the party or the list of numbers created by ``range``.  Since we know that it will iterate once for each value in the collection, it is often said that a ``for`` loop creates a
    **definite iteration** because we definitely know how many times we are going to iterate.  On the other
    hand, the ``while`` statement is dependent on a condition that needs to evaluate to ``False`` in order
    for the loop to terminate.  Since we do not necessarily know when this will happen, it creates what we
    call **indefinite iteration**.  Indefinite iteration simply means that we don't know how many times we will repeat but eventually the condition controlling the iteration will fail and the iteration will stop. (Unless we have an infinite loop which is of course a problem)

What you will notice here is that the ``while`` loop is more work for
you --- the programmer --- than the equivalent ``for`` loop.  When using a ``while``
loop you have to control the loop variable yourself.  You give it an initial value, test
for completion, and then make sure you change something in the body so that the loop
terminates.


**Check your understanding**

.. mchoicemf:: test_question7_2_1
   :answer_a: True
   :answer_b: False
   :correct: a
   :feedback_a: Although the while loop uses a different syntax, it is just as powerful as a for-loop and often more flexible.
   :feedback_b: Often a for-loop is more natural and convenient for a task, but that same task can always be expressed using a while loop.

   True or False: You can rewrite any for-loop as a while-loop.

.. mchoicemf:: test_question7_2_2
   :answer_a: n starts at 10 and is incremented by 1 each time through the loop, so it will always be positive
   :answer_b: answer starts at 1 and is incremented by n each time, so it will always be positive
   :answer_c: You cannot compare n to 0 in while loop.  You must compare it to another variable.
   :answer_d: In the while loop body, we must set n to False, and this code does not do that.  
   :correct: a
   :feedback_a: The loop will run as long as n is positive.  In this case, we can see that n will never become non-positive.
   :feedback_b: While it is true that answer will always be positive, answer is not considered in the loop condition.
   :feedback_c: It is perfectly valid to compare n to 0.  Though indirectly, this is what causes the infinite loop.
   :feedback_d: The loop condition must become False for the loop to terminate, but n by itself is not the condition in this case.

   The following code contains an infinite loop.  Which is the best explanation for why the loop does not terminate?

   .. code-block:: python

     n = 10
     answer = 1
     while ( n > 0 ):
       answer = answer + n
       n = n + 1
     print answer

.. mchoicemf:: test_question7_3_1
   :answer_a: a for-loop or a while-loop
   :answer_b: only a for-loop
   :answer_c: only a while-loop
   :correct: a
   :feedback_a: Although you do not know how many iterations you loop will run before the program starts running, once you have chosen your random integer, Python knows exactly how many iterations the loop will run, so either a for-loop or a while-loop will work.
   :feedback_b: As you learned in section 7.2, a while-loop can always be used for anything a for-loop can be used for.
   :feedback_c: Although you do not know how many iterations you loop will run before the program starts running, once you have chosen your random integer, Python knows exactly how many iterations the loop will run, so this is an example of definite iteration.

   Which type of loop can be used to perform the following iteration: You choose a positive integer at random and then print the numbers from 1 up to and including the selected integer.

So why have two kinds of loop if ``for`` looks easier?  

In the problem sets involving the Hangman game, you have seen an example where guesses are made until
either the word is guessed or health goes down to 0. Since the number of guesses 
that would be needed can't be fixed in advance, a while loop was needed rather
than a for loop.

The next example shows another indefinite iteration where
we need the extra power that we get from the ``while`` loop because we can't predict
in advance how many repetitions of the code block will be needed (or even 
whether an infinite number will be needed).


.. index:: 3n + 1 sequence

The 3n + 1 Sequence
-------------------

As another example of indefinite iteration, let's look at a sequence that has fascinated mathematicians for many years.
The rule  for creating the sequence is to start from
some given number, call it ``n``, and to generate
the next term of the sequence from ``n``, either by halving ``n``,
whenever ``n`` is even, or else by multiplying it by three and adding 1 when it is odd.  The sequence
terminates when ``n`` reaches 1.

This Python function captures that algorithm.  Try running this program several times supplying different values for n.

.. activecode:: ch07_indef1

    def seq3np1(n):
        """ Print the 3n+1 sequence from n, terminating when it reaches 1."""
        while n != 1:
            print(n)
            if n % 2 == 0:        # n is even
                n = n // 2
            else:                 # n is odd
                n = n * 3 + 1
        print(n)                  # the last print is 1

    seq3np1(3)


The condition for this loop is ``n != 1``.  The loop will continue running until
``n == 1`` (which will make the condition false).

Each time through the loop, the program prints the value of ``n`` and then
checks whether it is even or odd using the remainder operator. If it is even, the value of ``n`` is divided
by 2 using integer division. If it is odd, the value is replaced by ``n * 3 + 1``.
Try some other examples.

Since ``n`` sometimes increases and sometimes decreases, there is no obvious
proof that ``n`` will ever reach 1, or that the program terminates. For some
particular values of ``n``, we can prove termination. For example, if the
starting value is a power of two, then the value of ``n`` will be even each
time through the loop until it reaches 1.

You might like to have some fun and see if you can find a small starting
number that needs more than a hundred steps before it terminates.

Particular values aside, the interesting question is whether we can prove that
this sequence terminates for *all* values of ``n``. So far, no one has been able
to prove it *or* disprove it!

Think carefully about what would be needed for a proof or disproof of the hypothesis
*"All positive integers will eventually converge to 1"*.  With fast computers we have
been able to test every integer up to very large values, and so far, they all
eventually end up at 1.  But this doesn't mean that there might not be some
as-yet untested number which does not reduce to 1.

You'll notice that if you don't stop when you reach one, the sequence gets into
its own loop:  1, 4, 2, 1, 4, 2, 1, 4, and so on.  One possibility is that there might
be other cycles that we just haven't found.

.. admonition:: Choosing between ``for`` and ``while``

   Use a ``for`` loop if you know the maximum number of times that you'll
   need to execute the body.  For example, if you're traversing a list of elements,
   or can formulate a suitable call to ``range``, then choose the ``for`` loop.

   So any problem like "iterate this weather model run for 1000 cycles", or "search this
   list of words", "check all integers up to 10000 to see which are prime" suggest that a ``for`` loop is best.

   By contrast, if you are required to repeat some computation until some condition is
   met, as we did in this 3n + 1 problem, you'll need a ``while`` loop.

   As we noted before, the first case is called **definite iteration** --- we have some definite bounds for
   what is needed.   The latter case is called **indefinite iteration** --- we are not sure
   how many iterations we'll need --- we cannot even establish an upper bound!



.. There are also some great visualization tools becoming available to help you
.. trace and understand small fragments of Python code.  The one we recommend is at
.. http://netserv.ict.ru.ac.za/python3_viz


**Check your understanding**

.. mchoicemf:: test_question7_4_1
   :answer_a: Yes.
   :answer_b: No.
   :answer_c: No one knows.
   :correct: c
   :feedback_a: The 3n+1 sequence has not been proven to terminate for all values of n.
   :feedback_b: It has not been disproven that the 3n+1 sequence will terminate for all values of n.  In other words, there might be some value for n such that this sequence does not terminate. We just have not found it yet.
   :feedback_c: That this sequence terminates for all values of n has not been proven or disproven so no one knows whether the while loop will always terminate or not.

   Consider the code that prints the 3n+1 sequence in ActiveCode box 6.  Will the while loop in this code always terminate for any value of n?


.. index::
    single: Newton's method


Newton's Method
---------------

Loops are often used in programs that compute numerical results by starting
with an approximate answer and iteratively improving it.

For example, one way of computing square roots is Newton's method.  Suppose
that you want to know the square root of ``n``. If you start with almost any
approximation, you can compute a better approximation with the following
formula:

.. sourcecode:: python

    better =  1/2 * (approx + n/approx)

Execute this algorithm a few times using your calculator.  Can you
see why each iteration brings your estimate a little closer?  One of the amazing
properties of this particular algorithm is how quickly it converges to an accurate
answer.

The following implementation of Newton's method requires two parameters.  The first is the
value whose square root will be approximated.  The second is the number of times to iterate the
calculation yielding a better result.

.. activecode:: chp07_newtonsdef

    def newtonSqrt(n, howmany):
        approx = 0.5 * n
        for i in range(howmany):
            betterapprox = 0.5 * (approx + n/approx)
            approx = betterapprox
        return betterapprox

    print(newtonSqrt(10,3))
    print(newtonSqrt(10,5))
    print(newtonSqrt(10,10))


You may have noticed that the second and third calls to ``newtonSqrt`` in the previous example both returned the same value for the square root of 10.  Using 10 iterations instead of 5 did not improve the the value.  In general, Newton's algorithm will eventually reach a point where the new approximation is no better than the previous.  At that point, we could simply stop.
In other words, by repeatedly applying this formula until the better approximation gets close
enough to the previous one, we can write a function for computing the square root that uses the number of iterations necessary and no more.

This implementation, shown in codelens,
uses a ``while`` condition to execute until the approximation is no longer changing.  Each time thru the loop we compute a "better" approximation using the formula described earlier.  As long as the "better" is different, we try again.  Step thru the program and watch the approximations get closer and closer.

.. codelens:: chp07_newtonswhile

    def newtonSqrt(n):
        approx = 0.5 * n
        better = 0.5 * (approx + n/approx)
        while  better !=  approx:
            approx = better
            better = 0.5 * (approx + n/approx)
        return approx

    print(newtonSqrt(10))

.. note::

    The ``while`` statement shown above uses comparison of two floating point numbers in the condition.  Since floating point numbers are themselves approximation of real numbers in mathematics, it is often
    better to compare for a result that is within some small threshold of the value you are looking for.

.. index:: algorithm


Algorithms Revisited
--------------------

Newton's method is an example of an **algorithm**: it is a mechanical process
for solving a category of problems (in this case, computing square roots).

It is not easy to define an algorithm. It might help to start with something
that is not an algorithm. When you learned to multiply single-digit numbers,
you probably memorized the multiplication table.  In effect, you memorized 100
specific solutions. That kind of knowledge is not algorithmic.

But if you were lazy, you probably cheated by learning a few tricks.  For
example, to find the product of n and 9, you can write n - 1 as the first digit
and 10 - n as the second digit. This trick is a general solution for
multiplying any single-digit number by 9. That's an algorithm!

Similarly, the techniques you learned for addition with carrying, subtraction
with borrowing, and long division are all algorithms. One of the
characteristics of algorithms is that they do not require any intelligence to
carry out. They are mechanical processes in which each step follows from the
last according to a simple set of rules.

On the other hand, understanding that hard problems can be solved by step-by-step
algorithmic processess is one of the major simplifying breakthroughs that has
had enormous benefits.  So while the execution of the algorithm
may be boring and may require no intelligence, algorithmic or computational
thinking is having a vast impact.  It is the process of designing algorithms that is interesting,
intellectually challenging, and a central part of what we call programming.

Some of the things that people do naturally, without difficulty or conscious
thought, are the hardest to express algorithmically.  Understanding natural
language is a good example. We all do it, but so far no one has been able to
explain *how* we do it, at least not in the form of a step-by-step mechanical
algorithm.


Glossary
--------

.. glossary::


    algorithm
        A step-by-step process for solving a category of problems.

    body
        The statements inside a loop.


    counter
        A variable used to count something, usually initialized to zero and
        incremented in the body of a loop.


    definite iteration
        A loop where we have an upper bound on the number of times the
        body will be executed.  Definite iteration is usually best coded
        as a ``for`` loop.

    generalize
        To replace something unnecessarily specific (like a constant value)
        with something appropriately general (like a variable or parameter).
        Generalization makes code more versatile, more likely to be reused, and
        sometimes even easier to write.



    infinite loop
        A loop in which the terminating condition is never satisfied.

    indefinite iteration
        A loop where we just need to keep going until some condition is met.
        A ``while`` statement is used for this case.



    iteration
        Repeated execution of a set of programming statements.

    loop
        A statement or group of statements that execute repeatedly until a
        terminating condition is satisfied.

    loop variable
        A variable used as part of the terminating condition of a loop.    

    nested loop
        A loop inside the body of another loop.

    reassignment
        Making more than one assignment to the same variable during the
        execution of a program.



     
    tab
        A special character that causes the cursor to move to the next tab stop
        on the current line.



Exercises
---------



#.

    .. tabbed:: q1

        .. tab:: Question

           Add a print statement to Newton's ``sqrt`` function that
           prints out ``better`` each time it is calculated. Call your modified
           function with 25 as an argument and record the results.
        
           .. actex:: ex_7_7
        
                def newtonSqrt(n):
                    approx = 0.5 * n
                    better = 0.5 * (approx + n/approx)
                    while  better !=  approx:
                        approx = better
                        better = 0.5 * (approx + n/approx)
                    return approx


                print ("Final approx:", newtonSqrt(25))

        .. tab:: Answer
            
            .. activecode:: q1_answer

                def newtonSqrt(n):
                    approx = 0.5 * n
                    better = 0.5 * (approx + n/approx)
                    while  better !=  approx:
                        approx = better
                        better = 0.5 * (approx + n/approx)
                        print (" Approx:", better)
                    return approx


                print ("Final approx:", newtonSqrt(25))


#.

    .. tabbed:: q2

        .. tab:: Question

           A note above suggests that when testing whether two floating point
           numbers are equal, it's better to check if they are almost equal, because
           of rounding errors in the representation of floating point numbers internally
           in computers. 
           
           Rewrite  Newton's ``sqrt`` function to take an extra parameter, the tolerance,
           and have the iteration stop when better and approx are almost equal, the difference
           being no greater than the tolerance. Try invoking it with a tolerance of .01, .0001, and .000001.
        
           .. actex:: ex_7_7a
        
                def newtonSqrt(n):
                    approx = 0.5 * n
                    better = 0.5 * (approx + n/approx)
                    while  better !=  approx:
                        approx = better
                        better = 0.5 * (approx + n/approx)
                        print (" Approx:", better)
                    return approx


        .. tab:: Answer
            
            .. activecode:: q2_answer

                def newtonSqrt(n, tolerance = .01):
                    approx = 0.5 * n
                    better = 0.5 * (approx + n/approx)
                    while  abs(better - approx) > tolerance:
                        approx = better
                        better = 0.5 * (approx + n/approx)
                    return approx
                
                for x in [.01,.0001, .0000001]:
                    y = newtonSqrt(10, x)
                    print (newtonSqrt(10, x), y*y)

