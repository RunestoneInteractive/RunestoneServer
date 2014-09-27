..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Exercises
---------

1. Fill in the parameter list for g so that the invocations of g yield the return values specified

.. actex:: ex_opt_params_1

    def g():
        return 2*x + y + z
    print(g(3))     # should output 10
    print(g(3, 2))  # should output 8
    print(g(3, 2, 1)) #should output 9
 
