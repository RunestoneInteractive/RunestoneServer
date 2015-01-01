..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Beginning tips for Debugging
----------------------------

Debugging a program is a different way of thinking than writing a program.  The process of debugging is much more like being a detective.  Here are a few rules to get you thinking about debugging.

#. Everyone is a suspect (Except Python)!  Its common for beginner programmers to blame Python, but that should be your last resort.  Remember that Python has been used to solve CS1 level problems millions of times by millions of other programmers.  So, Python is probably not the problem.

#. Find clues.  This is the biggest job of the detective and right now there are two important kinds of clues for you to understand.
    * Error Messages
    * Print Statements

There are also more advanced ways to debug a program. For example, later in the course you will learn about a module called pdb. It lets you set breakpoints in your code. Execution stops at each breakpoint and you can then inspect the value of variables and continue the execution. It's a faster way to understand what's going wrong than using print statements alone.  
