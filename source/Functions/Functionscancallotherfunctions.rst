..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Functions can Call Other Functions
----------------------------------

It is important to understand that each of the functions we write can be used
and called from other functions we write.  This is one of the most important
ways that computer scientists take a large problem and break it down into a
group of smaller problems. This process of breaking a problem into smaller
subproblems is called **functional decomposition**.

Here's a simple example of functional decomposition using two functions. The
first function called ``square`` simply computes the square of a given number.
The second function called ``sum_of_squares`` makes use of square to compute
the sum of three numbers that have been squared.

.. codelens:: sumofsquares

    def square(x):
        y = x * x
        return y

    def sum_of_squares(x, y, z):
        a = square(x)
        b = square(y)
        c = square(z)

        return a + b + c

    a = -5
    b = 2
    c = 10
    result = sum_of_squares(a, b, c)
    print(result)


Even though this is a pretty simple idea, in practice this example
illustrates many very important Python concepts, including local and global
variables along with parameter passing.  Note that when you step through this
example, codelens bolds line 1 and line 5 as the functions are defined.  The
body of square is not executed until it is called from the ``sum_of_squares``
function for the first time on line 6.  Also notice that when ``square`` is
called there are two groups of local variables, one for ``square`` and one
for ``sum_of_squares``.  As you step through you will notice that ``x``, and ``y`` are local variables in both functions and may even have
different values.  This illustrates that even though they are named the same,
they are in fact, very different.

Now we will look at another example that uses two functions.  This example illustrates an
important computer science problem solving technique called
**generalization**.  Assume we want to write a
function to draw a square.  The generalization step is to realize that a
square is just a special kind of rectangle.

To draw a rectangle we need to be able to call a function with different
arguments for width and height.  Unlike the case of the square,
we cannot repeat the same thing 4 times, because the four sides are not equal.
However, it is the case that drawing the bottom and right sides are the
same sequence as drawing the top and left sides.  So we eventually come up with
this rather nice code that can draw a rectangle.

.. code-block:: python

    def drawRectangle(t, w, h):
        """Get turtle t to draw a rectangle of width w and height h."""
        for i in range(2):
            t.forward(w)
            t.left(90)
            t.forward(h)
            t.left(90)

The parameter names are deliberately chosen as single letters to ensure they're not misunderstood.
In real programs, once you've had more experience, we will insist on better variable names than this.
The point is that the program doesn't "understand" that you're drawing a rectangle or that the
parameters represent the width and the height.  Concepts like rectangle, width, and height are meaningful
for humans.  They are not concepts that the program or the computer understands.

*Thinking like a computer scientist* involves looking for patterns and
relationships.  In the code above, we've done that to some extent.  We did
not just draw four sides. Instead, we spotted that we could draw the
rectangle as two halves and used a loop to repeat that pattern twice.

But now we might spot that a square is a special kind of rectangle.  A square
simply uses the same value for both the height and the width.
We already have a function that draws a rectangle, so we can use that to draw
our square.

.. code-block:: python

    def drawSquare(tx, sz):        # a new version of drawSquare
        drawRectangle(tx, sz, sz)

Here is the entire example with the necessary set up code.

.. activecode:: ch04_3

    import turtle

    def drawRectangle(t, w, h):
        """Get turtle t to draw a rectangle of width w and height h."""
        for i in range(2):
            t.forward(w)
            t.left(90)
            t.forward(h)
            t.left(90)

    def drawSquare(tx, sz):        # a new version of drawSquare
        drawRectangle(tx, sz, sz)

    wn = turtle.Screen()             # Set up the window
    wn.bgcolor("lightgreen")

    tess = turtle.Turtle()           # create tess

    drawSquare(tess, 50)

    wn.exitonclick()



There are some points worth noting here:

* Functions can call other functions.
* Rewriting `drawSquare` like this captures the relationship
  that we've spotted.
* A caller of this function might say `drawSquare(tess, 50)`.  The parameters
  of this function, ``tx`` and ``sz``, are assigned the values of the tess object, and
  the integer 50 respectively.
* In the body of the function, ``tz`` and ``sz`` are just like any other variable.
* When the call is made to ``drawRectangle``, the values in variables ``tx`` and ``sz``
  are fetched first, then the call happens.  So as we enter the top of
  function `drawRectangle`, its variable ``t`` is assigned the tess object, and ``w`` and
  ``h`` in that function are both given the value 50.


So far, it may not be clear why it is worth the trouble to create all of these
new functions. Actually, there are a lot of reasons, but this example
demonstrates two:

#. Creating a new function gives you an opportunity to name a group of
   statements. Functions can simplify a program by hiding a complex computation
   behind a single command. The function (including its name) can capture your
   mental chunking, or *abstraction*, of the problem.
#. Creating a new function can make a program smaller by eliminating repetitive
   code.
#. Sometimes you can write functions that allow you to solve a specific
   problem using a more general solution.


.. admonition:: Lab

    * `Drawing a Circle <../Labs/lab04_01.html>`_ In this guided lab exercise we will work
      through a simple problem solving exercise related to drawing a circle with the turtle.

.. index:: flow of execution



