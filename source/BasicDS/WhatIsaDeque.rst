..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

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


