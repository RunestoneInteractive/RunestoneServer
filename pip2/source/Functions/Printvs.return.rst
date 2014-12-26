..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Print vs. return
----------------

Many beginning programmers find the distinction between print and return very
confusing, especially since most of the illustrations of return values in intro
texts like this one show the returned value from a function call by printing it, as
in ``print square(g(2))``.

The print statement is fairly easy to understand. It takes a python object and 
outputs a printed representation of it in the output window. You can think of
the print statement as something that takes an object from the land of the program
and makes it visible to the land of the human observer.

.. note::

   **Print is for people**. Remember that slogan. Printing has no effect on the ongoing execution of a program. It doesn't assign a value to a variable. It doesn't return a value from a function call.

If you're confused, chances are it not's really about the print statement but
about returned values and the evaluation of complex expressions. A function that
returns a value is producing a value for use *by the program*, in particular for
use in the part of the code where the function was invoked. Remember that when a function
is invoked, control passes to the function, meaning that the function's code block
is executed. But when the function returns, control goes back to the calling location,
and a return value may come back with it.

If a returned value is for use *by the program*, what is it used for? There are
three possibilities.

#. Save it for later. 
    The returned value may be:
    
    * Assigned to a variable. For example, `w = square(3)`
    * Put in a list. For example, `L.append(square(3))`
    * Put in a dictionary. For example, `d[3] = square(3)`

#. Use it in a more complex expression. 
    In that case, think of the return value as 
    replacing the entire text of the function invocation. For example, if there is a line
    of code ``w = square(square(3) + 7) - 5``, think of the return value 9 replacing the
    text square(3) in that invocation, so it becomes `square(9 + 7) -5`.

#. Print it for human consumption. 
    For example, `print square(3)` outputs 9 to the
    output area. Note that, unless the return value is first  saved as in possibility 1, it will be available
    only to the humans watching the output area, not to the program as it continues executing.

If your only purpose in running a function is to make an output visible for human consumption,
there are two ways to do it. You can put one or more print statements inside the
function definition and not bother to return anything from the function (the value None will be returned). 
In that case, invoke the function without a print statement. For example, you can have an entire line of code
that reads ``f(3)``. That will run the function f and throw away the return value. Of course,
if square doesn't print anything out or have any side effects, it's useless to call it and do 
nothting with the return value. But with a function that has print statements inside it, 
it can be quite useful.

The other possibility is to return a value from the function and print it, as in ``print f(3)``. As 
you start to write larger, more complex programs, this will be more typical. Indeed the print statement
will usually only be a temporary measure while you're developing the program. Eventually, you'll end
up calling f and saving the return value or using it as part of a more complex expression.

You will know you've really internalized the idea of functions when you are
no longer confused about the difference between print and return. Keep working at it
until it makes sense to you!

**Check your understanding**

.. mchoicemf:: test_questionfunctions_4_1
   :answer_a: 2
   :answer_b: 5
   :answer_c: 7
   :answer_d: 25
   :answer_e: Error: y has a value but x is an unbound variable inside the square function
   :correct: c
   :feedback_a: 2 is the input; the value returned from h is what will be printed
   :feedback_b: Don't forget that 2 gets squared.
   :feedback_c: First square 2, then add 3.
   :feedback_d: 3 is added to the result of squaring 2
   :feedback_e: When square is called, x is bound to the parameter value that is passed in, 2.
   
   What will the following code output?
   
   .. code-block:: python 

       def square(x):
           return x*x
           
       def g(y):
           return y + 3
           
       def h(y):
           return square(y) + 3
           
       print h(2)


.. mchoicemf:: test_questionfunctions_4_2
   :answer_a: 2
   :answer_b: 5
   :answer_c: 7
   :answer_d: 10
   :answer_e: Error: you can't nest function calls
   :correct: d
   :feedback_a: Better read the section above one more time.
   :feedback_b: Better read the section above one more time.
   :feedback_c: That's h(2), but it is passed to g.
   :feedback_d: h(2) returns 7, so y is bound to 7 when g is invoked 
   :feedback_e: Ah, but you can next function calls.
   
   What will the following code output?
   
   .. code-block:: python 

       def square(x):
           return x*x
           
       def g(y):
           return y + 3
           
       def h(y):
           return square(y) + 3
           
       print g(h(2))

