..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Check
-----

To check your understanding or your predictions, you will run a program. 

To check your understanding about the state of variables before your code snippet runs, add diagnostic print statements that print out the types and values of variables. Add these print statements just *before* the code snippet you are trying to understand.

If you made a prediction about the output that will be generated when the code snippet runs, then you can just run the program. If, however, you made a prediction about a change that occurs in the value of a variable, you will need to add an extra diagnostic print statement right after the line of code that you think should be changing that variable. 

The diagnostic print statements are temporary.  Once you have verified that a program is doing what you think it’s doing, you will remove these extra print statements.

If you get any surprises, then you will want to revise your understanding or your predictions. If you were wrong about the values or types of variables before the code snippet was run, you may to revisit your understanding of the previous code. 

If you were wrong about the effect of an operation, you may need to revisit your understanding of that operation. One good way to do that is to run that operation on some very simple values. For example, if you thought ``x.append([4, 5])`` appended x as the second element of the list that already contains 4 and 5, you might want to try it on even simpler values, like ``x.append(4)`` in order to realize that the item in parentheses in the one being appended, not the list one being appended to.

