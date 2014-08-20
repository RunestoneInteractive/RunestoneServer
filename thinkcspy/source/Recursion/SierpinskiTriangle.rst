..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Sierpinski Triangle
-------------------


Another fractal that exhibits the property of self-similarity is the
Sierpinski triangle. An example is shown in :ref:`Figure 3 <fig_sierpinski>`. The
Sierpinski triangle illustrates a three-way recursive algorithm. The
procedure for drawing a Sierpinski triangle by hand is simple. Start
with a single large triangle. Divide this large triangle into four new
triangles by connecting the midpoint of each side. Ignoring the middle
triangle that you just created, apply the same procedure to each of the
three corner triangles. Each time you create a new set of triangles, you
recursively apply this procedure to the three smaller corner triangles.
You can continue to apply this procedure indefinitely if you have a
sharp enough pencil. Before you continue reading, you may want to try
drawing the Sierpinski triangle yourself, using the method described.


.. _fig_sierpinski:

.. figure:: Figures/sierpinski.png
     :align: center

     Figure 3: The Sierpinski Triangle

Since we can continue to apply the algorithm indefinitely, what is the
base case? We will see that the base case is set arbitrarily as the
number of times we want to divide the triangle into pieces. Sometimes we
call this number the “degree” of the fractal. Each time we make a
recursive call, we subtract 1 from the degree until we reach 0. When we
reach a degree of 0, we stop making recursive calls. The code that
generated this Sierpinski Triangle is shown below.

.. _lst_st:

.. activecode:: lst_st
    :caption: Drawing a Sierpinski Triangle
    :nocodelens:

    import turtle

    def drawTriangle(points,color,myTurtle):
        myTurtle.fillcolor(color)
        myTurtle.up()
        myTurtle.goto(points[0][0],points[0][1])
        myTurtle.down()
        myTurtle.begin_fill()
        myTurtle.goto(points[1][0],points[1][1])
        myTurtle.goto(points[2][0],points[2][1])
        myTurtle.goto(points[0][0],points[0][1])
        myTurtle.end_fill()

    def getMid(p1,p2):
        return ( (p1[0]+p2[0]) / 2, (p1[1] + p2[1]) / 2)

    def sierpinski(points,degree,myTurtle):
        colormap = ['blue','red','green','white','yellow',
                    'violet','orange']
        drawTriangle(points,colormap[degree],myTurtle)
        if degree > 0:
            sierpinski([points[0],
                            getMid(points[0], points[1]),
                            getMid(points[0], points[2])],
                       degree-1, myTurtle)
            sierpinski([points[1],
                            getMid(points[0], points[1]),
                            getMid(points[1], points[2])],
                       degree-1, myTurtle)
            sierpinski([points[2],
                            getMid(points[2], points[1]),
                            getMid(points[0], points[2])],
                       degree-1, myTurtle)

    def main():
       myTurtle = turtle.Turtle()
       myWin = turtle.Screen()
       myPoints = [[-100,-50],[0,100],[100,-50]]
       sierpinski(myPoints,3,myTurtle)
       myWin.exitonclick()

    main()



    
    
This program follows the ideas outlined above. The
first thing ``sierpinski`` does is draw the outer triangle. Next, there
are three recursive calls, one for each of the new corner triangles we
get when we connect the midpoints. 

Look at the code and think about the order in which the triangles will
be drawn. While the exact order of the corners depends upon how the
initial set is specified, let’s assume that the corners are ordered
lower left, top, lower right. Because of the way the ``sierpinski``
function calls itself, ``sierpinski`` works its way to the smallest
allowed triangle in the lower-left corner, and then begins to fill out
the rest of the triangles working back. Then it fills in the triangles
in the top corner by working toward the smallest, topmost triangle.
Finally, it fills in the lower-right corner, working its way toward the
smallest triangle in the lower right.

Sometimes it is helpful to think of a recursive algorithm in terms of a
diagram of function calls. :ref:`Figure 4 <fig_stcalltree>` shows that the recursive
calls are always made going to the left. The active functions are
outlined in black, and the inactive function calls are in gray. The
farther you go toward the bottom of :ref:`Figure 4 <fig_stcalltree>`, the smaller the
triangles. The function finishes drawing one level at a time; once it is
finished with the bottom left it moves to the bottom middle, and so on.


.. _fig_stcalltree:

.. figure:: Figures/stCallTree.png
    :align: center   
   
    Figure 4: Building a Sierpinski Triangle

The ``sierpinski`` function relies heavily on the ``getMid`` function.
``getMid`` takes as arguments two endpoints and returns the point
halfway between them. In addition, this program has a function that
draws a filled triangle using the ``begin_fill`` and ``end_fill`` turtle
methods.
