..  Copyright (C)  Brad Miller, David Ranum
    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


Programming Exercises
---------------------

#. Extend the ``buildParseTree`` function to handle mathematical
   expressions that do not have spaces between every character.

#. Modify the ``buildParseTree`` and ``evaluate`` functions to handle
   boolean statements (and, or, and not). Remember that “not” is a unary
   operator, so this will complicate your code somewhat.

#. Using the ``findSuccessor`` method, write a non-recursive inorder
   traversal for a binary search tree.

#. Modify the code for a binary search tree to make it threaded. Write a
   non-recursive inorder traversal method for the threaded binary search
   tree. A threaded binary tree maintains a reference from each node to
   its successor.

#. Modify our implementation of the binary search tree so that it
   handles duplicate keys properly. That is, if a key is already in the
   tree then the new payload should replace the old rather than add
   another node with the same key.

#. Create a binary heap with a limited heap size. In other words, the
   heap only keeps track of the ``n`` most important items. If the heap
   grows in size to more than ``n`` items the least important item is
   dropped.

#. Clean up the ``printexp`` function so that it does not include an
   ‘extra’ set of parentheses around each number.

#. Using the ``buildHeap`` method, write a sorting function that can
   sort a list in :math:`O(n\log{n})` time.

#. Write a function that takes a parse tree for a mathematical
   expression and calculates the derivative of the expression with
   respect to some variable.

#. Implement a binary heap as a max heap.

#. Using the ``BinaryHeap`` class, implement a new class called
   ``PriorityQueue``. Your ``PriorityQueue`` class should implement the
   constructor, plus the ``enqueue`` and ``dequeue`` methods.

