..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Thursday In-class Exercises
---------------------------

If you had trouble with the exercise at the bottom of the sorting chapter, I've broken
it up into several steps here. 

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
            L2 = sorted(L, None, None, True)
            L2[:5]
    
        
    
Now make a dictionary of counts for how often these numbers appear in the lists.

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
            
            
Now sort the (number, count) pairs and keep just the top five pairs. Review
:ref:`Sorting a Dictionary <sort_dictionaries>` if you're not sure how to do this.

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

            s = sorted(d.items(), None, lambda x: x[1], True)
            
            print(s[:5])
            

Finally, generalize what you've done. Write a function that takes a string as a parameter and returns a list of the five
most frequent characters in the string. If you're amibitious write a few test cases for it, using import test and then test.testEqual.

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
                
                s = sorted(d.items(), None, lambda x: x[1], True)
                res = []
                for (k, v) in s[:5]:
                    res.append(k)
                return res
                
            import test
            test.testEqual(five_most_frequent("aaaaaabbbbbccccdefggghijkk"), ['a', 'b', 'c', 'g', 'k'])                
             
.. _functions_review_5:

