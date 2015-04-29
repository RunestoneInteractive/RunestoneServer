..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. qnum::
   :prefix: list-21-
   :start: 1

Functions that Produce Lists
----------------------------

The pure version of ``doubleStuff`` above made use of an 
important **pattern** for your toolbox. Whenever you need to
write a function that creates and returns a list, the pattern is
usually::

    initialize a result variable to be an empty list
    loop
       create a new element 
       append it to result
    return the result

Let us show another use of this pattern.  Assume you already have a function
``is_prime(x)`` that can test if x is prime.  Now, write a function
to return a list of all prime numbers less than n::

   def primes_upto(n):
       """ Return a list of all prime numbers less than n. """
       result = []
       for i in range(2, n):
           if is_prime(i):
               result.append(i)
       return result


