..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

A function that accumulates
---------------------------

We have used the ``len`` function a lot already. If it weren't part of python,
our lives as programmers would have been a lot harder.

Well, actually, not that much harder. Now that we know how to define functions, we could define
``len`` ourselves if it did not exist. Previously, we have used the accumlator to
pattern to count the number of lines in a file. Let's use that same idea and 
just wrap it in a function definition. We'll call it ``mylen`` to distinguish it
from the real ``len`` which already exists. We actually *could* call it len, but
that wouldn't be a very good idea, because it would replace the original len function,
and our implementation may not be a very good one.

.. activecode:: functions_6

   def mylen(x):
      c = 0 # initialize count variable to 0
      for y in x:
         c = c + 1   # increment the counter for each item in x
      return c
      
   print(mylen("hello"))
   print(mylen([1, 2, 7])) 






.. note::

   This workspace is provided for your convenience.  You can use this activecode window to try out anything you like.

   .. activecode:: scratch_05_06

