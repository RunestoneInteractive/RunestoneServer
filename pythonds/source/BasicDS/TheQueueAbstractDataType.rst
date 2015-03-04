..  Copyright (C)  Brad Miller, David Ranum
    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


The Queue Abstract Data Type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The queue abstract data type is defined by the following structure and
operations. A queue is structured, as described above, as an ordered
collection of items which are added at one end, called the “rear,” and
removed from the other end, called the “front.” Queues maintain a FIFO
ordering property. The queue operations are given below.

-  ``Queue()`` creates a new queue that is empty. It needs no parameters
   and returns an empty queue.

-  ``enqueue(item)`` adds a new item to the rear of the queue. It needs
   the item and returns nothing.

-  ``dequeue()`` removes the front item from the queue. It needs no
   parameters and returns the item. The queue is modified.

-  ``isEmpty()`` tests to see whether the queue is empty. It needs no
   parameters and returns a boolean value.

-  ``size()`` returns the number of items in the queue. It needs no
   parameters and returns an integer.

As an example, if we assume that ``q`` is a queue that has been created
and is currently empty, then :ref:`Table 1 <tbl_queueoperations>` shows the
results of a sequence of queue operations. The queue contents are shown
such that the front is on the right. 4 was the first item enqueued so it
is the first item returned by dequeue.

.. _tbl_queueoperations:

.. table:: **Table 1: Example Queue Operations**

    ============================ ======================== ================== 
             **Queue Operation**       **Queue Contents**   **Return Value** 
    ============================ ======================== ================== 
                 ``q.isEmpty()``                   ``[]``           ``True`` 
                ``q.enqueue(4)``                  ``[4]``                    
            ``q.enqueue('dog')``            ``['dog',4]``                    
             ``q.enqueue(True)``       ``[True,'dog',4]``                    
                    ``q.size()``       ``[True,'dog',4]``              ``3`` 
                 ``q.isEmpty()``       ``[True,'dog',4]``          ``False`` 
              ``q.enqueue(8.4)``   ``[8.4,True,'dog',4]``                    
                 ``q.dequeue()``     ``[8.4,True,'dog']``              ``4`` 
                 ``q.dequeue()``           ``[8.4,True]``          ``'dog'`` 
                    ``q.size()``           ``[8.4,True]``              ``2`` 
    ============================ ======================== ================== 


