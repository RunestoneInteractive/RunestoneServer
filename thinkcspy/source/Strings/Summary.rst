..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Summary 
------- 

This chapter introduced a lot of new ideas.  The following summary 
may prove helpful in remembering what you learned.

.. glossary::

    indexing (``[]``)
        Access a single character in a string using its position (starting from
        0).  Example: ``'This'[2]`` evaluates to ``'i'``.

    length function (``len``)
        Returns the number of characters in a string.  Example:
        ``len('happy')`` evaluates to ``5``.

    for loop traversal (``for``)
        *Traversing* a string means accessing each character in the string, one
        at a time.  For example, the following for loop:

        .. sourcecode:: python

            for ix in 'Example':
                ...

        executes the body of the loop 7 times with different values of `ix` each time.

    slicing (``[:]``)
        A *slice* is a substring of a string. Example: ``'bananas and
        cream'[3:6]`` evaluates to ``ana`` (so does ``'bananas and
        cream'[1:4]``).

    string comparison (``>, <, >=, <=, ==, !=``)
        The six common comparision operators work with strings, evaluating according to
        `lexigraphical order
        <http://en.wikipedia.org/wiki/Lexicographic_order>`__.  Examples:
        ``'apple' < 'banana'`` evaluates to ``True``.  ``'Zeta' < 'Appricot'``
        evaluates to ``False``.  ``'Zebra' <= 'aardvark'`` evaluates to
        ``True`` because all upper case letters precede lower case letters.

    in and not in operator (``in``, ``not in``)
        The ``in`` operator tests whether one string is contained
        inside another string.  Examples: ``'heck' in "I'll be checking for
        you."`` evaluates to ``True``.  ``'cheese' in "I'll be checking for
        you."`` evaluates to ``False``.


