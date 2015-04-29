..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Objects and References
----------------------

If we execute these assignment statements,

.. sourcecode:: python
    
    a = "banana"
    b = "banana"

we know that ``a`` and ``b`` will refer to a string with the letters
``"banana"``. But we don't know yet whether they point to the *same* string.

There are two possible ways the Python interpreter could arrange its internal states:

.. image:: Figures/refdiag1.png
   :alt: List illustration 

or


.. image:: Figures/refdiag2.png
   :alt: List illustration

In one case, ``a`` and ``b`` refer to two different string objects that have the same
value. In the second case, they refer to the same object. Remember that an object is something a variable can
refer to.

We can test whether two names refer to the same object using the *is*
operator.  The *is* operator will return true if the two references are to the same object.  In other words, the references are the same.  Try our example from above.

.. activecode:: chp09_is1

    a = "banana"
    b = "banana"

    print a is b

The answer is ``True``.  This tells us that both ``a`` and ``b`` refer to the same object, and that it
is the second of the two reference diagrams that describes the relationship. 
Since strings are *immutable*, Python optimizes resources by making two names
that refer to the same string value refer to the same object.

This is not the case with lists.  Consider the following example.  Here, ``a`` and ``b`` refer to two different lists, each of which happens to have the same element values.

.. activecode:: chp09_is2
    
    a = [81,82,83]
    b = [81,82,83]

    print a is b

    print a == b  

The reference diagram for this example looks like this:

.. image:: Figures/refdiag3.png
   :alt: Reference diagram for equal different lists 

``a`` and ``b`` have the same value but do not refer to the same object.

There is one other important thing to notice about this reference diagram.  The variable ``a`` is a reference to a **collection of references**.  Those references actually refer to the integer values in the list.  In other words, a list is a collection of references to objects.  Interestingly, even though ``a`` and ``b`` are two different lists (two different collections of references), the integer object ``81`` is shared by both.  Like strings, integers are also immutable so Python optimizes and lets everyone share the same object.

Here is the example in codelens.  Pay particular attention to the `id` values.

.. codelens:: chp09_istrace
    :showoutput:
    
    a = [81,82,83]
    b = [81,82,83]

    print a is b
    print a == b

.. index:: aliases
