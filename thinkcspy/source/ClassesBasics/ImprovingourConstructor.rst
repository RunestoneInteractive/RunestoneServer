..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Improving our Constructor
------------------------- 

Our constructor so far can only create points at location ``(0,0)``.  To create a point at position (7, 6) requires that we
provide some additional capability for the user to pass information to the constructor.  Since constructors are simply specially named functions, we can use parameters (as we've seen before) to provide the specific information.
    
We can make our class constructor more general by putting extra parameters into
the ``__init__`` method, as shown in this codelens example.

.. codelens:: chp13_improveconstructor
    
    class Point:
        """ Point class for representing and manipulating x,y coordinates. """
        
        def __init__(self, initX, initY):
            """ Create a new point at the given coordinates. """
            self.x = initX
            self.y = initY
    
    p = Point(7, 6)



Now when we create new points, we supply the x and y coordinates as parameters.  When the point is created, the values of ``initX`` and ``initY`` are assigned to the state of the object.


.. image:: Figures/objectpic5.png
   :alt: Simple object has state and methods



       
