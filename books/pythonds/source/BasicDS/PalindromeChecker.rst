..  Copyright (C)  Brad Miller, David Ranum
    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


Palindrome-Checker
~~~~~~~~~~~~~~~~~~

An interesting problem that can be easily solved using the deque data
structure is the classic palindrome problem. A **palindrome** is a
string that reads the same forward and backward, for example, *radar*,
*toot*, and *madam*. We would like to construct an algorithm to input a
string of characters and check whether it is a palindrome.

The solution to this problem will use a deque to store the characters of
the string. We will process the string from left to right and add each
character to the rear of the deque. At this point, the deque will be
acting very much like an ordinary queue. However, we can now make use of
the dual functionality of the deque. The front of the deque will hold
the first character of the string and the rear of the deque will hold
the last character (see :ref:`Figure 2 <fig_palindrome>`).

.. _fig_palindrome:

.. figure:: Figures/palindromesetup.png
   :align: center

   Figure 2: A Deque


Since we can remove both of them directly, we can compare them and
continue only if they match. If we can keep matching first and the last
items, we will eventually either run out of characters or be left with a
deque of size 1 depending on whether the length of the original string
was even or odd. In either case, the string must be a palindrome. The
complete function for palindrome-checking appears in
:ref:`ActiveCode 1 <lst_palchecker>`.

.. _lst_palchecker:

.. activecode:: palchecker
   :caption: A Palindrome Checker Using Deque
   :nocodelens:

   from pythonds.basic.deque import Deque
   
   def palchecker(aString):
       chardeque = Deque()

       for ch in aString:
           chardeque.addRear(ch)

       stillEqual = True

       while chardeque.size() > 1 and stillEqual:
           first = chardeque.removeFront()
           last = chardeque.removeRear()
           if first != last:
               stillEqual = False

       return stillEqual

   print(palchecker("lsdkjfskf"))
   print(palchecker("radar"))
