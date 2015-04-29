..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Cloning Lists
-------------

If we want to modify a list and also keep a copy of the original, we need to be
able to make a copy of the list itself, not just the reference. This process is
sometimes called **cloning**, to avoid the ambiguity of the word copy.

The easiest way to clone a list is to use the slice operator.

Taking any slice of ``a`` creates a new list. In this case the slice happens to
consist of the whole list.

.. codelens:: chp09_is4
    :showoutput:
    
    a = [81,82,83]

    b = a[:]       # make a clone using slice
    print a == b
    print a is b

    b[0] = 5

    print a
    print b

Now we are free to make changes to ``b`` without worrying about ``a``.  Again, we can clearly see in codelens that ``a`` and ``b`` are entirely different list objects.



**Check your understanding**

.. mchoicemf:: test_question9_12_1
   :answer_a: [4,2,8,999,5,4,2,8,6,5]
   :answer_b: [4,2,8,999,5]
   :answer_c: [4,2,8,6,5]
   :correct: c
   :feedback_a: print alist not print blist
   :feedback_b: blist is changed, not alist.
   :feedback_c: Yes, alist was unchanged by the assignment statement. blist was a copy of the references in alist.
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [4,2,8,6,5]
     blist = alist * 2
     blist[3] = 999
     print alist


.. index:: list; append
