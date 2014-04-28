..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Instances --- A Herd of Turtles
-------------------------------

Just like we can have many different integers in a program, we can have many
turtles.  Each of them is an independent object and we call each one an **instance** of the Turtle type (class).  Each instance has its own
attributes and methods --- so alex might draw with a thin black pen and be at
some position, while tess might be going in her own direction with a fat pink
pen.  So here is what happens when alex completes a square and tess
completes her triangle:

.. activecode:: ch03_3
   :tour_1: "Overall Tour"; 1-31: Example03_Tour01_Line01; 1-3: Example03_Tour01_Line02; 6-8: Example03_Tour01_Line03; 10: Example03_Tour01_Line04; 6,10: Example03_Tour01_Line05; 12-17: Example03_Tour01_Line06; 19-20: Example03_Tour01_Line07; 22-29: Example03_Tour01_Line08; 31: Example03_Tour01_Line09;
   :tour_2: "Line by Line Tour"; 1: Example01_Tour02_Line01; 2: Example01_Tour02_Line02; 3: Example02_Tour02_Line03; 6: Example02_Tour02_Line04; 7: Example03_Tour02_Line05; 8: Example03_Tour02_Line06; 10: Example01_Tour02_Line03; 6,10: Example03_Tour01_Line05; 12-17: Example03_Tour02_Line09; 12-13: Example03_Tour02_Line10; 12: Example03_Tour02_Line11; 13: Example03_Tour02_Line12; 14-15: Example03_Tour02_Line13; 14: Example03_Tour02_Line14; 15: Example03_Tour02_Line15; 16-17: Example03_Tour02_Line16; 16: Example03_Tour02_Line17; 17: Example03_Tour02_Line18; 19-20: Example03_Tour01_Line07; 19: Example03_Tour02_Line20; 20: Example03_Tour02_Line21; 22-29: Example03_Tour01_Line08; 10: Example03_Tour02_Line23; 22-23: Example03_Tour02_Line24; 22: Example03_Tour02_Line25; 23: Example03_Tour02_Line26; 24-25: Example03_Tour02_Line27; 26-27: Example03_Tour02_Line28; 28-29: Example03_Tour02_Line29; 31: Example02_Tour02_Line10;

   import turtle
   wn = turtle.Screen()             # Set up the window and its attributes
   wn.bgcolor("lightgreen")


   tess = turtle.Turtle()           # create tess and set some attributes
   tess.color("hotpink")
   tess.pensize(5)

   alex = turtle.Turtle()           # create alex

   tess.forward(80)                 # Let tess draw an equilateral triangle
   tess.left(120)
   tess.forward(80)
   tess.left(120)
   tess.forward(80)
   tess.left(120)                   # complete the triangle

   tess.right(180)                  # turn tess around
   tess.forward(80)                 # move her away from the origin

   alex.forward(50)                 # make alex draw a square
   alex.left(90)
   alex.forward(50)
   alex.left(90)
   alex.forward(50)
   alex.left(90)
   alex.forward(50)
   alex.left(90)

   wn.exitonclick()


Here are some *How to think like a computer scientist* observations:

* There are 360 degrees in a full circle.  If you add up all the turns that a
  turtle makes, *no matter what steps occurred between the turns*, you can
  easily figure out if they add up to some multiple of 360.  This should
  convince you that alex is facing in exactly the same direction as he was when
  he was first created. (Geometry conventions have 0 degrees facing East and
  that is the case here too!)
* We could have left out the last turn for alex, but that would not have been
  as satisfying.  If you're asked to draw a closed shape like a square or a
  rectangle, it is a good idea to complete all the turns and to leave the
  turtle back where it started, facing the same direction as it started in.
  This makes reasoning about the program and composing chunks of code into
  bigger programs easier for us humans!
* We did the same with tess: she drew her triangle and turned through a full
  360 degress.  Then we turned her around and moved her aside.  Even the blank
  line 18 is a hint about how the programmer's *mental chunking* is working: in
  big terms, tess' movements were chunked as "draw the triangle"  (lines 12-17)
  and then "move away from the origin" (lines 19 and 20).
* One of the key uses for comments is to record your mental chunking, and big
  ideas.   They're not always explicit in the code.
* And, uh-huh, two turtles may not be enough for a herd, but you get the idea!


**Check your understanding**

.. mchoicemf:: test_question3_2_1
   :answer_a: True
   :answer_b: False
   :correct: b
   :feedback_a: You can create and use as many turtles as you like.  As long as they have different names, you can operate them independently, and make them move in any order you like.  To convince yourself this is true, try interleaving the instructions for alex and tess in ActiveCode box 3.
   :feedback_b: You can create and use as many turtles as you like.  As long as they have different names, you can operate them independently, and make them move in any order you like.  If you are not totally convinced, try interleaving the instructions for alex and tess in ActiveCode box 3.

   True or False: You can only have one active turtle at a time.  If you create a second one, you will no longer be able to access or use the first.

**Mixed up programs**

.. parsonsprob:: 3_6

   The following program has one turtle, "jamal", draw a capital L in blue and then another, "tina", draw a line to the west in orange as shown to the left, <img src="../_static/TwoTurtles1.png" width="150" align="left" hspace="10" vspace="5" />.  The program should do all set-up, have "jamal" draw the L, and then have "tina" draw the line.   Finally, it should set the window to close when the user clicks in it.<br /><br /><p>Drag the blocks of statements from the left column to the right column and put them in the right order.  Then click on <i>Check Me</i> to see if you are right. You will be told if any of the lines are in the wrong order.</p>
   -----
   import turtle
   wn = turtle.Screen()
   =====    	
   jamal = turtle.Turtle()
   jamal.pensize(10)
   jamal.color("blue")               	               
   jamal.right(90)
   jamal.forward(150)
   ===== 
   jamal.left(90)
   jamal.forward(75)
   =====
   tina = turtle.Turtle()
   tina.pensize(10)
   tina.color("orange")
   tina.left(180)
   tina.forward(75)
   =====
   wn.exitonclick()

.. parsonsprob:: 3_7

   The following program has one turtle, "jamal", draw a line to the north in blue and then another, "tina", draw a line to the east in orange as shown to the left, <img src="../_static/TwoTurtlesL.png" width="150" align="left" hspace="10" vspace="5" />.  The program should import the turtle module, get the window to draw on, create the turtle "jamal", have it draw a line to the north, then create the turtle "tina", and have it draw a line to the east.  Finally, it should set the window to close when the user clicks in it.<br /><br /><p>Drag the blocks of statements from the left column to the right column and put them in the right order.  Then click on <i>Check Me</i> to see if you are right. You will be told if any of the lines are in the wrong order.</p> 
   -----
   import turtle
   =====
   wn = turtle.Screen()
   =====   	
   jamal = turtle.Turtle()
   jamal.color("blue") 
   jamal.pensize(10)   
   =====            	               
   jamal.left(90)
   jamal.forward(150)
   =====
   tina = turtle.Turtle()
   tina.pensize(10)  
   tina.color("orange")
   tina.forward(150)
   =====
   wn.exitonclick()


.. index:: for loop

