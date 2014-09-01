..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. qnum::
   :prefix: strings-12-
   :start: 1

Traversal and the ``while`` Loop
--------------------------------

The ``while`` loop can also control the
generation of the index values.  Remember that the programmer is responsible for setting up the initial
condition, making sure that the condition is correct, and making sure that something changes inside the
body to guarantee that the condition will eventually fail.


.. activecode:: ch08_7c
    :nocanvas:


    fruit = "apple"

    position = 0
    while position < len(fruit):
        print(fruit[position])
        position = position + 1


The loop condition is ``position < len(fruit)``, so when ``position`` is equal to the
length of the string, the condition is false, and the body of the loop is not
executed. The last character accessed is the one with the index
``len(fruit)-1``, which is the last character in the string.


Here is the same example in codelens so that you can trace the values of the variables.

.. codelens:: ch08_7c1
    
    fruit = "apple"

    position = 0
    while position < len(fruit):
        print(fruit[position])
        position = position + 1

**Check your understanding**

.. mchoicemf:: test_question8_10_1
   :answer_a: 0
   :answer_b: 1
   :answer_c: 2
   :correct: a
   :feedback_a: Yes, idx goes through the odd numbers starting at 1.  o is at position 4 and 8.
   :feedback_b: o is at positions 4 and 8.  idx starts at 1, not 0.
   :feedback_c: There are 2 o characters but idx does not take on the correct index values.


   How many times is the letter o printed by the following statements?
   
   .. code-block:: python

      s = "python rocks"
      idx = 1
      while idx < len(s):
          print(s[idx])
          idx = idx + 2
      

.. note::

    This workspace is provided for your convenience.  You can use this activecode window to try out anything you like.

    .. activecode:: scratch_08_02



.. index::
    single: in operator
    single: operator; in

