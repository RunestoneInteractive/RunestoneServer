..  Copyright (C)  Brad Miller, David Ranum
    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


The Unordered List Abstract Data Type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The structure of an unordered list, as described above, is a collection
of items where each item holds a relative position with respect to the
others. Some possible unordered list operations are given below.

-  ``List()`` creates a new list that is empty. It needs no parameters
   and returns an empty list.

-  ``add(item)`` adds a new item to the list. It needs the item and
   returns nothing. Assume the item is not already in the list.

-  ``remove(item)`` removes the item from the list. It needs the item
   and modifies the list. Assume the item is present in the list.

-  ``search(item)`` searches for the item in the list. It needs the item
   and returns a boolean value.

-  ``isEmpty()`` tests to see whether the list is empty. It needs no
   parameters and returns a boolean value.

-  ``size()`` returns the number of items in the list. It needs no
   parameters and returns an integer.

-  ``append(item)`` adds a new item to the end of the list making it the
   last item in the collection. It needs the item and returns nothing.
   Assume the item is not already in the list.

-  ``index(item)`` returns the position of item in the list. It needs
   the item and returns the index. Assume the item is in the list.

-  ``insert(pos,item)`` adds a new item to the list at position pos. It
   needs the item and returns nothing. Assume the item is not already in
   the list and there are enough existing items to have position pos.

-  ``pop()`` removes and returns the last item in the list. It needs
   nothing and returns an item. Assume the list has at least one item.

-  ``pop(pos)`` removes and returns the item at position pos. It needs
   the position and returns the item. Assume the item is in the list.

