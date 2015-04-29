..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Converting an Object to a String
--------------------------------

 
When we're working with classes and objects, it is often necessary to print an object (that is to print the state of an object).
Consider the example below.

.. activecode:: chp13_classesstr1
    
    class Point:
        """ Point class for representing and manipulating x,y coordinates. """
        
        def __init__(self, initX, initY):
            """ Create a new point at the given coordinates. """ 
            self.x = initX
            self.y = initY

        def getX(self):
            return self.x

        def getY(self):
            return self.y

        def distanceFromOrigin(self):
            return ((self.x ** 2) + (self.y ** 2)) ** 0.5

    
    p = Point(7, 6)
    print(p)

The ``print`` function shown above produces a string representation of the Point ``p``.  The default functionality provided by
Python tells you that ``p`` is an object of type ``Point``.  However, it does not tell you anything about the specific
state of the point.

We can improve on this representation if we include a special method call ``__str__``.  Notice that this method uses the same naming convention as the constructor, that is two underscores before and after the name.  It is common that Python
uses this naming technique for special methods.

The ``__str__`` method is responsible for returning a string representation as defined by the class creator.  In other words, you as the programmer, get to choose what a ``Point`` should look like when it gets printed.  In this case, we
have decided that the string representation will include the values of x and y as well as some identifying text.  It
is required that the ``__str__`` method create and *return* a string.

.. activecode:: chp13_classesstr2

    class Point:
        """ Point class for representing and manipulating x,y coordinates. """

        def __init__(self, initX, initY):
            """ Create a new point at the given coordinates. """
            self.x = initX
            self.y = initY

        def getX(self):
            return self.x

        def getY(self):
            return self.y

        def distanceFromOrigin(self):
            return ((self.x ** 2) + (self.y ** 2)) ** 0.5
          
        def __str__(self):
            return "x=" + str(self.x) + ", y=" + str(self.y)

    p = Point(7, 6)
    print(p)


When we run the program above you can see that the ``print`` function now shows the string that we chose.

Now, you ask, don't we already have an ``str`` type converter that can 
turn our object into a string?  Yes we do!  

And doesn't ``print``
automatically use this when printing things?  Yes again! 


But, as we saw earlier, these automatic mechanisms do not do exactly what we want.  Python provides many default implementations for
methods that we as programmers will probably want to change.  When a programmer changes the meaning of a special method we
say that we **override** the method.  Note also that the ``str`` type converter function uses whatever ``__str__`` method we
provide.

