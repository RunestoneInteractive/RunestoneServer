..  Copyright (C)  Brad Miller, David Ranum
    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


What Is a Deque?
~~~~~~~~~~~~~~~~

A **deque**, also known as a double-ended queue, is an ordered
collection of items similar to the queue. It has two ends, a front and a
rear, and the items remain positioned in the collection. What makes a
deque different is the unrestrictive nature of adding and removing
items. New items can be added at either the front or the rear. Likewise,
existing items can be removed from either end. In a sense, this hybrid
linear structure provides all the capabilities of stacks and queues in a
single data structure. :ref:`Figure 1 <fig_basicdeque>` shows a deque of Python
data objects.

It is important to note that even though the deque can assume many of
the characteristics of stacks and queues, it does not require the LIFO
and FIFO orderings that are enforced by those data structures. It is up
to you to make consistent use of the addition and removal operations.

.. _fig_basicdeque:

.. figure:: Figures/basicdeque.png
   :align: center

   Figure 1: A Deque of Python Data Objects


