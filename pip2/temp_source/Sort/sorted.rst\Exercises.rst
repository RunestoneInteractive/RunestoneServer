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

1. Write a function that takes a string as a parameter and returns a list of the five
most frequent characters in the string. [Hint: count the frequencies of all the characters,
as we've done before, using a dictionary and the accumulator pattern. Then sort the (key, value) pairs.
Finally, take a slice of the sorted list to get just the top five.]

.. activecode:: sorted_ex_01
    
