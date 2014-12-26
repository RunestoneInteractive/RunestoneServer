..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".



.. index::
    single: function
    single: function definition
    single: definition; functionFunctions Definitions

.. _functions_chap:


Function Definition
-------------------

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

We've already seen the ``for`` statement which has the same structure, with an indented block of code, and the ``if``, ``elif``, and ``else`` statements that do so as well.

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
      print "Hello"
      print "Glad to meet you"

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



