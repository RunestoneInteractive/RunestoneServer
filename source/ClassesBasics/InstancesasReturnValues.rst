..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Instances as Return Values
--------------------------

Functions and methods can return objects.  This is actually nothing new since everything in Python is an object and we have
been returning values for quite some time.  The difference here is that we want to have the method create an object using
the constructor and then return it as the value of the method.

    
Suppose you have a point object
and wish to find the midpoint halfway between it and some other target point.  We would like to write a method, call
it ``halfway`` that takes another ``Point`` as a parameter and returns the ``Point`` that is halfway between the point and
the target.

.. activecode:: chp13_classesmid1

    class Point:

        def __init__(self, initX, initY):

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

        def halfway(self, target): 
             mx = (self.x + target.x)/2
             my = (self.y + target.y)/2
             return Point(mx, my)

    p = Point(3,4)
    q = Point(5,12)
    mid = p.halfway(q)

    print(mid)
    print(mid.getX())
    print(mid.getY())
       

The resulting Point, ``mid``, has an x value of 4 and a y value of 8.  We can also use any other methods since ``mid`` is a
``Point`` object.

    

.. note::

    This workspace is provided for your convenience.  You can use this activecode window to try out anything you like.

    .. activecode:: scratch_cl_01


