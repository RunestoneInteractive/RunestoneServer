..  Copyright (C)  Brad Miller, David Ranum
    Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Drawing Fractals
----------------

**Recursion** means "defining something in terms of itself" usually at some 
smaller scale, perhaps multiple times, to achieve your objective.  
For example, we might say "A human being is someone whose mother is a human being."   

For our purposes, a **fractal** is drawing which also has *self-similar* structure.
Its structure can be defined in terms of itself.

Let us start by looking at the famous Koch fractal.  An order 0 Koch fractal is simply
a straight line of a given size.

.. image:: Figures/koch_0.png

An order 1 Koch fractal is obtained like this: instead of drawing just one line,
draw instead four smaller segments, in the pattern shown here:

.. image:: Figures/koch_1.png

Now what would happen if we repeated this Koch pattern again on each of the order 1 segments?  
We'd get this order 2 Koch fractal:

.. image:: Figures/koch_2.png

Repeating our pattern again gets us an order 3 Koch fractal:

.. image:: Figures/koch_3.png

Now let us think about it the other way around.  To draw a Koch fractal
of order 3, we can simply draw four order 2 Koch fractals.  But each of these
in turn needs four order 1 Koch fractals, and each of those in turn needs four
order 0 fractals.  Ultimately, the only drawing that will take place is 
at order 0. This is very simple to code up in Python.

.. activecode:: chp12_koch
   
    import turtle

    def koch(t, order, size):
        """
           Make turtle t draw a Koch fractal of 'order' and 'size'.
           Leave the turtle facing the same direction.
        """

        if order == 0:                  # The base case is just a straight line
            t.forward(size)
        else:
            koch(t, order-1, size/3)   # go 1/3 of the way
            t.left(60)
            koch(t, order-1, size/3)
            t.right(120)
            koch(t, order-1, size/3)
            t.left(60)
            koch(t, order-1, size/3) 

    fred = turtle.Turtle()
    wn = turtle.Screen()
  
    fred.color("blue")
    wn.bgcolor("green")
    fred.penup()
    fred.backward(150)
    fred.pendown()

    koch(fred, 3, 300)

    wn.exitonclick()

Try running this program with different values for the order.  For example, try order 0, then 1, then 2, and so on.
            
The key thing that is new here is that if order is not zero,
``koch`` calls itself four times to get the job done.  This self-reference is the recursion.


.. admonition:: Recursion, the high-level view

    One way to think about this is to convince yourself that the function
    works correctly when you call it for an order 0 fractal.  Then do
    a mental *leap of faith*, saying *"the fairy godmother* (or Python, if
    you can think of Python as your fairy godmother) *knows how to 
    handle the recursive level 0 calls for me on lines 12, 14, 16, and 18, so
    I don't need to think about that detail!"*  All I need to focus on
    is how to draw an order 1 fractal *if I can assume the order 0 one is
    already working.*
    
    You're practicing *mental abstraction* --- ignoring the subproblem 
    while you solve the big problem.

    If this mode of thinking works (and you should practice it!), then take
    it to the next level.  Aha! now can I see that it will work when called
    for order 2 *under the assumption that it is already working for level 1*.  

    And, in general, if I can assume the order n-1 case works, can I just 
    solve the level n problem?

    Students of mathematics who have played with proofs of induction should
    see some very strong similarities here.  



.. index::
    single: data structure
    single: data structure; recursive
    single: recursive definition
    single: definition; recursive
    single: recursive data structure
