..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Exercises
---------

#.

    .. tabbed:: q1

        .. tab:: Question

           Write a program that prints ``We like Python's turtles!`` 1000 times.
        
           .. actex:: ex_3_1

        .. tab:: Answer
            
            .. activecode::  q1_answer
                :nocanvas:

                for i in range(1000):
                    print("We like Python's turtles!")

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: f858d02024e54ae1b6b50ed8c65a01e6


#. Turtle objects have methods and attributes. For example, a turtle has a position and when you move the turtle forward, the position changes.  Think about the other methods shown in the summary above.  Which attibutes, if any, does each method relate to?  Does the method change the attribute?


#.

    .. tabbed:: q3

        .. tab:: Question

           Write a program that uses a for loop to print
             |  ``One of the months of the year is January``
             |  ``One of the months of the year is February``
             |  ``One of the months of the year is March``
             |  etc ...
        
           .. actex:: ex_3_3

        .. tab:: Answer
            
            .. activecode:: q3_answer
                
                
                for amonth in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'November', 'December']:
                    print("One of the months of the year is", amonth)

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: b271442ee0864973a023c19f27aeb401


#. Assume you have a list of numbers ``12, 10, 32, 3, 66, 17, 42, 99, 20``

   a. Write a loop that prints each of the numbers on a new line.
   b. Write a loop that prints each number and its square on a new line.

   .. actex:: ex_3_4

#.

    .. tabbed:: q5

        .. tab:: Question

           Use ``for`` loops to make a turtle draw these regular polygons
           (regular means all sides the same lengths, all angles the same):
        
           * An equilateral triangle
           * A square
           * A hexagon (six sides)
           * An octagon (eight sides)
        
           .. actex:: ex_3_5

        .. tab:: Answer
            
            .. sourcecode:: python
                
                # draw an equilateral triangle
                import turtle

                wn = turtle.Screen()
                norvig = turtle.Turtle()

                for i in range(3):
                    norvig.forward(100)

                    # the angle of each vertice of a regular polygon 
                    # is 360 divided by the number of sides
                    norvig.left(360/3)

                wn.exitonclick()

            .. sourcecode:: python

                # draw a square    
                import turtle

                wn = turtle.Screen()
                kurzweil = turtle.Turtle()

                for i in range(4):
                    kurzweil.forward(100)
                    kurzweil.left(360/4)

                wn.exitonclick()

            .. sourcecode:: python

                # draw a hexagon    
                import turtle

                wn = turtle.Screen()
                dijkstra = turtle.Turtle()

                for i in range(6):
                    dijkstra.forward(100)
                    dijkstra.left(360/6)

                wn.exitonclick()

            .. sourcecode:: python

                # draw an octogon    
                import turtle

                wn = turtle.Screen()
                knuth = turtle.Turtle()

                for i in range(8):
                    knuth.forward(75)
                    knuth.left(360/8)

                wn.exitonclick()
                
        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: f36e8bc742b89424e82f111ba2d1dd33f


#.  Write a program that asks the user for the number of sides, the length of the side, the color, and the fill color of a
    regular polygon.  The program should draw the polygon and then fill it in.

   

    .. actex:: ex_3_6


#. 
    .. tabbed:: q7

       .. tab:: Question

            A drunk pirate makes a random turn and then takes 100 steps forward, makes another random turn, takes another 100 steps, turns another random amount, etc.  A social science student records the angle of each turn before the next 100 steps are taken.  Her experimental data is ``160, -43, 270, -97, -43, 200, -940, 17, -86``. (Positive angles are counter-clockwise.)  Use a turtle to draw the path taken by our drunk friend.  After the pirate is done walking, print the current heading.

            .. actex:: ex_3_7

       .. tab:: Answer

           .. activecode:: q7_answer

               import turtle

               wn = turtle.Screen()
               lovelace = turtle.Turtle()

               # move the turtle forward a little so that the whole path fits on the screen
               lovelace.penup()
               lovelace.forward(60)

               # now draw the drunk pirate's path
               lovelace.pendown()
               for angle in [160, -43, 270, -97, -43, 200, -940, 17, -86]:
                   
                   # we use .left() so that positive angles are counter-clockwise
                   # and negative angles are clockwise
                   lovelace.left(angle)
                   lovelace.forward(100)

               # the .heading() method gives us the turtle's current heading in degrees
               print("The pirate's final heading was", lovelace.heading())

               wn.exitonclick()

       .. tab:: Discussion

	       .. disqus::
	            :shortname: interactivepython
	            :identifier: a7e34946f59f348f2bfeb3f918eb57b7a


#. On a piece of scratch paper, trace the following program and show the drawing.  When you are done, press ``run``
   and check your answer.

   .. actex:: ex_3_8

       import turtle
       wn = turtle.Screen()
       tess = turtle.Turtle()
       tess.right(90)
       tess.left(3600)
       tess.right(-90)
       tess.left(3600)
       tess.left(3645)
       tess.forward(-100)


#.

    .. tabbed:: q9

        .. tab:: Question

           Write a program to draw a shape like this:
        
           .. image:: Figures/star.png
        
           .. actex:: ex_3_9

        .. tab:: Answer

            .. activecode:: q9_answer
                
                import turtle

                turing = turtle.Turtle()

                for i in range(5):
                    turing.forward(110)
                    turing.left(216)

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: c611217310057488aab6a34d4b591e753


#. Write a program to draw a face of a clock that looks something like this:

   .. image:: Figures/tess_clock1.png

   .. actex:: ex_3_10

#.

    .. tabbed:: q11

        .. tab:: Question

           Write a program to draw some kind of picture.  Be creative and experiment
           with the turtle methods provided in :ref:`turtle_methods`.
        
           .. actex:: ex_3_11

        .. tab:: Answer
            
            .. activecode:: q11_answer

                import turtle

                tanenbaum = turtle.Turtle()

                tanenbaum.hideturtle()
                tanenbaum.speed(20)

                for i in range(350):
                    tanenbaum.forward(i)
                    tanenbaum.right(98)

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: e928a562a4f5c41f9892c9bfc4a1d5883


#. Create a turtle and assign it to a variable.  When you print its type, what do you get?

   .. actex:: ex_3_12

#.

    .. tabbed:: q13

        .. tab:: Question
            
            A sprite is a simple spider shaped thing with n legs coming out from a center 
            point. The angle between each leg is 360 / n degrees.

            Write a program to draw a sprite where the number of legs is provided by the user.
                   
            .. actex:: ex_3_13

        .. tab:: Answer
            
            .. activecode:: q13_answer
                
                import turtle

                wn = turtle.Screen()

                babbage = turtle.Turtle()
                babbage.shape("triangle")

                n = int(input("How many legs should this sprite have? "))
                angle = 360 / n

                for i in range(n):
                    # draw the leg
                    babbage.right(angle)
                    babbage.forward(65)
                    babbage.stamp()
                    
                    # go back to the middle and turn back around
                    babbage.right(180)
                    babbage.forward(65)
                    babbage.right(180)

                babbage.shape("circle")

                wn.exitonclick()
    
        

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: b65d7e616d2b548f592205dba699cc132

