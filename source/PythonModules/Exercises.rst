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

#.  .. tabbed:: q1

        .. tab:: Question

           Use a ``for`` statement to print 10 random numbers.
        

        .. tab:: Answer
            
            .. activecode:: mod_q1_answer
            
               import random
            
               howmany = 10
               for counter in range(howmany):
                  arandom = random.random()
                  print(arandom)

        .. tab:: Discussion

            .. disqus::
                :shortname: interactivepython
                :identifier: mods_111


#.  Repeat the above exercise but this time print 10 random numbers between 25 and 35.

    .. actex:: ex_mod_2

#.  .. tabbed:: q3

        .. tab:: Question

           The **Pythagorean Theorem** tells us that the length of the hypotenuse of a right triangle is related to the lengths of the other two sides.  Look through the ``math`` module and see if you can find a function that will compute this relationship for you.  Once you find it, write a short program to try it out.
        

        .. tab:: Answer
            
            .. activecode:: mod_q3_answer
            
               import math
            
               side1 = 3
               side2 = 4
               hypotenuse = math.hypot(side1,side2)
               print(hypotenuse)

        .. tab:: Discussion

            .. disqus::
                :shortname: interactivepython
                :identifier: mods_333

#.  Search on the internet for a way to calculate an approximation for **pi**.  There are many that use simple arithmetic.  Write a program to compute the approximation and then print that value as well as the value of ``math.pi`` from the math module.

    .. actex:: ex_mod_4
    
