..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

A Few More turtle Methods and Observations
------------------------------------------

Here are a few more things that you might find useful as you write programs that use turtles.

* Turtle methods can use negative angles or distances.  So ``tess.forward(-100)``
  will move tess backwards, and ``tess.left(-30)`` turns her to the right.
  Additionally, because there are 360 degrees in a circle, turning 30 to the
  left will leave you facing in the same direction as turning 330 to the right!
  (The on-screen animation will differ, though --- you will be able to tell if
  tess is turning clockwise or counter-clockwise!)

  This suggests that we don't need both a left and a right turn method --- we
  could be minimalists, and just have one method.  There is also a *backward*
  method.  (If you are very nerdy, you might enjoy saying
  ``alex.backward(-100)`` to move alex forward!)

  Part of *thinking like a scientist* is to understand more of the structure
  and rich relationships in your field.  So revising a few basic facts about
  geometry and number lines, like we've done here is a good start if we're
  going to play with turtles.

* A turtle's pen can be picked up or put down.  This allows us to move a turtle
  to a different place without drawing a line.   The methods are ``up`` and ``down``.  Note that the methods ``penup`` and ``pendown`` do the
  same thing.

  .. sourcecode:: python

     alex.up()
     alex.forward(100)     # this moves alex, but no line is drawn
     alex.down()

* Every turtle can have its own shape.  The ones available "out of the box"
  are ``arrow``, ``blank``, ``circle``, ``classic``, ``square``, ``triangle``,
  ``turtle``.

  .. sourcecode:: python

     ...
     alex.shape("turtle")
     ...


* You can speed up or slow down the turtle's animation speed. (Animation
  controls how quickly the turtle turns and moves forward).  Speed settings can
  be set between 1 (slowest) to 10 (fastest).  But if you set the speed to 0,
  it has a special meaning --- turn off animation and go as fast as possible.

  .. sourcecode:: python

     alex.speed(10)

* A turtle can "stamp" its footprint onto the canvas, and this will remain
  after the turtle has moved somewhere else.  Stamping works even when the pen
  is up.

Let's do an example that shows off some of these new features.

.. activecode:: ch03_7

   import turtle
   wn = turtle.Screen()
   wn.bgcolor("lightgreen")
   tess = turtle.Turtle()
   tess.color("blue")
   tess.shape("turtle")

   print(range(5, 60, 2))
   tess.up()                     # this is new
   for size in range(5, 60, 2):    # start with size = 5 and grow by 2
       tess.stamp()                # leave an impression on the canvas
       tess.forward(size)          # move tess along
       tess.right(24)              # and turn her

   wn.exitonclick()

The list of integers shown above is created by printing the ``range(5,60,2)`` result.  It is only
done to show you the distances being used to move the turtle forward.  The actual use appears
as part of the ``for`` loop.

One more thing to be careful about.  All except one of the shapes you see on the screen here are
footprints created by ``stamp``.  But the program still only has *one* turtle
instance --- can you figure out which one is the real tess?  (Hint: if you're
not sure, write a new line of code after the ``for`` loop to change tess'
color, or to put her pen down and draw a line, or to change her shape, etc.)

**Mixed up program**

.. parsonsprob:: 3_10

   The following program uses the stamp method to create a circle of turtle shapes as shown to the left, <img src="../_static/TurtleCircle.png" width="150" align="left" hspace="10" vspace="5"/> but the lines are mixed up.  The program should do all necessary set-up, create the turtle, set the shape to "turtle", and pick up the pen.  Then the turtle should repeat the following ten times: go forward 50 pixels, leave a copy of the turtle at the current position, reverse for 50 pixels, and then turn right 36 degrees.  After the loop, set the window to close when the user clicks in it.<br /><br /><p>Drag the blocks of statements from the left column to the right column and put them in the right order with the correct indention.  Click on <i>Check Me</i> to see if you are right. You will be told if any of the lines are in the wrong order or are incorrectly indented.</p>  
   -----
   import turtle
   wn = turtle.Screen()
   jose = turtle.Turtle()
   jose.shape("turtle")
   jose.penup()
   =====                   
   for size in range(10):  
   =====    
     jose.forward(50)
   =====
     jose.stamp()    
   =====      
     jose.forward(-50)
   =====
     jose.right(36)             
   =====
   wn.exitonclick()

**Mixed up program**

.. parsonsprob:: 3_11

   The following program uses the stamp method to create a line of turtle shapes as shown to the left, <img src="../_static/Turtle3Stamp.png" width="150" align="left" hspace="10" vspace="5" /> but the lines are mixed up.  The program should do all necessary set-up, create the turtle, set the shape to "turtle", and pick up the pen.  Then the turtle should repeat the following three times: go forward 50 pixels and leave a copy of the turtle at the current position.  After the loop, set the window to close when the user clicks in it.<br /><br /><p>Drag the blocks of statements from the left column to the right column and put them in the right order with the correct indention.  Click on <i>Check Me</i> to see if you are right. You will be told if any of the lines are in the wrong order or are incorrectly indented.</p>
   -----
   import turtle
   wn = turtle.Screen()
   =====
   nikea = turtle.Turtle()
   =====
   nikea.shape("turtle")
   =====
   nikea.penup()
   =====                   
   for size in range(3):  
   =====    
     nikea.forward(50)
   =====
     nikea.stamp()   
   =====                 
   wn.exitonclick()

.. admonition:: Lab

    * `Turtle Race <../Labs/lab03_01.html>`_ In this guided lab exercise we will work
      through a simple problem solving exercise related to having some turtles
      race.


.. _summary_of_turtle_methods:

