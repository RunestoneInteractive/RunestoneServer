..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Objects as Arguments and Parameters
-------------------------------------

You can pass an object as a argument in the usual way.  We've already seen
this in some of the turtle examples where we passed the turtle to
some function like ``drawRectangle`` so that the function could 
control and use whatever turtle instance we passed to it.

Here is a simple function called ``distance`` involving our new ``Point`` objects.  The job of this function is to figure out the 
distance between two points.
 
.. activecode:: chp13_classes6

    import math
    
    class Point:
        """ Point class for representing and manipulating x,y coordinates. """
        
        def __init__(self, initX, initY):
 
            self.x = initX
            self.y = initY

        def getX(self):
            return self.x

        def getY(self):
            return self.y

        def distanceFromOrigin(self):
            return ((self.x ** 2) + (self.y ** 2)) ** 0.5

    def distance(point1, point2):
        xdiff = point2.getX()-point1.getX()
        ydiff = point2.getY()-point1.getY()

        dist = math.sqrt(xdiff**2 + ydiff**2)
        return dist
    
    p = Point(4,3)
    q = Point(0,0)
    print(distance(p,q))


``distance`` takes two points and returns the distance between them.  Note that ``distance`` is **not** a method of the Point class.  You can see this by looking at the indentation pattern.  It is not inside the class definition.  The other way we
can know that ``distance`` is not a method of Point is that ``self`` is not included as a formal parameter.  In addition, we do not invoke ``distance`` using the dot notation.


