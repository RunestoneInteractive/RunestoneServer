..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Explain (Make a reference diagram)
----------------------------------

To understand what a snippet of code (one or more lines) does, you should first form a hypothesis about the *state* of the program just before your snippet executes.

It’s a good idea to make a reference diagram by hand, the kind of diagram that CodeLens produces for you. In particular, for each of the variable names that are referred to in the code snippet you are trying to understand, you should make a prediction about:

   * the type of that variable’s value (integer, string, list, dictionary, etc.)   
   * the value of that variable

You should also be able to state, in English, what each of the operations in your code snippet does. For example, if your code snippet includes a line ``x.append(4)``, then you should be able to say, “The append operation takes a list, x in this case, and appends an item, 4 in this case, to the end of the list. It changes the actual list, so any other variable that is an alias for the list will also have its value changed.”

