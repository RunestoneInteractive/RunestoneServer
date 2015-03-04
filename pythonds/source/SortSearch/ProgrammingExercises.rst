..  Copyright (C)  Brad Miller, David Ranum
    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


Programming Exercises
---------------------

#. Set up a random experiment to test the difference between a
   sequential search and a binary search on a list of integers.

#. Use the binary search functions given in the text (recursive and
   iterative). Generate a random, ordered list of integers and do a
   benchmark analysis for each one. What are your results? Can you
   explain them?

#. Implement the binary search using recursion without the slice
   operator. Recall that you will need to pass the list along with the
   starting and ending index values for the sublist. Generate a random,
   ordered list of integers and do a benchmark analysis.

#. Implement the ``len`` method (\_\_len\_\_) for the hash table Map ADT
   implementation.

#. Implement the ``in`` method (\_\_contains\_\_) for the hash table Map
   ADT implementation.

#. How can you delete items from a hash table that uses chaining for
   collision resolution? How about if open addressing is used? What are
   the special circumstances that must be handled? Implement the ``del``
   method for the ``HashTable`` class.

#. In the hash table map implementation, the hash table size was chosen
   to be 101. If the table gets full, this needs to be increased.
   Re-implement the ``put`` method so that the table will automatically
   resize itself when the loading factor reaches a predetermined value
   (you can decide the value based on your assessment of load versus
   performance).

#. Implement quadratic probing as a rehash technique.

#. Using a random number generator, create a list of 500 integers.
   Perform a benchmark analysis using some of the sorting algorithms
   from this chapter. What is the difference in execution speed?

#. Implement the bubble sort using simultaneous assignment.

#. A bubble sort can be modified to “bubble” in both directions. The
   first pass moves “up” the list, and the second pass moves “down.”
   This alternating pattern continues until no more passes are
   necessary. Implement this variation and describe under what
   circumstances it might be appropriate.

#. Implement the selection sort using simultaneous assignment.

#. Perform a benchmark analysis for a shell sort, using different
   increment sets on the same list.

#. Implement the ``mergeSort`` function without using the slice
   operator.

#. One way to improve the quick sort is to use an insertion sort on
   lists that have a small length (call it the “partition limit”). Why
   does this make sense? Re-implement the quick sort and use it to sort
   a random list of integers. Perform an analysis using different list
   sizes for the partition limit.

#. Implement the median-of-three method for selecting a pivot value as a
   modification to ``quickSort``. Run an experiment to compare the two
   techniques.
