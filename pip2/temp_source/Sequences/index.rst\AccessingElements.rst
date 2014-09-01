..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Accessing Elements
------------------

The syntax for accessing the elements of a list is the same as the syntax for
accessing the characters of a string.  We use the index operator ( ``[]`` -- not to
be confused with an empty list). The expression inside the brackets specifies
the index. Remember that the indices start at 0.  Any integer expression can be used
as an index and as with strings, negative index values will locate items from the right instead
of from the left.

Try to predict what will be printed out by the following code, and then run it to check your
prediction. (Actually, it's a good idea to always do that with the code examples. You 
will learn much more if you force yourself to make a prediction before you see the output.)

.. activecode:: chp09_02
    
    numbers = [17, 123, 87, 34, 66, 8398, 44]
    print(numbers[2])
    print(numbers[9-8])
    print(numbers[-2])
    print(numbers[len(numbers)-1])
    
