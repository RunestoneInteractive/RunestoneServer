..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Glossary
--------

.. glossary::

    sort
        A method that sorts a list in place, changing the contents of the list. It
        return None, not a new list.
        
    sorted
        A function that returns a sorted list, without changing the original.
        
    reverse parameter
        If True, the sorting is done in reverse order.
        
    key parameter
        If a value is specified, it must be a function object that takes one parameter.
        The function will be called once for each item in the list that's getting
        sorted. The return value will be used to decorate the item with a post-it
        note. Values on the post-it notes are used to determine the sort order of
        the items. 

