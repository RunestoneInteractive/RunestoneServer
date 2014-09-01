..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Boolean Functions
-----------------

Functions can return boolean values, which is often convenient for hiding
complicated tests inside functions. For example:

.. activecode:: ch06_boolfun1
    
    def isDivisible(x, y):
        if x % y == 0:
            return True 
        else:
            return False 

    print(isDivisible(10,5))

The name of this function is ``isDivisible``. It is common to give **boolean
functions** names that sound like yes/no questions.  ``isDivisible`` returns
either ``True`` or ``False`` to indicate whether the ``x`` is or is not
divisible by ``y``.

We can make the function more concise by taking advantage of the fact that the
condition of the ``if`` statement is itself a boolean expression. We can return
it directly, avoiding the ``if`` statement altogether:

.. sourcecode:: python
    
    def isDivisible(x, y):
        return x % y == 0


Boolean functions are often used in conditional statements:

.. sourcecode:: python
    
    if isDivisible(x, y):
        ... # do something ...
    else:
        ... # do something else ...

It might be tempting to write something like:

.. sourcecode:: python
    
    if isDivisible(x, y) == True:


but the extra comparison is unnecessary.

.. activecode:: ch06_boolfun2
    
    def isDivisible(x, y):
        if x % y == 0:
            return True 
        else:
            return False 

    if isDivisible(10,5):
        print("That works")
    else:
        print("Those values are no good")


Try a few other pairs of values to see the results.

.. index:: style

