..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Implementing a Queue in Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is again appropriate to create a new class for the implementation of
the abstract data type queue. As before, we will use the power and
simplicity of the list collection to build the internal representation
of the queue.

We need to decide which end of the list to use as the rear and which to
use as the front. The implementation shown in :ref:`Listing 1 <lst_queuecode>`
assumes that the rear is at position 0 in the list. This allows us to
use the ``insert`` function on lists to add new elements to the rear of
the queue. The ``pop`` operation can be used to remove the front element
(the last element of the list). Recall that this also means that enqueue
will be O(n) and dequeue will be O(1). 

.. _lst_queuecode:

**Listing 1**

::

    class Queue:
        def __init__(self):
            self.items = []

        def isEmpty(self):
            return self.items == []

        def enqueue(self, item):
            self.items.insert(0,item)

        def dequeue(self):
            return self.items.pop()

        def size(self):
            return len(self.items)

CodeLens 1 shows the ``Queue`` class in
action as we perform the sequence of operations from
:ref:`Table 1 <tbl_queueoperations>`.

.. codelens:: ququeuetest
   :caption: Example Queue Operations

   class Queue:
       def __init__(self):
           self.items = []

       def isEmpty(self):
           return self.items == []

       def enqueue(self, item):
           self.items.insert(0,item)

       def dequeue(self):
           return self.items.pop()

       def size(self):
           return len(self.items)

   q=Queue()
   
   q.enqueue(4)
   q.enqueue('dog')
   q.enqueue(True)
   print(q.size())


Further manipulation of this queue would give the following results:


::

    >>> q.size()
    3
    >>> q.isEmpty()
    False
    >>> q.enqueue(8.4)
    >>> q.dequeue()
    4
    >>> q.dequeue()
    'dog'
    >>> q.size()
    2

.. admonition:: Self Check

   .. mchoicemf:: queue_1
      :correct: b
      :iscode:
      :answer_a: 'hello', 'dog'
      :answer_b: 'dog', 3
      :answer_c: 'hello', 3
      :answer_d: 'hello', 'dog', 3
      :feedback_a: Remember the first thing added to the queue is the first thing removed.  FIFO
      :feedback_b: Yes, first in first out means that hello is gone
      :feedback_c: Queues, and Stacks are both data structures where you can only access the first and the last thing.
      :feedback_d: Ooops, maybe you missed the dequeue call at the end?

      Suppose you have the following series of queue operations.

      ::
      
          q = Queue()
          q.enqueue('hello')
          q.enqueue('dog')
          q.enqueue(3)
          q.dequeue()

      What items are left on the queue?

