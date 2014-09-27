..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

The main() function
-------------------

By convention, programmers often define a bunch of functions, including one called main, and
then just have a single statement at top-level, an invocation of the function main(). Inside main,
code invokes other functions.

One of the benefits of wrapping your top-level code in a main() function is that 
it ensures that there will be no global variables. Any values that you want your
functions to have access to they will get through parameter passing. There is
no danger of accidentally accessing a global variable.

There is nothing special about the name 'main', as far as python is concerned. But
other programmers will know, when they see a function called 'main', that it 
will be called at top-level, and its job is to call other functions. If you look
through a large file containing many function definitions, and one of them is
called main, the bottom of the file will probably be a single invocation of main().
You can start understanding the whole program by looking at the code block inside the
main() function.

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

