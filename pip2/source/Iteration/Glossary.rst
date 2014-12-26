..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Glossary
========

.. glossary::

    for loop traversal (``for``)
        *Traversing* a string or a list means accessing each character in the string or item in the list, one
        at a time.  For example, the following for loop:

        .. sourcecode:: python

            for ix in 'Example':
                ...

        executes the body of the loop 7 times with different values of `ix` each time.
        
    range
        A function that produces a list of numbers. For example, `range(5)`, produces a list of five 
        numbers, starting with 0, `[0, 1, 2, 3, 4]`. 

    pattern
        A sequence of statements, or a style of coding something that has
        general applicability in a number of different situations.  Part of
        becoming a mature programmer is to learn and establish the
        patterns and algorithms that form your toolkit.   

    index
        A variable or value used to select a member of an ordered collection, such as
        a character from a string, or an element from a list.

    traverse
        To iterate through the elements of a collection, performing a similar
        operation on each.

    accumulator pattern
         A pattern where the program initializes an accumulator variable and then changes it
         during each iteration, accumulating a final result.

