..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Glossary
--------


.. glossary::

    argument
        A value provided to a function when the function is called. This value
        is assigned to the corresponding parameter in the function.  The argument
        can be the result of an expression which may involve operators,
        operands and calls to other fruitful functions.

    body
        The second part of a compound statement. The body consists of a
        sequence of statements all indented the same amount from the beginning
        of the header.  The standard amount of indentation used within the
        Python community is 4 spaces.

    compound statement
        A statement that consists of two parts:

        #. header - which begins with a keyword determining the statement
           type, and ends with a colon.
        #. body - containing one or more statements indented the same amount
           from the header.

        The syntax of a compound statement looks like this:

        .. code-block:: python

            keyword expression:
                statement
                statement 
                ...

    docstring
        If the first thing in a function body is a string (or, we'll see later, in other situations
        too) that is attached to the function as its ``__doc__`` attribute.

    flow of execution
        The order in which statements are executed during a program run.

    function
        A named sequence of statements that performs some useful operation.
        Functions may or may not take parameters and may or may not produce a
        result.

    function call
        A statement that executes a function. It consists of the name of the
        function followed by a list of arguments enclosed in parentheses.

    function definition
        A statement that creates a new function, specifying its name,
        parameters, and the statements it executes.

    fruitful function
        A function that returns a value when it is called.

    header line
        The first part of a compound statement. A header line begins with a keyword and
        ends with a colon (:)

    parameter
        A name used inside a function to refer to the value which was passed
        to it as an argument.
   
