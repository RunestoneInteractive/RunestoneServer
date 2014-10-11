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

The sorted function takes some optional parameters (see :ref:`Optional parameters <optional_params_chap>`).
The first one is a comparison function. We will not be using it in this course (indeed, in python 3, 
this parameter is not even available any longer). The second optional parameter is a key function, which 
will be described in the next section. The third optional parameter is a Boolean value which 
determines whether to sort the items in reverse order. By default, it is False,
but if you set it to True, the list will be sorted in reverse order.

.. activecode:: sort_3

    L2 = ["Cherry", "Apple", "Blueberry"]
    print sorted(L2, reverse = True)
    
.. note::

    This is a situation where it is convenient to use the keyword mechanism for providing optional parameters. It is possible to provide the value True for the reverse parameter without naming that parameter, but then we would have to provide values for the second and third parameters as well rather than allowing the default parameters to be used. We would have had to write ``sorted(L2, None, None, True)``. That's a lot harder for humans to read and understand.
