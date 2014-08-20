..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Summary
-------

-  A sequential search is :math:`O(n)` for ordered and unordered
   lists.

-  A binary search of an ordered list is :math:`O(\log n)` in the
   worst case.

-  Hash tables can provide constant time searching.

-  A bubble sort, a selection sort, and an insertion sort are
   :math:`O(n^{2})` algorithms.

-  A shell sort improves on the insertion sort by sorting incremental
   sublists. It falls between :math:`O(n)` and :math:`O(n^{2})`.

-  A merge sort is :math:`O(n \log n)`, but requires additional space
   for the merging process.

-  A quick sort is :math:`O(n \log n)`, but may degrade to
   :math:`O(n^{2})` if the split points are not near the middle of the
   list. It does not require additional space.

