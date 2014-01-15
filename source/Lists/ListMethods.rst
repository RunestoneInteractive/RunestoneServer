..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

List Methods
------------

The dot operator can also be used to access built-in methods of list objects.  
``append`` is a list method which adds the argument passed to it to the end of
the list. Continuing with this example, we show several other list methods.  Many of them are
easy to understand.  

.. activecode:: chp09_meth1

    mylist = []
    mylist.append(5)
    mylist.append(27)
    mylist.append(3)
    mylist.append(12)
    print(mylist)

    mylist.insert(1, 12)
    print(mylist)
    print(mylist.count(12))

    print(mylist.index(3))
    print(mylist.count(5))

    mylist.reverse()
    print(mylist)

    mylist.sort()
    print(mylist)

    mylist.remove(5)
    print(mylist)

    lastitem = mylist.pop()
    print(lastitem)
    print(mylist)

There are two ways to use the ``pop`` method.  The first, with no parameter, will remove and return the
last item of the list.  If you provide a parameter for the position, ``pop`` will remove and return the
item at that position.  Either way the list is changed.

The following table provides a summary of the list methods shown above.  The column labeled
`result` gives an explanation as to what the return value is as it relates to the new value of the list.  The word
**mutator** means that the list is changed by the method but nothing is returned (actually ``None`` is returned).  A **hybrid** method is one that not only changes the list but also returns a value as its result.  Finally, if the result is simply a return, then the list
is unchanged by the method.

Be sure
to experiment with these methods to gain a better understanding of what they do.




==========  ==============  ============  ================================================
Method      Parameters       Result       Description
==========  ==============  ============  ================================================
append      item            mutator       Adds a new item to the end of a list
insert      position, item  mutator       Inserts a new item at the position given
pop         none            hybrid        Removes and returns the last item
pop         position        hybrid        Removes and returns the item at position
sort        none            mutator       Modifies a list to be sorted
reverse     none            mutator       Modifies a list to be in reverse order
index       item            return idx    Returns the position of first occurrence of item
count       item            return ct     Returns the number of occurrences of item
remove      item            mutator       Removes the first occurrence of item
==========  ==============  ============  ================================================


Details for these and others
can be found in the `Python Documentation <http://docs.python.org/py3k/library/stdtypes.html#sequence-types-str-bytes-bytearray-list-tuple-range>`_.

It is important to remember that methods like ``append``, ``sort``, 
and ``reverse`` all return ``None``.  This means that re-assigning ``mylist`` to the result of sorting ``mylist`` will result in losing the entire list.  Calls like these will likely never appear as part of an assignment statement (see line 8 below).

.. activecode:: chp09_meth2

    mylist = []
    mylist.append(5)
    mylist.append(27)
    mylist.append(3)
    mylist.append(12)
    print(mylist)

    mylist = mylist.sort()   #probably an error
    print(mylist)

**Check your understanding**

.. mchoicemf:: test_question9_13_1
   :answer_a: [4,2,8,6,5,False,True]
   :answer_b: [4,2,8,6,5,True,False]
   :answer_c: [True,False,4,2,8,6,5]
   :correct: b
   :feedback_a: True was added first, then False was added last.
   :feedback_b: Yes, each item is added to the end of the list.
   :feedback_c: append adds at the end, not the beginning.
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [4,2,8,6,5]
     alist.append(True)
     alist.append(False)
     print(alist)



.. mchoicemf:: test_question9_13_2
   :answer_a: [False,4,2,True,8,6,5]
   :answer_b: [4,False,True,2,8,6,5]
   :answer_c: [False,2,True,6,5]
   :correct: a
   :feedback_a: Yes, first True was added at index 2, then False was added at index 0.
   :feedback_b: insert will place items at the index position specified and move everything down to the right.
   :feedback_c: insert does not remove anything or replace anything.
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [4,2,8,6,5]
     alist.insert(2,True)
     alist.insert(0,False)
     print(alist)


.. mchoicemf:: test_question9_13_3
   :answer_a: [4,8,6]
   :answer_b: [2,6,5]
   :answer_c: [4,2,6]
   :correct: c
   :feedback_a: pop(2) removes the item at index 2, not the 2 itself.
   :feedback_b: pop() removes the last item, not the first.
   :feedback_c: Yes, first the 8 was removed, then the last item, which was 5.
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [4,2,8,6,5]
     temp = alist.pop(2)
     temp = alist.pop()
     print(alist)

   
   
.. mchoicemf:: test_question9_13_4
   :answer_a: [2,8,6,5]
   :answer_b: [4,2,8,6,5]
   :answer_c: 4
   :answer_d: None
   :correct: c
   :feedback_a: alist is now the value that was returned from pop(0).
   :feedback_b: pop(0) changes the list by removing the first item.
   :feedback_c: Yes, first the 4 was removed from the list, then returned and assigned to alist.  The list is lost.
   :feedback_d: pop(0) returns the first item in the list so alist has now been changed.
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [4,2,8,6,5]
     alist = alist.pop(0)
     print(alist)



.. note::

   This workspace is provided for your convenience.  You can use this activecode window to try out anything you like.

   .. activecode:: scratch_09_03




