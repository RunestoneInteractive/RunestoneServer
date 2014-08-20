..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Nested Lists
------------

A nested list is a list that appears as an element in another list. In this
list, the element with index 3 is a nested list.  
If we print(``nested[3]``), we get ``[10, 20]``. To extract an element from the
nested list, we can proceed in two steps.  First, extract the nested list, then extract the item
of interest.  It is also possible to combine those steps using bracket operators that evaluate from
left to right.

.. activecode:: chp09_nest
    
    nested = ["hello", 2.0, 5, [10, 20]]
    innerlist = nested[3]
    print(innerlist)
    item = innerlist[1]
    print(item)

    print(nested[3][1])


.. index:: matrix

**Check your understanding**

.. mchoicemf:: test_question9_21_1
   :answer_a: 6
   :answer_b: 8
   :answer_c: 888
   :answer_d: 999
   :correct: c
   :feedback_a: 6 is in the wrong list.  alist[1] refers to the second item in alist, namely [888,999].
   :feedback_b: 8 is in the wrong list.  alist[1] refers to the second item in alist, namely [888,999].
   :feedback_c: Yes, alist[0][1][0] is True and alist[1] is the second list, the first item is 888.
   :feedback_d: alist[0][1][0] is True.  Take another look at the if statement.
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [ [4, [True, False], 6, 8], [888, 999] ]
     if alist[0][1][0]:
        print(alist[1][0])
     else:
        print(alist[1][1])


.. index:: strings and lists, split, join

