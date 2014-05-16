..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

The Bubble Sort
~~~~~~~~~~~~~~~

The **bubble sort** makes multiple passes through a list. It compares
adjacent items and exchanges those that are out of order. Each pass
through the list places the next largest value in its proper place. In
essence, each item “bubbles” up to the location where it belongs.

:ref:`Figure 1 <fig_bubblepass>` shows the first pass of a bubble sort. The shaded
items are being compared to see if they are out of order. If there are
*n* items in the list, then there are :math:`n-1` pairs of items that
need to be compared on the first pass. It is important to note that once
the largest value in the list is part of a pair, it will continually be
moved along until the pass is complete.

.. _fig_bubblepass:

.. figure:: Figures/bubblepass.png
   :align: center

   Figure 1: ``bubbleSort``: The First Pass


At the start of the second pass, the largest value is now in place.
There are :math:`n-1` items left to sort, meaning that there will be
:math:`n-2` pairs. Since each pass places the next largest value in
place, the total number of passes necessary will be :math:`n-1`. After
completing the :math:`n-1` passes, the smallest item must be in the
correct position with no further processing required. :ref:`ActiveCode 1 <lst_bubble>`
shows the complete ``bubbleSort`` function. It takes the list as a
parameter, and modifies it by exchanging items as necessary.

The exchange operation, sometimes called a “swap,” is slightly different
in Python than in most other programming languages. Typically, swapping
two elements in a list requires a temporary storage location (an
additional memory location). A code fragment such as

::

    temp = alist[i]
    alist[i] = alist[j]
    alist[j] = temp

will exchange the `ith` and `jth` items in the list. Without the
temporary storage, one of the values would be overwritten.

In Python, it is possible to perform simultaneous assignment. The
statement ``a,b=b,a`` will result in two assignment statements being
done at the same time (see :ref:`Figure 2 <fig_pythonswap>`). Using simultaneous
assignment, the exchange operation can be done in one statement.

Lines 5-7 in :ref:`ActiveCode 1 <lst_bubble>` perform the exchange of the :math:`i` and
:math:`(i+1)th` items using the three–step procedure described
earlier. Note that we could also have used the simultaneous assignment
to swap the items.

.. _fig_pythonswap:

.. figure:: Figures/swap.png
   :align: center

   Figure 2: Exchanging Two Values in Python

The following activecode example shows the complete ``bubbleSort`` function working on the list
shown above.


.. _lst_bubble:

.. activecode:: lst_bubble
    :caption: The Bubble Sort

    def bubbleSort(alist):
        for passnum in range(len(alist)-1,0,-1):
            for i in range(passnum):
                if alist[i]>alist[i+1]:
                    temp = alist[i]
                    alist[i] = alist[i+1]
                    alist[i+1] = temp

    alist = [54,26,93,17,77,31,44,55,20]
    bubbleSort(alist)
    print(alist)

The following animation shows ``bubbleSort`` in action.

.. animation:: bubble_anim
   :modelfile: sortmodels.js
   :viewerfile: sortviewers.js
   :model: BubbleSortModel
   :viewer: BarViewer

For more detail, CodeLens 1 allows you to step thru the algorithm.

.. codelens:: bubbletrace
    :caption: Tracing the Bubble Sort
    
    def bubbleSort(alist):
        for passnum in range(len(alist)-1,0,-1):
            for i in range(passnum):
                if alist[i]>alist[i+1]:
                    temp = alist[i]
                    alist[i] = alist[i+1]
                    alist[i+1] = temp
    
    alist = [54,26,93,17,77,31,44,55,20]
    bubbleSort(alist)    
    print(alist)       
                    

To analyze the bubble sort, we should note that regardless of how the
items are arranged in the initial list, :math:`n-1` passes will be
made to sort a list of size *n*. :ref:`Table 1 <tbl_bubbleanalysis>` shows the number
of comparisons for each pass. The total number of comparisons is the sum
of the first :math:`n-1` integers. Recall that the sum of the first
*n* integers is :math:`\frac{1}{2}n^{2} + \frac{1}{2}n`. The sum of
the first :math:`n-1` integers is
:math:`\frac{1}{2}n^{2} + \frac{1}{2}n - n`, which is
:math:`\frac{1}{2}n^{2} - \frac{1}{2}n`. This is still
:math:`O(n^{2})` comparisons. In the best case, if the list is already
ordered, no exchanges will be made. However, in the worst case, every
comparison will cause an exchange. On average, we exchange half of the
time.

.. _tbl_bubbleanalysis:

.. table:: **Table 1: Comparisons for Each Pass of Bubble Sort**

    ================= ==================
    **Pass**          **Comparisons**
    ================= ==================
             1         :math:`n-1`
             2         :math:`n-2`
             3         :math:`n-3`
             ...       ...
       :math:`n-1`     :math:`1`
    ================= ==================


A bubble sort is often considered the most inefficient sorting method
since it must exchange items before the final location is known. These
“wasted” exchange operations are very costly. However, because the
bubble sort makes passes through the entire unsorted portion of the
list, it has the capability to do something most sorting algorithms
cannot. In particular, if during a pass there are no exchanges, then we
know that the list must be sorted. A bubble sort can be modified to stop
early if it finds that the list has become sorted. This means that for
lists that require just a few passes, a bubble sort may have an
advantage in that it will recognize the sorted list and stop.
:ref:`ActiveCode 2 <lst_shortbubble>` shows this modification, which is often referred
to as the **short bubble**.

.. _lst_shortbubble:

.. activecode:: lst_shortbubble
    :caption: The Short Bubble Sort

    def shortBubbleSort(alist):
        exchanges = True
        passnum = len(alist)-1
        while passnum > 0 and exchanges:
           exchanges = False
           for i in range(passnum):
               if alist[i]>alist[i+1]:
                   exchanges = True
                   temp = alist[i]
                   alist[i] = alist[i+1]
                   alist[i+1] = temp
           passnum = passnum-1

    alist=[20,30,40,90,50,60,70,80,100,110]
    shortBubbleSort(alist)
    print(alist)
    
Finally, here is ``shortBubbleSort`` in CodeLens (CodeLens 2)..
    
.. codelens:: shortbubbletrace
    :caption: Tracing the Short Bubble Sort

    def shortBubbleSort(alist):
        exchanges = True
        passnum = len(alist)-1
        while passnum > 0 and exchanges:
           exchanges = False
           for i in range(passnum):
               if alist[i]>alist[i+1]:
                   exchanges = True
                   temp = alist[i]
                   alist[i] = alist[i+1]
                   alist[i+1] = temp
           passnum = passnum-1

    alist=[20,30,40,90,50,60,70,80,100,110]
    shortBubbleSort(alist)
    print(alist)
 
.. admonition:: Self Check

   .. mchoicemf:: question_sort_1
       :correct: b
       :answer_a: [1, 9, 19, 7, 3, 10, 13, 15, 8, 12]
       :answer_b: [1, 3, 7, 9, 10, 8, 12, 13, 15, 19]
       :answer_c: [1, 7, 3, 9, 10, 13, 8, 12, 15, 19]
       :answer_d: [1, 9, 19, 7, 3, 10, 13, 15, 8, 12]
       :feedback_a:  This answer represents three swaps.  A pass means that you continue swapping all the way to the end of the list.
       :feedback_b:  Very Good
       :feedback_c: A bubble sort contines to swap numbers up to index position passnum.  But remember that passnum starts at the length of the list - 1.
       :feedback_d: You have been doing an insertion sort, not a bubble sort.

       Suppose you have the following list of numbers to sort: <br>
       [19, 1, 9, 7, 3, 10, 13, 15, 8, 12] which list represents the partially sorted list after three complete passes of bubble sort?
 
