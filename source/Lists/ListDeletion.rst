..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

List Deletion
-------------

Using slices to delete list elements can be awkward and therefore error-prone.
Python provides an alternative that is more readable.
The ``del`` statement removes an element from a list by using its position.

.. activecode:: ch09_11
    
    a = ['one', 'two', 'three']
    del a[1]
    print(a)

    alist = ['a', 'b', 'c', 'd', 'e', 'f']
    del alist[1:5]
    print(alist)

As you might expect, ``del`` handles negative indices and causes a runtime
error if the index is out of range.
In addition, you can use a slice as an index for ``del``.
As usual, slices select all the elements up to, but not including, the second
index.


.. note::

    This workspace is provided for your convenience.  You can use this activecode window to try out anything you like.

    .. activecode:: scratch_09_01




.. index:: is operator, objects and values

