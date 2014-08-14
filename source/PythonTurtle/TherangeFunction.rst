..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

The range Function
------------------

.. video:: advrange
   :controls:
   :thumb: ../_static/advrange.png

   http://media.interactivepython.org/thinkcsVideos/AdvancedRange.mov
   http://media.interactivepython.org/thinkcsVideos/AdvancedRange.webm

In our simple example from the last section (shown again below), we used a list of four integers to cause the iteration
to happen four times.  We said that we could have used any four values.  In fact, we even used four colors.

.. sourcecode:: python

   import turtle            # set up alex
   wn = turtle.Screen()
   alex = turtle.Turtle()

   for i in [0, 1, 2, 3]:   # repeat four times
       alex.forward(50)
       alex.left(90)

   wn.exitonclick()

It turns out that generating lists with a specific number of integers is a very common thing to do, especially when you
want to write simple ``for loop`` controlled iteration.  Even though you can use any four items, or any four integers for that matter, the conventional thing to do is to use a list of integers starting with 0.
In fact, these lists are so popular that Python gives us special built-in
``range`` objects
that can deliver a sequence of values to
the ``for`` loop.  The sequence provided by ``range`` always starts with 0.  If you ask for ``range(4)``, then you will get 4 values starting with 0.  In other words, 0, 1, 2, and finally 3.  Notice that 4 is not included since we started with 0.  Likewise, ``range(10)`` provides 10 values, 0 through 9.

.. sourcecode:: python

      for i in range(4):
          # Executes the body with i = 0, then 1, then 2, then 3
      for x in range(10):
          # sets x to each of ... [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

.. note::

    Computer scientists like to count from 0!


So to repeat something four times, a good Python programmer would do this:

.. sourcecode:: python

    for i in range(4):
        alex.forward(50)
        alex.left(90)


The `range <http://docs.python.org/py3k/library/functions
.html?highlight=range#range>`_ function is actually a very powerful function
when it comes to
creating sequences of integers.  It can take one, two, or three parameters.  We have seen
the simplest case of one parameter such as ``range(4)`` which creates ``[0, 1, 2, 3]``.
But what if we really want to have the sequence ``[1, 2, 3, 4]``?
We can do this by using a two parameter version of ``range`` where the first parameter is the starting point and the second parameter is the ending point.  The evaluation of ``range(1,5)`` produces the desired sequence.  What happened to the 5?
In this case we interpret the parameters of the range function to mean
range(start,stop+1).


.. note::

    Why in the world would range not just work like range(start,
    stop)?  Think about it like this.  Because computer scientists like to
    start counting at 0 instead of 1, ``range(N)`` produces a sequence of
    things that is N long, but the consequence of this is that the final
    number of the sequence is N-1.  In the case of start,
    stop it helps to simply think that the sequence begins with start and
    continues as long as the number is less than stop.

Here are a two examples for you to run.  Try them and then add another line below to create a sequence starting
at 10 and going up to 20 (including 20).


.. activecode:: ch03_5
    :nocanvas:

    print(range(4))
    print(range(1, 5))


Codelens will help us to further understand the way range works.  In this case, the variable ``i`` will take on values
produced by the ``range`` function.

.. codelens:: rangeme

    for i in range(10):
       print(i)





Finally, suppose we want to have a sequence of even numbers.
How would we do that?  Easy, we add another parameter, a step,
that tells range what to count by.  For even numbers we want to start at 0
and count by 2's.  So if we wanted the first 10 even numbers we would use
``range(0,19,2)``.  The most general form of the range is
``range(start, stop, step)``.  You can also create a sequence of numbers that
starts big and gets smaller by using a negative value for the step parameter.

.. activecode:: ch03_6
    :nocanvas:

    print(range(0, 19, 2))
    print(range(0, 20, 2))
    print(range(10, 0, -1))

Try it in codelens.

.. codelens:: rangeme2

    for i in range(0, 20, 2):
       print(i)

**Check your understanding**

.. mchoicemf:: test_question3_5_1
  :answer_a: Range should generate a list that stops at 9 (including 9).
  :answer_b: Range should generate a list that starts at 10 (including 10).
  :answer_c: Range should generate a list starting at 3 that stops at 10 (including 10).
  :answer_d: Range should generate a list using every 10th number between the start and the stopping number.
  :correct: a
  :feedback_a: Range will generate the list [3, 5, 7, 9].
  :feedback_b: The first argument (3) tells range what number to start at.
  :feedback_c: Range will always stop at the number before (not including) the specified ending point for the list.
  :feedback_d: The third argument (2) tells range how many numbers to skip between each element in the list.

  In the command range(3, 10, 2), what does the second argument (10) specify?

.. mchoicemf:: test_question3_5_2
  :answer_a: range(2, 5, 8)
  :answer_b: range(2, 8, 3)
  :answer_c: range(2, 10, 3)
  :answer_d: range(8, 1, -3)
  :correct: c
  :feedback_a: This command generates the list [2] because the first number (2) tells range where to start, the second number tells range where to end (5, not inclusive) and the third number tells range how many numbers to skip between elements (8).  Since 10>= 8, there is only one number in this list.
  :feedback_b: This command generates the list [2, 5] because 8 is not less than 8 (the specified ending number).
  :feedback_c: The first number is the starting point, the second is the maximum allowed, and the third is the amount to increment by.
  :feedback_d: This command generates the list [8, 5, 3] because it starts at 8, ends at (or above 1), and skips every third number going down.

  What command correctly generates the list [2, 5, 8]?

.. mchoicemf:: test_question3_5_3
  :answer_a: It will generate a list starting at 0, with every number included up to but not including the argument it was passed.
  :answer_b: It will generate a list starting at 1, with every number up to but not including the argument it was passed.
  :answer_c: It will generate a list starting at 1, with every number including the argument it was passed.
  :answer_d: It will cause an error: range always takes exactly 3 arguments.
  :correct: a
  :feedback_a: Yes, if you only give one number to range it starts with 0 and ends before the number specified incrementing by 1.
  :feedback_b: Range starts at 0 unless otherwise specified.
  :feedback_c: Range starts at 0 unless otherwise specified, and never includes its ending element (which is the argument it was passed).
  :feedback_d: If range is passed only one argument, it interprets that argument as the end of the list (not inclusive).

  What happens if you give range only one argument?  For example: range(4)




