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
        
          We can represent a rectangle by knowing three things: the location of its lower left corner, its width, and its height.
          Create a class definition for a Rectangle class using this idea.  To create a Rectangle object at location (4,5) with width 6
          and height 5, we would do the following::
          
              r = Rectangle(Point(4,5), 6, 5)
              
        .. tab:: Answer
        
            .. activecode:: ch_cl2_answer1
            
                class Point:
                    """ Point class for representing and manipulating x,y coordinates. """

                    def __init__(self, initX, initY):

                        self.x = initX
                        self.y = initY

                    def getX(self):
                        return self.x

                    def getY(self):
                        return self.y

                    def __str__(self):
                        return "x=" + str(self.x) + ", y=" + str(self.y)
                    
                    
                class Rectangle:
                    """Rectangle class using Point, width and height"""
                
                    def __init__(self, initP, initW, initH):
                
                        self.location = initP
                        self.width = initW
                        self.height = initH
                        
                loc = Point(4, 5)
                r = Rectangle(loc, 6, 5)
                print(r)
                    
                    
        .. tab:: Discussion
        
             .. disqus::
                 :shortname: interactivepython
                 :identifier: disqus_ch_cl2_q1
                 
   
   
                 
#. Add the following accessor methods to the Rectangle class: ``getWidth``, ``getHeight``, ``__str__``.

   .. activecode:: ch_cl2_q2  
   
   
                    

#.

    .. tabbed:: q3

        .. tab:: Question

           Add a method ``area`` to the Rectangle class that returns the area of any instance::
        
              r = Rectangle(Point(0, 0), 10, 5)
              test(r.area(), 50)

        .. tab:: Answer
        
            .. activecode:: ch_cl2_q3answer
            
                class Point:
                    """ Point class for representing and manipulating x,y coordinates. """

                    def __init__(self, initX, initY):

                        self.x = initX
                        self.y = initY

                    def getX(self):
                        return self.x

                    def getY(self):
                        return self.y

                    def __str__(self):
                        return "x=" + str(self.x) + ", y=" + str(self.y)
            
            
                class Rectangle:
                    """Rectangle class using Point, width and height"""
        
                    def __init__(self, initP, initW, initH):
        
                        self.location = initP
                        self.width = initW
                        self.height = initH
                        
                    def area(self):
                        return self.width * self.height
                        
                        

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_d43c8f8afb2c4c808917bb7e948dbcbe


#. Write a ``perimeter`` method in the Rectangle class so that we can find
   the perimeter of any rectangle instance::
   
      r = Rectangle(Point(0, 0), 10, 5)
      test(r.perimeter(), 30)
      

   .. activecode:: ch_cl2_q4

#.

    .. tabbed:: q5

        .. tab:: Question

           Write a ``transpose`` method in the Rectangle class that swaps the width
           and the height of any rectangle instance::
           
              r = Rectangle(Point(100, 50), 10, 5)
              test(r.width, 10)
              test(r.height, 5)
              r.transpose()
              test(r.width, 5)
              test(r.height, 10)

        .. tab:: Answer
            
            .. activecode:: ch_cl2_q5answer
        
                class Point:
                    """ Point class for representing and manipulating x,y coordinates. """

                    def __init__(self, initX, initY):

                        self.x = initX
                        self.y = initY

                    def getX(self):
                        return self.x

                    def getY(self):
                        return self.y

                    def __str__(self):
                        return "x=" + str(self.x) + ", y=" + str(self.y)
        
        
                class Rectangle:
                    """Rectangle class using Point, width and height"""
    
                    def __init__(self, initP, initW, initH):
    
                        self.location = initP
                        self.width = initW
                        self.height = initH
                    
                    def transpose(self):
                        temp = self.width
                        self.width = self.height
                        self.height = temp
                    
                    
        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_chcl_q5disc


#. Write a new method in the Rectangle class to test if a Point falls within
   the rectangle.  For this exercise, assume that a rectangle at (0,0) with
   width 10 and height 5 has *open* upper bounds on the width and height, 
   i.e. it stretches in the x direction from [0 to 10), where 0 is included
   but 10 is excluded, and from [0 to 5) in the y direction.  So
   it does not contain the point (10, 2).  These tests should pass::
   
      r = Rectangle(Point(0, 0), 10, 5)
      test(r.contains(Point(0, 0)), True)
      test(r.contains(Point(3, 3)), True)
      test(r.contains(Point(3, 7)), False)
      test(r.contains(Point(3, 5)), False)
      test(r.contains(Point(3, 4.99999)), True)
      test(r.contains(Point(-3, -3)), False)
   
#.

    .. tabbed:: q7

        .. tab:: Question

           Write a new method called ``diagonal`` that will return the length of the diagonal that runs
           from the lower left corner to the opposite corner.
        
             

        .. tab:: Answer
            
            .. activecode:: ch_cl2_answer7
            
                class Point:
                    """ Point class for representing and manipulating x,y coordinates. """

                    def __init__(self, initX, initY):

                        self.x = initX
                        self.y = initY

                    def getX(self):
                        return self.x

                    def getY(self):
                        return self.y

                    def __str__(self):
                        return "x=" + str(self.x) + ", y=" + str(self.y)
    
    
                class Rectangle:
                    """Rectangle class using Point, width and height"""

                    def __init__(self, initP, initW, initH):

                        self.location = initP
                        self.width = initW
                        self.height = initH
                        
                    def diagonal(self):
                    
                        d = (self.width**2 + self.height**2) ** 0.5
                        return d

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_5f1e3f17064f44088a896e9bc0e10b4d


#.  In games, we often put a rectangular "bounding box" around our sprites in
    the game.  We can then do *collision detection* between, say, bombs and 
    spaceships, by comparing whether their rectangles overlap anywhere. 

    Write a function to determine whether two rectangles collide. *Hint:
    this might be quite a tough exercise!  Think carefully about all the
    cases before you code.*
    
    .. activecode:: ch_cl2_q8
    
