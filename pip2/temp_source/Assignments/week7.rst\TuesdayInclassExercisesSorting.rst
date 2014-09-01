..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Tuesday In-class Exercises: Sorting
-----------------------------------


.. tabbed:: q1

    .. tab:: Question
   
        Sort this list in descending order by value
        
        .. actex:: session_12_1
            
            L = [0, 1, 6, 7, 3, 6, 8, 4, 4]
    
    .. tab:: Answer
        
        .. hidden
        
            .. actex:: session_12_1a
            
                 L = [8, 7, 6, 6, 4, 4, 3, 1, 0]
                 sorted(L, None, True)

.. tabbed:: q2

    .. tab:: Question
   
        Sort this list in descending order by absolute value
        
        .. actex:: session_12_2
            
            L = [0, -1, -6, 7, 3, 6, 8, 4, 4]
    
    .. tab:: Answer
        
        .. hidden
        
            .. actex:: session_12_2a
            
                 L = [8, 7, 6, 6, 4, 4, 3, 1, 0]
                 sorted(L, lambda x: abs(x), True)

.. tabbed:: q3

    .. tab:: Question
   
        Sort the top-level list in ascending order by the number of items in the sublists.
        
        .. actex:: session_12_3
            
            L = [[1, 2, 3], [4], [5, 6], [7, 8, 9, 10]]
    
    .. tab:: Answer
        
        .. hidden
        
            .. actex:: session_12_3a
            
                L = [[1, 2, 3], [4], [5, 6], [7, 8, 9, 10]]
                sorted(L, None, lambda x: len(x), True)

.. tabbed:: q4

    .. tab:: Question
   
        Sort the top-level list in ascending order by the value of the first item in each sublist.
        
        .. actex:: session_12_4
            
            L = [[5, 2, 3], [4], [9, 6], [1, 8, 9, 10]]
    
    .. tab:: Answer
        
        .. hidden
        
            .. actex:: session_12_4a
            
                L = [[5, 2, 3], [4], [9, 6], [1, 8, 9, 10]]
                sorted(L, None, lambda x: x[1], True)
                
.. tabbed:: q5

    .. tab:: Question
   
        Write a function that takes a dictionary as input and returns a list
        of its keys, sorted based on their associated values.
        
        .. actex:: session_12_5
            
     
    .. tab:: Answer
        
        .. hidden
        
            .. actex:: session_12_5a
            
                def keys_sorted_by_value(d):
                    in_order = sorted(d.items(), None, lambda x: x[1], True)
                    res = []
                    for (k, v) in in_order:
                        res.append(k)
                    return res
                    
                


