..  Copyright (C)  Brad Miller, David Ranum
    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


Lists
-----

Throughout the discussion of basic data structures, we have used Python
lists to implement the abstract data types presented. The list is a
powerful, yet simple, collection mechanism that provides the programmer
with a wide variety of operations. However, not all programming
languages include a list collection. In these cases, the notion of a
list must be implemented by the programmer.

A **list** is a collection of items where each item holds a relative
position with respect to the others. More specifically, we will refer to
this type of list as an unordered list. We can consider the list as
having a first item, a second item, a third item, and so on. We can also
refer to the beginning of the list (the first item) or the end of the
list (the last item). For simplicity we will assume that lists cannot
contain duplicate items.

For example, the collection of integers 54, 26, 93, 17, 77, and 31 might
represent a simple unordered list of exam scores. Note that we have
written them as comma-delimited values, a common way of showing the list
structure. Of course, Python would show this list as
:math:`[54,26,93,17,77,31]`.

