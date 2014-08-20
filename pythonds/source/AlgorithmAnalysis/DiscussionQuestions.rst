..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Discussion Questions
--------------------

#. Give the Big-O performance of the following code fragment:

   ::

       for i in range(n):
          for j in range(n):
             k = 2 + 2

#. Give the Big-O performance of the following code fragment:

   ::

       for i in range(n):
            k = 2 + 2

#. Give the Big-O performance of the following code fragment:

   ::

       i = n
       while i > 0:
          k = 2 + 2
          i = i // 2

#. Give the Big-O performance of the following code fragment:

   ::

       for i in range(n):
          for j in range(n):
             for k in range(n):
                k = 2 + 2

#. Give the Big-O performance of the following code fragment:

   ::

       i = n
       while i > 0:
          k = 2 + 2
          i = i // 2

#. Give the Big-O performance of the following code fragment:

   ::

       for i in range(n):
          k = 2 + 2
       for j in range(n):
          k = 2 + 2
       for k in range(n):
          k = 2 + 2
