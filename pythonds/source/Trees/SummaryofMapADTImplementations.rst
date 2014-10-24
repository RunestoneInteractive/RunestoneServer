..  Copyright (C)  Brad Miller, David Ranum
    Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Summary of Map ADT Implementations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Over the past two chapters we have looked at several data structures
that can be used to implement the map abstract data type. A binary
Search on a list, a hash table, a binary search tree, and a balanced
binary search tree. To conclude this section, let’s summarize the
performance of each data structure for the key operations defined by the
map ADT (see :ref:`Table 1 <tab_compare>`).


.. _tab_compare:

.. table:: **Table 1: Comparing the Performance of Different Map Implementations**

    =========== ======================  ============   ==================  ====================
    operation   Sorted List             Hash Table     Binary Search Tree     AVL Tree
    =========== ======================  ============   ==================  ====================
         put    :math:`O(n)`            :math:`O(1)`       :math:`O(n)`    :math:`O(\log_2{n})`   
         get    :math:`O(\log_2{n})`    :math:`O(1)`       :math:`O(n)`    :math:`O(\log_2{n})`   
         in     :math:`O(\log_2{n})`    :math:`O(1)`       :math:`O(n)`    :math:`O(\log_2{n})`   
         del    :math:`O(n))`           :math:`O(1)`       :math:`O(n)`    :math:`O(\log_2{n})`   
    =========== ======================  ============   ==================  ====================
