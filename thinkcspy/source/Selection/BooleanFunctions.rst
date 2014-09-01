..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. qnum::
   :prefix: select-8-
   :start: 1

Boolean Functions
-----------------

We have already seen that boolean values result from the evaluation of boolean expressions.  Since the result of any
expression evaluation can be returned by a function (using the ``return`` statement),
functions can return boolean values.  This turns out to be a very convenient way to hide the details of complicated tests. For example:

.. activecode:: ch06_boolfun1

    def isDivisible(x, y):
        if x % y == 0:
            result = True
        else:
            result = False

        return result

    print(isDivisible(10, 5))

The name of this function is ``isDivisible``. It is common to give **boolean
functions** names that sound like yes/no questions.  ``isDivisible`` returns
either ``True`` or ``False`` to indicate whether the ``x`` is or is not
divisible by ``y``.

We can make the function more concise by taking advantage of the fact that the
condition of the ``if`` statement is itself a boolean expression. We can return
it directly, avoiding the ``if`` statement altogether:

.. sourcecode:: python

    def isDivisible(x, y):
        return x % y == 0


Boolean functions are often used in conditional statements:

.. sourcecode:: python

    if isDivisible(x, y):
        ... # do something ...
    else:
        ... # do something else ...

It might be tempting to write something like
``if isDivisible(x, y) == True:``
but the extra comparison is  not necessary.  The following example shows the ``isDivisible`` function at work.  Notice how
descriptive the code is when we move the testing details into a boolean function.  Try it
with a few other actual parameters to see what is printed.

.. activecode:: ch06_boolfun2

    def isDivisible(x, y):
        if x % y == 0:
            result = True
        else:
            result = False

        return result

    if isDivisible(10, 5):
        print("That works")
    else:
        print("Those values are no good")

Here is the same program in codelens.  When we evaluate the ``if`` statement in the main part of the program, the evaluation of
the boolean expression causes a call to the ``isDivisible`` function.  This is very easy to see in codelens.

.. codelens:: ch06_boolcodelens
    :showoutput:

    def isDivisible(x, y):
        if x % y == 0:
            result = True
        else:
            result = False

        return result

    if isDivisible(10, 5):
        print("That works")
    else:
        print("Those values are no good")



**Check your understanding**

.. mchoicemf:: test_question6_8_1
   :answer_a: A function that returns True or False
   :answer_b: A function that takes True or False as an argument
   :answer_c: The same as a Boolean expression
   :correct: a
   :feedback_a: A Boolean function is just like any other function, but it always returns True or False.
   :feedback_b: A Boolean function may take any number of arguments (including 0, though that is rare), of any type.
   :feedback_c: A Boolean expression is a statement that evaluates to True or False, e.g. 5+3==8.  A function is a series of expressions grouped together with a name that are only executed when you call the function.

   What is a Boolean function?

.. mchoicemf:: test_question6_8_2
   :answer_a: Yes
   :answer_b: No
   :correct: a
   :feedback_a: It is perfectly valid to return the result of evaluating a Boolean expression.
   :feedback_b: x +y < z is a valid Boolean expression, which will evaluate to True or False.  It is perfectly legal to return True or False from a function, and to have the statement to be evaluated in the same line as the return keyword.

   Is the following statement legal in Python (assuming x, y and z are defined to be numbers)?

   .. code-block:: python

     return x + y < z



.. note::

   This workspace is provided for your convenience.  You can use this activecode window to try out anything you like.

   .. activecode:: scratch_06_03



