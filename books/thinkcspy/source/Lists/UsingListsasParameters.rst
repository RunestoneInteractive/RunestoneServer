..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. qnum::
   :prefix: list-18-
   :start: 1

Using Lists as Parameters
-------------------------

Functions which take lists as arguments and change them during execution are
called **modifiers** and the changes they make are called **side effects**.
Passing a list as an argument actually passes a reference to the list, not a
copy of the list. Since lists are mutable, changes made to the 
elements referenced by the parameter change
the same list that the argument is referencing. 
For example, the function below takes a list as an
argument and multiplies each element in the list by 2:

.. activecode:: chp09_parm1
    
    def doubleStuff(aList):
        """ Overwrite each element in aList with double its value. """
        for position in range(len(aList)):
            aList[position] = 2 * aList[position]

    things = [2, 5, 9]
    print(things)
    doubleStuff(things)
    print(things)
    


The parameter ``aList`` and the variable ``things`` are aliases for the
same object.  

.. image:: Figures/references4.png
   :alt: State snapshot for multiple references to a list as a parameter
   
Since the list object is shared by two references, there is only one copy.
If a function modifies the elements of a list parameter, the caller sees the change since the change
is occurring to the original.

This can be easily seen in codelens.  Note that after the call to ``doubleStuff``, the formal parameter ``aList`` refers to the same object as the actual parameter ``things``.  There is only one copy of the list object itself.


.. codelens:: chp09_parm1_trace
    
    def doubleStuff(aList):
        """ Overwrite each element in aList with double its value. """
        for position in range(len(aList)):
            aList[position] = 2 * aList[position]

    things = [2, 5, 9]

    doubleStuff(things)



.. index:: side effect, modifier

.. _pure-func-mod:

