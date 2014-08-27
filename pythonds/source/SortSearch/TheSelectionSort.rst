..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

The Selection Sort
~~~~~~~~~~~~~~~~~~

The **selection sort** improves on the bubble sort by making only one
exchange for every pass through the list. In order to do this, a
selection sort looks for the largest value as it makes a pass and, after
completing the pass, places it in the proper location. As with a bubble
sort, after the first pass, the largest item is in the correct place.
After the second pass, the next largest is in place. This process
continues and requires :math:`n-1` passes to sort *n* items, since the
final item must be in place after the :math:`(n-1)` st pass.

:ref:`Figure 3 <fig_selectionsort>` shows the entire sorting process. On each pass,
the largest remaining item is selected and then placed in its proper
location. The first pass places 93, the second pass places 77, the third
places 55, and so on. The function is shown in
:ref:`ActiveCode 1 <lst_selectionsortcode>`.

.. _fig_selectionsort:

.. figure:: Figures/selectionsortnew.png
   :align: center

   
   Figure 3: ``selectionSort``


.. _lst_selectionsortcode:


.. activecode:: lst_selectionsortcode
    :caption: Selection Sort

    def selectionSort(alist):
       for fillslot in range(len(alist)-1,0,-1):
           positionOfMax=0
           for location in range(1,fillslot+1):
               if alist[location]>alist[positionOfMax]:
                   positionOfMax = location

           temp = alist[fillslot]
           alist[fillslot] = alist[positionOfMax]
           alist[positionOfMax] = temp

    alist = [54,26,93,17,77,31,44,55,20]
    selectionSort(alist)
    print(alist)

.. animation:: selection_anim
   :modelfile: sortmodels.js
   :viewerfile: sortviewers.js
   :model: SelectionSortModel
   :viewer: BarViewer
   

.. For more detail, CodeLens 3 allows you to step through the algorithm.
..
..
.. .. codelens:: selectionsortcodetrace
..     :caption: Tracing the Selection Sort
..
..     def selectionSort(alist):
..        for fillslot in range(len(alist)-1,0,-1):
..            positionOfMax=0
..            for location in range(1,fillslot+1):
..                if alist[location]>alist[positionOfMax]:
..                    positionOfMax = location
..
..            temp = alist[fillslot]
..            alist[fillslot] = alist[positionOfMax]
..            alist[positionOfMax] = temp
..
..     alist = [54,26,93,17,77,31,44,55,20]
..     selectionSort(alist)
..     print(alist)

You may see that the selection sort makes the same number of comparisons
as the bubble sort and is therefore also :math:`O(n^{2})`. However,
due to the reduction in the number of exchanges, the selection sort
typically executes faster in benchmark studies. In fact, for our list,
the bubble sort makes 20 exchanges, while the selection sort makes only
8.


.. admonition:: Self Check

   .. mchoicemf:: question_sort_2
      :correct: d
      :answer_a: [7, 11, 12, 1, 6, 14, 8, 18, 19, 20]
      :answer_b: [7, 11, 12, 14, 19, 1, 6, 18, 8, 20]
      :answer_c: [11, 7, 12, 13, 1, 6, 8, 18, 19, 20]
      :answer_d: [11, 7, 12, 14, 8, 1, 6, 18, 19, 20]
      :feedback_a: Selection sort is similar to bubble sort (which you appear to have done) but uses fewer swaps
      :feedback_b: This looks like an insertion sort.
      :feedback_c: This one looks similar to the correct answer but instead of swapping the numbers have been shifted to the left to make room for the correct numbers.
      :feedback_d: Selection sort improves upon bubble sort by making fewer swaps.

      Suppose you have the following list of numbers to sort:
      [11, 7, 12, 14, 19, 1, 6, 18, 8, 20] which list represents the partially sorted list after three complete passes of selection sort?


