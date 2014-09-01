..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

List Length
-----------

As with strings, the function ``len`` returns the length of a list (the number
of items in the list).  However, since lists can have items which are themselves sequences (e.g., strings), 
it important to note that ``len`` only returns the top-most length.

.. activecode:: chp09_01a

    alist =  ["hello", 2.0, 5]
    print(len(alist))
    print(len(alist[0]))

Note that ``alist[0]`` is the string ``"hello"``, which has length 5. 

**Check your understanding**

.. mchoicemf:: test_question9_2_1 
   :answer_a: 4
   :answer_b: 5
   :correct: b
   :feedback_a: len returns the actual number of items in the list, not the maximum index value.
   :feedback_b: Yes, there are 5 items in this list.

   What is printed by the following statements?
   
   .. code-block:: python

     alist = [3, 67, "cat", 3.14, False]
     print(len(alist))
   
