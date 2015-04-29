..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. _formatting_chap:

More on Formatting Output
=========================

In python 2.7, print is a special statement, not a function call. The general form of its syntax is ``print <expr> [, <expr>]*``. The square brackets indicates that it's optional to have additional expressions. The * means that you can have 0 or more of them. If <expr> evaluates to a single value, then the printed representation of that value is output. 

If there are several expressions, then the printed representation of each one is output, with spaces separating them.

If there is a trailing comma, then a space is output at the end rather than a newline.

.. activecode: printing_0
   :nocanvas:
   
   print 1
   print 2, 3
   print 4,
   print 5,
   print 6 

If there is just one expression and it is in parentheses, it has the same effect as not including the parentheses.

If there are multiple values, separated by commas, enclosed in parentheses, it is treated as a single tuple. For example, 
``print (3, 5)`` outputs the printed representation, which is ``(3, 5)``.

.. _interpolation_chap:


