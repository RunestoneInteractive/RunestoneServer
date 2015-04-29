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

           Add a ``distanceFromPoint`` method that works similar to ``distanceFromOrigin`` except that it 
           takes a ``Point`` as a parameter and
           computes the distance between that point and self.
           
           .. actex:: classes_q1

        .. tab:: Answer
            
            .. activecode:: ch_cl_ex_1_answer
            
                import math
                
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
                        
                    def distanceFromPoint(self, otherP):
                        dx = (otherP.getX() - self.x)
                        dy = (otherP.getY() - self.y)
                        return math.sqrt(dy**2 + dx**2)

                p = Point(3, 3)
                q = Point(6, 7)
                print(p.distanceFromPoint(q))
                

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_090fe2d30b8d4fe58b829d06c58661f0


#. Add a method ``reflect_x`` to Point which returns a new Point, one which is the 
   reflection of the point about the x-axis.  For example, 
   ``Point(3, 5).reflect_x()`` is (3, -5)
   
   .. actex:: ch_cl_02

#.

    .. tabbed:: q3

        .. tab:: Question

           Add a method ``slope_from_origin`` which returns the slope of the line joining the origin
           to the point.   For example, ::
           
              >>> Point(4, 10).slope_from_origin()
              2.5     
              
           What cases will cause your method to fail? Return None when it happens.
           
           .. actex:: classes_q3

        .. tab:: Answer
            
            .. activecode:: ch_cl_ex_3_answer
            
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
                        
                    def slope_from_origin(self):
                        if self.x == 0:
                           return None
                        else:
                           return self.y / self.x


                p = Point(4, 10)
                print(p.slope_from_origin())
                

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_d70d350ae8284138a5726f8140c45533


#. The equation of a straight line is  "y = ax + b", (or perhaps "y = mx + c").
   The coefficients a and b completely describe the line.  Write a method in the 
   Point class so that if a point instance is given another point, it will compute the equation
   of the straight line joining the two points.  It must return the two coefficients as a tuple
   of two values.  For example,   ::
   
      >>> print(Point(4, 11).get_line_to(Point(6, 15))) 
      >>> (2, 3)
 
   This tells us that the equation of the line joining the two points is "y = 2x + 3".    
   When will your method fail?
   
   .. actex:: ch_cl_04
   
#.

    .. tabbed:: q5

        .. tab:: Question

           Add a method called ``move`` that will take two parameters, call them ``dx`` and ``dy``.  The method will
           cause the point to move in the x and y direction the number of units given. (Hint: you will change the values of the
           state of the point)
           
           .. actex:: classes_q5
           
        .. tab:: Answer
            
            .. activecode:: ch_cl_05_answer
            
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
                    
                    def move(self, dx, dy):
                        self.x = self.x + dx
                        self.y = self.y + dy
                        
                    def __str__(self):
                        return str(self.x) + "," + str(self.y)


                p = Point(7, 6)
                print(p)
                p.move(5, 10)
                print(p)
 

        .. tab:: Discussion 

            .. disqus::
                :shortname: interactivepython
                :identifier: disqus_fc589edaa0e14bd28175850c95b79d15


#.  Given three points that fall on the circumference of a circle, find the center and radius of the circle.

    .. actex:: classes_q6
