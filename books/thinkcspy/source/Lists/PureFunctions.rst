..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. qnum::
   :prefix: list-19-
   :start: 1

Pure Functions
--------------


A **pure function** does not produce side effects. It communicates with the
calling program only through parameters (which it does not modify) and a return
value. Here is the ``doubleStuff`` function from the previous section written as a pure function.
To use the pure function version of ``double_stuff`` to modify ``things``,
you would assign the return value back to ``things``.


.. activecode:: ch09_mod2
    
    def doubleStuff(a_list):
        """ Return a new list in which contains doubles of the elements in a_list. """
        new_list = []
        for value in a_list:
            new_elem = 2 * value
            new_list.append(new_elem)
        return new_list
    
    things = [2, 5, 9]
    print(things)
    things = doubleStuff(things)
    print(things)

Once again, codelens helps us to see the actual references and objects as they are passed and returned.

.. codelens:: ch09_mod3

    def doubleStuff(a_list):
        """ Return a new list in which contains doubles of the elements in a_list. """
        new_list = []
        for value in a_list:
            new_elem = 2 * value
            new_list.append(new_elem)
        return new_list

    things = [2, 5, 9]
    things = doubleStuff(things)



