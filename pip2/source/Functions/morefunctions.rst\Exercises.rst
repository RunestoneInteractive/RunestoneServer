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


#. Write a function ``to_secs`` that converts hours, minutes and seconds to 
   a total number of seconds.  
       
#. Extend ``to_secs`` so that it can cope with real values as inputs.  It
   should always return an integer number of seconds (truncated towards zero):

       
#. Write three functions that are the "inverses" of ``to_secs``:
   
   #. ``hours_in`` returns the whole integer number of hours
      represented by a total number of seconds.
      
   #. ``minutes_in`` returns the whole integer number of left over minutes
      in a total number of seconds, once the hours
      have been taken out.
      
   #. ``seconds_in`` returns the left over seconds
      represented by a total number of seconds.
      
   You may assume that the total number of seconds passed to these functions is an integer.
       
       
#. Write a ``compare`` function that returns ``1`` if ``a > b``, ``0`` if
   ``a == b``, and ``-1`` if ``a < b``.


#. Write a function called ``hypotenuse`` that
   returns the length of the hypotenuse of a right triangle given the lengths
   of the two legs as parameters.
    

 
#. Write a function ``slope(x1, y1, x2, y2)`` that returns the slope of
   the line through the points (x1, y1) and (x2, y2).

   Then use a call to ``slope`` in a new function named
   ``intercept(x1, y1, x2, y2)`` that returns the y-intercept of the line
   through the points ``(x1, y1)`` and ``(x2, y2)``.


 

#. Write the function ``f2c(t)`` designed to return the
   degrees Celsius for given temperature in
   Fahrenheit.
    


#. Now do the opposite: write the function ``c2f`` which converts Celcius to Fahrenheit.

