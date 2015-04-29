..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. qnum::
   :prefix: modules-3-
   :start: 1

The `math` module
-----------------

The ``math`` module contains the kinds of mathematical functions you would typically find on your
calculator and some mathematical constants
like `pi` and `e`.
As we noted above, when we ``import math``, we create a reference to a module object that contains these elements.

.. image:: Figures/mathmod.png

Here are some items from the math module in action.  If you want more information, you can check out the
`Math Module <http://docs.python.org/py3k/library/math.html#module-math>`_ Python Documentation.

.. activecode:: chmodule_02

    import math

    print(math.pi)
    print(math.e)

    print(math.sqrt(2.0))

    print(math.sin(math.radians(90)))   # sin of 90 degrees



..  Like almost all other programming languages, angles are expressed in *radians*
.. rather than degrees.  There are two functions ``radians`` and ``degrees`` to
.. convert between the two popular ways of measuring angles.

Notice another difference between this module and our use of ``turtle``.
In  ``turtle`` we create objects (either ``Turtle`` or ``Screen``) and call methods on those objects.  Remember that
a turtle is a data object (recall ``alex`` and ``tess``).  We need to create one in order to use it.  When we say
``alex = turtle.Turtle()``, we are calling the constructor for the Turtle class which returns a single turtle object.


Mathematical functions do not need to be constructed.  They simply
perform a task.
They are all housed together in a module called `math`.  Once we have imported the math module, anything defined there
can be used in our program.  Notice that we always use the name of the module followed by a `dot` followed by the
specific item from the module (``math.sqrt``).  You can think of this as lastname.firstname where the lastname is the module
family and the firstname is the individual entry in the module.

If you have not done so already, take a look at the documentation
for the math module.

**Check your understanding**

.. mchoicemf:: question4_2_1
   :answer_a: import math
   :answer_b: include math
   :answer_c: use math
   :answer_d:  You don’t need a statement.  You can always use the math module
   :correct: a
   :feedback_a: The module must be imported before you can use anything declared inside the module.
   :feedback_b: The correct term is not include, but you are close.
   :feedback_c: You will be using parts of the module, but that is not the right term.
   :feedback_d: You cannot use a Python module without a statement at the top of your program that explicitly tells Python you want to use the module.

   Which statement allows you to use the math module in your program?


