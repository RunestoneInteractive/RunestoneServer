..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Optional reverse parameter
--------------------------

The sorted function takes some optional parameters (see :ref:`Optional parameters <optional_pararams_chap>`).
The first one is a comparison function. We will not be using it in this course (indeed, in python 3, 
this parameter is not even available any longer). The second optional parameter is a key function, which 
will be described in the next section. The third optional parameter is a Boolean value which 
determines whether to sort the items in reverse order. By default, it is False,
but if you set it to True, the list will be sorted in reverse order.

.. activecode:: sort_3

    L2 = ["Cherry", "Apple", "Blueberry"]
    print(sorted(L2, None, None, True))
    
.. note::

    In order to specify the third optional parameter, we had to provide values for the
    other two optional parameters as well. In this case, we provided the value None
    for both of them. This code would be easier to read if we used the keyword
    technique, like this: ``sorted(L2, reverse=True)``. Unforutnately, specifying
    keyword parameters is not yet supported for the sorted function in this
    online environment. To discourage you from trying to specify a parameter with a keyword and then getting confused
    about why it doesn't work with sorted, I have delayed introduction of 
    keyword parameters entirely. We will learn about them after you start running
    python natively on your computer, when you will have a full implementation of
    python.
    
