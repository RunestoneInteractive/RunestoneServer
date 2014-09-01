..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Composition
-----------

As we have already seen, you can call one function from within another.
This ability is called **composition**.

As an example, we'll write a function that takes two points, the center of the
circle and a point on the perimeter, and computes the area of the circle.

Assume that the center point is stored in the variables ``xc`` and ``yc``, and
the perimeter point is in ``xp`` and ``yp``. The first step is to find the
radius of the circle, which is the distance between the two points.
Fortunately, we've just written a function, ``distance``, that does just that,
so now all we have to do is use it:

.. sourcecode:: python
    
    radius = distance(xc, yc, xp, yp)

The second step is to find the area of a circle with that radius and return it.
Again we will use one of our earlier functions:

.. sourcecode:: python
    
    result = area(radius)
    return result

Wrapping that up in a function, we get:

.. activecode:: ch06_newarea
    
    def distance(x1, y1, x2, y2):
	    dx = x2 - x1
	    dy = y2 - y1
	    dsquared = dx**2 + dy**2
	    result = dsquared**0.5
	    return result

    def area(radius):
        b = 3.14159 * radius**2
        return b

    def area2(xc, yc, xp, yp):
        radius = distance(xc, yc, xp, yp)
        result = area(radius)
        return result

    print(area2(0,0,1,1))



We called this function ``area2`` to distinguish it from the ``area`` function
defined earlier. There can only be one function with a given name within a
module.

Note that we could have written the composition without storing the intermediate results.

.. sourcecode:: python
    
    def area2(xc, yc, xp, yp):
        return area(distance(xc, yc, xp, yp))


.. index:: boolean function

