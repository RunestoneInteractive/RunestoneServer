..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".
    
..  shortname:: IntroToClasses
..  description:: This is the introduction to the idea of building a class

.. qnum::
   :prefix: cls-
   :start: 1

.. _classes_chap:

Classes and Objects - the Basics
================================


.. index:: object-oriented programming

Object-oriented programming
---------------------------



Python is an **object-oriented programming language**.  That means it
provides features that support `object-oriented programming
<http://en.wikipedia.org/wiki/Object-oriented_programming>`__ (**OOP**).

Object-oriented programming has its roots in the 1960s, but it wasn't until the
mid 1980s that it became the main `programming paradigm
<http://en.wikipedia.org/wiki/Programming_paradigm>`__ used in the creation
of new software. It was developed as a way to handle the rapidly increasing
size and complexity of software systems and to make it easier to modify these
large and complex systems over time.

Up to now, some of the programs we have been writing use a `procedural programming
<http://en.wikipedia.org/wiki/Procedural_programming>`__ paradigm. In
procedural programming the focus is on writing functions or *procedures* which
operate on data. In object-oriented programming the focus is on the creation of
**objects** which contain both data and functionality together.
Usually, each object definition corresponds to some object or concept in the real
world and the functions that operate on that object correspond to the ways
real-world objects interact.


Objects Revisited
-----------------

In Python, every value is actually an object. Whether it be a dictionary, a list, or even an integer, they are all objects.  Programs manipulate those objects either by performing
computation with them or by asking them to perform methods.  To be more specific, we say that an object has
a **state** and a collection of **methods** that it can perform. (More about **methods** below.) The state of an object represents those things
that the object knows about itself.  For example, each list has state, the items in the list. And it has methods, such as append and pop, which can operate on the list to change its state or do something else useful. 


.. index:: compound data type

User Defined Classes
--------------------

We've already seen classes like ``str``, ``int``,  ``float`` and ``list``.  These were defined by Python and
made available for us to use.  However, in many cases when we are solving problems we need to create data objects
that are related to the problem we are trying to solve.  We need to create our own classes.

As an example, consider the concept of a mathematical point. In two dimensions, a point is two
numbers (coordinates) that are treated collectively as a single object. 
Points are often written in parentheses with a comma
separating the coordinates. For example, ``(0, 0)`` represents the origin, and
``(x, y)`` represents the point ``x`` units to the right and ``y`` units up
from the origin.  This ``(x,y)`` is the state of the point.

Thinking about our diagram above, we could draw a ``point`` object as shown here.

.. image:: Figures/objectpic2.png
   :alt: A point has an x and a y


Some of the typical operations that one associates with points might be to ask
the point for its x coordinate, ``getX``, or to ask for its y coordinate, ``getY``.  You may also
wish to calculate the distance of a point from the origin, or the distance of a point from another point,
or find the midpoint between two points, or answer the question as to whether a point falls within a
given rectangle or circle.  We'll shortly see how we can organize these
together with the data.

.. image:: Figures/objectpic3.png
   :alt: A point also has methods


Now that we understand what a ``point`` object might look like, we can define a new **class**. 
We'll want our points to each have an ``x`` and a ``y`` attribute,
so our first class definition looks like this.

.. sourcecode:: python
    :linenos:
    
    class Point:
        """ Point class for representing and manipulating x,y coordinates. """
        
        def __init__(self):
            """ Create a new point at the origin """
            self.x = 0
            self.y = 0          

Class definitions can appear anywhere in a program, but they are usually near
the beginning (after the ``import`` statements). The syntax rules for a class
definition are the same as for other compound statements. There is a header
which begins with the keyword, ``class``, followed by the name of the class,
and ending with a colon.

If the first line after the class header is a string, it becomes
the docstring of the class, and will be recognized by various tools.  (This
is also the way docstrings work in functions.)

Every class should have a method with the special name ``__init__``.  
This **initializer method**, often referred to as the **constructor**, is automatically called whenever a new 
instance of ``Point`` is created.  It gives the programmer the opportunity 
to set up the attributes required within the new instance by giving them 
their initial state values.  The ``self`` parameter (you could choose any
other name, but nobody ever does!) is automatically set to reference
the newly created object that needs to be initialized.   

So let's use our new Point class now.

.. activecode:: chp13_classes1
    
    class Point:
        """ Point class for representing and manipulating x,y coordinates. """
        
        def __init__(self):
 
            self.x = 0
            self.y = 0
    
    p = Point()         # Instantiate an object of type Point
    q = Point()         # and make a second point

    print("Nothing seems to have happened with the points")
    
   
During the initialization of the objects, we created two
attributes called `x` and `y` for each, and gave them both the value 0.  You will note that when you run the
program, nothing happens.  It turns out that this is not quite the case.  In fact, two ``Points`` have been created, each
having an x and y coordinate with value 0.  However, because we have not asked the point to do anything, we don't see any other result.


.. image:: Figures/objectpic4.png
   :alt: Simple object has state and methods



The following program adds a few print statements. You can see that the output suggests that each one is a ``Point object``.
However, notice that the ``is`` operator returns ``False`` meaning that they are different objects (we will have more to say about this in a later chapter).

.. activecode:: chp13_classes2
    
    class Point:
        """ Point class for representing and manipulating x,y coordinates. """
        
        def __init__(self):
 
            self.x = 0
            self.y = 0
    
    p = Point()         # Instantiate an object of type Point
    q = Point()         # and make a second point

    print(p)
    print(q)

    print(p is q)


A function like ``Point`` that creates a new object instance 
is called a **constructor**.  Every class automatically uses the name of the class as the name of the constructor function.
The definition of the constructor function is done
when you write the ``__init__`` function (method) inside the class definition.

It may be helpful to think of a class as a factory for making objects.  
The class itself isn't an instance of a point, but it contains the machinery 
to make point instances.   Every time you call the constructor, you're asking
the factory to make you a new object.  As the object comes off the 
production line, its initialization method is executed to 
get the object properly set up with it's factory default settings.

The combined process of "make me a new object" and "get its settings initialized
to the factory default settings" is called **instantiation**.  

To get a clearer understanding of what happens when instantiating a new instance, examine the previous code using CodeLens.

.. codelens:: chp13_classes2a
    
    class Point:
        """ Point class for representing and manipulating x,y coordinates. """
        
        def __init__(self):
 
            self.x = 0
            self.y = 0
    
    p = Point()         # Instantiate an object of type Point
    q = Point()         # and make a second point

    print(p)
    print(q)

    print(p is q)
    
At Step 6 in the codelens, you can see that Point has been bound to an object representing the point class, but there are not yet any instances. The execution of line 9, ``p = Point()``, occurs at steps 7-9. First, at step 7, you can see that a blank instance of the class has been created, and is passed as the first (and only parameter) to the ``__init__`` method. That method's code is executed, with the variable self bound to that instance. At steps 8 and 9, two instance variables are filled in: x and y are both set to 0. Nothing is returned from the __init__ method, but the point object itself is returned from the call to ``Point()``. Thus, at step 10,  p is bound to the new point that was created and initialized.

Skipping ahead, by the time we get to Step 16, p and q are each bound to different points. Even though both have x and y instance variables set to 0, they are *different objects*. Thus ``p is q`` evaluates to False.


Improving our Constructor
------------------------- 

Our constructor so far can only create points at location ``(0,0)``.  To create a point at position (7, 6) requires that we
provide some additional capability for the user to pass information to the constructor.  Since constructors are simply specially named functions, we can use parameters (as we've seen before) to provide the specific information. 
    
We can make our class constructor more generally usable by putting extra parameters into
the ``__init__`` method, as shown in this example.

.. sourcecode:: python
    
    class Point:
        """ Point class for representing and manipulating x,y coordinates. """
        
        def __init__(self, initX, initY):
 
            self.x = initX
            self.y = initY
    
    p = Point(7,6)



Now when we create new points, we supply the x and y coordinates as parameters.  When the point is created, the values of ``initX`` and ``initY`` are assigned to the state of the object.


.. image:: Figures/objectpic5.png
   :alt: Simple object has state and methods



       
Adding Other Methods to our Class
---------------------------------
          
The key advantage of using a class like ``Point`` rather than something like a simple
tuple ``(7, 6)`` now becomes apparent.  We can add methods to
the ``Point`` class that are sensible operations for points.  Had we chosen to use a simple
tuple to represent the point, we would not have this capability.
Creating a class like ``Point`` brings an exceptional
amount of "organizational power" to our programs, and to our thinking. 
We can group together the sensible operations, and the kinds of data 
they apply to, and each instance of the class can have its own state.       
          
A **method** behaves like a function but it is invoked on a specific
instance.  For example, with a list bound to variable L, ``L.append(7)`` calls the function append, with the list itself as the first parameter and 7 as the second parameter.   Methods are accessed using dot notation. This is why ``L.append(7)`` has 2 parameters even though you may think it only has one: the list stored in the variable ``L`` is the first.  

Let's add two simple methods to allow a point to give us information about its state.  The ``getX`` method, when invoked, will return the value of the x coordinate.

The implementation of this method is straight forward since we already know how
to write functions that return values.  One thing to notice is that even though the ``getX`` method does not need any other parameter information to do its work, there is still one formal parameter, ``self``.  As we stated earlier, all methods defined in a class that operate on objects of that class will have ``self`` as their first parameter.  Again, this serves as reference to the object itself which in turn gives access to the state data inside the object.

.. activecode:: chp13_classes4
    
    class Point:
        """ Point class for representing and manipulating x,y coordinates. """
        
        def __init__(self, initX, initY):
 
            self.x = initX
            self.y = initY

        def getX(self):
            return self.x

        def getY(self):
            return self.y

    
    p = Point(7,6)
    print(p.getX())
    print(p.getY())

Note that the ``getX`` method simply returns the value of ``self.x`` from the object itself.  In other words, the implementation of the method is to go to the state of the object itself and get the value of ``x``.  Likewise, the ``getY`` method looks almost the same.

Let's add another method, ``distanceFromOrigin``, to see better how methods
work.  This method will again not need any additional information to do its work.
It will perform a more complex task.


.. activecode:: chp13_classes5
    
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

    
    p = Point(7,6)
    print(p.distanceFromOrigin())


Notice that the call of ``distanceFromOrigin`` does not *explicitly* 
supply an argument to match the ``self`` parameter.  This is true of all method calls. The definition will always seem to
have one additional parameter as compared to the invocation.  

    
Objects as Arguments and Parameters
-----------------------------------

You can pass an object as a argument, in the usual way.

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

We *could have* made distance be a method of the Point class. Then, we would have called the first parameter self, and would have invoked it using the dot notation, as in the following code. Which way to implement it is a matter of coding style. Both work correctly. Most programmers choose whether to make functions be stand-alone or methods of a class based on whether the function semantically seems to be an operation that is performed on instances of the class. In this case, because distance is really a property of a pair of points and is symmetric (the distance from a to b is the same as that from b to a) it makes more sense to have it be a standalone function and not a method. Many heated discussions have occurred between programmers about such style decisions.

.. activecode:: chp13_classes6a

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

        def distance(self, point2):
            xdiff = point2.getX()-self.getX()
            ydiff = point2.getY()-self.getY()

            dist = math.sqrt(xdiff**2 + ydiff**2)
            return dist
    
    p = Point(4,3)
    q = Point(0,0)
    print(p.distance(q))


Converting an Object to a String
--------------------------------

 
When we're working with classes and objects, it is often necessary to print an object (that is to print the state of an object).
Consider the example below.

.. activecode:: chp13_classesstr1
    
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

    
    p = Point(7,6)
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

    p = Point(7,6)
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

Instances as Return Values
--------------------------

Functions and methods can return objects.  This is actually nothing new since everything in Python is an object and we have
been returning values for quite some time. (You can also have lists or tuples of object instances, etc.)  The difference here is that we want to have the method create an object using
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
       

The resulting Point, ``mid``, has an x value of 4 and a y value of 8.  We can also use any other methods on ``mid`` since it is a
``Point`` object.

    

Glossary
--------

.. glossary::


    attribute
        One of the named data items that makes up an instance.

    class
        A user-defined compound type. A class can also be thought of as a
        template for the objects that are instances of it.
        
    constructor
        Every class has a "factory", called by the same name as the class, for
        making new instances.  If the class has an *initializer method*, this method
        is used to get the attributes (i.e. the state) of the new object properly set up. 
            
    initializer method
        A special method in Python (called ``__init__``) 
        that is invoked automatically to set a newly created object's
        attributes to their initial (factory-default) state.
        
    instance
        An object whose type is of some class.  Instance and object are used
        interchangeably.
        
    instantiate
        To create an instance of a class, and to run its initializer. 
        
    method
        A function that is defined inside a class definition and is invoked on
        instances of that class. 

    object
        A compound data type that is often used to model a thing or concept in
        the real world.  It bundles together the data and the operations that 
        are relevant for that kind of data.  Instance and object are used
        interchangeably.

    object-oriented programming
        A powerful style of programming in which data and the operations 
        that manipulate it are organized into classes and methods.        

    object-oriented language
        A language that provides features, such as user-defined classes and
        inheritance, that facilitate object-oriented programming.



Exercises
---------

#. Add a method ``reflect_x`` to Point which returns a new Point, one which is the 
   reflection of the point about the x-axis.  For example, 
   ``Point(3, 5).reflect_x()`` is (3, -5)
   
   .. activecode:: ch_cl_02


#.

    .. tabbed:: q2

        .. tab:: Question

           Add a method called ``move`` that will take two parameters, call them ``dx`` and ``dy``.  The method will
           cause the point to move in the x and y direction the number of units given. (Hint: you will change the values of the
           state of the point)
           

        .. tab:: Answer
            
            .. activecode:: ch_cl_05_answer
            
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
                    
                    def move(self, dx, dy):
                        self.x = self.x + dx
                        self.y = self.y + dy
                        
                    def __str__(self):
                        return str(self.x)+","+str(self.y)


                p = Point(7,6)
                print(p)
                p.move(5,10)
                print(p)
 