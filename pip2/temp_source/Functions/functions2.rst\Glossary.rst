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

    local variable
        A variable defined inside a function. A local variable can only be used
        inside its function.  Parameters of a function are also a special kind
        of local variable.
        
    global variable
        A variable defined at the top level, not inside any function.

    lifetime
        Variables and objects have lifetimes --- they are created at some point during
        program execution, and will be destroyed at some time. In python, objects
        live as long as there is some variable pointing to it, or it is part of some 
        other compound object, like a list or a dictionary. In python, local variables
        live only until the function finishes execution.

    method
        A special kind of function that is invoked on objects of particular types of
        objects, using the syntax ``<expr>.<methodname>(<additional parameter values>)``
   
    flow of execution
        The order in which statements are executed during a program run.

    function composition
        Using the output from one function call as the input to another.

    stack frame
        A frame that keeps track of the values of local variables during a function execution,
        and where to return control when the function execution completes.
      
    calling stack
        A sequence (stack) of frames, showing all the function calls that are in process
        but not yet complete. When one function's code invokes another function call,
        there will be more than one frame on the stack. 
   
    side effect
