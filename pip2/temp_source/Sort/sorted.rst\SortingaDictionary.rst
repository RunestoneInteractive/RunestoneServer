..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

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

