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

#.  Repeat the above exercise but this time print 10 random numbers between
    25 and 35.

    .. actex:: ex_mod_2
