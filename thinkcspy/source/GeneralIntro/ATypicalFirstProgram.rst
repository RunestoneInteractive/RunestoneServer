..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. qnum::
   :prefix: intro-12-
   :start: 1

A Typical First Program
-----------------------

Traditionally, the first program written in a new language is called *Hello,
World!* because all it does is display the words, Hello, World!  In Python, the source code
looks like this.

.. sourcecode:: python

    print("Hello, World!")

This is an example of using the **print function**, which doesn't actually
print anything on paper. It displays a value on the screen. In this case, the result is the phrase:

.. sourcecode:: python

    Hello, World!

Here is the example in activecode.  Give it a try!

.. activecode:: ch01_2

    print("Hello, World!")

The quotation marks in the program mark the beginning and end of the value.
They don't appear in the result.

Some people judge the quality of a programming language by the simplicity of
the Hello, World! program. By this standard, Python does about as well as
possible.

**Check your understanding**

.. mchoicemf:: question1_11_1
   :answer_a: sends information to the printer to be printed on paper.
   :answer_b: displays a value on the screen.
   :answer_c: tells the computer to put the information in print, rather than cursive, format.
   :answer_d: tells the computer to speak the information.
   :correct: b
   :feedback_a: Within the Python programming language, the print function has nothing to do with the printer.
   :feedback_b: Yes, the print function is used to display the value of the thing being printed.
   :feedback_c: The format of the information is called its font and has nothing to do with the print function.
   :feedback_d: That would be a different function.

   The print function:


.. index:: comments

