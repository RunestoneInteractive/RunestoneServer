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

    calling stack
        A sequence (stack) of frames, showing all the function calls that are in process
        but not yet complete. When one function's code invokes another function call,
        there will be more than one frame on the stack. 

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

    function composition
        Using the output from one function call as the input to another.

    function definition
        A statement that creates a new function, specifying its name,
        parameters, and the statements it executes.

    fruitful function
        A function that returns a value when it is called.

    global variable
        A variable defined at the top level, not inside any function.

    header line
        The first part of a compound statement. A header line begins with a keyword and
        ends with a colon (:)

    lifetime
        Variables and objects have lifetimes --- they are created at some point during
        program execution, and will be destroyed at some time. In python, objects
        live as long as there is some variable pointing to it, or it is part of some 
        other compound object, like a list or a dictionary. In python, local variables
        live only until the function finishes execution.

    local variable
        A variable defined inside a function. A local variable can only be used
        inside its function.  Parameters of a function are also a special kind
        of local variable.

    method
        A special kind of function that is invoked on objects of particular types of
        objects, using the syntax ``<expr>.<methodname>(<additional parameter values>)``

    parameter
        A name used inside a function to refer to the value which was passed
        to it as an argument.
   
    side effect
        Some lasting effect of a function call, other than its return value. Side effects include print statements, changes to mutable objects, and changes to the values of global variables.

    stack frame
        A frame that keeps track of the values of local variables during a function execution,
        and where to return control when the function execution completes.
   