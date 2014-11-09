..  Copyright (C)  Paul Resnick.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".
 
    
Zip
---
 
One more common pattern with lists, besides accumulation, is to step through a pair of lists (or several lists), doing something with all of the first items, then something with all of the second items, and so on. For example, given two lists of numbers, you might like to add them up pairwise, taking [3, 4, 5] and [1, 2, 3] to yield [4, 6, 8].

One way to do that with a for loop is to loop through the possible index values. 

.. activecode:: zip_1

   L1 = [3, 4, 5]
   L2 = [1, 2, 3]
   L3 = []
   
   for i in range(len(L1)):
      L3.append(L1[i] + L2[i])
   
   print L3
      
You have seen this idea :ref:`previously <for_by_index>` for iterating through the items in a single list. In many other programming languages that's really the only way to iterate through the items in a list. In python, however, we have gotten used to for loop where the iteration variable is bound successively to each item in the list, rather than just to a number that's used as a position or index into the list. 

Can't we do something similar with pairs of lists? It turns out we can.

The zip function takes multiple lists and turns them into a list of tuples, pairing up all the first items as one tuple, all the second items as a tuple, and so on. Then we can iterate through those tuples, and perform some operation on all the first items, all the second items, and so on.

.. activecode:: zip_2

   L1 = [3, 4, 5]
   L2 = [1, 2, 3]
   L4 = zip(L1, L2)
   print L4

Here's what happens when you loop through the tuples.
   
.. activecode:: zip_3

   L1 = [3, 4, 5]
   L2 = [1, 2, 3]
   L3 = []
   L4 = zip(L1, L2)

   for (x1, x2) in L4:
      L3.append(x1+x2)
   
   print L3

Or, simplifying and using a list comprehension:

.. activecode:: zip_4

   L1 = [3, 4, 5]
   L2 = [1, 2, 3]
   L3 = [x1 + x2 for (x1, x2) in zip(L1, L2)]
   print L3
   
Or, using map and not unpacking the tuple (our online environment has trouble with unpacking the tuple in a lambda expression):

.. activecode:: zip_5

   L1 = [3, 4, 5]
   L2 = [1, 2, 3]
   L3 = map(lambda x: x[0] + x[1], zip(L1, L2))
   print L3

Consider the task from Problem Set 7 where we asked you write a function possible(), as one component of a hangman guesser. It determines whether a word is still possible, given the guesses that have been made and the current state of the blanked word.

We provided a solution that involved iterating through the indexes of the word, checking whether the blanked character was compatible with the word's character in that same position, given the guesses so far. It's slightly simplified here, because the original solution was unnecessarily complex.


.. activecode:: zip_6

   def possible(word, blanked, guesses_made):
       if len(word) != len(blanked):
           return False
       for i in range(len(word)):
           bc = blanked[i]
           wc = word[i]
           if bc == '_' and wc in guesses_made:
               return False
           elif bc != '_' and bc != wc:
               return False
       return True
            
   import test         
   test.testEqual(possible("HELLO", "_ELL_", "ELJ"), True)
   test.testEqual(possible("HELLO", "_ELL_", "ELJH"), False)
   test.testEqual(possible("HELLO", "_E___", "ELJ"), False)

We can rewrite that using zip, to be a little more comprehensible.

.. activecode:: zip_7

   def possible(word, blanked, guesses_made):
       if len(word) != len(blanked):
           return False
       for (bc, wc) in zip(blanked, word):
           if bc == '_' and wc in guesses_made:
               return False
           elif bc != '_' and bc != wc:
               return False
       return True
            
   import test         
   test.testEqual(possible("HELLO", "_ELL_", "ELJ"), True)
   test.testEqual(possible("HELLO", "_ELL_", "ELJH"), False)
   test.testEqual(possible("HELLO", "_E___", "ELJ"), False)
