..  Copyright (C)  Brad Miller, David Ranum
    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


The Stack Abstract Data Type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The stack abstract data type is defined by the following structure and
operations. A stack is structured, as described above, as an ordered
collection of items where items are added to and removed from the end
called the “top.” Stacks are ordered LIFO. The stack operations are
given below.

-  ``Stack()`` creates a new stack that is empty. It needs no parameters
   and returns an empty stack.

-  ``push(item)`` adds a new item to the top of the stack. It needs the
   item and returns nothing.

-  ``pop()`` removes the top item from the stack. It needs no parameters
   and returns the item. The stack is modified.

-  ``peek()`` returns the top item from the stack but does not remove
   it. It needs no parameters. The stack is not modified.

-  ``isEmpty()`` tests to see whether the stack is empty. It needs no
   parameters and returns a boolean value.

-  ``size()`` returns the number of items on the stack. It needs no
   parameters and returns an integer.

For example, if ``s`` is a stack that has been created and starts out
empty, then :ref:`Table 1 <tbl_stackops>` shows the results of a sequence of
stack operations. Under stack contents, the top item is listed at the
far right.

.. _tbl_stackops:

.. table:: **Table 1: Sample Stack Operations**

    ============================ ======================== ==================
             **Stack Operation**       **Stack Contents**   **Return Value**
    ============================ ======================== ==================
                 ``s.isEmpty()``                   ``[]``           ``True``
                   ``s.push(4)``                  ``[4]``
               ``s.push('dog')``            ``[4,'dog']``
                    ``s.peek()``            ``[4,'dog']``          ``'dog'``
                ``s.push(True)``       ``[4,'dog',True]``
                    ``s.size()``       ``[4,'dog',True]``              ``3``
                 ``s.isEmpty()``       ``[4,'dog',True]``          ``False``
                 ``s.push(8.4)``   ``[4,'dog',True,8.4]``
                     ``s.pop()``       ``[4,'dog',True]``            ``8.4``
                     ``s.pop()``            ``[4,'dog']``           ``True``
                    ``s.size()``            ``[4,'dog']``              ``2``
    ============================ ======================== ==================


