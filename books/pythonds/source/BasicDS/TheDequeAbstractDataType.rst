..  Copyright (C)  Brad Miller, David Ranum
    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


The Deque Abstract Data Type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The deque abstract data type is defined by the following structure and
operations. A deque is structured, as described above, as an ordered
collection of items where items are added and removed from either end,
either front or rear. The deque operations are given below.

-  ``Deque()`` creates a new deque that is empty. It needs no parameters
   and returns an empty deque.

-  ``addFront(item)`` adds a new item to the front of the deque. It
   needs the item and returns nothing.

-  ``addRear(item)`` adds a new item to the rear of the deque. It needs
   the item and returns nothing.

-  ``removeFront()`` removes the front item from the deque. It needs no
   parameters and returns the item. The deque is modified.

-  ``removeRear()`` removes the rear item from the deque. It needs no
   parameters and returns the item. The deque is modified.

-  ``isEmpty()`` tests to see whether the deque is empty. It needs no
   parameters and returns a boolean value.

-  ``size()`` returns the number of items in the deque. It needs no
   parameters and returns an integer.

As an example, if we assume that ``d`` is a deque that has been created
and is currently empty, then Table {dequeoperations} shows the results
of a sequence of deque operations. Note that the contents in front are
listed on the right. It is very important to keep track of the front and
the rear as you move items in and out of the collection as things can
get a bit confusing.

.. _tbl_dequeoperations:

.. table:: **Table 1: Examples of Deque Operations**

    ============================ ============================ ================== 
             **Deque Operation**           **Deque Contents**   **Return Value** 
    ============================ ============================ ================== 
                 ``d.isEmpty()``                       ``[]``           ``True`` 
                ``d.addRear(4)``                      ``[4]``                    
            ``d.addRear('dog')``               ``['dog',4,]``                    
           ``d.addFront('cat')``          ``['dog',4,'cat']``                    
            ``d.addFront(True)``     ``['dog',4,'cat',True]``                    
                    ``d.size()``     ``['dog',4,'cat',True]``              ``4`` 
                 ``d.isEmpty()``     ``['dog',4,'cat',True]``          ``False`` 
              ``d.addRear(8.4)`` ``[8.4,'dog',4,'cat',True]``                    
              ``d.removeRear()``     ``['dog',4,'cat',True]``            ``8.4`` 
             ``d.removeFront()``          ``['dog',4,'cat']``           ``True`` 
    ============================ ============================ ================== 


