..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Accumulating the Best Key
-------------------------
               
Now what if we want to find the *key* associated with the maximum value? It would be nice to just find
the maximum value as above, and then look up the key associated with it, but dictionaries don't work
that way. You can look up the value associated with a key, but not the key associated with a value. (The
reason for that is there may be more than one key that has the same value).

The trick is to have the accumulator keep track of the best key so far instead of the best value so far.
For simplicity, let's assume that there are at least two keys in the dictionary. Then, similar to our
first version of computing the max of a list, we can initialize the best-key-so-far to be the first key, 
and loop through the keys, replacing the best-so-far whenever we find a better one.

In the exercise below, we have provided skeleton code. See if you can fill it in. An answer is provided,
but you'll learn more if you try to write it yourself first.

.. tabbed:: q0

   .. tab:: Question
   
      Write a program that finds the key in a dictionary that has the maximum value. If
      two keys have the same maximum value, it's OK to print out either one. Fill
      in the skeleton code
      
      .. actex:: ex_dict_accum_3

         d = {'a': 194, 'b': 54, 'c':34, 'd': 44, 'e': 312, 'full':31}
         
         ks = d.keys()
         # initialize variable best_key_so_far to be the first key in d
         for k in ks:
            # check if the value associated with the current key is
            # bigger than the value associated with the best_key_so_far
            # if so, save the current key as the best so far
            
         print "key " + best_key_so_far + " has the highest value, " + str(d[best_key_so_far])
   
   .. tab:: Answer 
   
      .. activecode:: ex_dict_accum_3_answer
      
         d = {'a': 194, 'b': 54, 'c':34, 'd': 44, 'e': 312, 'full':31}
         
         ks = d.keys()
         best_key_so_far = ks[0]
         for k in ks:
            if d[k] > d[best_key_so_far]:
               best_key_so_far = k
            
         print "key " + best_key_so_far + " has the highest value, " + str(d[best_key_so_far])
         

