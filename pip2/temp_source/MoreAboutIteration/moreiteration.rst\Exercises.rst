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

           Add a print statement to Newton's ``sqrt`` function that
           prints out ``better`` each time it is calculated. Call your modified
           function with 25 as an argument and record the results.
        
           .. actex:: ex_7_7
        
                def newtonSqrt(n):
                    approx = 0.5 * n
                    better = 0.5 * (approx + n/approx)
                    while  better !=  approx:
                        approx = better
                        better = 0.5 * (approx + n/approx)
                    return approx


                print ("Final approx:", newtonSqrt(25))

        .. tab:: Answer
            
            .. activecode:: q1_answer

                def newtonSqrt(n):
                    approx = 0.5 * n
                    better = 0.5 * (approx + n/approx)
                    while  better !=  approx:
                        approx = better
                        better = 0.5 * (approx + n/approx)
                        print (" Approx:", better)
                    return approx


                print ("Final approx:", newtonSqrt(25))


#.

    .. tabbed:: q2

        .. tab:: Question

           A note above suggests that when testing whether two floating point
           numbers are equal, it's better to check if they are almost equal, because
           of rounding errors in the representation of floating point numbers internally
           in computers. 
           
           Rewrite  Newton's ``sqrt`` function to take an extra parameter, the tolerance,
           and have the iteration stop when better and approx are almost equal, the difference
           being no greater than the tolerance. Try invoking it with a tolerance of .01, .0001, and .000001.
        
           .. actex:: ex_7_7a
        
                def newtonSqrt(n):
                    approx = 0.5 * n
                    better = 0.5 * (approx + n/approx)
                    while  better !=  approx:
                        approx = better
                        better = 0.5 * (approx + n/approx)
                        print (" Approx:", better)
                    return approx


        .. tab:: Answer
            
            .. activecode:: q2_answer

                def newtonSqrt(n, tolerance = .01):
                    approx = 0.5 * n
                    better = 0.5 * (approx + n/approx)
                    while  abs(better - approx) > tolerance:
                        approx = better
                        better = 0.5 * (approx + n/approx)
                    return approx
                
                for x in [.01,.0001, .0000001]:
                    y = newtonSqrt(10, x)
                    print (newtonSqrt(10, x), y*y)
