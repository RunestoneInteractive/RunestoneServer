..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. qnum::
   :prefix: iter-9-
   :start: 1

2-Dimensional Iteration: Image Processing
-----------------------------------------

Two dimensional tables have both rows and columns.  You have probably seen many tables like this if you have used a
spreadsheet program.  Another object that is organized in rows and columns is a digital image.  In this section we will
explore how iteration allows us to manipulate these images.

A **digital image** is a finite collection of small, discrete picture elements called **pixels**.  These pixels are organized in a two-dimensional grid.  Each pixel represents the smallest amount of picture information that is
available.  Sometimes these pixels appear as small "dots".

Each image (grid of pixels) has its own width and its own height.  The width is the number of columns and the height is the number of rows.  We can name the pixels in the grid by using the column number and row number.  However, it is very important to remember
that computer scientists like to start counting with 0!  This means that if there are 20 rows, they will be named 0,1,2, and so on through 19.  This will be very useful later when we iterate using range.


In the figure below, the pixel of interest is found at column **c** and row **r**.

.. image:: Figures/image.png

The RGB Color Model
^^^^^^^^^^^^^^^^^^^

Each pixel of the image will represent a single color.  The specific color depends on a formula that mixes various amounts
of three basic colors: red, green, and blue.  This technique for creating color is known as the **RGB Color Model**.
The amount of each color, sometimes called the **intensity** of the color, allows us to have very fine control over the
resulting color.

The minimum intensity value for a basic color is 0.  For example if the red intensity is 0, then there is no red in the pixel.  The maximum
intensity is 255.  This means that there are actually 256 different amounts of intensity for each basic color.  Since there
are three basic colors, that means that you can create 256\ :sup:`3` distinct colors using the RGB Color Model.


Here are the red, green and blue intensities for some common colors.  Note that "Black" is represented by a pixel having
no basic color.  On the other hand, "White" has maximum values for all three basic color components.

	=======  =======  =======  =======
	Color    Red      Green    Blue
	=======  =======  =======  =======
	Red      255      0        0
	Green    0        255      0
	Blue     0        0        255
	White    255      255      255
	Black    0        0        0
	Yellow   255      255      0
	Magenta  255      0        255
	=======  =======  =======  =======

In order to manipulate an image, we need to be able to access individual pixels.  This capability is provided by
a module called **image**.  The image module defines two classes: ``Image`` and ``Pixel``.

Each Pixel object has three attributes: the red intensity, the green intensity, and the blue intensity.  A pixel provides three methods
that allow us to ask for the intensity values.  They are called ``getRed``, ``getGreen``, and ``getBlue``.  In addition, we can ask a
pixel to change an intensity value using its ``setRed``, ``setGreen``, and ``setBlue`` methods.


    ============  ================            ===============================================
    Method Name   Example                     Explanation
    ============  ================            ===============================================
    Pixel(r,g,b)  Pixel(20,100,50)            Create a new pixel with 20 red, 100 green, and 50 blue.
    getRed()      r = p.getRed()              Return the red component intensity.
    getGreen()    r = p.getGreen()            Return the green component intensity.
    getBlue()     r = p.getBlue()             Return the blue component intensity.
    setRed()      p.setRed(100)               Set the red component intensity to 100.
    setGreen()    p.setGreen(45)              Set the green component intensity to 45.
    setBlue()     p.setBlue(156)              Set the blue component intensity to 156.
    ============  ================            ===============================================

In the example below, we first create a pixel with 45 units of red, 76 units of green, and 200 units of blue.
We then print the current amount of red, change the amount of red, and finally, set the amount of blue to be
the same as the current amount of green.

.. activecode::  pixelex1a
    :nocodelens:

    import image

    p = image.Pixel(45, 76, 200)
    print(p.getRed())
    p.setRed(66)
    print(p.getRed())
    p.setBlue(p.getGreen())
    print(p.getGreen(), p.getBlue())

**Check your understanding**

.. mchoicemf:: test_question7_8_1_1
   :answer_a: Dark red
   :answer_b: Light red
   :answer_c: Dark green
   :answer_d: Light green
   :correct: a
   :feedback_a: Because all three values are close to 0, the color will be dark.  But because the red value is higher than the other two, the color will appear red.
   :feedback_b: The closer the values are to 0, the darker the color will appear.
   :feedback_c: The first value in RGB is the red value.  The second is the green.  This color has no green in it.
   :feedback_d: The first value in RGB is the red value.  The second is the green.  This color has no green in it.

   If you have a pixel whose RGB value is (50, 0, 0), what color will this pixel appear to be?

Image Objects
^^^^^^^^^^^^^


To access the pixels in a real image, we need to first create an ``Image`` object.  Image objects can be created in two
ways.  First, an Image object can be made from the
files that store digital images.  The image object has an attribute corresponding to the width, the height, and the
collection of pixels in the image.

It is also possible to create an Image object that is "empty".  An ``EmptyImage`` has a width and a height.  However, the
pixel collection consists of only "White" pixels.

We can ask an image object to return its size using the ``getWidth`` and ``getHeight`` methods.  We can also get a pixel from a particular location in the image using ``getPixel`` and change the pixel at
a particular location using ``setPixel``.


The Image class is shown below.  Note that the first two entries show how to create image objects.  The parameters are
different depending on whether you are using an image file or creating an empty image.

    =================== =============================== ==================================================
    Method Name         Example                         Explanation
    =================== =============================== ==================================================
    Image(filename)     img = image.Image("cy.png")     Create an Image object from the file cy.png.
    EmptyImage()        img = image.EmptyImage(100,200) Create an Image object that has all "White" pixels
    getWidth()          w = img.getWidth()              Return the width of the image in pixels.
    getHeight()         h = img.getHeight()             Return the height of the image in pixels.
    getPixel(col,row)   p = img.getPixel(35,86)         Return the pixel at column 35, row 86d.
    setPixel(col,row,p) img.setPixel(100,50,mp)         Set the pixel at column 100, row 50 to be mp.
    =================== =============================== ==================================================

Consider the image shown below.  Assume that the image is stored in a file called "luther.jpg".  Line 2 opens the
file and uses the contents to create an image object that is referred to by ``img``.  Once we have an image object,
we can use the methods described above to access information about the image or to get a specific pixel and check
on its basic color intensities.





.. raw:: html

    <img src="../_static/LutherBellPic.jpg" id="luther.jpg">



.. activecode::  pixelex1
    :nocodelens:

    import image
    img = image.Image("luther.jpg")

    print(img.getWidth())
    print(img.getHeight())

    p = img.getPixel(45, 55)
    print(p.getRed(), p.getGreen(), p.getBlue())


When you run the program you can see that the image has a width of 400 pixels and a height of 244 pixels.  Also, the
pixel at column 45, row 55, has RGB values of 165, 161, and 158.  Try a few other pixel locations by changing the ``getPixel`` arguments and rerunning the program.

**Check your understanding**

.. mchoicemf:: test_question7_8_2_1
   :answer_a: 149 132 122
   :answer_b: 183 179 170
   :answer_c: 165 161 158
   :answer_d: 201 104 115
   :correct: b
   :feedback_a: These are the values for the pixel at row 30, column 100.  Get the values for row 100 and column 30 with p = img.getPixel(100, 30).
   :feedback_b: Yes, the RGB values are 183 179 170 at row 100 and column 30.
   :feedback_c: These are the values from the original example (row 45, column 55). Get the values for row 100 and column 30 with p = img.getPixel(30, 100).
   :feedback_d: These are simply made-up values that may or may not appear in the image.  Get the values for row 100 and column 30 with p = img.getPixel(30, 100).

   Using the previous ActiveCode example, select the answer that is closest to the RGB values of the pixel at row 100, column 30?  The values may be off by one or two due to differences in browsers.


Image Processing and Nested Iteration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Image processing** refers to the ability to manipulate the individual pixels in a digital image.  In order to process
all of the pixels, we need to be able to systematically visit all of the rows and columns in the image.  The best way
to do this is to use **nested iteration**.

Nested iteration simply means that we will place one iteration construct inside of another.  We will call these two
iterations the **outer iteration** and the **inner iteration**.
To see how this works, consider the iteration below.

.. sourcecode:: python

    for i in range(5):
        print(i)

We have seen this enough times to know that the value of ``i`` will be 0, then 1, then 2, and so on up to 4.
The ``print`` will be performed once for each pass.
However, the body of the loop can contain any statements including another iteration (another ``for`` statement).  For example,

.. sourcecode:: python

    for i in range(5):
        for j in range(3):
            print(i, j)

The ``for i`` iteration is the `outer iteration` and the ``for j`` iteration is the `inner iteration`.  Each pass through
the outer iteration will result in the complete processing of the inner iteration from beginning to end.  This means that
the output from this nested iteration will show that for each value of ``i``, all values of ``j`` will occur.

Here is the same example in activecode.  Try it.  Note that the value of ``i`` stays the same while the value of ``j`` changes.  The inner iteration, in effect, is moving faster than the outer iteration.

.. activecode:: nested1

    for i in range(5):
        for j in range(3):
            print(i, j)

Another way to see this in more detail is to examine the behavior with codelens.  Step through the iterations to see the
flow of control as it occurs with the nested iteration.  Again, for every value of ``i``, all of the values of ``j`` will occur.  You can see that the inner iteration completes before going on to the next pass of the outer iteration.

.. codelens:: nested2

    for i in range(5):
        for j in range(3):
            print(i, j)

Our goal with image processing is to visit each pixel.  We will use an iteration to process each `row`.  Within that iteration, we will use a nested iteration to process each `column`.  The result is a nested iteration, similar to the one
seen above, where the outer ``for`` loop processes the rows, from 0 up to but not including the height of the image.
The inner ``for`` loop will process each column of a row, again from 0 up to but not including the width of the image.

The resulting code will look like the following.  We are now free to do anything we wish to each pixel in the image.

.. sourcecode:: python

	for row in range(img.getHeight()):
	    for col in range(img.getWidth()):
	        # do something with the pixel at position (col,row)

One of the easiest image processing algorithms will create what is known as a **negative** image.  A negative image simply means that
each pixel will be the `opposite` of what it was originally.  But what does opposite mean?

In the RGB color model, we can consider the opposite of the red component as the difference between the original red
and 255.  For example, if the original red component was 50, then the opposite, or negative red value would be
``255-50`` or 205.  In other words, pixels with a lot of red will have negatives with little red and pixels with little red will have negatives with a lot.  We do the same for the blue and green as well.

The program below implements this algorithm using the previous image (luther.jpg).  Run it to see the resulting negative image.  Note that there is a lot of processing taking place and this may take a few seconds to complete.  In addition, here are two other images that you can use (cy.png and goldygopher.png).  


.. raw:: html

    <img src="../_static/cy.png" id="cy.png">
    <h4 style="text-align: center;">cy.png</h4>

.. raw:: html

    <img src="../_static/goldygopher.png" id="goldygopher.png">
    <h4 style="text-align: center;">goldygopher.png</h4>


Change the name of the file in the ``image.Image()`` call to see how these images look as negatives.  Also, note that there is an ``exitonclick`` method call at the very end which will close the window when you click on it.  This will allow you to "clear the screen" before drawing the next negative.


.. activecode::  acimg_1
    :nocodelens:

    import image

    img = image.Image("luther.jpg")
    win = image.ImageWin(img.getWidth(), img.getHeight())
    img.draw(win)
    img.setDelay(1,15)   # setDelay(0) turns off animation

    for row in range(img.getHeight()):
        for col in range(img.getWidth()):
            p = img.getPixel(col, row)

            newred = 255 - p.getRed()
            newgreen = 255 - p.getGreen()
            newblue = 255 - p.getBlue()

            newpixel = image.Pixel(newred, newgreen, newblue)

            img.setPixel(col, row, newpixel)

    img.draw(win)
    win.exitonclick()

Let's take a closer look at the code.  After importing the image module, we create two image objects.  The first, ``img``, represents a typical digital photo.  The second, ``newimg``, is an empty image that will be "filled in" as we process the original pixel by pixel.  Note that the width and height of the empty image is set to be the same as the width and height of the original.

Lines 7 and 8 create the nested iteration that we discussed earlier.  This allows us to process each pixel in the image.
Line 9 gets an individual pixel.

Lines 11-13 create the negative intensity values by extracting the original intensity from the pixel and subtracting it
from 255.  Once we have the ``newred``, ``newgreen``, and ``newblue`` values, we can create a new pixel (Line 15).

Finally, we need to replace the old pixel with the new pixel in our image. It is important to put the new pixel into the same location as the original pixel that it came from in the digital photo.

Try to change the program above so that the outer loop iterates over the columns and the inner loop iterates over the rows.  We still create a negative image, but you can see that the pixels update in a very different order.

.. admonition:: Other pixel manipulation

	There are a number of different image processing algorithms that follow the same pattern as shown above.  Namely, take the original pixel, extract the red, green, and blue intensities, and then create a new pixel from them.  The new pixel is inserted into an empty image at the same location as the original.

	For example, you can create a **gray scale** pixel by averaging the red, green and blue intensities and then using that value for all intensities.

	From the gray scale you can create **black white** by setting a threshold and selecting to either insert a white pixel or a black pixel into the empty image.

	You can also do some complex arithmetic and create interesting effects, such as
	`Sepia Tone <http://en.wikipedia.org/wiki/Sepia_tone#Sepia_toning>`_






You have just passed a very important point in your study of Python programming.  Even though there is much more that we will do, you have learned all of the basic building blocks that are necessary to solve many interesting problems.  From an algorithm point of view, you can now implement selection and iteration.  You can also solve problems by breaking them down into smaller parts, writing functions for those parts, and then calling the functions to complete the implementation.
What remains is to focus on ways that we can better represent our problems in terms of the data that we manipulate.  We will now turn our attention to studying the main data collections provided by Python.

**Check your understanding**

.. mchoicemf:: test_question7_8_3_1
   :answer_a: Output a
   :answer_b: Output b
   :answer_c: Output c
   :answer_d: Output d
   :correct: a
   :feedback_a: i will start with a value of 0 and then j will iterate from 0 to 1.  Next, i will be 1 and j will iterate from 0 to 1.  Finally, i will be 2 and j will iterate from 0 to 1.
   :feedback_b: The inner for-loop controls the second digit (j).  The inner for-loop must complete before the outer for-loop advances.
   :feedback_c: The inner for-loop controls the second digit (j).  Notice that the inner for-loop is over the list [0, 1].
   :feedback_d: The outer for-loop runs 3 times (0, 1, 2) and the inner for-loop runs twice for each time the outer for-loop runs, so this code prints exactly 6 lines.

   What will the following nested for-loop print?  (Note, if you are having trouble with this question, review CodeLens 3).

   .. code-block:: python

      for i in range(3):
          for j in range(2):
              print(i, j)

   ::

      a.

      0	0
      0	1
      1	0
      1	1
      2	0
      2	1

      b.

      0   0
      1   0
      2   0
      0   1
      1   1
      2   1

      c.

      0   0
      0   1
      0   2
      1   0
      1   1
      1   2

      d.

      0   1
      0   1
      0   1



.. mchoicemf:: test_question7_8_3_2
   :answer_a: It would look like a red-washed version of the bell image
   :answer_b: It would be a solid red rectangle the same size as the original image
   :answer_c: It would look the same as the original image
   :answer_d: It would look the same as the negative image in the example code
   :correct: a
   :feedback_a: Because we are removing the green and the blue values, but keeping the variation of the red the same, you will get the same image, but it will look like it has been bathed in red.
   :feedback_b: Because the red value varies from pixel to pixel, this will not look like a solid red rectangle.  For it to look like a solid red rectangle each pixel would have to have exactly the same red value.
   :feedback_c: If you remove the blue and green values from the pixels, the image will look different, even though there does not appear to be any blue or green in the original image (remember that other colors are made of combinations of red, green and blue).
   :feedback_d: Because we have changed the value of the pixels from what they were in the original ActiveCode box code, the image will not be the same.

   What would the image produced from ActiveCode box 16 look like if you replaced the lines:

   .. code-block:: python

      newred = 255 - p.getRed()
      newgreen = 255 - p.getGreen()
      newblue = 255 - p.getBlue()

   with the lines:

   .. code-block:: python

      newred = p.getRed()
      newgreen = 0
      newblue = 0



