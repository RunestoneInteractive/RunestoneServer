..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. qnum::
   :prefix: list-15-
   :start: 1

The Return of L-Systems
-----------------------

Let's return to the L-systems we introduced in the previous chapter and
introduce a very interesting new feature that requires the use of lists.

Suppose we have the following grammar::

    X
    X --> F[-X]+X
    F --> FF

This L-system looks very similar to the old L-system except that we've added
one change.  We've added the characters '[' and ']'.  The meaning of these
characters adds a very interesting new dimension to our L-Systems.  The '['
character indicates that we want to save the state of our turtle,
namely its position and its heading so that we can come back to this position
later.  The ']' tells the turtle to warp to the most recently saved position.
The way that we will accomplish this is to use lists.  We can save the
heading and position of the turtle as a list of 3 elements.  ``[heading x
y]``  The first index position in the list holds the heading,
the second index position in the list holds the x coordinate,
and the third index position holds the y coordinate.

Now, if we create an empty list and every time we see a '[' we append the
list that contains ``[heading, x, y]`` we create a history of saved places
the turtle has been where the most recently saved location will always be at
the end of the list.  When we find a ']' in the string we use the pop
function to remove the the most recently appended information.

Let's modify our ``drawLsystem`` function to begin to implement this new
behavior.

.. activecode:: list_lsys1
    :nocodelens:

    import turtle

    def drawLsystem(aTurtle, instructions, angle, distance):
        savedInfoList = []
        for cmd in instructions:
            if cmd == 'F':
                aTurtle.forward(distance)
            elif cmd == 'B':
                aTurtle.backward(distance)
            elif cmd == '+':
                aTurtle.right(angle)
            elif cmd == '-':
                aTurtle.left(angle)
            elif cmd == '[':
                savedInfoList.append([aTurtle.heading(), aTurtle.xcor(), aTurtle.ycor()])
                print(savedInfoList)
            elif cmd == ']':
                newInfo = savedInfoList.pop()
                print(newInfo)
                print(savedInfoList)

    t = turtle.Turtle()
    inst = "FF[-F[-X]+X]+F[-X]+X"
    drawLsystem(t, inst, 60, 20)

When we run this example we can see that the picture is not very interesting,
but notice what gets printed out, and how the saved information about the
turtle gets added and removed from the end of the list.  In the next example
we'll make use of the information from the list to save and restore the
turtle's position and heading when needed.  We'll use a longer example here
so you get an idea of what the kind of drawing the L-System can really make.

.. activecode:: list_lsys2
    :nocodelens:

    import turtle

    def drawLsystem(aTurtle, instructions, angle, distance):
        savedInfoList = []
        for cmd in instructions:
            if cmd == 'F':
                aTurtle.forward(distance)
            elif cmd == 'B':
                aTurtle.backward(distance)
            elif cmd == '+':
                aTurtle.right(angle)
            elif cmd == '-':
                aTurtle.left(angle)
            elif cmd == '[':
                savedInfoList.append([aTurtle.heading(), aTurtle.xcor(), aTurtle.ycor()])
                print(savedInfoList)
            elif cmd == ']':
                newInfo = savedInfoList.pop()
                aTurtle.setheading(newInfo[0])
                aTurtle.setposition(newInfo[1], newInfo[2])

    t = turtle.Turtle()
    inst = "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF[-FFFFFFFFFFFFFFFF[-FFFFFFFF[-FFFF[-FF[-F[-X]+X]+F[-X]+X]+FF[-F[-X]+X]+F[-X]+X]+FFFF[-FF[-F[-X]+X]+F[-X]+X]+FF[-F[-X]+X]+F[-X]+X]+FFFFFFFF[-FFFF[-FF[-F[-X]+X]+F[-X]+X]+FF[-F[-X]+X]+F[-X]+X]+FFFF[-FF[-F[-X]+X]+F[-X]+X]+FF[-F[-X]+X]+F[-X]+X]+FFFFFFFFFFFFFFFF[-FFFFFFFF[-FFFF[-FF[-F[-X]+X]+F[-X]+X]+FF[-F[-X]+X]+F[-X]+X]+FFFF[-FF[-F[-X]+X]+F[-X]+X]+FF[-F[-X]+X]+F[-X]+X]+FFFFFFFF[-FFFF[-FF[-F[-X]+X]+F[-X]+X]+FF[-F[-X]+X]+F[-X]+X]+FFFF[-FF[-F[-X]+X]+F[-X]+X]+FF[-F[-X]+X]+F[-X]+X"
    t.setposition(0, -200)
    t.left(90)
    drawLsystem(t, inst, 30, 2)


Rather than use the ``inst`` string supplied here, use the code from the string
chapter, and write your own applyRules function to implement this L-system.
This example only uses 6 expansions.  Try it out with a larger number of
expansions.  You may also want to try this example with different values for
the angle and distance parameters.




