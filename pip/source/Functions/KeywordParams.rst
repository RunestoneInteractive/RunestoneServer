..  Copyright (C)  Paul Rensick, Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

..  shortname:: Keyword Parameters
..  description:: Using keyword parameters when calling a function.

.. qnum::
   :prefix: keyword-params-
   :start: 1
   
.. _keyword_pararams_chap:

Keyword Parameters
==================

Previously, in the chapter on :ref:`Optional Parameters <optional_pararams_chap>` you learned how to define default values for formal parameters, which made it optional to provide values for those parameters when invoking the functions.

In this chapter, you'll see one more way to invoke functions with optional parameters, with keyword-based parameter passing. This is particularly convenient when there are several optional parameters and you want to provide a value for one of the later parameters while not providing a value for the earlier ones.

The online official python documentation includes a tutorial on optional parameters which covers the topic quite well. Please read the content there. Below I provide links to specific sections, and a few notes on python constructs that they are using that you may not have seen before.

* `Keyword arguments <http://docs.python.org/2/tutorial/controlflow.html#keyword-arguments>`_

The basic idea is very simple. When invoking a function, in the parentheses there are always 0 or more values, separated by commas. With keyword arguments, some of the values can be of the form ``paramname = <expr>`` instead of just ``<expr>``. Note that when you have ``paramname = <expr>`` in a function definition, it is defining the default value for a parameter when no value is provided in the invocation; when you have ``paramname = <expr>`` in the invocation, it is supplying a value, overriding the default for that paramname.

To make it easier to follow the details of the examples in the official python tutorial, you can step through them in CodeLens.

.. codelens:: keyword_params_1

   def parrot(voltage, state='a stiff', action='voom', type='Norwegian Blue'):
       print "-- This parrot wouldn't", action,
       print "if you put", voltage, "volts through it."
       print "-- Lovely plumage, the", type
       print "-- It's", state, "!"
       
   parrot(1000)                                          # 1 positional argument
   parrot(voltage=1000)                                  # 1 keyword argument
   parrot(voltage=1000000, action='VOOOOOM')             # 2 keyword arguments
   parrot(action='VOOOOOM', voltage=1000000)             # 2 keyword arguments
   parrot('a million', 'bereft of life', 'jump')         # 3 positional arguments
   parrot('a thousand', state='pushing up the daisies')  # 1 positional, 1 keyword
   
As you step through it, each time the function is invoked, make a prediction about what each of the four parameter values will be during execution of lines 2-5. Then, look below at the stack frame to see what they actually are.

