..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Flow of Execution Summary
-------------------------

When you are working with functions it is really important to know the order
in which statements are executed. This is called the **flow of
execution** and we've already talked about it a number of times in this
chapter.

Execution always begins at the first statement of the program.  Statements are
executed one at a time, in order, from top to bottom.
Function definitions do not alter the flow of execution of the program, but
remember that statements inside the function are not executed until the
function is called.
Function calls are like a detour in the flow of execution. Instead of going to
the next statement, the flow jumps to the first line of the called function,
executes all the statements there, and then comes back to pick up where it left
off.

That sounds simple enough, until you remember that one function can call
another. While in the middle of one function, the program might have to execute
the statements in another function. But while executing that new function, the
program might have to execute yet another function!

Fortunately, Python is adept at keeping track of where it is, so each time a
function completes, the program picks up where it left off in the function that
called it. When it gets to the end of the program, it terminates.

What's the moral of this sordid tale? When you read a program, don't read from
top to bottom. Instead, follow the flow of execution.  This means that you will read the def statements as you
are scanning from top to bottom, but you should skip the body of the function
until you reach a point where that function is called.


.. index::
    single: parameter
    single: function; parameter
    single: argument
    single: function; argument
    single: import statement
    single: statement; import
    single: composition
    single: function; composition


.. index:: bar chart


**Check your understanding**

.. mchoicemf:: test_question5_6_1
   :answer_a: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
   :answer_b: 1, 2, 3, 5, 6, 7, 9, 10, 11
   :answer_c: 9, 10, 11, 1, 2, 3, 5, 6, 7
   :answer_d: 9, 10, 5, 6, 7, 1, 2, 3, 11
   :answer_e: 1, 5, 9, 10, 6, 2, 3, 7, 11
   :correct: e
   :feedback_a: Although Python typically processes lines in order from top to bottom, function definitions and calls are an exception to this rule.
   :feedback_b: Although Python typically processes lines in order from top to bottom, function definitions and calls are an exception to this rule.  Although this order skips blank lines, it still lists the lines of code in order.
   :feedback_c: This is close, in that Python will not execute the functions until after they are called, but there are two problems here.  First, Python does not know which lines are function definitions until it processes them, so it must at least process the function headers before skipping over the functions. Section, notice that line 10 involves a function call.  Python must execute the function square before moving on to line 11.
   :feedback_d: This is close, in that Python will not execute the functions until after they are called, but there is one problem here.  Python does not know which lines are function definitions until it processes them, so it must at least process the function headers before skipping over the functions.
   :feedback_e: Python starts at line 1, notices that it is a function definition and skips over all of the lines in the function definition until it finds a line that it no longer included in the function (line 5).  It then notices line 5 is also a function definition and again skips over the function body to line 9.  On line 10 it notices it has a function to execute, so it goes back and executes the body of that function.  Notice that that function includes another function call.  Finally, it will return to line 11 after the function square is complete.

   Consider the following Python code. Note that line numbers are included on the left.

   .. code-block:: python
      :linenos:

      def pow(b, p):
          y = b ** p
          return y
     
      def square(x):
          a = pow(x, 2)
          return a
     
      n = 5
      result = square(n)
      print(result)

   Which of the following best reflects the order in which these lines of code are processed in Python?

.. mchoicemf:: test_question5_6_2
   :answer_a: 25
   :answer_b: 5
   :answer_c: 125
   :answer_d: 32
   :correct: a
   :feedback_a: The function square returns the square of its input (via a call to pow)
   :feedback_b: What is printed is the output of the square function.  5 is the input to the square function.
   :feedback_c: Notice that pow is called from within square with a base (b) of 5 and a power (p) of two.
   :feedback_d: Notice that pow is called from within square with a base (b) of 5 and a power (p) of two.

   Consider the following Python code. Note that line numbers are included on the left.

   .. code-block:: python
      :linenos:

      def pow(b, p):
          y = b ** p
          return y
     
      def square(x):
          a = pow(x, 2)
          return a
     
      n = 5
      result = square(n)
      print(result)

   What does this function print?

