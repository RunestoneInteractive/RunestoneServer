..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Unpacking Dictionary Items
--------------------------

A dictionary consists of key-value pairs. When you call the items() method on 
a dictionary, you get back a list of key-value pairs. Each of those pairs is a
two-item tuple. (More generally, we refer to any two-item tuple as a **pair**).
You can iterate the key-value pairs.

.. activecode:: cp_09_tuple5

    d = {"k1": 3, "k2": 7, "k3": "some other value"}
    
    for p in d.items():
        print p[0]
        print p[1]
        print '*** LOOP ***'
        
Each time line 4 is executed, p will refer to one key-value pair from d. A pair is just
a tuple, so p[0] refers to the key and p[1] refers to the value.

That code is easier to read if we unpacked to the key-value pairs into 
two variable names.

.. activecode:: cp_09_tuple6

    d = {"k1": 3, "k2": 7, "k3": "some other value"}
    
    for (k, v) in d.items():
        print k
        print v
        print '*** LOOP ***'

More generally, if you have a list of tuples that each has more than two items, and you iterate through
them with a for loop pulling out information from the tuples, the code will be far more readable if you unpack them
into separate variable names.
