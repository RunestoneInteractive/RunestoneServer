..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Binary Heap Operations
~~~~~~~~~~~~~~~~~~~~~~

The basic operations we will implement for our binary heap are as
follows:

-  ``BinaryHeap()`` creates a new, empty, binary heap.

-  ``insert(k)`` adds a new item to the heap.

-  ``findMin()`` returns the item with the minimum key value, leaving
   item in the heap.

-  ``delMin()`` returns the item with the minimum key value, removing
   the item from the heap.

-  ``isEmpty()`` returns true if the heap is empty, false otherwise.

-  ``size()`` returns the number of items in the heap.

-  ``buildHeap(list)`` builds a new heap from a list of keys.

:ref:`ActiveCode 1 <lst_heap1>` demonstrates the use of some of the binary
heap methods.  Notice that no matter the order that we add items to the heap, the smallest
is removed each time.  We will now turn our attention to creating an implementation for this idea.

.. _lst_heap1:


.. activecode:: heap1
    :caption: Using the Binary Heap
    :nocodelens:
    
    from pythonds.trees.binheap import BinHeap
    
    bh = BinHeap()
    bh.insert(5)
    bh.insert(7)
    bh.insert(3)
    bh.insert(11)
    
    print(bh.delMin())

    print(bh.delMin())

    print(bh.delMin())

    print(bh.delMin())


