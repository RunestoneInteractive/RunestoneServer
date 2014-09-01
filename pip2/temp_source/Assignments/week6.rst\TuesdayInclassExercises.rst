..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Tuesday In-class Exercises
--------------------------

Call greet so that it prints out::
 
    Hello Jackie
    Hello Nick

.. tabbed:: q1

    .. tab:: Question

        .. actex:: session_10_1
        
            def greet(x, y = ["Jackie", "Nick"], z = 1):
                for nm in y:
                    for i in range(z):
                        print (x + " " + nm)

    .. tab:: Answer
        
        .. actex:: session_10_1a

            def greet(x, y = ["Jackie", "Nick"], z = 1):
                for nm in y:
                    for i in range(z):
                        print (x + " " + nm)

            greet("Hello")
            
Call greet so that it prints out::
 
    Hello Prof. Resnick
    Hello Prof. Resnick
    Hello Prof. Resnick

.. tabbed:: q2

    .. tab:: Question
    
        .. actex:: session_10_2
    
            def greet(x, y = ["Jackie", "Nick"], z = 1):
                for nm in y:
                    for i in range(z):
                        print (x + " " + nm)

    .. tab:: Answer
    
        .. actex:: session_10_2a

            def greet(x, y = ["Jackie", "Nick"], z = 1):
                for nm in y:
                    for i in range(z):
                        print (x + " " + nm)

            greet("Hello", ["Prof. Resnick"], 3)

Define the function `t` so that it multiples its two arguments, but has default
values such that it produces the outputs specified

.. tabbed:: q3

    .. tab:: Question
    
        .. actex:: session_10_3
         
            t()
            #prints 1
            
            t(2)
            #prints 2
            
            t(2, 3)
            #prints 6

    .. tab:: Answer
    
        .. actex:: session_10_3a

            def t(x=1, y=1):
                return x*y
                
            print t()
            #prints 1
            
            print t(2)
            #prints 2
            
            print t(2, 3)
            #prints 6

                
Expand the definition of the function print_d so that it produces the following
outputs::

    #alphabetic order
    Jackie, 100
    Lara, 150
    Nick, 42
    
    # reverse order
    Nick, 42
    Lara, 150
    Jackie, 100
    
    # sorted by values
    Nick, 42
    Jackie, 100
    Lara, 150

.. tabbed:: q4

    .. tab:: Question
    
        .. actex:: session_10_4
        
            # change the definition of print_d
            def print_d(d):
                pairs = d.items()
                for (k, v) in pairs:
                    print(k + ", " + str(v))
            
            d = {"Nick" : 42, "Jackie": 100, "Lara": 150}        
        
            #alhabetic order
            print_d(d)
            
            # reverse order
            print_d(d, True)
            
            # sorted by values
            print_d(d, False, True)
        
    .. tab:: Answer
        
        .. actex:: session_10_4a
        
            # change the definition of print_d
            def print_d(d, reverse=False, by_value=False):
                pairs = d.items()
                if by_value:
                    if reverse:
                        s = sorted(pairs, None, lambda x: x[1], True)
                    else:
                        s = sorted(pairs, None, lambda x: x[1])
                    # we should have just been able to pass reverse as the
                    # fourth parameter to sorted, but there seems to be a 
                    # bug that when we pass False it still sorts in reverse
                    # order
                else:
                    if reverse:
                        s = sorted(pairs, None, lambda x: x[0], True)
                    else:
                        s = sorted(pairs, None, lambda x: x[0])
                
                for (k, v) in s:
                    print(k + ", " + str(v))
                
            d = {"Nick" : 42, "Jackie": 100, "Lara": 150}
        
            #alhabetic order
            print_d(d)
            
            # reverse order
            print_d(d, True)
            
            # sorted by values
            print_d(d, False, True)
            


Define a function filtered_count that takes a list as its first parameter and
a function as its second parameter. The function passed as the second value should be a boolean function that
takes a single parameter and returns True or False.

.. tabbed:: q5

    .. tab:: Question
    
        .. actex:: session_10_5
    
            def filtered_count(...
    

    .. tab:: Answer
    
        .. actex:: session_10_5a

            def filtered_count(L, f):
                
                count = 0
                
                for x in L:
                    if f(x):
                        count = count + 1 
                
                return count


            print(filtered_count([4, 2, 0, 5, 6, 5], lambda x: x > 3))
            # Should return 4, the count of items in the list that are bigger than 3
    
    
.. _session_11:

