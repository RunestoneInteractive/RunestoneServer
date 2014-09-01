..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Index Operator: Working with the Characters of a String
-------------------------------------------------------

The **indexing operator** (Python uses square brackets to enclose the index) 
selects a single character from a string.  The characters are accessed by their position or 
index value.  For example, in the string shown below, the 14 characters are indexed left to right 
from postion 0 to position 13.  


.. image:: Figures/indexvalues.png
   :alt: index values

It is also the case that the positions are named from right to left using negative numbers where -1 is the rightmost
index and so on.
Note that the character at index 6 (or -8) is the blank character.


.. activecode:: chp08_index1
    
    school = "Luther College"
    m = school[2]
    print(m)
    
    lastchar = school[-1]
    print(lastchar)

The expression ``school[2]`` selects the character at index 2 from ``school``, and creates a new
string containing just this one character. The variable ``m`` refers to the result. 

The letter at index zero of ``"Luther College"`` is ``L``.  So at
position ``[2]`` we have the letter ``t``.

If you want the zero-eth letter of a string, you just put 0, or any expression
with the value 0, in the brackets.  Give it a try.

The expression in brackets is called an **index**. An index specifies a member
of an ordered collection.  In this case the collection of characters in the string. The index
*indicates* which character you want. It can be any integer
expression so long as it evaluates to a valid index value.

Note that indexing returns a *string* --- Python has no special type for a single character.
It is just a string of length 1.

**Check your understanding**

.. mchoicemf:: test_question8_2_1
   :answer_a: t
   :answer_b: h
   :answer_c: c
   :answer_d: Error, you cannot use the [ ] operator with a string.
   :correct: b
   :feedback_a: Index locations do not start with 1, they start with 0.
   :feedback_b: Yes, index locations start with 0.
   :feedback_c: s[-3] would return c, counting from right to left.
   :feedback_d: [ ] is the index operator


   What is printed by the following statements?
      
   .. code-block:: python
   
      s = "python rocks"
      print(s[3])




.. mchoicemf:: test_question8_2_2
   :answer_a: tr
   :answer_b: t0
   :answer_c: ps
   :answer_d: nn
   :answer_e: Error, you cannot use the [ ] operator with the + operator.
   :correct: b
   :feedback_a: Yes, t is at postion 2, counting left to right starting from 0; and s at -4, counting right to left starting from -1.
   :feedback_b: Almost. For -4 you count from right to left, starting with -1. 
   :feedback_c: p is at location 0, not 2.
   :feedback_d: n is at location 5, not 2.
   :feedback_e: [ ] operator returns a string that can be concatenated with another string.


   What is printed by the following statements?
   
   .. code-block:: python
   
      s = "python rocks"
      print(s[2] + s[-4])


.. note::
   Why does counting start at 0 going from left to right, but at -1 going from right to left? Well, indexing starting at 0
   has a long history in computer science having to do with some low-level implementation details that we won't
   go into. For indexing from right to left, it might seem natural to do the analgous thing
   and start at -0. Unfortunately, -0 is the same as 0, so s[-0] can't be the last item. Remember we
   said that programming languages are formal languages where details matter and
   everything is taken literally?
