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


    aliases
        Multiple variables that contain references to the same object.

    clone
        To create a new object that has the same value as an existing object.
        Copying a reference to an object creates an alias but doesn't clone the
        object.

    delimiter
        A character or string used to indicate where a string should be split.

    element
        One of the values in a list (or other sequence). The bracket operator
        selects elements of a list.

    index
        An integer variable or value that indicates an element of a list.

    list
        A collection of objects, where each object is identified by an index.
        Like other types ``str``, ``int``, ``float``, etc. there is also a
        ``list`` type-converter function that tries to turn its argument into a 
        list. 

    list traversal
        The sequential accessing of each element in a list.

    modifier
        A function which changes its arguments inside the function body. Only
        mutable types can be changed by modifiers.
        
    mutable data type
        A data type in which the elements can be modified. All mutable types
        are compound types. Lists are mutable data types; strings are not.

    nested list
        A list that is an element of another list.

    object
        A thing to which a variable can refer.
        
    pattern
        A sequence of statements, or a style of coding something that has
        general applicability in a number of different situations.  Part of
        becoming a mature Computer Scientist is to learn and establish the
        patterns and algorithms that form your toolkit.  Patterns often 
        correspond to your "mental chunking".   


    pure function
        A function which has no side effects. Pure functions only make changes
        to the calling program through their return values.

    sequence
        Any of the data types that consist of an ordered collection of elements, with
        each element identified by an index.
        
    side effect
        A change in the state of a program made by calling a function that is
        not a result of reading the return value from the function. Side
        effects can only be produced by modifiers.


    tuple
	    A sequential collection of items, similar to a list.  Any python object can be an element of a tuple.  However, unlike a list, tuples are immutable.
