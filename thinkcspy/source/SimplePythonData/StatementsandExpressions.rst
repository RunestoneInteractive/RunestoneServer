..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Statements and Expressions
--------------------------

.. video:: expression_vid
    :controls:
    :thumb: ../_static/expressions.png

    http://media.interactivepython.org/thinkcsVideos/Expressions.mov
    http://media.interactivepython.org/thinkcsVideos/Expressions.webm

A **statement** is an instruction that the Python interpreter can execute. We
have only seen the assignment statement so far.  Some other kinds of statements
that we'll see shortly are ``while`` statements, ``for`` statements, ``if``
statements,  and ``import`` statements.  (There are other kinds too!)


.. index:: expression

An **expression** is a combination of values, variables, operators, and calls
to functions. Expressions need to be evaluated.  If you ask Python to ``print`` an expression, the interpreter
**evaluates** the expression and displays the result.

.. activecode:: ch02_13
    :nocanvas:

    print(1 + 1)
    print(len("hello"))


In this example ``len`` is a built-in Python function that returns the number
of characters in a string.  We've previously seen the ``print`` and the
``type`` functions, so this is our third example of a function!

The *evaluation of an expression* produces a value, which is why expressions
can appear on the right hand side of assignment statements. A value all by
itself is a simple expression, and so is a variable.  Evaluating a variable gives the value that the variable refers to.

.. activecode:: ch02_14
    :nocanvas:

    y = 3.14
    x = len("hello")
    print(x)
    print(y)

If we take a look at this same example in the Python shell, we will see one of the distinct differences between statements and expressions.

.. sourcecode:: python

	>>> y = 3.14
	>>> x = len("hello")
	>>> print(x)
	5
	>>> print(y)
	3.14
	>>> y
	3.14
	>>>

Note that when we enter the assignment statement, ``y = 3.14``, only the prompt is returned.  There is no value.  This
is due to the fact that statements, such as the assignment statement, do not return a value.  They are simply executed.

On the other hand, the result of executing the assignment statement is the creation of a reference from a variable, ``y``, to a value, ``3.14``.  When we execute the print function working on ``y``, we see the value that y is referring to.  In fact, evaluating ``y`` by itself results in the same response.


.. index:: operator, operand, expression, integer division

