..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".
	

Using a Main Function
---------------------

Using functions is a good idea.  It helps us to modularize our code by breaking a program
into logical parts where each part is responsible for a specific task.  For example, in one of our first programs there
was a function called ``drawSquare`` that was responsible for having some turtle draw a square of some size.
The actual turtle and the actual size of the square were defined to be provided as parameters. Here is that original program.

.. code-block:: python

    import turtle

    def drawSquare(t, sz):
        """Make turtle t draw a square of with side sz."""

        for i in range(4):
            t.forward(sz)
            t.left(90)


    wn = turtle.Screen()          # Set up the window and its attributes
    wn.bgcolor("lightgreen")

    alex = turtle.Turtle()        # create alex
    drawSquare(alex, 50)          # Call the function to draw the square

    wn.exitonclick()


If you look closely at the structure of this program, you will notice that we first perform all of our necessary ``import`` statements, in this case to be able to use the ``turtle`` module.  Next, we define the function ``drawSquare``.  At this point, we could have defined as many functions as were needed.  Finally, there are five statements that set up the window, create the turtle, perform the function invocation, and wait for a user click to terminate the program.

These final five statements perform the main processing that the program will do.  Notice that much of the detail has been pushed inside the ``drawSquare`` function.  However, there are still these five lines of code that are needed to get things done.

In many programming languages (e.g. Java and C++), it is not possible to simply have statements sitting alone like this at the bottom of the program.  They are required to be part of a special function that is automatically invoked by the operating system when the program is executed.  This special function is called **main**.  Although this is not required by the Python programming language, it is actually a good idea that we can incorporate into the logical structure of our program.  In other words, these five lines are logically related to one another in that they provide the main tasks that the program will perform.  Since functions are designed to allow us to break up a program into logical pieces, it makes sense to call this piece ``main``.

The following activecode shows this idea.  In line 11 we have defined a new function called ``main`` that doesn't need any parameters.  The five lines of main processing are now placed inside this function.  Finally, in order to execute that main processing code, we need to invoke the ``main`` function (line 20).  When you push run, you will see that the program works the same as it did before.

.. activecode:: ch04_1
    :nocodelens:

    import turtle

    def drawSquare(t, sz):
        """Make turtle t draw a square of with side sz."""

        for i in range(4):
            t.forward(sz)
            t.left(90)


    def main():                      # Define the main function
        wn = turtle.Screen()         # Set up the window and its attributes
        wn.bgcolor("lightgreen")

        alex = turtle.Turtle()       # create alex
        drawSquare(alex, 50)         # Call the function to draw the square

        wn.exitonclick()

    main()                           # Invoke the main function
    
    
Now our program structure is as follows.  First, import any modules that will be required.  Second, define any functions that will be needed.  Third, define a ``main`` function that will get the process started.  And finally, invoke the main function (which will in turn call the other functions as needed).

.. note::

     In Python there is nothing special about the name ``main``.  We could have called this function anything we wanted.  We chose ``main`` just to be consistent with some of the other languages.
     