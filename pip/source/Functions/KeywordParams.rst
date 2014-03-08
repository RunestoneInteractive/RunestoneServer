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

The online official python documentation includes a tutorial on optional parameters which covers the topic quite well. Please read the content there: * `Keyword arguments <http://docs.python.org/2/tutorial/controlflow.html#keyword-arguments>`_

Don't worry about the ``def cheeseshop(kind, *arguments, **keywords):`` example. You should be able to get by without understanding ``*parameters`` and ``**parameters`` in this course. But do make sure you understand the stuff above that.

The basic idea of passing arguments by keyword is very simple. When invoking a function, inside the parentheses there are always 0 or more values, separated by commas. With keyword arguments, some of the values can be of the form ``paramname = <expr>`` instead of just ``<expr>``. Note that when you have ``paramname = <expr>`` in a function definition, it is defining the default value for a parameter when no value is provided in the invocation; when you have ``paramname = <expr>`` in the invocation, it is supplying a value, overriding the default for that paramname.

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

**Check your understanding**

.. mchoicemf:: test_questionkeyword_params_1
   :answer_a: 2
   :answer_b: 3
   :answer_c: 5
   :answer_d: 7
   :answer_e: Runtime error since not enough values are passed in the call to f
   :correct: d
   :feedback_a: 2 is bound to x, not z
   :feedback_b: 3 is the default value for y, not z
   :feedback_c: 5 is bound to y, not z
   :feedback_d: 2 is bound x, 3 to y, and z gets its default value
   :feedback_e: z has a default value in the function definition, so it's optional to pass a value for it.

   What value will be printed for z?
   
   .. code-block:: python 

      initial = 7
      def f(x, y = 3, z = initial):
          print "x, y, z are:", x, y, z
      
      f(2, 5) 
         
.. mchoicemf:: test_questionkeyword_params_2
   :answer_a: 2
   :answer_b: 3
   :answer_c: 5
   :answer_d: 10
   :answer_e: Runtime error since no value is provided for y, which comes before z
   :correct: b
   :feedback_a: 2 is bound to x, not y
   :feedback_b: 3 is the default value for y, and no value is specified for y, 
   :feedback_c: say what?
   :feedback_d: 10 is the second value passed, but it is bound to z, not y.
   :feedback_e: That's the beauty of passing parameters with keywords; you can skip some parameters and they get their default values.

   What value will be printed for y?
   
   .. code-block:: python 

      initial = 7
      def f(x, y = 3, z = initial):
          print "x, y, z are:", x, y, z
      
      f(2, z = 10)
           
.. mchoicemf:: test_questionkeyword_params_3
   :answer_a: 2
   :answer_b: 3
   :answer_c: 5
   :answer_d: 7
   :answer_e: Runtime error since two different values are provided for x
   :correct: e
   :feedback_a: 2 is bound to x since it's the first value, but so is 5, based on keyword
   :feedback_b: 
   :feedback_c: 5 is bound to x by keyword, but 2 is also bound to it by virtue of being the value and not having a keyword
   :feedback_d: 
   :feedback_e: 2 is bound to x since it's the first value, but so is 5, based on keyword

   What value will be printed for x?
   
   .. code-block:: python 

      initial = 7
      def f(x, y = 3, z = initial):
          print "x, y, z are:", x, y, z
      
      f(2, x=5) 
   
.. mchoicemf:: test_questionkeyword_params_4
   :answer_a: 2
   :answer_b: 7
   :answer_c: 0
   :answer_d: Runtime error since two different values are provided for initial
   :correct: b
   :feedback_a: 2 is bound to x, no z
   :feedback_b: the default value for z is determined at the time the function is defined; at that time initial has the value 0.
   :feedback_c: the default value for z is determined at the time the function is defined, not when it is invoked
   :feedback_d: there's nothing wrong with reassigning the value of a variable at a later time

   What value will be printed for z?
   
   .. code-block:: python 

      initial = 7
      def f(x, y = 3, z = initial):
          print "x, y, z are:", x, y, z
      initial = 0
      f(2)
   
