..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Order of Operations
-------------------

When more than one operator appears in an expression, the order of evaluation
depends on the **rules of precedence**. Python follows the same precedence
rules for its mathematical operators that mathematics does.

.. The acronym PEMDAS
.. is a useful way to remember the order of operations:

#. *Parentheses* have the highest precedence and can be used to force an
   expression to evaluate in the order you want. Since expressions in
   parentheses are evaluated first, ``2 * (3-1)`` is 4, and ``(1+1)**(5-2)`` is
   8. You can also use parentheses to make an expression easier to read, as in
   ``(minute * 100) / 60``: in this case, the parentheses don't change the result,
   but they reinforce that the expression in parentheses will be evaluated first.
#. *Exponentiation* has the next highest precedence, so ``2**1+1`` is 3 and
   not 4, and ``3*1**3`` is 3 and not 27.  Can you explain why?
#. *Multiplication and division* operators have the same
   precedence, which is higher than addition and subtraction, which
   also have the same precedence. So ``2*3-1`` yields 5 rather than 4, and
   ``5-2*2`` is 1, not 6.
#. Operators with the *same* precedence are
   evaluated from left-to-right. In algebra we say they are *left-associative*.
   So in the expression ``6-3+2``, the subtraction happens first, yielding 3.
   We then add 2 to get the result 5. If the operations had been evaluated from
   right to left, the result would have been ``6-(3+2)``, which is 1.

.. (The
..   acronym PEDMAS could mislead you to thinking that division has higher
..   precedence than multiplication, and addition is done ahead of subtraction -
..   don't be misled.  Subtraction and addition are at the same precedence, and
..   the left-to-right rule applies.)

.. note::

    Due to some historical quirk, an exception to the left-to-right
    left-associative rule is the exponentiation operator `**`. A useful hint
    is to always use parentheses to force exactly the order you want when
    exponentiation is involved:

.. activecode:: ch02_23
  :nocanvas:

  print 2 ** 3 ** 2     # the right-most ** operator gets done first!
  print (2 ** 3) ** 2   # use parentheses to force the order you want!

.. note::

   This is a second way that parentheses are used in Python. The first way you've already seen is that () indicates a function call, with the inputs going inside the parentheses. How can Python tell when parentheses specify to call a function, and when they are just forcing the order of operations for ambiguous operator expressions? 
   
   The answer is that if there's a an expression to the left of the parentheses that evaluates to a function object, then the parentheses indicate a function call, and otherwise not. You will have to get used to making the same inference when you see parentheses: is this a function call, or just specifying precedence?  

**Check your understanding**

.. mchoicemf:: test_question2_8_1
   :answer_a: 14
   :answer_b: 24
   :answer_c: 3
   :answer_d: 13.667
   :correct: a
   :feedback_a: Using parentheses, the expression is evaluated as (2*5) first, then (10 // 3), then (16-3), and then (13+1).
   :feedback_b: Remember that * has precedence over  -.
   :feedback_c: Remember that // has precedence over -.
   :feedback_d: Remember that // does integer division.

   What is the value of the following expression:

   .. code-block:: python

      16 - 2 * 5 // 3 + 1



