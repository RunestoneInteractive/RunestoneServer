..  Copyright (C)  Brad Miller, David Ranum
    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


The Ordered List Abstract Data Type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We will now consider a type of list known as an ordered list. For
example, if the list of integers shown above were an ordered list
(ascending order), then it could be written as 17, 26, 31, 54, 77, and
93. Since 17 is the smallest item, it occupies the first position in the
list. Likewise, since 93 is the largest, it occupies the last position.

The structure of an ordered list is a collection of items where each
item holds a relative position that is based upon some underlying
characteristic of the item. The ordering is typically either ascending
or descending and we assume that list items have a meaningful comparison
operation that is already defined. Many of the ordered list operations
are the same as those of the unordered list.

-  ``OrderedList()`` creates a new ordered list that is empty. It needs
   no parameters and returns an empty list.

-  ``add(item)`` adds a new item to the list making sure that the order
   is preserved. It needs the item and returns nothing. Assume the item
   is not already in the list.

-  ``remove(item)`` removes the item from the list. It needs the item
   and modifies the list. Assume the item is present in the list.

-  ``search(item)`` searches for the item in the list. It needs the item
   and returns a boolean value.

-  ``isEmpty()`` tests to see whether the list is empty. It needs no
   parameters and returns a boolean value.

-  ``size()`` returns the number of items in the list. It needs no
   parameters and returns an integer.

-  ``index(item)`` returns the position of item in the list. It needs
   the item and returns the index. Assume the item is in the list.

-  ``pop()`` removes and returns the last item in the list. It needs
   nothing and returns an item. Assume the list has at least one item.

-  ``pop(pos)`` removes and returns the item at position pos. It needs
   the position and returns the item. Assume the item is in the list.

