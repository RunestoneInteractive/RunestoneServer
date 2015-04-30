..  Copyright (C)  Paul Resnick.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. qnum::
   :prefix: exceptions-
   :start: 1

.. _exceptions_chap:

Raising and Catching Errors
---------------------------

.. index:: try, except, Exception

The try/except control structure provides a way to process a run-time error and continue on with program execution. Until now, any run-time error, such asking for the 8th item in a list with only 3 items, or dividing by 0, has caused the program execution to stop. In the browser ActiveCode windows, you get an error message in a box below. When you are executing python programs from the command-line, you also get an error message saying something about what went wrong and what line it occurred on. After the run-time error is encountered, the python interpreter does not try to execute the rest of the code. You have to make some change in your code and rerun the whole program.

With try/except, you tell the python interpreter:

* Try to execute a block of code, the "try" clause.
   * If the whole block of code executes without any run-time errors, just carry on with the rest of the program after the try/except statement.

* If a run-time error does occur during execution of the block of code:
   * skip the rest of that block of code (but don't exit the whole program)
   * execute a block of code in the "except" clause
   * then carry on with the rest of the program after the try/except statement

.. sourcecode:: python

   try:
      <try clause code block>
   except <ErrorType>:
      <exception handler code block>

The syntax is fairly straightforward. The only tricky part is that after the word except, there can optionally be a specification of the kinds of errors that will be handled. The catchall is the class Exception. If you write ``except Exception:`` all runtime errors will be handled. If you specify a more restricted class of errors, only those errors will be handled; any other kind of error will still cause the program to stop running and an error message to be printed.

The code below causes an error of type IndexError, by trying to access the third element of a two-element list.

.. activecode:: exceptions_1
   :nocanvas:

   items = ['a', 'b']
   third = items[2]
   
   
The code below causes an error of type ZeroDivisionError, or less specifically ArithmeticError.

.. activecode:: exceptions_2
   :nocanvas:

   x = 5
   y = x/0

Let's see what happens if we wrap some of this problematic code in a try/except statement. Note that ``this won't print`` doesn't print: when the error is encountered, the rest of the try block is skipped and the exception block is executed. When the except block is done, it continues on with the nex line of code that's outdented to the same level as the try: ``continuing`` is printed.

.. activecode:: exceptions_3
   :nocanvas:
   
   try:
       items = ['a', 'b']
       third = items[2]
       print "This won't print"
   except Exception:
       print "got an error"
   
   print "continuing"

 
If we catch only IndexEror, and we actually have a divide by zero error, the program does stop executing.   
   
.. activecode:: exceptions_4
   :nocanvas:
   
   try:
       items = ['a', 'b']
       third = items[2]
       print "This won't print"
   except IndexError:
       print "error 1"
      
   print "continuing"
   
   try:
       x = 5
       y = x/0
       print "This won't print, either"
   except IndexError:
       print "error 2"
       
       
   print "continuing again"
   
   
There's one other useful feature. The exception code can access a variable that contains information about exactly what the error was. Thus, for example, in the except clause you could print out the information that would normally be printed as an error message but continue on with execution of the rest of the program. To do that, you specify a variable name after the exception class that's being handled. The exception clause code can refer to that variable name.

.. activecode:: exceptions_5
   :nocanvas:
   
   try:
       items = ['a', 'b']
       third = items[2]
       print "This won't print"
   except Exception, e:
       print "got an error"
       print e
   
   print "continuing"


**Check your understanding**

.. mchoicemf:: exceptions_1
   :answer_a: syntax
   :answer_b: run-time
   :answer_c: semantic
   :correct: b
   :feedback_a: Syntax errors are things like missing colons or strings that are not terminated. Try/except will not help with those. The program still will not run.
   :feedback_b: Run-time errors like index out of bounds can be caught and handled gracefully with try/except.
   :feedback_c: If your program runs to completion but does the wrong thing, try/except won't help you.
   
   Which type of error can be noticed and handled using try/except?
   
.. mchoicemf:: exceptions_2
   :answer_a: True
   :answer_b: False
   :correct: a
   :feedback_a: If your code is only catching IndexError errors, then the exception will not be handled, and execution will terminate.
   :feedback_b: If your code is only catching IndexError errors, then the exception will not be handled, and execution will terminate.

   When a run-time exception of type ZeroDivisionError occurs, and you have a statement ``except IndexError``, the program will stop executing completely.

.. mchoicemf:: exceptions_3
   :answer_a: True
   :answer_b: False
   :correct: b
   :feedback_a: The rest of the code after the whole try/except statement will execute, but not the rest of the code in the try block.
   :feedback_b: The rest of the code after the whole try/except statement will execute, but not the rest of the code in the try block.

   After a run-time exception is handled by an except clause, the rest of the code in the try clause will be executed.


.. mchoicemf:: exceptions_4
   :answer_a: 0
   :answer_b: 1
   :answer_c: 3
   :answer_d: 4
   :answer_e: 5  
   :correct: d
   :feedback_a: Try i = 0; that should print out .3333
   :feedback_b: Keep trying.
   :feedback_c: When i=3, it will no longer be able to pring 1.0/ (3-i), but it will still print one more line in the except clause
   :feedback_d: It will print the fraction for three values of i, and then one error message
   :feedback_e: When i=3, it will get a run-time error, and execution stops after that.

   How many lines will print out when the following code is executed?
   
   .. sourcecode:: python
   
      try:
          for i in range(5):
              print 1.0 / (3-i)
      except Exception, error_inst:
          print "Got an error", error_inst


