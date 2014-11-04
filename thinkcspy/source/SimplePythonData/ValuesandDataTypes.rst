..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. qnum::
   :prefix: data-2-
   :start: 1

Values and Data Types
---------------------

A **value** is one of the fundamental things --- like a word or a number ---
that a program manipulates. The values we have seen so far are ``5`` (the
result when we added ``2 + 3``), and ``"Hello, World!"``.  We often refer to these values as **objects** and we will use the words value and object interchangeably.

.. note::
	Actually, the 2 and the 3 that are part of the addition above are values(objects) as well.

These objects are classified into different **classes**, or **data types**: ``4``
is an *integer*, and ``"Hello, World!"`` is a *string*, so-called because it
contains a string or sequence of letters. You (and the interpreter) can identify strings
because they are enclosed in quotation marks.

If you are not sure what class a value falls into, Python has a function called
**type** which can tell you.

.. activecode:: ch02_1
    :nocanvas:

    print(type("Hello, World!"))
    print(type(17))
    print("Hello, World")

Not surprisingly, strings belong to the class **str** and integers belong to the
class **int**.

.. note::

	When we show the value of a string using the ``print`` function, such as in the third example above, the quotes are no longer present.  The
	value of the string is the sequence of characters inside the quotes.  The quotes are only necessary to help Python know what the value is.


In the Python shell, it is not necessary to use the ``print`` function to see the values shown above.  The shell evaluates the Python function and automatically prints the result.  For example, consider the shell session shown below.  When
we ask the shell to evaluate ``type("Hello, World!")``, it responds with the appropriate answer and then goes on to
display the prompt for the next use.

.. sourcecode:: python

	Python 3.1.2 (r312:79360M, Mar 24 2010, 01:33:18)
	[GCC 4.0.1 (Apple Inc. build 5493)] on darwin
	Type "help", "copyright", "credits" or "license" for more information.
	>>> type("Hello, World!")
	<class 'str'>
	>>> type(17)
	<class 'int'>
	>>> "Hello, World"
	'Hello, World'
	>>>

Note that in the last example, we simply ask the shell to evaluate the string "Hello, World".  The result is as you might expect, the string itself.

Continuing with our discussion of data types, numbers with a decimal point belong to a class
called **float**, because these numbers are represented in a format called
*floating-point*.  At this stage, you can treat the words *class* and *type*
interchangeably.  We'll come back to a deeper understanding of what a class
is in later chapters.

.. activecode:: ch02_2
    :nocanvas:

    print(type(3.2))


What about values like ``"17"`` and ``"3.2"``? They look like numbers, but they
are in quotation marks like strings.

.. activecode:: ch02_3
    :nocanvas:

    print(type("17"))
    print(type("3.2"))

They're strings!

Strings in Python can be enclosed in either single quotes (``'``) or double
quotes (``"``), or three of each (``'''`` or ``"""``)

.. activecode:: ch02_4
    :nocanvas:

    print(type('This is a string.') )
    print(type("And so is this.") )
    print(type("""and this.""") )
    print(type('''and even this...''') )


Double quoted strings can contain single quotes inside them, as in ``"Bruce's
beard"``, and single quoted strings can have double quotes inside them, as in
``'The knights who say "Ni!"'``.
Strings enclosed with three occurrences of either quote symbol are called
triple quoted strings.  They can contain either single or double quotes:

.. activecode:: ch02_5
    :nocanvas:

    print('''"Oh no", she exclaimed, "Ben's bike is broken!"''')



Triple quoted strings can even span multiple lines:

.. activecode:: ch02_6
    :nocanvas:

    message = """This message will
    span several
    lines."""
    print(message)

    print("""This message will span
    several lines
    of the text.""")

Python doesn't care whether you use single or double quotes or the
three-of-a-kind quotes to surround your strings.  Once it has parsed the text of
your program or command, the way it stores the value is identical in all cases,
and the surrounding quotes are not part of the value.

.. activecode:: ch02_7
    :nocanvas:

    print('This is a string.')
    print("""And so is this.""")

So the Python language designers usually chose to surround their strings by
single quotes.  What do you think would happen if the string already contained
single quotes?

When you type a large integer, you might be tempted to use commas between
groups of three digits, as in ``42,000``. This is not a legal integer in
Python, but it does mean something else, which is legal:

.. activecode:: ch02_8
    :nocanvas:

    print(42000)
    print(42,000)


Well, that's not what we expected at all! Because of the comma, Python chose to
treat this as a *pair* of values.     In fact, the print function can print any number of values as long
as you separate them by commas.  Notice that the values are separated by spaces when they are displayed.

.. activecode:: ch02_8a
    :nocanvas:

    print(42, 17, 56, 34, 11, 4.35, 32)
    print(3.4, "hello", 45)

Remember not to put commas or spaces in your integers, no
matter how big they are. Also revisit what we said in the previous chapter:
formal languages are strict, the notation is concise, and even the smallest
change might mean something quite different from what you intended.

**Check your understanding**

.. mchoicemf:: test_question2_1_1
   :answer_a: Print out the value and determine the data type based on the value printed.
   :answer_b: Use the type function.
   :answer_c: Use it in a known equation and print the result.
   :answer_d: Look at the declaration of the variable.
   :correct: b
   :feedback_a: You may be able to determine the data type based on the printed value, but it may also be  deceptive, like when a string prints, there are no quotes around it.
   :feedback_b: The type function will tell you the class the value belongs to.
   :feedback_c: Only numeric values can be used in equations.
   :feedback_d: In Python variables are not declared.

   How can you determine the type of a variable?

.. mchoicemf:: test_question2_1_2
   :answer_a: Character
   :answer_b: Integer
   :answer_c: Float
   :answer_d: String
   :correct: d
   :feedback_a: It is not a single character.
   :feedback_b: The data is not numeric.
   :feedback_c: The value is not numeric with a decimal point.
   :feedback_d: Strings can be enclosed in single quotes.

   What is the data type of 'this is what kind of data'?


.. index:: type converter functions, int, float, str, truncation

