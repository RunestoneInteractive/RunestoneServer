..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Values and Data Types
---------------------

A **value** is one of the fundamental things --- like a word or a number ---
that a program manipulates. The values we have seen so far are ``5`` (the
result when we added ``2 + 3``), and ``"Hello, World!"``.  

We can specifiy values directly in the programs we write. For example we can specify a number as a literal just by writing it directly, (e.g., ``5`` or ``4.32``). In a program, we specify a word, or more generally a **string** of characters, by enclosing the characters inside quotation marks (e.g.,  ``"Hello, World!"``).

During execution of a program, the python interpreter creates an internal representation of values that are specified in a program. It can then manipulate them. For example, in the next section, we'll look at how a program can specify that values should be combined using operators like ``+`` and ``*``. We call the internal representations **objects** or just **values**. 

.. note:
   When we are being careful, we will refer to a number or string that is specified directly in a program as a **literal**, and use the word **value** to refer to the Python interpreter's internal representation of the number or string during the execution of the program. Sometimes, however, we will get a little sloppy and refer to literals as values. It may help you to keep in mind the distinction between a value as written in a program (a literal) and the internal representation of a value. 

Normally, people don't get to see directly what is happening when a program executes. Codelens is really useful for learning because it does make a lot of things visible during a program execution. 

The print statement is also a good way to make a computed value visible to people. Each internal object has an external, printed representation. When a print statement in the program's code says to print out the object, the printed representation appears in the output window. The printed representation of a number uses the familiar decimal representation (reading `Roman Numerals <http://en.wikipedia.org/wiki/Roman_numerals>`_ is a fun challenge in museums, but thank goodness the Python interpreter doesn't present the number 2014 as MMXIV). The printed representation of a character string is just the characters, *without the quotation marks*.

.. activecode:: values_1
    :nocanvas:

    print 3.2
    print "Hello, World!"

As you will learn in more detail later, there are some special characters, like the tab character ``\t`` and the newline character ``\n`` whose internal and external representations are different.

.. activecode:: values_2
    :nocanvas:

    print "Two tabs after this\tand then newlines\n\nand that's all"

Numbers with a decimal point belong to a class
called **float**, because these numbers are represented in a format called
*floating-point*.  At this stage, you can treat the words *class* and *type*
interchangeably.  We'll come back to a deeper understanding of what a class
is in later chapters.

You will soon encounter other types of objects as well, such as lists and dictionaries. Each of these has its own special representation for specifying an object in a program, and for displaying an object when you print it. For example, list contents are enclosed in square brackets ``[ ]``. You will also encounter some more complicated objects that do not have very nice printed representations: printing those won't be very useful. 

