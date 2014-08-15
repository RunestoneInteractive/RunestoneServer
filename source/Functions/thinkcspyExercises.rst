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

            Use the drawsquare function we wrote in this chapter in a program to draw
            the image shown below.
            Assume each side is 20 units.
            (Hint: notice that the turtle has already moved away from the ending point of the last
            square when the program ends.)
        
            .. image:: Figures/five_squares.png
        
            .. actex:: ex_5_1
        
                import turtle
        
                def drawSquare(t, sz):
                    """Get turtle t to draw a square of sz side"""
        
                    for i in range(4):
                        t.forward(sz)
                        t.left(90)
        
                wn = turtle.Screen()
                wn.bgcolor("lightgreen")
        
                alex = turtle.Turtle()
                alex.color("pink")
        
                drawSquare(alex,20)
        
                wn.exitonclick()
        

        .. tab:: Answer
            
            .. activecode:: q1_answer

                import turtle

                def drawSquare(t, sz):
                    """Make turtle t draw a square of with side sz."""
                    for i in range(4):
                        t.forward(sz)
                        t.left(90)

                wn = turtle.Screen()       # Set up the window and its attributes
                wn.bgcolor("lightgreen")

                alex = turtle.Turtle()     # create alex
                alex.color('hotpink')
                alex.pensize(3)

                for i in range(5):
                    drawSquare(alex, 20)   # Call the function to draw the square
                    alex.penup()
                    alex.forward(40)       # move alex to the starting position for the next square
                    alex.pendown()

                wn.exitonclick()

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: a2ac86a8d0524fc6830aefb785199048


#.  Write a program to draw this. Assume the innermost square is 20 units per side,
    and each successive square is 20 units bigger, per side, than the one inside it.

    .. image:: Figures/nested_squares.png


    .. actex:: ex_5_2


#.

    .. tabbed:: q3

        .. tab:: Question

            Write a non-fruitful function ``drawPoly(someturtle, somesides, somesize)`` which makes a turtle
            draw a regular polygon.
            When called with ``drawPoly(tess, 8, 50)``, it will draw a shape like this:
        
            .. image:: Figures/regularpolygon.png
        
            .. actex:: ex_5_3
        

        .. tab:: Answer
            
            .. activecode:: q3_answer

                import turtle

                def drawPoly(t, num_sides, side_length):
                    for i in range(num_sides):
                        t.forward(side_length)
                        t.left(360/num_sides)

                wn = turtle.Screen()       # Set up the window and its attributes
                wn.bgcolor("lightgreen")

                tess = turtle.Turtle()
                tess.color('hotpink')
                tess.pensize(3)

                drawPoly(tess, 8, 50)

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: ba2f11265c524c7581bf7cf25d23bf3a


#. Draw this pretty pattern.

    .. image:: Figures/tess08.png

    .. actex:: ex_5_4

#.

    .. tabbed:: q5

        .. tab:: Question

            The two spirals in this picture differ only by the turn angle.  Draw both.
        
            .. image:: Figures/tess_spirals.png
               :height: 240
        
            .. actex:: ex_5_5

        .. tab:: Answer
            
            .. activecode:: q5_answer

                import turtle

                def drawSpiral(t, angle):
                    ''' takes a turtle, t, and an angle in degrees '''
                    length = 1
                    for i in range(84):
                        t.forward(length)
                        t.right(angle)
                        length = length + 2


                wn = turtle.Screen()       # Set up the window and its attributes
                wn.bgcolor("lightgreen")

                guido = turtle.Turtle()    # create guido
                guido.color('blue')

                ## draw the first spiral ##
                # position guido
                guido.penup()
                guido.backward(110)
                guido.pendown()

                # draw the spiral using a 90 degree turn angle
                drawSpiral(guido, 90)


                ## draw the second spiral ##
                # position guido
                guido.home()
                guido.penup()
                guido.forward(90)
                guido.pendown()

                drawSpiral(guido, 89)


        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: c587119991344db988f8fb37c8c9a31e


#.  Write a non-fruitful function ``drawEquitriangle(someturtle, somesize)`` which calls ``drawPoly`` from the
    previous question to have its turtle draw a equilateral triangle.

    .. actex:: ex_5_6


#.

    .. tabbed:: q7

        .. tab:: Question

            Write a fruitful function ``sumTo(n)`` that returns the sum of all integer numbers up to and
            including `n`.   So ``sumTo(10)`` would be ``1+2+3...+10`` which would return the value 55.  Use the
            equation  (n * (n + 1)) / 2.
        
            .. actex:: ex_5_7
        
                from test import testEqual
        
                def sumTo(n):
                    # your code here


        .. tab:: Answer
            
            .. activecode:: q7_answer

                from test import testEqual

                def sumTo(n):
                    result = (n * (n + 1)) / 2
                    return result

                # Now lets see how well this works
                t = sumTo(0)
                print("The sum from 1 to 0 is",t)
                t = sumTo(10)
                print("The sum from 1 to 10 is",t)
                t = sumTo(5)
                print("The sum from 1 to 5 is",t)

        .. tab:: Discussion

            .. disqus::
                :shortname: interactivepython
                :identifier: d6ba37a51d09845f39c96d4d4ef1d6f45


#.  Write a function `areaOfCircle(r)` which returns the area of a circle of radius `r`.  Make sure you use the math module in your solution.

    .. actex:: ex_5_8

        from test import testEqual

        def areaOfCircle(r):
            # your code here

        t = areaOfCircle(0)
        testEqual(t,0)
        t = areaOfCircle(1)
        testEqual(t,math.pi)
        t = areaOfCircle(100)
        testEqual(t,31415.926535897932)


#.

    .. tabbed:: q9

        .. tab:: Question

            Write a non-fruitful function to draw a five pointed star, where the length of each side is 100 units.

            .. image:: Figures/star.png

            .. actex:: ex_5_9

        .. tab:: Answer

            .. activecode:: q9_answer

                import turtle

                def drawFivePointStar(t):
                    for i in range(5):
                        t.forward(100)
                        t.left(216)

                wolfram = turtle.Turtle()
                drawFivePointStar(wolfram)

        .. tab:: Discussion

            .. disqus::
                :shortname: interactivepython
                :identifier: e757873187bb4581bffecdad449b5f61


#.  Extend your program above.  Draw five stars, but between each, pick up the pen,
    move forward by 350 units, turn right by 144, put the pen down, and draw the next star.
    You'll get something like this (note that you will need to move to the left before drawing your first star in order to fit everything in the window):

    .. image:: Figures/five_stars.png

    What would it look like if you didn't pick up the pen?

    .. actex:: ex_5_10


#.

    .. tabbed:: q11

        .. tab:: Question

            Extend the star function to draw an n pointed star.  (Hint: n must be an odd number greater or
            equal to 3).

            .. actex:: ex_5_11


        .. tab:: Answer

            .. activecode:: q11_answer

                import turtle

                def drawStar(t, n):
                    for i in range(n):
                        t.forward(100)
                        t.left(180 - 180/n)

                stroustrup = turtle.Turtle()
                drawStar(stroustrup, 7)

        .. tab:: Discussion

            .. disqus::
                :shortname: interactivepython
                :identifier: f2f8ff1b301e4d99bd4ac52e68c8c1ed


#.  Write a function called drawSprite that will draw a sprite.  The function will need parameters for
    the turtle, the number of legs, and the length of the legs.  Invoke the function to create a sprite
    with 15 legs of length 120.

    .. actex:: ex_5_12


#.

    .. tabbed:: q13

        .. tab:: Question

            Rewrite the function ``sumTo(n)`` that returns the sum of all integer numbers up to and
            including `n`.   This time use the accumulator pattern.

            .. actex:: ex_5_13

                def sumTo(n):
                    # your code here


        .. tab:: Answer

            .. activecode:: q13_answer

                def sumTo(n):
                    sum = 0
                    for i in range(1,n+1):
                        sum = sum + i
                    return sum

                # Now lets see how well this works
                t = sumTo(0)
                print("The sum from 1 to 0 is",t)
                t = sumTo(10)
                print("The sum from 1 to 10 is",t)
                t = sumTo(5)
                print("The sum from 1 to 5 is",t)

        .. tab:: Discussion

            .. disqus::
                :shortname: interactivepython
                :identifier: eda665389fda49a584b128cc30515595


#.  Write a function called ``mySqrt`` that will approximate the square root of a number, call it n, by using
    Newton's algorithm.
    Newton's approach is an iterative guessing algorithm where the initial guess is n/2 and each subsequent guess
    is computed using   the formula:  newguess = (1/2) * (oldguess + (n/oldguess)).

    .. actex:: ex_5_14


#.

    .. tabbed:: q15

        .. tab:: Question

            Write a function called ``myPi`` that will return an approximation of PI (3.14159...).  Use the `Leibniz <http://en.wikipedia.org/wiki/Leibniz_formula_for_%CF%80>`_ approximation.

            .. actex:: ex_5_15


        .. tab:: Answer

            .. activecode:: q15_answer

                def myPi(iters):
                    ''' Calculate an approximation of PI using the Leibniz
                    approximation with iters number of iterations '''
                    pi = 0
                    sign = 1
                    denominator = 1
                    for i in range(iters):
                        pi = pi + (sign/denominator)
                        sign = sign * -1  # alternate positive and negative
                        denominator = denominator + 2

                    pi = pi * 4.0
                    return pi

                pi_approx = myPi(10000)
                print(pi_approx)

        .. tab:: Discussion

            .. disqus::
                :shortname: interactivepython
                :identifier: b699e4b7bad44db6bd788c795c124b23


#.  Write a function called `myPi` that will return an approximation of PI (3.14159...).  Use the `Madhava <http://en.wikipedia.org/wiki/Madhava_of_Sangamagrama>`_ approximation.

    .. actex:: ex_5_16

#.

    .. tabbed:: q17

        .. tab:: Question

            Write a function called `fancySquare` that will draw a square with fancy corners (spites on the corners).  You should
            implement and use the `drawSprite` function from above.  For an even more interesting look, how about adding small
            triangles to the ends of the sprite legs.

            .. actex:: ex_5_17

        .. tab:: Answer

            .. activecode:: q17_answer

                import turtle
                
                def drawSprite(t, numlegs, leglength):
                   angle = 360/numlegs
                   for i in range(numlegs):
                      t.forward(leglength)
                      t.backward(leglength)
                      t.left(angle)
                      
                def drawFancySquare(t, sz, lgs, lgl):
                   for i in range(4):
                       t.forward(sz)
                       drawSprite(t, lgs, lgl)
                       t.left(90)
                       
                wn = turtle.Screen()
                wn.bgcolor("lightgreen")
                
                alex = turtle.Turtle()
                drawFancySquare(alex, 100, 10, 15)
                
                wn.exitonclick()

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: db5d8808bf5749579718bdd2088b539f



