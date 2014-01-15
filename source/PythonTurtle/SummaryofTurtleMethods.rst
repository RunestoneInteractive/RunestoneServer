..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Summary of Turtle Methods
-------------------------

==========  ==========  =========================
Method      Parameters  Description
==========  ==========  =========================
Turtle      None          Creates and returns a new turtle object
forward     distance      Moves the turtle forward
backward    distance      Moves the turle backward
right       angle         Turns the turtle clockwise
left        angle         Turns the turtle counter clockwise
up          None          Picks up the turtles tail
down        None          Puts down the turtles tail
color       color name    Changes the color of the turtle's tail
fillcolor   color name    Changes the color of the turtle will use to fill a polygon
heading     None          Returns the current heading
position    None          Returns the current position
goto        x,y           Move the turtle to position x,y
begin_fill  None          Remember the starting point for a filled polygon
end_fill    None          Close the polygon and fill with the current fill color
dot         None          Leave a dot at the current position
stamp       None          Leaves an impression of a turtle shape at the current location
shape       shapename     Should be 'arrow', 'classic', 'turtle', or 'circle'
==========  ==========  =========================

Once you are comfortable with the basics of turtle graphics you can read about even
more options on the `Python Docs Website <http://docs.python.org/dev/py3k/library/turtle.html>`_.  Note that we
will describe Python Docs in more detail in the next chapter.


.. note::

   This workspace is provided for your convenience.  You can use this activecode window to try out anything you like.

   .. activecode:: scratch_03




