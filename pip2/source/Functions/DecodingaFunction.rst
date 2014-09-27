..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Decoding a Function
-------------------

In general, when you see a function definition you will try figure out what the function does, but, unless you are
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
* ``for x in y``, y must be a sequence (string or list) or a dictionary (in which case it's really the dictionary's keys); x must be a character
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

