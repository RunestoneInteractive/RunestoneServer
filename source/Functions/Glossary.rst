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


    chatterbox function
        A function which interacts with the user (using ``input`` or ``print``) when
        it should not. Silent functions that just convert their input arguments into
        their output results are usually the most useful ones.
        
    composition (of functions)
        Calling one function from within the body of another, or using the
        return value of one function as an argument to the call of another.

    dead code
        Part of a program that can never be executed, often because it appears
        after a ``return`` statement.

    fruitful function
        A function that yields a return value instead of ``None``.

    incremental development
        A program development plan intended to simplify debugging by adding and
        testing only a small amount of code at a time.

    None
        A special Python value. One use in Python is that it is returned 
        by functions that do not execute a return statement with a return argument. 

    return value
        The value provided as the result of a function call.

    scaffolding
        Code that is used during program development to assist with development
        and debugging. The unit test code that we added in this chapter are
        examples of scaffolding.
        
    temporary variable
        A variable used to store an intermediate value in a complex
        calculation.
       



