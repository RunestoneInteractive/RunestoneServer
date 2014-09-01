..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

The `math` module
-----------------

The ``math`` module contains the kinds of mathematical functions you would
typically find on your calculator and some mathematical constants like `pi` and
`e`.

The first thing we need to do when we wish to use a module is perform an
**import**. In this case, we write ``import math``. That creates a reference to
a module object that contains the elements of that module. This looks very much
like the reference diagrams we saw earlier for simple variables, but the module
object has a lot more stuff in it than the simple objects we've seen before,
too much stuff to show all of it in the reference diagram.

.. image:: Figures/mathmod.png

Here are some items from the math module in action.  If you want more
information, you can check out the
`Math Module <http://docs.python.org/2/library/math.html#module-math>`_ Python
Documentation.

.. activecode:: chmodule_02

    import math

    print(math.pi)
    print(math.e)

    print(math.sqrt(2.0))

    print(math.sin(math.radians(90)))   # sin of 90 degrees



..  Like almost all other programming languages, angles are expressed in *radians*
.. rather than degrees.  There are two functions ``radians`` and ``degrees`` to
.. convert between the two popular ways of measuring angles.

The math module contains a bunch of functions, like sqrt and sin, and a few
variables, like pi and e. Once we have imported the math module, anything
defined there can be used in our program.  The syntax to refer to things from
the math module is the name of the module followed by a `dot` followed by the
specific item from the module (e.g., ``math.sqrt``).  You can think of this as
lastname.firstname where the lastname is the module family and the firstname is
the individual entry in the module.

.. note::

    Previously, you have seen the `dot` notation used for invoking a method on an
    object, as in ``[1, 2, 3].append(4)``, which invokes the append method on the list [1, 2, 3], passing
    the parameter 4. This may seem a little confusing, especially when we
    invoke a function from the math library, as in `math.sqrt(2.0)`. Here, sqrt is
    not a method being applied to the math object. It's just a variable name being
    looked up in the math module. 
    
    After you learn about classes, there will be a unifying interpretation of the
    dot notation that will help you understand why the dot is used here for looking up 
    a variable or a function inside a module and also used for method invocation.
    For now, you'll have to keep them straight just by paying attention to whether
    the word before the dot refers to an imported module, or something else.

If you have not done so already, take a look at the documentation for the
`Math Module <http://docs.python.org/2/library/math.html#module-math>`_.

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

.. mchoicema:: questions4_2_1a
    :answer_a: "math.pi".split('.')
    :answer_b: math.pi
    :answer_c: math.sqrt(2.0)
    :correct: a
    :feedback_a: math.pi is in quotes, so it's just a literal string. The split method is called on it. The return value is ["math", "pi"]
    :feedback_b: math.pi looks up pi within the math module. It is not a method invocation.
    :feedback_c: This looks up sqrt in the math module. It's a function, and that function is invoked, passing the value 2.0   
     
    Which of the following is a method invocation, in code followign the statement ``import math`` has been run?

