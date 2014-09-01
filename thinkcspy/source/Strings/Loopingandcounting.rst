..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. qnum::
   :prefix: strings-14-
   :start: 1

Looping and Counting
--------------------

We will finish this chapter with a few more examples that show variations on the theme of iteration through the characters of a string.  We will implement a few of the methods that we described earlier to show how they can be done.


The following program counts the number of times a particular letter, ``aChar``, appears in a
string.  It is another example of the accumulator pattern that we have seen in previous chapters.

.. activecode:: chp08_fun2

    def count(text, aChar): 
        lettercount = 0
        for c in text:
            if c == aChar:
                lettercount = lettercount + 1
        return lettercount

    print(count("banana","a"))    

The function ``count`` takes a string as its parameter.  The ``for`` statement iterates through each character in
the string and checks to see if the character is equal to the value of ``aChar``.  If so, the counting variable, ``lettercount``, is incremented by one.
When all characters have been processed, the ``lettercount`` is returned.

.. index:: traversal, eureka traversal, pattern of computation,
           computation pattern

