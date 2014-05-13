..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Recursive Data
--------------

All of the Python data types we have seen can be grouped inside lists and
tuples in a variety of ways. Lists and tuples can also be nested, providing a
myriad possibilities for organizing data. The organization of data for the
purpose of making it easier to use is called a **data structure**.

It's election time and we are helping to compute the votes as they come in.
Votes arriving from individual wards, precincts, municipalities, counties, and
states are sometimes reported as a sum total of votes and sometimes as a list
of subtotals of votes. After considering how best to store the tallies, we
decide to use a *nested number list*, which we define as follows:

A *nested number list* is a list whose elements are either:

a. numbers
b. nested number lists

Notice that the term, *nested number list* is used in its own definition.
**Recursive definitions** like this are quite common in mathematics and
computer science. They provide a concise and powerful way to describe
**recursive data structures** that are partially composed of smaller and
simpler instances of themselves. The definition is not circular, since at some
point we will reach a list that does not have any lists as elements.

Now suppose our job is to write a function that will sum all of the values in a
nested number list. We would want to call such a function on a list where some of the
items might be numbers and some of them might be lists of numbers.

Since the problem involves processing something that is recursively defined, it is likely that
a recursive function might easily do the trick.  But how do we design such a function?

The first thing you must do to write a recursive function is define the cases where you already know the
answer. In the Koch fractal example, the order 0 case is easy.  Just draw a straight line.  We call
such a case the **base case**.  It is entirely possible that there can be many base cases in a recursive
solution.  However, in each case, we know what to do.

For this problem, the base case is also very simple.  If the list has nothing in it, the sum of all the values
must be 0.  But what if the list is not empty?  Then there must be a first item and if we take away the first item
the rest must be a list with one fewer item than before.

If we already have a function that knows how to compute the sum of a list, we can use it to compute the sum of
the rest of the list.  The only problem we need to address is how to deal with the first item.

There are two possibilities.  The first item could be a simple integer.  If that is the case, we simply add it to the
sum returned for the rest of the list.  However, if the first item is itself a list, we will need to compute its sum (good news...we already have a function that knows how to do that) and then add that to the sum returned for the rest of
the list.

Either case will call the function of a smaller part of the original list.  This is known as the **recursive call** and must
be made with a parameter value that is moving toward becoming the base case.  The complete function is shown below. 

.. index:: recursion, recursive call, base case, infinite recursion, recursion; infinite


.. codelens:: chp11_recursivesum
    
    def rSum(nestedNumList):
        if nestedNumList == []:
            return 0
        else:
            firstitem = nestedNumList[0]
            if type(firstitem) == type(87):
                return firstitem + rSum(nestedNumList[1:])
            else:
                return rSum(firstitem) + rSum(nestedNumList[1:])


    result = rSum([])
    l = [1,2,3,4]
    result = rSum(l)
    m = [4,5,6]
    l = [1,2,m,7,8]
    result = rSum(l)

Note that three different calls are made to test the function.  In the first, list is empty.  This will test the base
case.  In the second, the list has no nesting.  The third requires that all parts of the recursion are working.  Try them
and then make modifications to the lists to add deeper nesting.  You might even want to try:

.. sourcecode:: python

    print(rSum([[[[[[[[[[]]]]]]]]]]))


.. admonition:: Scratch Editor

  .. actex:: recursion_scratch_1


