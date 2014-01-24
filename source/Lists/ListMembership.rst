..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

List Membership
---------------

``in`` and ``not in`` are boolean operators that test membership in a sequence. We
used them previously with strings and they also work here.

.. activecode:: chp09_4
    
    fruit = ["apple","orange","banana","cherry"]

    print("apple" in fruit)
    print("pear" in fruit)

**Check your understanding**

.. mchoicemf:: test_question9_4_1
   :answer_a: True
   :answer_b: False
   :correct: a
   :feedback_a: Yes, 3.14 is an item in the list alist.
   :feedback_b: There are 7 items in the list, 3.14 is one of them. 
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [3, 67, "cat", [56, 57, "dog"], [ ], 3.14, False]
     print(3.14 in alist)


.. mchoicemf:: test_question9_4_2
   :answer_a: True
   :answer_b: False
   :correct: b
   :feedback_a: in returns True for top level items only.  57 is in a sublist.
   :feedback_b: Yes, 57 is not a top level item in alist.  It is in a sublist.
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [3, 67, "cat", [56, 57, "dog"], [ ], 3.14, False]
     print(57 in alist)



