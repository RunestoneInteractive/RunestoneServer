..  Copyright (C)  Brad Miller, David Ranum
    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.


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
