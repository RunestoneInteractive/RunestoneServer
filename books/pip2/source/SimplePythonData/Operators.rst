..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. index:: operator, operand, expression, integer division

Operators and Operands
----------------------

**Operators** are special tokens that represent computations like addition,
multiplication and division. The values the operator works on are called
**operands**.

The following are all legal Python expressions whose meaning is more or less
clear::

    20 + 32
    5 ** 2
    (5 + 9) * (15 - 7)

The tokens ``+``, ``-``, and ``*``, and the use of parenthesis for grouping,
mean in Python what they mean in mathematics. The asterisk (``*``) is the
token for multiplication, and ``**`` is the token for exponentiation.
Addition, subtraction, multiplication, and exponentiation all do what you
expect.

Remember that if we want to see the results of the computation, the program needs to specify that with a print statement. The first three computations occur, but thir results are not printed out.

.. activecode:: ch02_15
    :nocanvas:

    20 + 32
    5 ** 2
    (5 + 9) * (15 - 7)
    print 7 + 5

In Python 2.7, which we will be using, the division operator ``/`` produces a floating point result
if either of the operands is  of type **float**. If both are of type **int**, then 
it performs **integer division**, which truncates its result down to the next smallest integer.


.. activecode:: ch02_16
    :nocanvas:

   print 9 / 5
   print 9.0 / 5
   print 9 / 5.0
   print 5/9

Pay particular attention to the examples above. Note that it truncates, rather than rounding, so ``9/5`` is ` and ``5/9`` is 0.

Take care that you choose 
the correct flavor of the division operator.  If you want a truncated integer output,
make both of your operands integers. If you want a floating point result, make
one or both of your operands into floats.

If you want to be sure to get integer division, even on floating point operands,
you can use the operator ``//``.

.. activecode:: ch02_16a
   :nocanvas:
   
   print 7.0 / 3.0
   print 7.0 // 3.0

.. index:: modulus

The **modulus operator**, sometimes also called the **remainder operator** or **integer remainder operator** works on integers (and integer expressions) and yields
the remainder when the first operand is divided by the second. In Python, the
modulus operator is a percent sign (``%``). The syntax is the same as for other
operators.

.. activecode:: ch02_18
    :nocanvas:

    print 7 // 3     # This is the integer division operator
    print 7 % 3      # This is the remainder or modulus operator

In the above example, 7 divided by 3 is 2 when we use integer division and there is a remainder of 1.

The modulus operator turns out to be surprisingly useful. For example, you can
check whether one number is divisible by another---if ``x % y`` is zero, then
``x`` is divisible by ``y``.
Also, you can extract the right-most digit or digits from a number.  For
example, ``x % 10`` yields the right-most digit of ``x`` (in base 10).
Similarly ``x % 100`` yields the last two digits.


**Check your understanding**


.. mchoicemf:: test_question2_6_1a
   :answer_a: 4.5
   :answer_b: 5
   :answer_c: 4
   :answer_d: 4.0
   :answer_e: 2
   :correct: c
   :feedback_a: Because 18 and 4 are ints, / does integer division.
   :feedback_b: Integer division results in truncation, not rounding up.
   :feedback_c: Because 18 and 4 are ints, / does integer division.
   :feedback_d: Because 18 and 4 are ints, / does integer division and produces an integer.
   :feedback_e: / does division. Perhaps you were thinking of %, which computes the remainder?
   
   What value is printed when the following statement executes?

   .. code-block:: python

      print 18 / 4

.. mchoicemf:: test_question2_6_1
   :answer_a: 4.5
   :answer_b: 5
   :answer_c: 4
   :answer_d: 4.0
   :answer_e: 2
   :correct: a
   :feedback_a: Because 18.0 is a float, / does exact division.
   :feedback_b: Because 18.0 is a float, / does exact division.
   :feedback_c: Because 18.0 is a float, / does exact division.
   :feedback_d: Because 18.0 is a float, / does exact division.
   :feedback_e: / does division. Perhaps you were thinking of %, which computes the remainder?
   
   What value is printed when the following statement executes?

   .. code-block:: python

      print 18.0 / 4



.. mchoicemf:: test_question2_6_2
   :answer_a: 4.5
   :answer_b: 5
   :answer_c: 4
   :answer_d: 4.0
   :answer_e: 2
   :correct: d
   :feedback_a: - The // operator does integer division, not exact divisions
   :feedback_b: - Integer division results in truncation, not rounding up.
   :feedback_c: - The // operator does integer division, but it yields a float when one of the operands is a float/
   :feedback_d: - The // operator does integer division, and  it yields a float when one of the operands is a float.
   :feedback_e: - / does division. Perhaps you were thinking of %, which computes the remainder?
   
   What value is printed when the following statement executes?

   .. code-block:: python

      print 18.0 // 4


.. mchoicemf:: test_question2_6_3
   :answer_a: 4.25
   :answer_b: 5
   :answer_c: 4
   :answer_d: 2
   :correct: d
   :feedback_a: The % operator returns the remainder after division.
   :feedback_b: The % operator returns the remainder after division.
   :feedback_c: The % operator returns the remainder after division.
   :feedback_d: The % operator returns the remainder after division.

   What value is printed when the following statement executes?

   .. code-block:: python

      print 18 % 4


.. index:: input, input dialog

.. _input:

