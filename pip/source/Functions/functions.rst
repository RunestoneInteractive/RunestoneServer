..  Copyright (C)  Paul Rensick, Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

..  shortname:: IntroToFunctions
..  description:: This is the introduction to the idea of defining and calling a function.

.. qnum::
   :prefix: func-
   :start: 1
   

Functions
=========

.. index::
    single: function
    single: function definition
    single: definition; function


Functions Definitions
---------------------

.. video:: function_intro
   :controls:
   :thumb: ../_static/function_intro.png

   http://media.interactivepython.org/thinkcsVideos/FunctionsIntro.mov
   http://media.interactivepython.org/thinkcsVideos/FunctionsIntro.webm

In Python, a **function** is a chunk of code that performs some operation that
is meaningful for a person to think about as a whole unit. Once a function has
been defined and you are satisfied that it does what it is supposed to do, 
you will start thinking about it in terms of the larger operation that it performs
rather than the specific lines of code that make it work. 

In this chapter you will learn about *named* functions, functions that can be
referred to by name when you want to execute them. 

The syntax for creating a named function, a **function definition**, is:

.. code-block:: python

    def name( parameters ):
        statements

You can make up any names you want for the functions you create, except that
you can't use a name that is a Python keyword, and the names must follow the rules
for legal identifiers that were given previously. The parameters specify
what information, if any, you have to provide in order to use the new function.  Another way to say this is that the parameters specify what the function needs to do it's work.

There can be any number of statements inside the function, but they have to be
indented from the ``def``. 
In the examples in this book, we will use the
standard indentation of four spaces. Function definitions are the third of
several **compound statements** we will see, all of which have the same
pattern:

#. A header line which begins with a keyword and ends with a colon.
#. A **body** consisting of one or more Python statements, each
   indented the same amount -- *4 spaces is the Python standard* -- from
   the header line.

We've already seen the ``for`` statement which follows this pattern and the ``if``, ``elif``, and ``else`` statements that do so as well.

In a function definition, the keyword in the header is ``def``, which is
followed by the name of the function and some *parameter names* enclosed in
parentheses. The parameter list may be empty, or it may contain any number of
parameters separated from one another by commas. In either case, the parentheses are required.

We will come back to the parameters in a little while, but first let's see what
happens when a function is executed, using a function without any parameters
to illustrate.

Here's the definition of a simple function, hello.

.. activecode:: functions_1

   def hello():
      """This function says hello and greets you"""
      print("Hello")
      print("Glad to meet you")

.. admonition::  docstrings

    If the first thing after the function header is a string (some tools insist that
    it must be a triple-quoted string), it is called a **docstring**
    and gets special treatment in Python and in some of the programming tools.

    Another way to retrieve this information is to use the interactive
    interpreter, and enter the expression ``<function_name>.__doc__``, which will retrieve the
    docstring for the function.  So the string you write as documentation at the start of a function is
    retrievable by python tools *at runtime*.  This is different from comments in your code,
    which are completely eliminated when the program is parsed.

    By convention, Python programmers use docstrings for the key documentation of
    their functions.



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

         
Function Parameters
-------------------

Named functions are nice because, once they are defined and we understand what they do,
we can refer to them by name and not think too much about what they do.
With parameters, functions are even more powerful, because they can do pretty
much the same thing on each invocation, but not exactly the same thing. The
parameters can cause them to do something a little different. 

The figure below shows this relationship.  A function needs certain information to do its work.  These values, often called **arguments** or **actual parameters** or **parameter values**, are passed to the function by the user.

.. image:: Figures/blackboxproc.png

This type of diagram is often called a **black-box diagram** because it only states the requirements from the perspective of the user (well, the programmer, but the programmer who uses the function, who may be different than the programmer who created the function).  
The user must know the name of the function and what arguments need to be passed.  The details of how the function works are hidden inside the "black-box".

You have already been making function invocations with parameters. For example,
when you write ``len("abc")`` or ``len([3, 9, "hello"])``, len is the name of
a function, and the value that you put inside the parentheses, the string "abc" 
or the list [3, 9, "hello"], is a parameter value.

When a function has one or more parameters, the names of the parameters appear
in the function definition, and the values to assign to those parameters appear
inside the parentheses of the function invocation. Let's look at each of those
a little more carefully.

In the definition, the parameter list is sometimes referred to 
as the **formal parameters** or **parameter names**.  These names can be any valid
variable name. If there is more than one, they are separated by commas. 

In the function invocation, inside the parentheses one value should be provided
for each of the parameter names. These values are separated by commas. The
values can be specified either directly, or by any python expression including a
reference to some other variable name.

That can get kind of confusing, so let's start by looking at a function with just
one parameter. The revised hello function personalizes the greeting: the person
to greet is specified by the parameter. 

.. codelens:: functions_3

   def hello2(s):
      print("Hello " + s)
      print("Glad to meet you")
         
   hello2("Nick")
   hello2("Jackie")

First, notice that hello2 has one formal parameter, s. You can tell that because
there is exactly one variable name inside the parentheses on line 1.

Next, notice what happened during Step 2. Control was passed to the function, just like
we saw before. But in addition, the variable s was bound to a value, the
string "Nick". When it got to Step 7, for the second invocation of the function, s
was bound to "Jackie".

Function invocations always work that way. The expression inside the parentheses
on the line that invokes the function is evaluated before control is passed to
the function. The value is assigned to the corresponding formal parameter. Then, when
the code block inside the function is executing, it can refer to that formal 
parameter and get its value, the value that was 'passed into' the function.

To get a feel for that, let's invoke hello2 using some more complicated expressions. 
Try some of your own, too.

.. activecode:: functions_4

   def hello2(s):
      print("Hello " + s)
      print("Glad to meet you")
         
   hello2("Nick" + " and Jackie")
   hello2("Class " * 3)

Now let's consider a function with two parameters. This version of hello takes
a parameter that controls how many times the greeting will be printed.

.. codelens:: functions_5

   def hello3(s, n):
      print((" hello " + s)*n)
         
   hello3("world", 4)
   hello3("", 1)
   hello3("Kitty", 11)

At Step 3 of the execution, in the first invocation of hello3, notice that the variable s is bound
to the value "world" and the variable n is bound to the value 4.

That's how function invocations always work. Each of the expressions, separated by commas, that are inside the
parentheses are evaluated to produce values. Then those values are matched up positionally
with the formal parameters. The first parameter name is bound to the first value
provided. The second parameter name is bound to the second value provided. And so on.

**Check your understanding**

.. mchoicemf:: test_questionfunctions_1_3
   :answer_a: def greet(t):
   :answer_b: def greet:
   :answer_c: greet(t, n):
   :answer_d: def greet(t, n)
   :correct: a
   :feedback_a: A function may take zero or more parameters.  In this case it has one.  
   :feedback_b: A function needs to specify its parameters in its header. If there are no paramters, put () after the function name.
   :feedback_c: A function definition needs to include the keyword def.
   :feedback_d: A function definition header must end in a colon (:).

   Which of the following is a valid function header (first line of a function definition)?

.. mchoicemf:: test_questionfunctions_1_4
   :answer_a: def print_many(x, y):
   :answer_b: print_many
   :answer_c: print_many(x, y)
   :answer_d: Print out string x, y times.
   :correct: b
   :feedback_a: This line is the complete function header (except for the semi-colon) which includes the name as well as several other components.
   :feedback_b: Yes, the name of the function is given after the keyword def and before the list of parameters.
   :feedback_c: This includes the function name and its parameters
   :feedback_d: This is a comment stating what the function does.

   What is the name of the following function?

   .. code-block:: python

     def print_many(x, y):
         """Print out string x, y times."""
         for i in range(y):
             print x



.. mchoicemf:: test_questionfunctions_1_5
   :answer_a: i
   :answer_b: x
   :answer_c: x, y
   :answer_d: x, y, i
   :correct: c
   :feedback_a: i is a variable used inside of the function, but not a parameter, which is passed in to the function.
   :feedback_b: x is only one of the parameters to this function.
   :feedback_c: Yes, the function specifies two parameters: x and y.
   :feedback_d: the parameters include only those variables whose values that the function expects to receive as input.  They are specified in the header of the function.

   What are the parameters of the following function?

   .. code-block:: python

     def print_many(x, y):
         """Print out string x, y times."""
         for i in range(y):
             print x



.. mchoicemf:: test_questionfunctions_1_6
   :answer_a: print_many(x, y)
   :answer_b: print_many
   :answer_c: print_many("Greetings")
   :answer_d: print_many("Greetings", 10):
   :answer_e: print_many("Greetings", z)
   :correct: e
   :feedback_a: No, x and y are the names of the formal parameters to this function.  When the function is called, it requires actual values to be passed in.
   :feedback_b: A function call always requires parentheses after the name of the function.
   :feedback_c: This function takes two parameters (arguments)
   :feedback_d: A colon is only required in a function definition.  It will cause an error with a function call.
   :feedback_e: Since z has the value 3, we have passed in two correct values for this function. "Greetings" will be printed 3 times.

   Considering the function below, which of the following statements correctly invokes, or calls, this function (i.e., causes it to run)?

   .. code-block:: python

      def print_many(x, y):
         """Print out string x, y times."""
         for i in range(y):
             print x

      z = 3

.. mchoicemf:: test_questionfunctions_1_7
   :answer_a: True
   :answer_b: False
   :correct: a
   :feedback_a: Yes, you can call a function multiple times by putting the call in a loop.
   :feedback_b: One of the purposes of a function is to allow you to call it more than once.   Placing it in a loop allows it to executed multiple times as the body of the loop runs multiple times.

   True or false: A function can be called several times by placing a function call in the body of a loop.

.. mchoicemf:: test_questionfunctions_1_8
   :answer_a: Hello
   :answer_b: Goodbye
   :answer_c: s1
   :answer_d: s2
   :correct: b
   :feedback_a: "Hello" is shorter than "Goodbye"
   :feedback_b: "Goodbye" is longer than "Hello"
   :feedback_c: s1 is a variable name; its value would print out, not the variable name
   :feedback_d: s2 is a variable name; its value would print out, not the variable name
   
   What output will the following code produce?
   
   .. code-block:: python

      def cyu(s1, s2):
         if len(s1) > len(s2):
            print s1
         else:
            print s2
            
      cyu("Hello", "Goodbye")
      


Returning a value from a function
---------------------------------

Not only can you pass a parameter value into a function, a function can also 
produce a value. You have already seen this in some previous functions that
you have used. For example, ``len`` takes a list or string as a parameter value
and returns a number, the length of that list or string. ``range`` takes an integer
as a parameter value and returns a list containing all the numbers from 0 up to
that parameter value.

Functions that return values are sometimes called **fruitful functions**.
In many other languages, a chunk that doesn't return a value is called a **procedure**,
but we will stick here with the Python way of also calling it a function, or if we want
to stress it, a *non-fruitful* function.

.. image:: Figures/blackboxfun.png


How do we write our own fruitful function?  Let's start by creating a very simple
mathematical function that we will call ``square``.  The square function will take one number
as a parameter and return the result of squaring that number.  Here is the
black-box diagram with the Python code following.


.. image:: Figures/squarefun.png

.. activecode:: ch04_square

    def square(x):
        y = x * x
        return y

    toSquare = 10
    result = square(toSquare)
    print("The result of",toSquare,"squared is",result)

The **return** statement is followed by an expression which is evaluated.  Its
result is returned to the caller as the "fruit" of calling this function.
Because the return statement can contain any Python expression we could have
avoided creating the **temporary variable** ``y`` and simply used
``return x*x``.
Try modifying the square function above to see that this works just the same.
On the other hand, using **temporary variables** like ``y`` in the program above makes
debugging
easier.  These temporary variables are referred to as **local variables**.

Notice something important here. The name of the variable we pass as an
argument --- ``toSquare`` --- has nothing to do with the name of the formal parameter
--- ``x``.  It is as if  ``x = toSquare`` is executed when ``square`` is called.
It doesn't matter what the value was named in
the caller (the place where the function was invoked). 
Inside ``square``, it's name is ``x``.  You can see this very clearly in
codelens, where the global variables and the local variables for the square
function are in separate boxes.

.. codelens:: ch04_clsquare

    def square(x):
        y = x * x
        return y

    toSquare = 10
    squareResult = square(toSquare)
    print("The result of ", toSquare, " squared is ", squareResult)


There is one more aspect of function return values that should be noted.  
All Python functions return the value ``None`` unless there is an explicit return statement with
a value other than ``None.``
Consider the following common mistake made by beginning Python
programmers.  As you step through this example, pay very close attention to the return
value in the local variables listing.  Then look at what is printed when the
function returns.


.. codelens:: ch04_clsquare_bad

    def square(x):
        y = x * x
        print(y)   # Bad! should use return instead!

    toSquare = 10
    squareResult = square(toSquare)
    print("The result of ", toSquare, " squared is ", squareResult)

The problem with this function is that even though it prints the value of the square, 
that value will not be returned to the place
where the call was done.  Since line 6 uses the return value as the right hand 
side of an assignment statement, the evaluation of the 
function will be ``None``.  In this case, ``squareResult`` will refer to that 
value after the assignment statement and therefore the result printed in line 7 is incorrect.  
Typically, functions will return values that can be printed or processed in some other way by the caller.

So far, we have just seen return values being assigned to variables. For example, 
we had the line ``squareResult = square(toSquare)``. As with all assignment statements,
the right hand side is executed first. It invokes the square function, passing in a
parameter value 10 (the current value of toSquare). That returns a value 100, which
completes the evaluation of the right-hand side of the assignment. 100 is then assigned
to the variable squareResult. In this case, the function invocation was the entire expression
that was evaluated.

Function invocations, however, can also be used as part of more complicated expressions. 
For example, ``squareResult = 2 * square(toSquare)``. In this case, the value 100 is
returned and is then multiplied by 2 to produce the value 200. When python evaluates an expression
like ``x * 3``, it substitutes the current value of x into the expression and then
does the multiplication. When python evaluates an expression like ``2 * square(toSquare)``, it substitutes
the return value 100 for entire function invocation and then does the multiplication.

To reiterate, when executing a line of code ``squareResult = 2 * square(toSquare)``, the python
interpreter does these steps:

   #. It's an assignment statement, so evaluate the right-hand side expression ``2 * square(toSquare)``.
   #. Look up the values of the variables square and toSquare: square is a function object and toSquare is 10
   #. Pass 10 as a parameter value to the function, get back the return value 100
   #. Substitute 100 for square(toSquare), so that the expression now reads ``2 * 100``
   #. Assign 200 to variable ``squareResult``

**Check your understanding**

.. mchoicemf:: test_questionfunctions_2_2
   :answer_a: Nothing (no value)
   :answer_b: The value of x+y+z
   :answer_c: The string 'x+y+z'
   :correct: a
   :feedback_a: We have accidentally used print where we mean return.  Therefore, the function will return the value None by default.  This is a VERY COMMON mistake so watch out!  This mistake is also particularly difficult to find because when you run the function the output looks the same.  It is not until you try to assign its value to a variable that you can notice a difference.
   :feedback_b: Careful!  This is a very common mistake.  Here we have printed the value x+y+z but we have not returned it.  To return a value we MUST use the return keyword.
   :feedback_c: x+y+z calculates a number (assuming x+y+z are numbers) which represents the sum of the values x, y and z.

   What will the following function return?

   .. code-block:: python

    def addEm(x, y, z):
        print(x+y+z)

.. mchoicemf:: test_questionfunctions_2_3
   :answer_a: 25
   :answer_b: 50
   :answer_c: 25 + 25
   :correct: b
   :feedback_a: It squares 5 twice, and adds them together
   :feedback_b: The two return values are added together
   :feedback_c: The two results are substituted into the expression and then it is evaluated. The returned values are integers in this case, not strings
   
   
   What will the following code output?
   
   .. code-block:: python

       def square(x):
           y = x * x
           return y
           
       print(square(5) + square(5))

.. mchoicemf:: test_questionfunctions_2_4
   :answer_a: 8
   :answer_b: 16
   :answer_c: Error: can't put a function invocation inside parentheses
   :correct: b
   :feedback_a: It squares 2, yielding the value 4. But that doesn't mean the next value multiplies 2 and 4.
   :feedback_b: It squares 2, yielding the value 4. 4 is then passed as a value to square again, yeilding 16.
   :feedback_c: This is a more complicated expression, but still valid. The expression square(2) is evaluated, and the return value 4 substitutes for square(2) in the expression.   
   
   What will the following code output?
   
   .. code-block:: python 

       def square(x):
           y = x * x
           return y
           
       print(square(square(2)))

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

Glossary
--------


.. glossary::

    argument
        A value provided to a function when the function is called. This value
        is assigned to the corresponding parameter in the function.  The argument
        can be the result of an expression which may involve operators,
        operands and calls to other fruitful functions.

    body
        The second part of a compound statement. The body consists of a
        sequence of statements all indented the same amount from the beginning
        of the header.  The standard amount of indentation used within the
        Python community is 4 spaces.

    compound statement
        A statement that consists of two parts:

        #. header - which begins with a keyword determining the statement
           type, and ends with a colon.
        #. body - containing one or more statements indented the same amount
           from the header.

        The syntax of a compound statement looks like this:

        .. code-block:: python

            keyword expression:
                statement
                statement ...

    docstring
        If the first thing in a function body is a string (or, we'll see later, in other situations
        too) that is attached to the function as its ``__doc__`` attribute.

    flow of execution
        The order in which statements are executed during a program run.

    function
        A named sequence of statements that performs some useful operation.
        Functions may or may not take parameters and may or may not produce a
        result.

    function call
        A statement that executes a function. It consists of the name of the
        function followed by a list of arguments enclosed in parentheses.

    function definition
        A statement that creates a new function, specifying its name,
        parameters, and the statements it executes.

    fruitful function
        A function that returns a value when it is called.

    header line
        The first part of a compound statement. A header line begins with a keyword and
        ends with a colon (:)

    parameter
        A name used inside a function to refer to the value which was passed
        to it as an argument.
   

