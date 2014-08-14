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

           Add a print statement to Newton's ``sqrt`` function that
           prints out ``better`` each time it is calculated. Call your modified
           function with 25 as an argument and record the results.
        
           .. actex:: ex_7_7
        

        .. tab:: Answer
            
            .. activecode:: q1_answer

                def newtonSqrt(n):
                    approx = 0.5 * n
                    better = 0.5 * (approx + n/approx)
                    while better != approx:
                        approx = better
                        better = 0.5 * (approx + n/approx)
                        print("Approx:", better)
                    return approx


                print("Final approx:", newtonSqrt(25))

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_5784e08291ba43199d43fdab277849f5


#. Write a function ``print_triangular_numbers(n)`` that prints out the first
   n triangular numbers. A call to ``print_triangular_numbers(5)`` would
   produce the following output::

       1       1
       2       3
       3       6
       4       10
       5       15

   (*hint: use a web search to find out what a triangular number is.*)

   .. actex:: ex_7_8


#.

    .. tabbed:: q3

        .. tab:: Question

           Write a function, ``is_prime``, that takes a single integer argument
           and returns ``True`` when the argument is a *prime number* and ``False``
           otherwise.
        
           .. actex:: ex_7_9
        
        

        .. tab:: Answer
            
            .. activecode:: q3_answer

                def is_prime(n):
                    for i in range(2, n):
                        if n % i == 0:
                            return False
                    return True

                print(is_prime(25))
                print(is_prime(7))
                print(is_prime(251))
                print(is_prime(20))

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_418de05233374e76b3b66aeb96b55656




#. Modify the walking turtle program so that rather than a 90 degree left or right turn the
   angle of the turn is determined randomly at each step.

    .. actex:: ex_7_14
    
    
    

#.

    .. tabbed:: q5

        .. tab:: Question

           Modify the turtle walk program so that you have two turtles each with a
           random starting location.  Keep the turtles moving until one of them leaves the screen.

           .. actex:: ex_7_13

        .. tab:: Answer

            .. activecode:: q5_answer

                import random
                import turtle

                def moveRandom(wn, t):
                    coin = random.randrange(0,2)
                    if coin == 0:
                        t.left(90)
                    else:
                        t.right(90)

                    t.forward(50)

                def areColliding(t1, t2):
                    if t1.distance(t2) < 2:
                        return True
                    else:
                        return False

                def isInScreen(w, t):
                    leftBound = - w.window_width() / 2
                    rightBound = w.window_width() / 2
                    topBound = w.window_height() / 2
                    bottomBound = -w.window_height() / 2

                    turtleX = t.xcor()
                    turtleY = t.ycor()

                    stillIn = True
                    if turtleX > rightBound or turtleX < leftBound:
                        stillIn = False
                    if turtleY > topBound or turtleY < bottomBound:
                        stillIn = False
                    return stillIn

                t1 = turtle.Turtle()
                t2 = turtle.Turtle()
                wn = turtle.Screen()

                t1.shape('turtle')
                t2.shape('circle')

                leftBound = -wn.window_width() / 2
                rightBound = wn.window_width() / 2
                topBound = wn.window_height() / 2
                bottomBound = -wn.window_height() / 2

                t1.up()
                t1.goto(random.randrange(leftBound, rightBound),
                        random.randrange(bottomBound, topBound))
                t1.setheading(random.randrange(0, 360))
                t1.down()

                t2.up()
                t2.goto(random.randrange(leftBound, rightBound),
                        random.randrange(bottomBound, topBound))
                t2.setheading(random.randrange(0, 360))
                t2.down()


                while isInScreen(wn, t1) and isInScreen(wn, t2):
                    moveRandom(wn, t1)
                    moveRandom(wn, t2)

                wn.exitonclick()

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_0cd01637a1814f86b11f576c37a46437



#. Modify the previous turtle walk program so that the turtle turns around
   when it hits the wall or when one turtle collides with another turtle.

   .. actex:: ex_7_12
   



#.

    .. tabbed:: q7

        .. tab:: Question

           Write a function to remove all the red from an image.
   
		   .. raw:: html

		       <img src="../_static/LutherBellPic.jpg" id="luther.jpg">
		       <h4 style="text-align: left;">For this and the following exercises, use the
			   luther.jpg photo.</h4>
        
           .. actex:: ex_7_15

        .. tab:: Answer
            
            .. activecode:: q7_answer

                import image

                img = image.Image("luther.jpg")
                newimg = image.EmptyImage(img.getWidth(), img.getHeight())
                win = image.ImageWin()

                for col in range(img.getWidth()):
                    for row in range(img.getHeight()):
                        p = img.getPixel(col, row)

                        newred = 0
                        green = p.getGreen()
                        blue = p.getBlue()

                        newpixel = image.Pixel(newred, green, blue)

                        newimg.setPixel(col, row, newpixel)

                newimg.draw(win)
                win.exitonclick()

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_777006b154ca4af7ab8bd11cc25c208a


#. Write a function to convert the image to grayscale.

    .. actex:: ex_7_16

#.

    .. tabbed:: q9

        .. tab:: Question

           Write a function to convert an image to black and white.
        
           .. actex:: ex_7_17

        .. tab:: Answer
            
            .. activecode:: q9_answer

                import image

                def convertBlackWhite(input_image):
                    grayscale_image = image.EmptyImage(input_image.getWidth(), input_image.getHeight())

                    for col in range(input_image.getWidth()):
                        for row in range(input_image.getHeight()):
                            p = input_image.getPixel(col, row)

                            red = p.getRed()
                            green = p.getGreen()
                            blue = p.getBlue()

                            avg = (red + green + blue) / 3.0

                            newpixel = image.Pixel(avg, avg, avg)
                            grayscale_image.setPixel(col, row, newpixel)

                    blackwhite_image = image.EmptyImage(input_image.getWidth(), input_image.getHeight())
                    for col in range(input_image.getWidth()):
                        for row in range(input_image.getHeight()):
                            p = grayscale_image.getPixel(col, row)
                            red = p.getRed()
                            if red > 140:
                                val = 255
                            else:
                                val = 0

                            newpixel = image.Pixel(val, val, val)
                            blackwhite_image.setPixel(col, row, newpixel)
                    return blackwhite_image


                win = image.ImageWin()
                img = image.Image("luther.jpg")

                bw_img = convertBlackWhite(img)
                bw_img.draw(win)

                win.exitonclick()

        .. tab:: Discussion

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_0f0fb41d607743998a86962a11eed53d


#. Sepia Tone images are those brownish colored images that may remind you of
   times past.  The formula for creating a sepia tone is as follows:

   .. sourcecode:: python

        newR = (R × 0.393 + G × 0.769 + B × 0.189)
        newG = (R × 0.349 + G × 0.686 + B × 0.168)
        newB = (R × 0.272 + G × 0.534 + B × 0.131)

   Write a function to convert an image to sepia tone. *Hint:*
   Remember that rgb values must be integers between 0 and 255.

    .. actex:: ex_7_18

#.

    .. tabbed:: q11

        .. tab:: Question

           Write a function to uniformly enlarge an image by a factor of 2 (double the size).
        
        
           .. actex:: ex_7_19

        .. tab:: Answer
            
            .. activecode:: answer_7_11
            
               import image
                
               def double(oldimage):
                   oldw = oldimage.getWidth()
                   oldh = oldimage.getHeight()
                   
                   newim = image.EmptyImage(oldw * 2, oldh * 2)
                   for row in range(oldh):
                       for col in range(oldw):
                           oldpixel = oldimage.getPixel(col, row)
                           
                           newim.setPixel(2*col, 2*row, oldpixel)
                           newim.setPixel(2*col+1, 2*row, oldpixel)
                           newim.setPixel(2*col, 2*row+1, oldpixel)
                           newim.setPixel(2*col+1, 2*row+1, oldpixel)
                           
                   return newim
                   
               win = image.ImageWin()
               img = image.Image("luther.jpg")

               bigimg = double(img)
               bigimg.draw(win)

               win.exitonclick()                
                

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_9ca319187b4a4c2399402de0d99c0b1d


#.   After you have scaled an image too much it looks blocky.  One way of
     reducing the blockiness of the image is to replace each pixel with the
     average values of the pixels around it.  This has the effect of smoothing
     out the changes in color.  Write a function that takes an image as a
     parameter and smooths the image.  Your function should return a new image
     that is the same as the old but smoothed.

       .. actex:: ex_7_20

#.

    .. tabbed:: q13

        .. tab:: Question

           Write a general pixel mapper function that will take an image and a pixel mapping function as
           parameters.  The pixel mapping function should perform a manipulation on a single pixel and return
           a new pixel.
        
           .. actex:: ex_7_21

        .. tab:: Answer
            
            .. activecode:: q13_answer
            
                import image
                
                def pixelMapper(oldimage, rgbFunction):
                    width = oldimage.getWidth()
                    height = oldimage.getHeight()
                    newim = image.EmptyImage(width, height)
                
                    for row in range(height):
                        for col in range(width):
                            originalpixel = oldimage.getPixel(col, row)
                            newpixel = rgbFunction(originalpixel)
                            newim.setPixel(col, row, newpixel)
                            
                    return newim
                        
                def graypixel(oldpixel):
                    intensitysum = oldpixel.getRed() + oldpixel.getGreen() + oldpixel.getBlue()
                    aveRGB = intensitysum // 3
                    newPixel = image.Pixel(aveRGB, aveRGB, aveRGB)
                    return newPixel
                
                win = image.ImageWin()
                img = image.Image("luther.jpg")

                newim = pixelMapper(img, graypixel)
                newim.draw(win)

                win.exitonclick()          
                

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_eb9f71a62de24efaa61f64b5a7e5d9c9


#. When you scan in images using a scanner they may have lots of noise due to
   dust particles on the image itself or the scanner itself,
   or the images may even be damaged.  One way of eliminating this noise is
   to replace each pixel by the median value of the pixels surrounding it.

    .. actex:: ex_7_22

#.

    .. tabbed:: q15

        .. tab:: Question

           Research the Sobel edge detection algorithm and implement it.
        
           .. actex:: ex_7_23
        

        .. tab:: Answer
            
            .. activecode:: q15_answer

                import image
                import math
                import sys

                # Code adapted from http://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/image-processing/edge_detection.html
                # Licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.

                # this algorithm takes some time for larger images - this increases the amount of time
                # the program is allowed to run before it times out
                sys.setExecutionLimit(20000)

                img = image.Image("luther.jpg")
                newimg = image.EmptyImage(img.getWidth(), img.getHeight())
                win = image.ImageWin()

                for x in range(1, img.getWidth()-1):  # ignore the edge pixels for simplicity (1 to width-1)
                    for y in range(1, img.getHeight()-1): # ignore edge pixels for simplicity (1 to height-1)

                        # initialise Gx to 0 and Gy to 0 for every pixel
                        Gx = 0
                        Gy = 0

                        # top left pixel
                        p = img.getPixel(x-1, y-1)
                        r = p.getRed()
                        g = p.getGreen()
                        b = p.getBlue()

                        # intensity ranges from 0 to 765 (255 * 3)
                        intensity = r + g + b

                        # accumulate the value into Gx, and Gy
                        Gx += -intensity
                        Gy += -intensity

                        # remaining left column
                        p = img.getPixel(x-1, y)
                        r = p.getRed()
                        g = p.getGreen()
                        b = p.getBlue()

                        Gx += -2 * (r + g + b)

                        p = img.getPixel(x-1, y+1)
                        r = p.getRed()
                        g = p.getGreen()
                        b = p.getBlue()

                        Gx += -(r + g + b)
                        Gy += (r + g + b)

                        # middle pixels
                        p = img.getPixel(x, y-1)
                        r = p.getRed()
                        g = p.getGreen()
                        b = p.getBlue()

                        Gy += -2 * (r + g + b)

                        p = img.getPixel(x, y+1)
                        r = p.getRed()
                        g = p.getGreen()
                        b = p.getBlue()

                        Gy += 2 * (r + g + b)

                        # right column
                        p = img.getPixel(x+1, y-1)
                        r = p.getRed()
                        g = p.getGreen()
                        b = p.getBlue()

                        Gx += (r + g + b)
                        Gy += -(r + g + b)

                        p = img.getPixel(x+1, y)
                        r = p.getRed()
                        g = p.getGreen()
                        b = p.getBlue()

                        Gx += 2 * (r + g + b)

                        p = img.getPixel(x+1, y+1)
                        r = p.getRed()
                        g = p.getGreen()
                        b = p.getBlue()

                        Gx += (r + g + b)
                        Gy += (r + g + b)

                        # calculate the length of the gradient (Pythagorean theorem)
                        length = math.sqrt((Gx * Gx) + (Gy * Gy))

                        # normalise the length of gradient to the range 0 to 255
                        length = length / 4328 * 255

                        length = int(length)

                        # draw the length in the edge image
                        newpixel = image.Pixel(length, length, length)
                        newimg.setPixel(x, y, newpixel)

                newimg.draw(win)
                win.exitonclick()

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_dd2d9ca5ea744aafbf7cdc2a4ad5e974

