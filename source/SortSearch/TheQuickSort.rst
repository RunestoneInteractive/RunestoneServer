..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

The Quick Sort
~~~~~~~~~~~~~~

The **quick sort** uses divide and conquer to gain the same advantages
as the merge sort, while not using additional storage. As a trade-ÁÁ off,
however, it is possible that the list may not be divided in half. When
this happens, we will see that performance is diminished.

A quick sort first selects a value, which is called the **pivot value**.
Although there are many different ways to choose the pivot value, we
will simply use the first item in the list. The role of the pivot value
is to assist with splitting the list. The actual position where the
pivot value belongs in the final sorted list, commonly called the
**split point**, will be used to divide the list for subsequent calls to
the quick sort.

:ref:`Figure 12 <fig_splitvalue>` shows that 54 will serve as our first pivot value.
Since we have looked at this example a few times already, we know that
54 will eventually end up in the position currently holding 31. The
**partition** process will happen next. It will find the split point and
at the same time move other items to the appropriate side of the list,
either less than or greater than the pivot value.

.. _fig_splitvalue:


.. figure:: Figures/firstsplit.png
   :align: center

   Figure 12: The First Pivot Value for a Quick Sort





Partitioning begins by locating two position markers—let’s call them
``leftmark`` and ``rightmark``—at the beginning and end of the remaining
items in the list (positions 1 and 8 in :ref:`Figure 13 <fig_partitionA>`). The goal
of the partition process is to move items that are on the wrong side
with respect to the pivot value while also converging on the split
point. :ref:`Figure 13 <fig_partitionA>` shows this process as we locate the position
of 54.

.. _fig_partitionA:

.. figure:: Figures/partitionA.png
   :align: center

   Figure 13: Finding the Split Point for 54

We begin by incrementing ``leftmark`` until we locate a value that is
greater than the pivot value. We then decrement ``rightmark`` until we
find a value that is less than the pivot value. At this point we have
discovered two items that are out of place with respect to the eventual
split point. For our example, this occurs at 93 and 20. Now we can
exchange these two items and then repeat the process again.

At the point where ``rightmark`` becomes less than ``leftmark``, we
stop. The position of ``rightmark`` is now the split point. The pivot
value can be exchanged with the contents of the split point and the
pivot value is now in place (:ref:`Figure 14 <fig_partitionB>`). In addition, all the
items to the left of the split point are less than the pivot value, and
all the items to the right of the split point are greater than the pivot
value. The list can now be divided at the split point and the quick sort
can be invoked recursively on the two halves.

.. _fig_partitionB:

.. figure:: Figures/partitionB.png
   :align: center

   Figure 14: Completing the Partition Process to Find the Split Point for 54


The ``quickSort`` function shown in :ref:`CodeLens 7 <lst_quick>` invokes a recursive
function, ``quickSortHelper``. ``quickSortHelper`` begins with the same
base case as the merge sort. If the length of the list is less than or
equal to one, it is already sorted. If it is greater, then it can be
partitioned and recursively sorted. The ``partition`` function
implements the process described earlier.

.. _lst_quick:

.. activecode:: lst_quick
    :caption: Quick Sort

    def quickSort(alist):
       quickSortHelper(alist,0,len(alist)-1)

    def quickSortHelper(alist,first,last):
       if first<last:

           splitpoint = partition(alist,first,last)

           quickSortHelper(alist,first,splitpoint-1)
           quickSortHelper(alist,splitpoint+1,last)


    def partition(alist,first,last):
       pivotvalue = alist[first]

       leftmark = first+1
       rightmark = last

       done = False
       while not done:

           while leftmark <= rightmark and \
                   alist[leftmark] <= pivotvalue:
               leftmark = leftmark + 1

           while alist[rightmark] >= pivotvalue and \
                   rightmark >= leftmark:
               rightmark = rightmark -1

           if rightmark < leftmark:
               done = True
           else:
               temp = alist[leftmark]
               alist[leftmark] = alist[rightmark]
               alist[rightmark] = temp

       temp = alist[first]
       alist[first] = alist[rightmark]
       alist[rightmark] = temp


       return rightmark

    alist = [54,26,93,17,77,31,44,55,20]
    quickSort(alist)
    print(alist)



.. animation:: quick_anim
   :modelfile: sortmodels.js
   :viewerfile: sortviewers.js
   :model: QuickSortModel
   :viewer: BarViewer


For more detail, CodeLens 7 lets you step thru the algorithm.

.. codelens:: quicktrace
    :caption: Tracing the Quick Sort

    def quickSort(alist):
       quickSortHelper(alist,0,len(alist)-1)

    def quickSortHelper(alist,first,last):
       if first<last:

           splitpoint = partition(alist,first,last)

           quickSortHelper(alist,first,splitpoint-1)
           quickSortHelper(alist,splitpoint+1,last)


    def partition(alist,first,last):
       pivotvalue = alist[first]

       leftmark = first+1
       rightmark = last

       done = False
       while not done:

           while leftmark <= rightmark and \
                   alist[leftmark] <= pivotvalue:
               leftmark = leftmark + 1

           while alist[rightmark] >= pivotvalue and \
                   rightmark >= leftmark:
               rightmark = rightmark -1

           if rightmark < leftmark:
               done = True
           else:
               temp = alist[leftmark]
               alist[leftmark] = alist[rightmark]
               alist[rightmark] = temp

       temp = alist[first]
       alist[first] = alist[rightmark]
       alist[rightmark] = temp


       return rightmark

    alist = [54,26,93,17,77,31,44,55,20]
    quickSort(alist)
    print(alist)

To analyze the ``quickSort`` function, note that for a list of length
*n*, if the partition always occurs in the middle of the list, there
will again be :math:`\log n` divisions. In order to find the split
point, each of the *n* items needs to be checked against the pivot
value. The result is :math:`n\log n`. In addition, there is no need
for additional memory as in the merge sort process.

Unfortunately, in the worst case, the split points may not be in the
middle and can be very skewed to the left or the right, leaving a very
uneven division. In this case, sorting a list of *n* items divides into
sorting a list of 0 items and a list of :math:`n-1` items. Then
sorting a list of :math:`n-1` divides into a list of size 0 and a list
of size :math:`n-2`, and so on. The result is an :math:`O(n^{2})`
sort with all of the overhead that recursion requires.

We mentioned earlier that there are different ways to choose the pivot
value. In particular, we can attempt to alleviate some of the potential
for an uneven division by using a technique called **median of three**.
To choose the pivot value, we will consider the first, the middle, and
the last element in the list. In our example, those are 54, 77, and 20.
Now pick the median value, in our case 54, and use it for the pivot
value (of course, that was the pivot value we used originally). The idea
is that in the case where the the first item in the list does not belong
toward the middle of the list, the median of three will choose a better
“middle” value. This will be particularly useful when the original list
is somewhat sorted to begin with. We leave the implementation of this
pivot value selection as an exercise.

.. admonition:: Self Check

   .. mchoicemf:: question_sort_7
      :correct: d
      :answer_a: [9, 3, 10, 13, 12]
      :answer_b: [9, 3, 10, 13, 12, 14]
      :answer_c: [9, 3, 10, 13, 12, 14, 17, 16, 15, 19]
      :answer_d: [9, 3, 10, 13, 12, 14, 19, 16, 15, 17]
      :feedback_a: It's important to remember that quicksort works on the entire list and sorts it in place.
      :feedback_b: Remember quicksort works on the entire list and sorts it in place.
      :feedback_c: The first partitioning works on the entire list, and the second partitioning works on the left partition not the right.
      :feedback_d: The first partitioning works on the entire list, and the second partitioning works on the left partition.

      Given the following list of numbers [14, 17, 13, 15, 19, 10, 3, 16, 9, 12] which answer shows the contents of the list after the second partitioning according to the quicksort algorithm?

   .. mchoicemf:: question_sort_8
       :correct: b
       :answer_a: 1
       :answer_b: 9
       :answer_c: 16
       :answer_d: 19
       :feedback_a: The three numbers used in selecting the pivot are 1, 9, 19.  1 is not the median, and would be a very bad choice for the pivot since it is the smallest number in the list.
       :feedback_b:  Good job.
       :feedback_c: although 16 would be the median of 1, 16, 19 the middle is at len(list) // 2.
       :feedback_d: the three numbers used in selecting the pivot are 1, 9, 19.  9 is the median.  19 would be a bad choice since it is almost the largest.

       Given the following list of numbers [1, 20, 11, 5, 2, 9, 16, 14, 13, 19] what would be the first pivot value using the median of 3 method?



   .. mchoicema:: question_sort_9
       :answer_a: Shell Sort
       :answer_b: Quick Sort
       :answer_c: Merge Sort
       :answer_d: Insertion Sort
       :correct: c
       :feedback_a: Shell sort is about ``n^1.5``
       :feedback_b: Quick sort can be O(n log n), but if the pivot points are not well chosen and the list is just so, it can be O(n^2).
       :feedback_c: Merge Sort is the only guaranteed O(n log n) even in the worst case.  The cost is that merge sort uses more memory.
       :feedback_d: Insertion sort is ``O(n^2)``

       Which of the following sort algorithms are guaranteed to be O(n log n) even in the worst case?
