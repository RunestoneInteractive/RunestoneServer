..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Functions can call other functions
----------------------------------

It is important to understand that each of the functions we write can be used
and called from other functions we write.  This is one of the most important
ways that computer scientists take a large problem and break it down into a
group of smaller problems. This process of breaking a problem into smaller
subproblems is called **functional decomposition**.

Here's a simple example of functional decomposition using two functions. The
first function called ``square`` simply computes the square of a given number.
The second function called ``sum_of_squares`` makes use of square to compute
the sum of three numbers that have been squared.

.. codelens:: functions2_6

    def square(x):
        y = x * x
        return y

    def sum_of_squares(x,y,z):
        a = square(x)
        b = square(y)
        c = square(z)

        return a+b+c

    a = -5
    b = 2
    c = 10
    result = sum_of_squares(a,b,c)
    print(result)


Even though this is a pretty simple idea, in practice this example
illustrates many very important Python concepts, including local and global
variables along with parameter passing.  Note that the body of ``square`` is not 
executed until it is called from inside the ``sum_of_squares``
function for the first time on line 6.  

Also notice that when ``square`` is
called (at Step 8, for example), there are two groups of local variables, one for ``square`` and one
for ``sum_of_squares``.  Each group of local variables is called a **stack
frame**. The variables ``x``, and ``y`` 
are local variables in both functions. These are completely differenet variables, even 
though they have the same name. Each function invocation creates a new frame, and
variables are looked up in that frame. Notice that at step 9, y has the value 25 is one frame
and 2 in the other.  

What happens you to refer to variable y on line 3? Python looks up the value of y
in the stack frame for the ``square`` function. If it didn't find it there, it
would go look in the global frame.  

.. index:: flow of execution


