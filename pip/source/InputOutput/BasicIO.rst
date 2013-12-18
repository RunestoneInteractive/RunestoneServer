..  Copyright (C)  Paul Resnick, Chuck Severance, Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

..  shortname:: BasicIO
..  description:: Input using input and raw_input; output using print

.. qnum::
   :prefix: basicIO-
   :start: 1

Basic Input and Output
======================


.. index:: input, data type, raw_input

Most programs take data inputs of some kind and transform them into data outputs.
In this course, you will see many kinds of inputs, including data from files and 
data that is fetched from sources on the Internet. Similarly, outputs may be
displayed on a screen, stored in files, or transmitted over the Internet.  This
chapter covers the simplest form of input, direct input from a person typing, and 
the simplest form of output, printing results to the screen.

Interactive input from the user
-------------------------------
To get input from the user, we use a built-in function called **raw_input**. When
this function is called, the program stops and waits for the user to type
something. When the user presses *Return* or *Enter*, the program resumes and ``raw_input``
returns what the user typed, as a string.

In our browser-based python environment, ``raw_input`` generates a popup window
for the user to enter a text input.

Before getting input from the user, it is a good idea to print a prompt telling the user what to input.
You can pass a string to ``raw_input`` to be displayed to the user before
pausing for input.

.. activecode:: basicIO_2
   :nocanvas:
   
   x = raw_input('What is your name?')
   print x
   
You always get a string back from **raw_input**. If you expect to get a number,
you can convert the string to a number using **int()**, as presented in the 
previous chapter.

.. activecode:: basicIO_3
   :nocanvas:
   
   x = raw_input('Enter a number, please')
   print type(x)
   print int(x) + 1
   
Try running the code. Now run it again and see what happens if you enter something other than a number
when prompted.

Try changing the print statement to say ``print x + 1``, without converting it
to an integer using ``int()``. Now what happens when you run it?

Output with print
-----------------

We have already been using the ``print`` statement. Later in the course, we'll see
some more advanced ways to generate text and write it to various output destinations. 
For now, there are just a few  things that you should know about ``print``.

First, you can put any python expression after the word ``print``

.. activecode:: basicIO_4
   :nocanvas:
   
   x = 3
   print x + 2
   
Second, if you put multiple expressions after ``print``, separated by commas, 
each of the commas will generate a space in the output.

.. activecode:: basicIO_5
   :nocanvas:
   
   x = 3
   print "x is", x
   
Third, each ``print`` statement that is executed generates a newline (line break)
at the end.

.. activecode:: basicIO_6
   :nocanvas:
   
   x = 3
   print "x is", x
   print "x squared is", x*x
   print
   print "That's all"

