..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Function Calls
--------------

Python can compute new values with function calls. You are familiar with the idea of functions from high school algebra. There you might define a function ``f`` by specifying how it transforms an input into an output, ``f(x) = 3x + 2``. Then, you might write ``f(5)`` and expect to get the value 17.

Python adopts a similar syntax for invoking functions. If there is a named function ``foo`` that takes a single input, we can invoke foo on the value 5 by writing ``foo(5)``.

There are many built-in functions available in python. You'll be seeing some in this chapter and the next couple of chapterse. 

It is also possible for programmers to define new functions in their programs. You will learn how to do that later in the course. For now, you just need to learn how to invoke, or call, a function, and understand that the execution of the function returns a computed value.

.. activecode:: functionCalls_1
   :nocanvas:
   :hidecode:
   
   def square(x):
      return x * x
      
   def sub(x, y):
      return x - y

We've defined two functions above. The code is hidden so as not to bother you (yet) with how functions are defined. `square`` takes a single input parameter, and returns that input multiplied by itself. ``sub`` takes two input parameters and returns the result of subtracting the second from the first. Obviously, these functions are not particularly useful, since we have the operators ``*`` and ``-`` available. But they illustrate how functions work.

.. activecode:: functionCalls_2
   :include: functionCalls_1
   :nocanvas:
   
   
   print square(3)
   square(5)
   print sub(6, 4)
   print sub(5, 9)


Notice that when a function takes more than one input parameter, the inputs are separated by a comma. Also notice that the order of the inputs matters. The value before the comma is treated as the first input, the value after it as the second input.

Again, remember that when python performs computations, the results are only show in the output window if there's a print statement that says to do that.

Remember the note that some kinds of python objects don't have a nice printed representation? Functions are themselves just objects. If you tell python to print the function object, rather than printing the results of invoking the function object, you'll get one of those not-so-nice printed representations. Just stating the name of the function refers to the function. The name of the function followed by parentheses ``()`` invokes the function.

.. activecode:: functionCalls_3
   :include: functionCalls_1
   :nocanvas:
   
   
   print square
   print sub

.. mchoicemf:: exercise_functionCalls_1
      :answer_a: sub(5, 8)
      :answer_b: -3
      :answer_c: 3
      :answer_d: nothing will rpint
      :correct: b
      :feedback_a: The result of executing the function call will print out
      :feedback_b: The second is subtracted from the first
      :feedback_c: The second is subtracted from the first
      :feedback_d: The print statement makes the results print

      What will the output be from this code?
       
      .. code-block:: python
       
         print sub(5, 8)
         
.. mchoicemf:: exercise_functionCalls_2
      :answer_a: sub(5, 8)
      :answer_b: -3
      :answer_c: 3
      :answer_d: nothing will rpint
      :correct: a
      :feedback_a: The character sting is treated as a literal and printed out, without executing
      :feedback_b: The character sting is treated as a literal and printed out, without executing
      :feedback_c: The character sting is treated as a literal and printed out, without executing
      :feedback_d: The character sting is treated as a literal and printed out, without executing

      What will the output be from this code?
       
      .. code-block:: python
       
         print "sub(5, 8)"
         
.. mchoicemf:: exercise_functionCalls_3
      :answer_a: sub(5, 8)
      :answer_b: -3
      :answer_c: 3
      :answer_d: nothing will rpint
      :correct: d
      :feedback_a: There is no print statement
      :feedback_b: There is no print statement
      :feedback_c: There is no print statement
      :feedback_d: There is no print statement

      What will the output be from this code?
       
      .. code-block:: python
       
         sub(5, 8)
         
.. mchoicemf:: exercise_functionCalls_4
      :answer_a: sub(5, 8)
      :answer_b: -3
      :answer_c: 3
      :answer_d: nothing will rpint
      :correct: d
      :feedback_a: There is no print statement
      :feedback_b: There is no print statement
      :feedback_c: There is no print statement
      :feedback_d: There is no print statement

      What will the output be from this code?
       
      .. code-block:: python
       
         "sub(5, 8)"