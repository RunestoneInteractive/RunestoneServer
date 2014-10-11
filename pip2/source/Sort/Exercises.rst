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

You're going to write a function that takes a string as a parameter and returns a list of the five
most frequent characters in the string. Eventually, you will be able to do this sort of problem without a lot of coaching. But we're going to step you through it as a series of exercises.

First, the function will count the frequencies of all the characters,
as we've done before, using a dictionary and the accumulator pattern. Then, it will sort the (key, value) pairs. Finally, it will take a slice of the sorted list to get just the top five. That slice will be returned.

Step 1. Suppose you had this list, [8, 7, 6, 6, 4, 4, 3, 1, 0], already sorted, how would you make a list of just the best 5? (Hint: take a slice).

.. tabbed:: q6

    .. tab:: Question
   

        .. actex:: session_11_1
            
            L = [8, 7, 6, 6, 4, 4, 3, 1, 0]
    
    .. tab:: Answer
    
        .. actex:: session_11_1a
        
             L = [8, 7, 6, 6, 4, 4, 3, 1, 0]
             L[:5]
            

Now suppose the list wasn't sorted yet. How would get those same five elements from this list?

.. tabbed:: q7

    .. tab:: Question

        .. actex:: session_11_2

            L = [0, 1, 6, 7, 3, 6, 8, 4, 4]
            
    .. tab:: Answer
 
         .. actex:: session_11_2a

            L = [0, 1, 6, 7, 3, 6, 8, 4, 4]
            L2 = sorted(L, reverse=True)
            L2[:5]
    
        
    
Now take a list L and make a dictionary of counts for how often these numbers appear in the list.

.. tabbed:: q8

    .. tab:: Question

        .. actex:: session_11_3
    
            L = [0, 1, 6, 7, 3, 6, 8, 4, 4, 6, 1, 6, 6, 5, 4, 4, 3, 35, 4, 11]
        

    .. tab:: Answer
    
        .. actex:: session_11_3a

            L = [0, 1, 6, 7, 3, 6, 8, 4, 4, 6, 1, 6, 6, 5, 4, 4, 3, 35, 4, 11]
            d = {}
            for x in L:
                if x in d:
                    d[x] = d[x] + 1
                else:
                    d[x] = 1
            
            
Now sort the keys (numbers) based on their frequencies. Review
:ref:`Sorting a Dictionary <sort_dictionaries>` if you're not sure how to do this. Keep just the top five keys

.. tabbed:: q9

    .. tab:: Question
    
        .. actex:: session_11_4

            L = [0, 1, 6, 7, 3, 6, 8, 4, 4, 6, 1, 6, 6, 5, 4, 4, 3, 35, 4, 11]
    
    .. tab:: Answer
    
        .. actex:: session_11_4a
        
            L = [0, 1, 6, 7, 3, 6, 8, 4, 4, 6, 1, 6, 6, 5, 4, 4, 3, 35, 4, 11]
        
            d = {}
            for x in L:
                if x in d:
                    d[x] = d[x] + 1
                else:
                    d[x] = 1

            s = sorted(d, key = lambda x: d[x], reverse=True)
            
            print s[:5]
            

Finally, generalize what you've done. Write a function that takes a string instead of a list as a parameter and returns a list of the five
most frequent characters in the string.

.. tabbed:: q10

    .. tab:: Question

        .. actex:: session_11_5

    .. tab:: Answer
    
        .. actex:: session_11_5a
        
            def five_most_frequent(s):
                d = {}
                for x in s:
                    if x in d:
                        d[x] = d[x] + 1
                    else:
                        d[x] = 1
                
                s = sorted(d, key = lambda x: d[x], reverse=True)
            
                return s[:5]
                
            import test
            test.testEqual(five_most_frequent("aaaaaabbbbbccccdefggghijkk"), ['a', 'b', 'c', 'g', 'k'])                
    
