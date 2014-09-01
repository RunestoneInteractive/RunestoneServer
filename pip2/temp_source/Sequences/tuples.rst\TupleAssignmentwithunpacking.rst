..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Tuple Assignment with unpacking
-------------------------------

Python has a very powerful **tuple assignment** feature that allows a tuple of variable names 
on the left of an assignment to be assigned values from a tuple
on the right of the assignment. Another ay to think of this is that the tuple of values
is **unpacked** into the variable names.

.. sourcecode:: python

    (name, surname, birth_year, movie, movie_year, profession, birth_place) = julia

This does the equivalent of seven assignment statements, all on one easy line.  
One requirement is that the number of variables on the left must match the number
of elements in the tuple. 

Once in a while, it is useful to swap the values of two variables.  With
conventional assignment statements, we have to use a temporary variable. For
example, to swap ``a`` and ``b``:

.. sourcecode:: python

    temp = a
    a = b
    b = temp

Tuple assignment solves this problem neatly:

.. sourcecode:: python

    (a, b) = (b, a)

The left side is a tuple of variables; the right side is a tuple of values.
Each value is assigned to its respective variable. All the expressions on the
right side are evaluated before any of the assignments. This feature makes
tuple assignment quite versatile.

Naturally, the number of variables on the left and the number of values on the
right have to be the same.

.. sourcecode:: python

    >>> (a, b, c, d) = (1, 2, 3)
    ValueError: need more than 3 values to unpack 

Python even provides a way to pass a single tuple to a function and have it be
unpacked for assignment to the named parameters. 

.. activecode:: cp09_tuple4

    def add(x, y):
        return x + y
        
    print(add(3, 4))
    z = (5, 4)
    print(add(*z)) # this line will cause the values to be unpacked
    print(add(z)) # this line causes an error

If you run this, you will be get an error caused by line 7, where it says that
the function add is expecting two parameters, but you're only passing one parameter
(a tuple). In line 6 you'll see that the tuple is unpacked and 5 is bound to x, 4 to y. 

Don't worry about mastering this idea yet. But later in the course, if you come
across some code that someone else has written that uses the * notation inside
a parameter list, come back and look at this again.

.. mchoicema:: test_questiontuples_2
   :answer_a: Make the last two lines of the function be "return x" and "return y"  
   :answer_b: Include the statement "return [x, y]" 
   :answer_c: Include the statement "return (x, y)"
   :answer_d: Include the statement "return x, y"
   :answer_e: It's not possible to return two values; make two functions that each compute one value.
   :correct: b,c,d
   :feedback_a: As soon as the first return statement is executed, the function exits, so the second one will never be executed; only x will be returned
   :feedback_b: return [x,y] is not the preferred method because it returns x and y in a list and you would have to manually unpack the values. But it is workable.
   :feedback_c: return (x, y) returns a tuple.
   :feedback_d: return x, y causes the two values to be packed into a tuple.
   :feedback_e: It is possible, and frequently useful, to have one function compute multiple values.

   If you want a function to return two values, contained in variables x and y, which of the following methods will work?

.. mchoicemf:: test_questiontuples_3
   :answer_a: You can't use different variable names on the left and right side of an assignment statement.
   :answer_b: At the end, x still has it's original value instead of y's original value.
   :answer_c: Actually, it works just fine!
   :correct: b
   :feedback_a: Sure you can; you can use any variable on the right-hand side that already has a value.
   :feedback_b: Once you assign x's value to y, y's original value is gone
   :feedback_c: Once you assign x's value to y, y's original value is gone

   Consider the following alternative way to swap the values of variables x and y. What's wrong with it?
   
   .. code-block:: python 
        
        # assume x and y already have values assigned to them
        y = x
        x = y   

