..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

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

If you really want to change the value of a global variable inside a function,
you can can do it by explicitly declaring the variable to be global, as in the example
below. Again, you should *not* do this in your code. The example is here only
to cement your understanding of how python works.

.. codelens::  functions2_4a

    def powerof(x,p):
        global power  # a really... 
        power = p     # ...bad idea, but valid code
        y = x ** power
        return y

    power = 3
    result = powerof(10,2)
    print(result)
    print(power)

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



