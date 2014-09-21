..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Accumulating a Maximum Value
----------------------------

Now let's take a detour for a moment, and see how we can use the accumulator 
pattern to compute the maximum value in a list. Then you'll have an exercise to 
find the key in a dictionary that has the largest associated value.

To accumulate the maximum value in a list, you can have your accumulator variable
keep track of the max-so-far. Initialize it to the first item in the list. Then 
iterate through the rest of the items. For each, if it's bigger than the max-so-far,
replace the accumulator variable's value with the value of the current item.

Step through the execution of this code to get a feel for how it works. 

.. codelens:: dict_accum_9

   L = [3, 6, 2, 5, 39, 7, 5]
   
   a = L[0]
   for x in L[1:]:
      if x > a:
         a = x
   print a

Now, you may notice that this code will break if there isn't more than one item in L. 
You would get an error on line 4 for trying to access item L[1], which is the second
item. If we assume that L will have only numbers >= 0, we can initialize the max-so-far to be
0 and loop through *all* of the items in L.

.. codelens:: dict_accum_10

   L = [3, 6, 2, 5, 39, 7, 5]
   
   a = 0
   for x in L:
      if x > a:
         a = x
   print a


We can do a similar thing with a dictionary to find the maximum value. You can loop
through the keys and replace the max-so-far whenever the current key's associated value is greater than the
max-so-far.

**Check your understanding**

.. mchoicemf:: test_question_dict_accum_2
   :answer_a: I
   :answer_b: II
   :answer_c: III
   :answer_d: IV
   :correct: c
   :feedback_a: c will be bound to a key, which is a string; you can't compare that to a number.   
   :feedback_b: That will treate the current value of a as a key in the dictionary and update that key's value. You want to update a instead.
   :feedback_c: When the value associated with the current key c is bigger than the max so far, replace the max so far with that value
   :feedback_d: That will set a to be the current key, a string like 'a', not a value like 194.

   Which is the right code block to use in place of line 5 if we want to print out the maximum value?

   .. code-block:: python
   
      d = {'a': 194, 'b': 54, 'c':34, 'd': 44, 'e': 312, 'full':31}
      
      a = 0
      for c in d:
         <what code goes here?>
         
      print "max value is " + a


   .. code-block:: python

      I.
      if c > a:
         a = c
    
      II.
      if d[c] > a:
         d[a] = c
         
      III.
      if d[c] > a:
         a = d[c]
         
      IV.
      if d[c] > a:
         a = c

