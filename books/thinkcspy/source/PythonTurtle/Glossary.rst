..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Glossary
--------

.. glossary::


    attribute
        Some state or value that belongs to a particular object.  For example,
        tess has a color.

    canvas
        A surface within a window where drawing takes place.

    control flow
        See *flow of execution* in the next chapter.

    for loop
        A statement in Python for convenient repetition of statements in
        the *body* of the loop.

    instance
        An object that belongs to a class.  `tess` and `alex` are different
        instances of the class `Turtle`


    invoke
        An object has methods.  We use the verb invoke to mean *activate the
        method*.  Invoking a method is done by putting parentheses after the
        method name, with some possible arguments.  So  ``wn.exitonclick()`` is
        an invocation of the ``exitonclick`` method.

    iteration
		A basic building block for algorithms (programs).  It allows steps to be repeated.  Sometimes called *looping*.

    loop body
        Any number of statements nested inside a loop. The nesting is indicated
        by the fact that the statements are indented under the for loop
        statement.

    loop variable
        A variable used as part of a for loop. It is assigned a different value
        on each iteration of the loop, and is used as part of the terminating
        condition of the loop,



    method
        A function that is attached to an object.  Invoking or activating the
        method causes the object to respond in some way, e.g. ``forward`` is
        the method when we say ``tess.forward(100)``.



    module
        A file containing Python definitions and statements intended for use in
        other Python programs. The contents of a module are made available to
        the other program by using the *import* statement.

    object
        A "thing" to which a variable can refer.  This could be a screen window,
        or one of the turtles you have created.

    range
        A built-in function in Python for generating sequences of integers.  It
        is especially useful when we need to write a for loop that executes a
        fixed number of times.

    sequential
		The default behavior of a program.  Step by step processing of algorithm.

    state
		The collection of attribute values that a specific data object maintains.

    terminating condition
        A condition that occurs which causes a loop to stop repeating its body.
        In the ``for`` loops we saw in this chapter, the terminating condition
        has been when there are no more elements to assign to the loop variable.

    turtle
		A data object used to create pictures (known as turtle graphics).


