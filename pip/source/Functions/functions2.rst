..  Copyright (C)  Paul Rensick, Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

..  shortname:: Functions Continued
..  description:: Local and global variables and the calling stack.

.. qnum::
   :prefix: func2-
   :start: 1
   
.. _functions2_chap:

More on Functions
=================

In the previous chapter, you saw how functions are defined and how they are
invoked. In this chapter, we will cover some more advanced topics with
functions. But first, let's review and consolidate what you know.

Decoding a Function
-------------------

In general, you will try figure out what the function does, but, unless you are
writing the function, you won't care *how it does it*. 

For example, here is a summary of some functions we have seen already.

* ``raw_input`` takes one parameter, a string. It is displayed to the user.
  Whatever the user types is returned, as a string.

* ``int`` takes one parameter. It can be of any type that can be converted
  into an integer, such as a floating point number or a string whose characters
  are all digits.

Sometimes, you will be presented with a function definition whose operation is
not so neatly summarized as above. Sometimes you will need to look at the code,
either the function definition or code that invokes the function, in order to
figure out what it does. 

To build your understanding of any function, you should aim to answer the
following questions:

1. How many parameters does it have? 

#. What is the type of values that will be passed when the function is
   invoked? 

#. What is the type of the return value that the function produces when it
   executes?

If you try to make use of functions, ones you write or that others write,
without being able to answer these questions, you will find that your debugging
sessions are long and painful. 

The first question is always easy to answer. Look at the line with the function
definition, look inside the parentheses, and count how many variable names
there are.

The second and third questions are not always so easy to answer. In python,
unlike some other programming languages, variables are not declared to have
fixed types, and the same holds true for the variable names that appear as
formal parameters of functions. You have to figure it out from context.

To figure out the types of values that a function expects to receive as
parameters, you can look at the function invocations or you can look at the
operations that are performed on the parameters inside the function.

Here are some clues that can help you determine the type of object associated
with any variable, including a function parameter. If you see...

* ``len(x)``, then x must be a string or a list. (Actually, it can also be a
  dictionary, in which case it is equivalent to the expression
  ``len(x.keys())``. Later in the course, we will also see some other sequence
  types that it could be). x can't be a number or a Boolean. 
* ``x - y``, x and y must be numbers (integer or float)
* ``x + y``, x and y must both be numbers, both be strings, or both be lists
* ``x[3]``, x must be a string or a list containing at least four items, or x
  must be a dictionary that includes 3 as a key.
* ``x['3']``, x must be a dictionary, with '3' as a key.
* ``x[y:z]``, x must be a sequence (string or list), and y and z must be
  integers
* ``x and y``, x and y must be Boolean
* ``for x in y``, y must be a sequence (string or list); x must be a character
  if y is a string; if y is a list, x could be of any type.

**Check your understanding: decode this function definition**

.. mchoicemf:: test_questionfunctions_3_1
   :answer_a: 0
   :answer_b: 1
   :answer_c: 2
   :answer_d: 3
   :answer_e: Can't tell
   :correct: d
   :feedback_a: Count the number of variable names inside the parenetheses on line 1.
   :feedback_b: Count the number of variable names inside the parenetheses on line 1.
   :feedback_c: Count the number of variable names inside the parenetheses on line 1.
   :feedback_d: x, y, and z.
   :feedback_e: You can tell by looking inside the parentheses on line 1. Each variable name is separated by a comma.

   How many parameters does function cyu3 take?

   .. code-block:: python

      def cyu3(x, y, z):
         if x - y > 0:
            return y -2
         else:
            z.append(y)
            return x + 3
         
.. mchoicema:: test_questionfunctions_3_2
   :answer_a: integer
   :answer_b: float
   :answer_c: list
   :answer_d: string
   :answer_e: Can't tell
   :correct: a,b
   :feedback_a: x - y, y-2, and x+3 can all be performed on integers
   :feedback_b: x - y, y-2, and x+3 can all be performed on floats
   :feedback_c: x - y, y-2, and x+3 can't be performed on lists
   :feedback_d: x - y and y-2 can't be performed on strings
   :feedback_e: You can tell from some of the operations that are performed on them.

   What are the possible types of variables x and y?

   .. code-block:: python

      def cyu3(x, y, z):
         if x - y > 0:
            return y -2
         else:
            z.append(y)
            return x + 3
         
.. mchoicema:: test_questionfunctions_3_3
   :answer_a: integer
   :answer_b: float
   :answer_c: list
   :answer_d: string
   :answer_e: Can't tell
   :correct: c
   :feedback_a: append can't be performed on integers
   :feedback_b: append can't be performed on floats
   :feedback_c: append can be performed on lists
   :feedback_d: append can't be performed on strings
   :feedback_e: You can tell from some of the operations that are performed on it.

   What are the possible types of variable z?

   .. code-block:: python

      def cyu3(x, y, z):
         if x - y > 0:
            return y -2
         else:
            z.append(y)
            return x + 3

.. mchoicema:: test_questionfunctions_3_4
   :answer_a: integer
   :answer_b: float
   :answer_c: list
   :answer_d: string
   :answer_e: Can't tell
   :correct: a,b
   :feedback_a: y-2 or  x+3 could produce an integer
   :feedback_b: y-2 or  x+3 could produce a float
   :feedback_c: y-2 or  x+3 can't produce a list
   :feedback_d: neither y-2 or  x+3 could produce a string
   :feedback_e: You can tell from the expressions that follow the word return.

   What are the possible types of the return value from cyu3?

   .. code-block:: python

      def cyu3(x, y, z):
         if x - y > 0:
            return y -2
         else:
            z.append(y)
            return x + 3

Method Invocations
------------------

There is one other special type of function called a **method**, which is invoked slightly differently. Some
object types have methods defined for them. You have already seen some methods that operate on strings (e.g., ``find``, ``index``, ``split``, ``join``) and on 
lists (e.g., ``append``, ``pop``). 

We will not learn about how define methods until later 
in the course, when we cover Classes. But it's worth getting a basic understanding now
of how methods are invoked. To invoke a method, the syntax is ``<expr>.<methodname>(<additional parameter values>)``.

The expression to the left of the dot should evaluate to an object of the right type, an object
for which <methodname> is defined. The method will be applied to that object (that object
will be a parameter value passed to the function/method.) If the method takes additional parameters (some do, some don't),
additional expressions that evaluate to values are included inside the parentheses.

For example, let's look at an invocation of the split method.

.. activecode:: functions2_1

   y = "This is a sentence"
   z = y.split()
   print(type(z))
   print(len(z))
   print(z)
   for w in z:
      print w
      
The split method operates on a string. Because it is a method rather than a
regular function, the string it operates on appears to the left of the period, 
rather than inside the parentheses. The split method always returns a list.
On line 2, that returned value is assigned to the variable z.

The split method actually takes an optional extra parameter. If no value is provided
inside the parentheses, the split method chops up the list whenever it encounters
and whitespace (a space, a tab, or a newline). But you can specifying a character
or character string to split on. Try putting "s" inside the parentheses on line 2
above, make a prediction about what the output will be, and then check it. Try
some other things inside the parentheses.

Note that the thing to the left of the period can be any expression, not just a variable name.
It can even be a return value from some other function call or method invocation. For
example, if we want to remove the s and t characters from a string, we can do it all on
one line as show below.

.. activecode:: functions2_2

   print("This is a sentence".replace("s", "").replace("t", ""))
 
What's going on there? Start reading left to right. "This is a sentence" is a string, and 
the replace method is invoked on it. Two additional parameter values are provided, "s", and and
empty string. So, in the sentence, all occurrences of "s" are replaced with the empty string. A new 
string is returned, "Thi i a entence." There is another period followed by the word replace, so
the replace method is called again on that string, returning the shorter string, which is printed.


Variables and parameters are local
----------------------------------

An assignment statement in a function creates a **local variable** for the
variable on the left hand side of the assignment operator. It is called local because this variable only
exists inside the function and you cannot use it outside. For example,
consider again the ``square`` function:

.. codelens:: bad_local

    def square(x):
        y = x * x
        return y

    z = square(10)
    print(y)


If you press the 'last >>' button you will see an error message.
When we try to use ``y`` on line 6 (outside the function) Python looks for a global
variable named ``y`` but does not find one.  This results in the
error: ``Name Error: 'y' is not defined.``

The variable ``y`` only exists while the function is being executed ---
we call this its **lifetime**.
When the execution of the function terminates (returns),
the local variables  are destroyed.  Codelens helps you  visualize this
because the local variables disappear after the function returns.  Go back and step thru the
statements paying particular attention to the variables that are created when the function is called.
Note when they are subsequently destroyed as the function returns.

Formal parameters are also local and act like local variables.
For example, the lifetime of ``x`` begins when ``square`` is
called,
and its lifetime ends when the function completes its execution.

So it is not possible for a function to set some local variable to a
value, complete its execution, and then when it is called again next
time, recover the local variable.  Each call of the function creates
new local variables, and their lifetimes expire when the function returns
to the caller.

Global Variables
----------------

Variable names that are at the *top-level*, not inside any function definition,
are called global. 

It is legal for a function to access a global variable.  However, this is considered
**bad form** by nearly all programmers and should be avoided.  This subsection
includes some examples that illustrate the potential interactions of global and
local variables. These will help you understand exactly how python works. Hopefully,
they will also convince you that things can get pretty confusing when you mix
local and global variables, and that you really shouldn't do it.  

Look at the following, nonsensical variation of the square function.

.. activecode:: function2_3

    def badsquare(x):
        y = x ** power
        return y

    power = 2
    result = badsquare(10)
    print(result)


Although the ``badsquare`` function works, it is silly and poorly written.  We have done it here to illustrate
an important rule about how variables are looked up in Python.
First, Python looks at the variables that are defined as local variables in
the function.  We call this the **local scope**.  If the variable name is not
found in the local scope, then Python looks at the global variables,
or **global scope**.  This is exactly the case illustrated in the code above.
``power`` is not found locally in ``badsquare`` but it does exist globally.
The appropriate way to write this function would be to pass power as a parameter.
For practice, you should rewrite the badsquare example to have a second parameter called power.

There is another variation on this theme of local versus global variables.  Assignment statements in the local function cannot 
change variables defined outside the function.  Consider the following
codelens example:

.. codelens::  functions2_4

    def powerof(x,p):
        power = p   # Another dumb mistake
        y = x ** power
        return y

    power = 3
    result = powerof(10,2)
    print(result)

Now step through the code.  What do you notice about the values of variable ``power``
in the local scope compared to the variable ``power`` in the global scope?

The value of ``power`` in the local scope was different than the global scope.
That is because in this example ``power`` was used on the left hand side of the
assignment statement ``power = p``.  When a variable name is used on the
left hand side of an assignment statement Python creates a local variable.
When a local variable has the same name as a global variable we say that the
local shadows the global.  A **shadow** means that the global variable cannot
be accessed by Python because the local variable will be found first. This is
another good reason not to use global variables. As you can see,
it makes your code confusing and difficult to
understand.

To cement all of these ideas even further lets look at one final example.
Inside the ``square`` function we are going to make an assignment to the
parameter ``x``  There's no good reason to do this other than to emphasize
the fact that the parameter ``x`` is a local variable.  If you step through
the example in codelens you will see that although ``x`` is 0 in the local
variables for ``square``, the ``x`` in the global scope remains 2.  This is confusing
to many beginning programmers who think that an assignment to a
formal parameter will cause a change to the value of the variable that was
used as the actual parameter, especially when the two share the same name.
But this example demonstrates that that is clearly not how Python operates.

.. codelens:: function2_5

    def square(x):
        y = x * x
        x = 0       # assign a new value to the parameter x
        return y

    x = 2
    z = square(x)
    print(z)


**Check your understanding**

.. mchoicemf:: test_question5_3_1
   :answer_a: Its value
   :answer_b: The range of statements in the code where a variable can be accessed.
   :answer_c: Its name
   :correct: b
   :feedback_a: Value is the contents of the variable.  Scope concerns where the variable is &quot;known&quot;.
   :feedback_b:
   :feedback_c: The name of a variable is just an identifier or alias.  Scope concerns where the variable is &quot;known&quot;.

   What is a variable's scope?

.. mchoicemf:: test_question5_3_2
   :answer_a: A temporary variable that is only used inside a function
   :answer_b: The same as a parameter
   :answer_c: Another name for any variable
   :correct: a
   :feedback_a: Yes, a local variable is a temporary variable that is only known (only exists) in the function it is defined in.
   :feedback_b: While parameters may be considered local variables, functions may also define and use additional local variables.
   :feedback_c: Variables that are used outside a function are not local, but rather global variables.

   What is a local variable?

.. mchoicemf:: test_question5_3_3
   :answer_a: Yes, and there is no reason not to.
   :answer_b: Yes, but it is considered bad form.
   :answer_c: No, it will cause an error.
   :correct: b
   :feedback_a: While there is no problem as far as Python is concerned, it is generally considered bad style because of the potential for the programmer to get confused.
   :feedback_b: it is generally considered bad style because of the potential for the programmer to get confused.  If you must use global variables (also generally bad form) make sure they have unique names.
   :feedback_c: Python manages global and local scope separately and has clear rules for how to handle variables with the same name in different scopes, so this will not cause a Python error.

   Can you use the same name for a local variable as a global variable?



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
           
       print(h(2))


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
           
       print(g(h(2)))

Passing Mutable Objects
-----------------------

As you have seen, when a function (or method is invoked) and a parameter value is provided, a new
stack frame is created, and the parameter name is bound to the parameter value.
What happens when the value that is provided is a mutable object, like a list or dictionary?
Is the parameter name bound to a *copy* of the original object, or does it become an 
alias for exactly that object? In python, the answer is that it becomes an alias
for the original object. This answer matters  when the code block inside the function
definition causes some change to be made to the object (e.g., adding a key-value
pair to a dictionary or appending to a list). 

This sheds a little different light
on the idea of parameters being *local*. They *are* local in the sense that if you have a parameter
x inside a function and there is a global variable x, any reference to x inside
the function gets you the value of local variable x, not the global one. If you set 
``x = 3``, it changes the value of the local variable x, but when the function finishes
executing, that local x disappears, and so does the value 3. 

If, one the other hand, the local variable x points to a list ``[1, 2, 7]``,
setting ``x[2] = 9`` makes x still point to the same list, but changes the list's contents to ``[1, 2, 0]``.
The local variable x is discarded when the function completes execution, but the 
mutation to the list lives on if there is some other variable outside the function
that also is an alias for the same list.

Consider the following example.

.. activecode:: function2_7
   
   def double(y):
      y = 2 * y
   
   def changeit(lst):
      lst[0] = "Michigan"
      lst[1] = "Wolverines"

   y = 5
   double(y)
   print(y)
      
   mylst = ['106', 'students', 'are', 'awesome']
   changeit(mylst)
   print(mylst)

Try running it. Similar to examples we have seen before, running double does 
not change the global y. But
running changeit does change mylst. The explanation is above, about the sharing
of mutable objects. Try stepping through it in codelens to see the difference.

.. codelens:: function2_8
   
   def double(n):
      n = 2 * n
   
   def changeit(lst):
      lst[0] = "Michigan"
      lst[1] = "Wolverines"

   y = 5
   double(y)
   print(y)
      
   mylst = ['106', 'students', 'are', 'awesome']
   changeit(mylst)
   print(mylst)

Side Effects
------------

We say that a function has a **side effect** on the list object that is passed to it.
Global variables are another way to have side effects. For example, similar to examples
you have seen above, we could make double have a side effect on the global variable y.

.. codelens:: function2_9
   
   def double(n):
      y = 2 * n
   
   y = 5
   double(y)
   print(y)

Side effects are sometimes convenient. For example, it may be convenient to have
a single dictionary that accumulates information, and pass it around to various
functions that might add to it or modify it.

However, programs that have side effects can be very difficult to debug. When an
object has a value that is not what you expected, it can be difficult to track
down exactly where in the code it was set. Wherever it is practical to do so, 
it is best to avoid side effects. The way to avoid using side effects is to use
return values instead.

Instead of modifying a global variable inside a function, pass the global variable's
value in as a parameter, and set that global variable to be equal to a value returned
from the function. For example, the following is a better version of the code 
above.

.. codelens:: function2_10
   
   def double(n):
      return 2 * n
   
   y = 5
   y = double(y)
   print(y)

You can use the same coding pattern to avoid confusing side effects with sharing
of mutable objects. To do that, explicitly make a copy of an object and pass the
copy in to the function. Then return the modified copy and reassign it to the 
original variable if you want to save the changes. The built-in ``list`` function, which
takes a sequence as a parameter and returns a new list, works to copy an existing
list. For dictionaries, there is a .copy() method that can be called.

.. codelens:: function2_11
      
   def changeit(lst):
      lst[0] = "Michigan"
      lst[1] = "Wolverines"
      return lst
      
   mylst = ['106', 'students', 'are', 'awesome']
   newlst = changeit(list(mylst))
   print(mylst)
   print(newlst)



Glossary
--------

.. glossary::

    local variable
        A variable defined inside a function. A local variable can only be used
        inside its function.  Parameters of a function are also a special kind
        of local variable.
        
    global variable
        A variable defined at the top level, not inside any function.

    lifetime
        Variables and objects have lifetimes --- they are created at some point during
        program execution, and will be destroyed at some time. In python, objects
        live as long as there is some variable pointing to it, or it is part of some 
        other compound object, like a list or a dictionary. In python, local variables
        live only until the function finishes execution.

    method
        A special kind of function that is invoked on objects of particular types of
        objects, using the syntax ``<expr>.<methodname>(<additional parameter values>)``
   
    flow of execution
        The order in which statements are executed during a program run.

    function composition
        Using the output from one function call as the input to another.

    stack frame
        A frame that keeps track of the values of local variables during a function execution,
        and where to return control when the function execution completes.
      
    calling stack
        A sequence (stack) of frames, showing all the function calls that are in process
        but not yet complete. When one function's code invokes another function call,
        there will be more than one frame on the stack. 
   
    side effect
        A last change to a variable or object that is accessible outside of a function invocation.  