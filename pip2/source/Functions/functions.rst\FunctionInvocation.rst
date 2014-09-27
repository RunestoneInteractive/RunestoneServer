..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Function Invocation
-------------------
   
Defining a new function does not make the function run. If you just run the code above, nothing will print!
To execute the function, we need a **function call**.  This is also known as a **function invocation**.

The way to invoke a function is to refer to it by name, followed by parentheses. Since there are no parameters for
the function hello, we won't need to put anything inside the parentheses when we call it. Once we've defined a function, we can call it as often as we like and its
statements will be executed each time we call it.  

.. codelens:: functions_2

   def hello():
      print("Hello")
      print("Glad to meet you")
   
   print(type(hello))
   print(type("hello"))
      
   hello()
   print("Hey, that just printed two lines with one line of code!")
   hello()  # do it again, just because we can...

Let's take a closer look at what happens when you define a function and when
you execute the function. Try stepping through the code above.

First, note that in Step 1, when it executes line 1, it does *not* execute lines 2 and 3.
Instead, as you can see in blue "Global variables" area, it creates a variable named hello whose
value is a python function object. In the diagram that object is labeled hello() with a notation above
it that it is a function.

At Step 2, the next line of code to execute is line 5. Just to emphasize that 
hello is a variable like any other, and that functions are python objects like any other, 
just of a particular type, line 5 prints out the type of the object referred to
by the variable hello. It's type is officially 'function'.

Line 6 is just there to remind you of the difference between referring to the
variable name (function name) hello and referring to the string "hello".

At Step 4 we get to line 8, which has an invocation of the function. The way function
invocation works is that the code block inside the function definition is executed
in the usual way, but at the end, execution jumps to the point after the function
invocation. 

You can see that by following the next few steps. At Step 5, the red arrow has moved to line
2, which will execute next. We say that *control has passed* from the top-level program
to the function hello. After Steps 5 and 6 print out two lines, at Step 7, control will
be passed back to the point after where the invocation was started. At Step 8, that has 
happened.

The same process of invocation occurs again on line 10, with lines 2 and 3 getting 
executed a second time.


**Check your understanding**

.. mchoicemf:: test_questionfunctions_1_1
   :answer_a: A named sequence of statements.
   :answer_b: Any sequence of statements.
   :answer_c: A mathematical expression that calculates a value.
   :answer_d: A statement of the form x = 5 + 4.
   :correct: a
   :feedback_a: Yes, a function is a named sequence of statements.
   :feedback_b: While functions contain sequences of statements, not all sequences of statements are considered functions.
   :feedback_c: While some functions do calculate values, the python idea of a function is slightly different from the mathematical idea of a function in that not all functions calculate values.  Consider, for example, the turtle functions in this section.   They made the turtle draw a specific shape, rather than calculating a value.
   :feedback_d: This statement is called an assignment statement.  It assigns the value on the right (9), to the name on the left (x).

   What is a function in Python?


.. mchoicemf:: test_questionfunctions_1_2
   :answer_a: To improve the speed of execution
   :answer_b: To help the programmer organize programs into chunks that match how they think about the solution to the problem.
   :answer_c: All Python programs must be written using functions
   :answer_d: To calculate values.
   :correct: b
   :feedback_a: Functions have little effect on how fast the program runs.
   :feedback_b: While functions are not required, they help the programmer better think about the solution by organizing pieces of the solution into logical chunks that can be reused.
   :feedback_c: In the first several chapters, you have seen many examples of Python programs written without the use of functions.  While writing and using functions is desirable and essential for good programming style as your programs get longer, it is not required.
   :feedback_d: Not all functions calculate values.

   What is one main purpose of a function?


.. mchoicemf:: test_questionfunctions_1_2a
   :answer_a: 0
   :answer_b: 1
   :answer_c: 2
   :correct: a
   :feedback_a: The code only defines the function. Nothing prints until the function is called.
   :feedback_b: Check again.
   :feedback_c: When the function is invoked, it will print two lines, but it has only been defined, not invoked.

   How many lines will be output by executing this code?
   
   .. code-block:: python

      def hello():
         print("Hello")
         print("Glad to meet you")


.. mchoicemf:: test_questionfunctions_1_2b
   :answer_a: 0
   :answer_b: 1
   :answer_c: 3
   :answer_d: 4
   :answer_e: 7
   :correct: e
   :feedback_a: Here the the function is invoked and there is also a separate print statement.
   :feedback_b: There is only one print statement outside the funciton, but the invocations of hello also cause lines to print.
   :feedback_c: There are three print statements, but the function is invoked more than once.
   :feedback_d: Each time the function is invoked, it will print two lines, not one.
   :feedback_e: Three invocations generate two lines each, plus the line "It works"

   How many lines will be output by executing this code?

   .. code-block:: python

      def hello():
         print("Hello")
         print("Glad to meet you")
         
      hello()
      print("It works")
      hello()
      hello()

         
