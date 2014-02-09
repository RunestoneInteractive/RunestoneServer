..  Copyright (C)  Paul Resnick.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

..  shortname:: Sorting
..  description:: Invoking sort and sorted using the key parameter to determine sort order.

.. qnum::
   :prefix: invoking-sort-
   :start: 1
   
.. _invoking_sort_chap:

Sorting with Sort and Sorted
============================

When we first introduced lists, we noted the existence of a method sort. When
invoked on a list, the order of items in the list is changed. If no optional
parameters are specified, the items are arranged in whatever
the natural ordering is for the item type. For example, if the items are
all integers, then smaller numbers go earlier in the list. If the items are all
strings, they are arranged in alphabetic order.

.. activecode:: sort_1

    L1 = [1, 7, 4, -2, 3]
    L2 = ["Cherry", "Apple", "Blueberry"]
    
    L1.sort()
    print(L1)
    L2.sort()
    print(L2)
    
Note that the sort method does **not** return a sorted version of the list. In
fact, it returns the value None. But the list itself has been modified. This
kind of operation that works by having a *side effect* on the list can be quite
confusing. 

In this course, we will generally use an alternative way of sorting, the function ``sorted`` rather
than the method ``sort``. Because it is a function rather than a method, it
is invoked on a list by passing the last as a parameter inside the parentheses,
rather than putting the list before the period. More importantly, ``sorted``
does not change the original list. Instead, it returns a new list.

.. activecode:: sort_2

    L2 = ["Cherry", "Apple", "Blueberry"]
    
    L3 = sorted(L2)
    print(L3)
    print(sorted(L2))
    print(L2) # unchanged
    
    L2.sort()
    print(L2)
    print(L2.sort()) #return value is None

Optional reverse parameter
--------------------------

The sorted function takes some optional parameters (see :ref:`Optional parameters <optional_pararams_chap>`).
The first one is a comparison function. We will not be using it in this course (indeed, in python 3, 
this parameter is not even available any longer). The second optional parameter is a key function, which 
will be described in the next section. The third optional parameter is a Boolean value which 
determines whether to sort the items in reverse order. By default, it is False,
but if you set it to True, the list will be sorted in reverse order.

.. activecode:: sort_3

    L2 = ["Cherry", "Apple", "Blueberry"]
    print(sorted(L2, None, None, True))
    
.. note::

    In order to specify the third optional parameter, we had to provide values for the
    other two optional parameters as well. In this case, we provided the value None
    for both of them. This code would be easier to read if we used the keyword
    technique, like this: ``sorted(L2, reverse=True)``. Unforutnately, specifying
    keyword parameters is not yet supported for the sorted function in this
    online environment. To discourage you from trying to specify a parameter with a keyword and then getting confused
    about why it doesn't work with sorted, I have delayed introduction of 
    keyword parameters entirely. We will learn about them after you start running
    python natively on your computer, when you will have a full implementation of
    python.
    
Optional key parameter
----------------------

If you want to sort things in some order other than the "natural" or or its reverse,
you can provide an additional parameter, the key parameter. For example, suppose
you want to sort a list of numbers based on their absolute value, so that -4 comes after 3?
Or suppose you have a dictionary with strings as the keys and numbers as the values. Instead
of sorting them in alphabetic order based on the keys, you might like to sort them in
order based on their values.

First, let's see an example, and then we'll dive into how it works.

First, let's define a function absolute that takes a number and returns its
absolute value. (Actually, python provides a built-in function ``abs`` that does
this, but we are going to define our own, for reasons that will be explained
in a minute.)

.. activecode:: sort_4

    L1 = [1, 7, 4, -2, 3]

    def absolute(x):
        if x >= 0:
            return x
        else:
            return -x
            
    print(absolute(3))
    print(absolute(-119))
    
    for y in L1:
        print(absolute(y))
        

Now, we can pass the absolute function to L1 in order to specify that we want
the items sorted in order of their absolute value, rather than in order of 
their actual value.

.. activecode:: sort_5

    L1 = [1, 7, 4, -2, 3]
     
    def absolute(x):
        if x >= 0:
            return x
        else:
            return -x
            
    L2 = sorted(L1, None, absolute)
    print(L2)
    
    #or in reverse order
    print(sorted(L1, None, absolute, True)) 
     
What's really going on there? We've done something pretty strange. Before, all the
values we have passed as parameters have been pretty easy to understand: numbers, strings,
lists, Booleans, dictionaries. Here we have passed a function object: absolute
is a variable name whose value is the function. When we pass that function object,
it is *not* automatically invoked. Instead, it is just bound the formal parameter
key of the function sorted.

We are not going to look at the source code for the built-in function sorted. But if
we did, we would find somewhere in its code a reference to the variable key, whose
value would be bound to the function we passed in. In fact, what the sorted function
does is call that key function once for each item in the list that's getting sorted.
It associates the result returned by that function (the absolute function in our case)
with the original value. Think of those associated values as being little post-it notes
that decorate the original values. The value 4 has a post-it note that says 4 on it,
but the value -2 has a post-it note that says 2 on it. Then the sorted function
rearranges the original items in order of the values written on their associated post-it notes.

To illustrate that the absolute function is invoked once on each item, during the execution
of sorted, I have added some print statements into the code.

.. activecode:: sort_6

    L1 = [1, 7, 4, -2, 3]
     
    def absolute(x):
        print("--- figuring out what to write on the post-it note for " + str(x)) 
        if x >= 0:
            return x
        else:
            return -x
    
    print("About to call sorted")
    L2 = sorted(L1, None, absolute)
    print("Finished execution of sorted")
    print(L2)

Note that this code never explicitly calls the absolute function at all. It passes
the absolute function as a parameter value to the sorted function. Inside the 
sorted function, whose code we haven't seen, that function gets invoked.

Anonymous functions with lambda expressions
-------------------------------------------

To further drive home the idea that we are passing a function object as a parameter
to the sorted object, let's see an alternative notation for creating a function,
a **lambda expression**. The syntax of a lambda expression is the word "lambda" followed
by parameter names, separated by commas but not inside (parentheses), followed 
by a colon and then an expression. ``lambda arguments: expression`` yields a function object. 
This unnamed object behaves like a function object defined with  

.. sourcecode:: python

    def fname(arguments):
        return expression
        
Consider the following code

.. activecode:: sort_7

    def f(x):
        return x - 1
    
    print(f)
    print(type(f))
    print(f(3))
    
    print(lambda x: x-2)
    print(type(lambda x: x-2))
    print((lambda x: x-2)(6))
    
Note the paralells between the two. At line 4, f is bound to a function object. Its printed representation
is "<function f>". At line 8, the lambda expression produces a function object. Because it is
unnamed (anonymous), its printed representation doesn't include a name for it, "<function <lambda>>". Both are of type
'function'.

A function, whether named or anonymous, can be called by placing parentheses () after it.
In this case, because there is one parameter, there is one value in parentheses. This
works the same way for the named function and the anonymous function produced by the lambda
expression. The lambda expression had to go in parentheses just for the purposes
of grouping all its contents together. Without the extra parentheses around it on line 10, 
the interpreter would group things differently and make a function of x that returns x - 2(6).

Some students find it more natural to work with lambda expressions than to refer to a function
by name. Others find the syntax of lambda expressions confusing. It's up to you
which version you want to use. In all the examples below, both ways of doing it will
be illustrated.

Below, sorting on absolute value has been rewritten using lambda notation.

.. activecode:: sort_8

    L1 = [1, 7, 4, -2, 3]
    
    print("About to call sorted")
    L2 = sorted(L1, None, lambda x: abs(x))
    print("Finished execution of sorted")
    print(L2)
  
.. note::
    Unfortunately, there is a bug in the online
    environment so that is not working currently. You can write ``sorted(L1, None, absolute)`` or ``sorted(L1, None, lambda x: abs(x)``.
    But you can't write ``sorted(L1, None, abs)`` or ``sorted(L1, None, lambda x: absolute(x))``. In a full python
    implementation, any of those four would work.

.. mchoicemf:: test_questionsort_1
   :answer_a: descending order, from 7 down to -2
   :answer_b: ascending order, from -2 up to 7
   :answer_c: the original order of L1
   :correct: a
   :feedback_a: 7 is decorated with -7, so it is first; -2 is decorated with 2, so it is last 
   :feedback_b: -x produces the negative of x
   :feedback_c: sorted changes the order

   Describe what the sort order will be for this.
   
   .. code-block:: python 

    L1 = [1, 7, 4, -2, 3]
     
    print(sorted(L1, None, lambda x: -x))

.. mchoicemf:: test_questionsort_2
   :answer_a: descending order, from 7 down to -2
   :answer_b: ascending order, from -2 up to 7
   :answer_c: the original order of L1
   :correct: b
   :feedback_a: The True value for the reverse parameter says to reverse the order 
   :feedback_b: The True value for the reverse parameter says to reverse the order
   :feedback_c: sorted changes the order

   Describe what the sort order will be for this.
   
   .. code-block:: python 

    L1 = [1, 7, 4, -2, 3]
     
    print(sorted(L1, None, lambda x: -x), True)


Sorting a Dictionary
--------------------

Previously, you have used a dictionary to accumulate counts, such as the frequencies of letters or words in a text.
For example, the following code counts the frequencies of different numbers in the list.

.. activecode:: sort_9

    L = [4, 5, 1, 0, 3, 8, 8, 2, 1, 0, 3, 3, 4, 3]

    d = {}
    for x in L:
        if x in d:
            d[x] = d[x] + 1
        else:
            d[x] = 1
    for x in d.keys():
        print(str(x) + " appears " + str(d[x]) + " times")

The dictionary's keys are not sorted in any particular order. In fact, you
may get a different order of output than someone else running the same
code. We can force the results to be displayed in some fixed ordering, by
sorting the keys.

.. activecode:: sort_10

    L = [4, 5, 1, 0, 3, 8, 8, 2, 1, 0, 3, 3, 4, 3]

    d = {}
    for x in L:
        if x in d:
            d[x] = d[x] + 1
        else:
            d[x] = 1
    y = sorted(d.keys())
    for x in y:
        print(str(x) + " appears " + str(d[x]) + " times")

    # or in reverse order
    print("---------")
    for x in sorted(d.keys(), None, None, True):
         print(str(x) + " appears " + str(d[x]) + " times")
    

With a dictionary that's maintaining counts or some other kind of score,
we might prefer to get the outputs sorted based on the count rather than
based on the items. There are a couple ways to do that. The first is, I think,
a little easier to understand. The second is the more standard idiom for 
python programmers; once you get used to it, it's a lot easier to read.

Here's the first way, using a lambda expression.

.. activecode:: sort_11

    L = [4, 5, 1, 0, 3, 8, 8, 2, 1, 0, 3, 3, 4, 3]

    d = {}
    for x in L:
        if x in d:
            d[x] = d[x] + 1
        else:
            d[x] = 1
            
    items = d.items();
    sorted_items = sorted(items, None, lambda x: x[1], True)
    for x in sorted_items:
        print(str(x[0]) + " appears " + str(x[1]) + " times")

Here's the first way, using a named function.

.. activecode:: sort_12

    L = [4, 5, 1, 0, 3, 8, 8, 2, 1, 0, 3, 3, 4, 3]

    d = {}
    for x in L:
        if x in d:
            d[x] = d[x] + 1
        else:
            d[x] = 1
    
    def g(pair):
        return pair[1]        
        
    items = d.items();
    sorted_items = sorted(items, None, g, True)
    for x in sorted_items:
        print(str(x[0]) + " appears " + str(x[1]) + " times")


Most python programmers would never sort the items (the key, value pairs) from
a dictionary. Instead, the standard idiom is to sort just the keys, based on their
associated values. Because python
lets you pass a function to the sorted parameter, you can pass a function that
looks up the value associated with a key and causes that value to be written on
the post-it notes that determine the sort order. 
Here's a version using a lambda expression.

.. sourcecode:: python

    L = [4, 5, 1, 0, 3, 8, 8, 2, 1, 0, 3, 3, 4, 3]
    
    d = {}
    for x in L:
        if x in d:
            d[x] = d[x] + 1
        else:
            d[x] = 1
    
    # just sort the keys, not the key-value pairs        
    y = sorted(d.keys(), None, lambda k: d[k], True)
    
    # now loop through the keys
    for k in y:
        print(str(k) + " appears " + str(val) + " times")

And here's a version of that using a named function. 

.. sourcecode:: python

    L = [4, 5, 1, 0, 3, 8, 8, 2, 1, 0, 3, 3, 4, 3]

    d = {}
    for x in L:
        if x in d:
            d[x] = d[x] + 1
        else:
            d[x] = 1
    
    def g(k):
        return d[k]

    # just sort the keys, not the key-value pairs        
    y = sorted(d.keys(), None, g, True)
    
    # now loop through the keys
    for k in y:
        print(str(k) + " appears " + str(val) + " times")

.. note:: 

    Unfortunately, due to a bug in
    the activecode implementation, neither of these will run in the browser. For
    now, you will have to sort the (key, value) pairs rather than just sorting
    the keys, even though that's not the preferred way to do things among python programmers.

.. omit this until sorted bugs are fixed in skuplt

    An experienced programmer would probably not even separate out the sorting step. And
    they might take advantage of the fact that when you pass a dictionary to something
    that is expecting a list, its the same as passing the list of keys.
    
    .. activecode:: sort_16
    
        L = [4, 5, 1, 0, 3, 8, 8, 2, 1, 0, 3, 3, 4, 3]
    
        d = {}
        for x in L:
            if x in d:
                d[x] = d[x] + 1
            else:
                d[x] = 1
            
        # now loop through the sorted keys
        for k in sorted(d, None, lambda k: d[k], True)
            print(str(k) + " appears " + str(val) + " times")
    
    
    Eventually, you will be able to read code like that above and immediately know
    what it's doing. For now, when you come across something confusing, like line 11,
    try breaking it down. The function sorted is invoked. Its first parameter value is a
    dictionary, which really means the keys of the dictionary. The third parameter, the
    key function, decorates the key with a post-it note containing that key's value in
    dictionary d. The last parameter, True, says to sort in reverse order.
    
.. mchoicema:: test_questionsort_3
   :answer_a: sorted(ks, None, g) 
   :answer_b: sorted(ks, None, lambda x: g(x, d))
   :answer_c: sorted(ks, None, lambda x: d[x])
   :correct: b,c
   :feedback_a: g is a function that takes two parameters. The key function passed to sorted must always take just one parameter 
   :feedback_b: The lambda function takes just one parameter, and calls g with two parameters. (Unfortunately, this won't run correctly in the browser due to a bug.)
   :feedback_c: The lambda function looks up the value of x in d. (Unfortunately, this won't run correctly in the browser due to a bug.)

   Which of the following will sort the keys of d in ascending order of their values (i.e., from lowest to highest)?
   
   .. code-block:: python 

        L = [4, 5, 1, 0, 3, 8, 8, 2, 1, 0, 3, 3, 4, 3]
    
        d = {}
        for x in L:
            if x in d:
                d[x] = d[x] + 1
            else:
                d[x] = 1
        
        def g(k, d):
            return d[k]
            
        ks = d.keys()

Glossary
--------

.. glossary::

    sort
        A method that sorts a list in place, changing the contents of the list. It
        return None, not a new list.
        
    sorted
        A function that returns a sorted list, without changing the original.
        
    reverse parameter
        If True, the sorting is done in reverse order.
        
    key parameter
        If a value is specified, it must be a function object that takes one parameter.
        The function will be called once for each item in the list that's getting
        sorted. The return value will be used to decorate the item with a post-it
        note. Values on the post-it notes are used to determine the sort order of
        the items. 

Exercises
---------

1. Write a function that takes a string as a parameter and returns a list of the five
most frequent characters in the string. [Hint: count the frequencies of all the characters,
as we've done before, using a dictionary and the accumulator pattern. Then sort the (key, value) pairs.
Finally, take a slice of the sorted list to get just the top five.]