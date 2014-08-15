..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Iteration Simplifies our Turtle Program
---------------------------------------

To draw a square we'd like to do the same thing four times --- move the turtle forward some distance and turn 90 degrees.  We previously used 8 lines of Python code to have alex draw the four sides of a
square.  This next program does exactly the same thing but, with the help of the for statement, uses just three lines (not including the setup code).  Remember that the for statement will repeat the `forward` and `left` four times, one time for
each value in the list.

.. activecode:: ch03_for1
   :nocodelens:

   import turtle            # set up alex
   wn = turtle.Screen()
   alex = turtle.Turtle()

   for i in [0, 1, 2, 3]:      # repeat four times
       alex.forward(50)
       alex.left(90)

   wn.exitonclick()



While "saving some lines of code" might be convenient, it is not the big
deal here.  What is much more important is that we've found a "repeating
pattern" of statements, and we reorganized our program to repeat the pattern.
Finding the chunks and somehow getting our programs arranged around those
chunks is a vital  skill when learning *How to think like a computer scientist*.

The values [0,1,2,3] were provided to make the loop body execute 4 times.
We could have used any four values.  For example, consider the following program.


.. activecode:: ch03_forcolor
   :nocodelens:

   import turtle            # set up alex
   wn = turtle.Screen()
   alex = turtle.Turtle()

   for aColor in ["yellow", "red", "purple", "blue"]:      # repeat four times
       alex.forward(50)
       alex.left(90)

   wn.exitonclick()

In the previous example, there were four integers in the list.  This time there are four strings.  Since there are four items in the list, the iteration will still occur four times.  ``aColor`` will
take on each color in the list.  We can even take this one step further and use the value of ``aColor`` as part
of the computation.

.. activecode:: colorlist
    :nocodelens:

    import turtle            # set up alex
    wn = turtle.Screen()
    alex = turtle.Turtle()

    for aColor in ["yellow", "red", "purple", "blue"]:
       alex.color(aColor)
       alex.forward(50)
       alex.left(90)

    wn.exitonclick()

In this case, the value of ``aColor`` is used to change the color attribute of ``alex``.  Each iteration causes ``aColor`` to change to the next value in the list.

**Mixed up program**

.. parsonsprob:: 3_8

   The following program uses a turtle to draw a triangle as shown to the left, <img src="../_static/TurtleTriangle.png" width="150" align="left" hspace="10" vspace="5"/> but the lines are mixed up.  The program should do all necessary set-up and create the turtle.  After that, iterate (loop) 3 times, and each time through the loop the turtle should go forward 175 pixels, and then turn left 120 degrees.  After the loop, set the window to close when the user clicks in it.<br /><br /><p>Drag the blocks of statements from the left column to the right column and put them in the right order with the correct indention.  Click on <i>Check Me</i> to see if you are right. You will be told if any of the lines are in the wrong order or are incorrectly indented.</p> 
   -----
   import turtle 
   =====         
   wn = turtle.Screen()
   marie = turtle.Turtle()
   =====
   # repeat 3 times
   for i in [0,1,2]:  
   =====   
     marie.forward(175)
   =====
     marie.left(120)
   =====
   wn.exitonclick()

**Mixed up program**

.. parsonsprob:: 3_9

   The following program uses a turtle to draw a rectangle as shown to the left, <img src="../_static/TurtleRect.png" width="150" align="left" hspace="10" vspace="5" /> but the lines are mixed up.  The program should do all necessary set-up and create the turtle.  After that, iterate (loop) 2 times, and each time through the loop the turtle should go forward 175 pixels, turn right 90 degrees, go forward 150 pixels, and turn right 90 degrees.  After the loop, set the window to close when the user clicks in it.<br /><br /><p>Drag the blocks of statements from the left column to the right column and put them in the right order with the correct indention.  Click on <i>Check Me</i> to see if you are right. You will be told if any of the lines are in the wrong order or are incorrectly indented.</p>  
   -----
   import turtle          
   wn = turtle.Screen()
   carlos = turtle.Turtle()
   =====
   # repeat 2 times
   for i in [1,2]:  
   =====   
     carlos.forward(175)
   =====
     carlos.right(90)
   =====  
     carlos.forward(150)
     carlos.right(90)
   =====
   wn.exitonclick()


**Check your understanding**

.. mchoicemf:: test_question3_4_1
   :answer_a: 1
   :answer_b: 5
   :answer_c: 6
   :answer_d: 10
   :correct: c
   :feedback_a: The loop body prints one line, but the body will execute exactly one time for each element in the list [5, 4, 3, 2, 1, 0].
   :feedback_b: Although the biggest number in the list is 5, there are actually 6 elements in the list.
   :feedback_c: The loop body will execute (and print one line) for each of the 6 elements in the list [5, 4, 3, 2, 1, 0].
   :feedback_d: The loop body will not execute more times than the number of elements in the list.

   In the following code, how many lines does this code print?

   .. code-block:: python

     for number in [5, 4, 3, 2, 1, 0]:
         print("I have", number, "cookies.  Iím going to eat one.")


.. mchoicemf:: test_question3_4_2
   :answer_a: They are indented to the same degree from the loop header.
   :answer_b: There is always exactly one line in the loop body.
   :answer_c: The loop body ends with a semi-colon (;) which is not shown in the code above.
   :correct: a
   :feedback_a: The loop body can have any number of lines, all indented from the loop header.
   :feedback_b: The loop body may have more than one line.
   :feedback_c: Python does not use semi-colons in its syntax, but relies mainly on indentation.

   How does python know what lines are contained in the loop body?

.. mchoicemf:: test_question3_4_3
      :answer_a: 2
      :answer_b: 4
      :answer_c: 5
      :answer_d: 1
      :correct: b
      :feedback_a: Python gives number the value of items in the list, one at a time, in order (from left to right).  number gets a new value each time the loop repeats.
      :feedback_b: Yes, Python will process the items from left to right so the first time the value of number is 5 and the second time it is 4.
      :feedback_c: Python gives number the value of items in the list, one at a time, in order.  number gets a new value each time the loop repeats.
      :feedback_d: Python gives number the value of items in the list, one at a time, in order (from left to right).  number gets a new value each time the loop repeats.

      In the following code, what is the value of number the second time Python executes the loop?

      .. code-block:: python

         for number in [5, 4, 3, 2, 1, 0]:
             print("I have", number, "cookies.  Iím going to eat one.")


.. mchoicemf:: test_question3_4_4
      :answer_a: Draw a square using the same color for each side.
      :answer_b: Draw a square using a different color for each side.
      :answer_c: Draw one side of a square.
      :correct: c
      :feedback_a: The items in the list are not actually used to control the color of the turtle because aColor is never used inside the loop.  But, the loop will execute once for each color in the list.
      :feedback_b: Notice that aColor is never actually used inside the loop.
      :feedback_c: The body of the loop only draws one side of the square.  It will be  repeated once for each item in the list.  However, the color of the turtle never changes.

      Consider the following code:

      .. code-block:: python

        for aColor in ["yellow", "red", "green", "blue"]:
           alex.forward(50)
           alex.left(90)

      What does each iteration through the loop do?

