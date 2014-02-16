..  Copyright (C)  Paul Resnick.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

..  shortname:: NestedData
..  description:: Nested lists and dictionaries and nested iteration to traverse them.

.. qnum::
   :prefix: nested_data-
   :start: 1
   
.. _nested_data_chap:

Nested Data and Nested Iteration
================================

Lists with Complex Items
------------------------


The lists we have seen so far have had numbers or strings as items. Perhaps you 
noticed the lists of tuples when we sorted the contents of dictionaries.

In fact, the items in a list can be any type of python object. For example,
we can have a list of lists.

.. activecode:: nested_data_1

    nested1 = [['a', 'b', 'c'],['d', 'e'],['f', 'g', 'h']]
    print(nested1[0])
    print(len(nested1))
    nested1.append(['i'])
    for L in nested1:
        print L

Line 2 prints out the first item from the list that nested1 is bound to. That
item is itself a list, so it prints out with square brackets. It has length 3,
which prints out on line 3. Line 4 adds a new item to nested1. It is a list 
with one element, 'i' (it a list with one element, it's not just the string 'i').

Codelens gives a you a reference diagram, a visual display of the contents of nested1. 

.. codelens:: nested_data_2

    nested1 = [['a', 'b', 'c'],['d', 'e'],['f', 'g', 'h']]
    print(nested1[0])
    print(len(nested1))
    nested1.append(['i'])
    for L in nested1:
        print L

When you get
to step 4 of the execution, take a look at the object that variable nested1 points to.
It is a list of three items, numbered 0, 1, and 2. The item in slot 1 is small enough
that it is shown right there as a list containing items "d" and "e". The item in
slot 0 didn't quite fit, so it is shown in the figure as a pointer to another separate list; same thing
for the item in slot 2, the list ["f", "g", "h"]. 

There's no special meaning to whether the list
is shown embedded or with a pointer to it: that's just CodeLens making the best use
of space that it can. In fact, if you go on to step 5, you'll see that, with the
addition of a fourth item, the list ['i'], CodeLens has chosen to show all four lists embedded in the 
top-level list.

With a nested list, you can make complex expressions to get or set a value in a sub-list. 

.. activecode:: nested_data_3

    nested1 = [['a', 'b', 'c'],['d', 'e'],['f', 'g', 'h']]
    y = nested1[1]
    print(y)
    print(y[0])
    
    print([10, 20, 30][1])
    print(nested1[1][0])
    
Lines 1-4 above probably look pretty natural to you. Line 6 is just a reminder that
you index into a list that is written out just as you can index into a list referred to by a variable.
    
Just as with a function call where the return value can be thought of as replacing the text of the
function call in an expression, you can evaluate an expression like that in line 7 from left to right. Because the
value of nested1[1] is the list ['d', 'e'], nested[1][0] is the same as ['d', 'e'][0]. So line 7 is equivalent to lines 2-4; it is a simpler way
of pulling out the first item from the second list. 

At first, expressions like that on line 7 may look foreign. They will soon feel more natural, and you will end up using them a lot. Once you are comfortable
with them, the only time you will write code like lines 2-4 is when you aren't quite sure what the structure is of your data, and so you need to incrementally
write and debug your code. Often, you will start by writing code like lines 2-4, then, once you're sure it's working, replace it with something like line 7.

You can change values in such lists in the usual ways. You can even use complex expressions to change values. Consider the following

.. codelens:: nested_data_4

    nested1 = [['a', 'b', 'c'],['d', 'e'],['f', 'g', 'h'], ['i']]
    nested1[1] = [1, 2, 3]
    nested1[1][0] = 100
    
The complex items in a list do not have to be lists. They can be tuples or dictionaries. The items in a list do not all have to be the same time, but you will drive yourself crazy if you have lists of objects of varying types. Save yourself
some headaches and don't do that. Here's a list of dictionaries and some operations on them. Take a look at its visual representation in codelens.

.. codelens:: nested_data_5

   nested2 = [{'a': 1, 'b': 3}, {'a': 5, 'c': 90, 5: 50}, {'b': 3, 'c': "yes"}]
   
Try practicing some operations to get or set values in a list of dictionaries.

.. actex:: nested_data_6

   nested2 = [{'a': 1, 'b': 3}, {'a': 5, 'c': 90, 5: 50}, {'b': 3, 'c': "yes"}]

   #write code to print the value associated with key 'c' in the second dictionary (90)
   
   #write code to print the value associated with key 'b' in the third dictionary
   
   #add a fourth dictionary add the end of the list; print something to check your work.
   
   #change the value associated with 'c' in the third dictionary from "yes" tio "no"; print something to check your work
   
   
You can even have a list of functions (!). 

.. activecode:: nested_data_7

    def square(x):
        return x*x
        
    L = [square, abs, lambda x: x + 1]

    print("****names****")        
    for f in L:
        print(f)
    
    print("****call each of them****")    
    for f in L:
        print(f(-2))
        
    print("****just the first one in the list****")
    print(L[0])
    print(L[0](3))
        
        
Here, L is a list with three items. All those items are functions. The first is the
function square that is defined on lines 1 and 2. The second is the built-in python
function abs. The third is an anonymous function that returns one more than its input.

In the first for loop, we do not call the functions, we just output their printed representations. The output <function square>
confirms that square truly is a function object. For some reason, in codelens, it's not able to produce a nice
printed representation of the built-in function abs, so it just outputs <unknown>

In the second for loop, we call each of the functions, passing in the value -2 each time and printing whatever value the function returns. 

The last two lines just emphasize that there's nothing special about lists of functions. They follow all the same rules for how python treats any other list. Because L[0] picks out the function square, L[0](3) calls the functions square, passing it the parameter 3.

Step through it in Codelens if that's not all clear to you yet.

.. codelens:: nested_data_8

    def square(x):
        return x*x
        
    L = [square, abs, lambda x: x + 1]

    print("****names****")        
    for f in L:
        print(f)
    
    print("****call each of them****")    
    for f in L:
        print(f(-2))
        
    print("****just the first one in the list****")
    print(L[0])
    print(L[0](3))

Nested Dictionaries
-------------------

Just as lists can contain items of any type, the value associated with a key in a dictionary 
can also be an object of any type. In particular, it is often useful to have a list or a dictionary as a value
in a dictionary. And of course, those lists or dictionaries can also contain lists and dictionaries. There
can be many layers of nesting.

Only the values in dictionaries can be objects of arbitrary type. The keys in dictionaries must be one of the
immutable data types (numbers, strings, tuples).

.. mchoicema:: test_questionnested_9
    :answer_a: d[5] = {1: 2, 3: 4}
    :answer_b: d[{1:2, 3:4}] = 5
    :answer_c: d['key1']['d'] = d['key2']
    :answer_d: d[key2] =3
    :correct: a,c
    :feedback_a: 5 is a valid key; {1:2, 3:4} is a dictionary with two keys, and is a valid value to associate with key 5.
    :feedback_b: Dictionary keys must be of immutable types. A dictionary can't be used as a key in a dictionary.
    :feedback_c: d['key2'] is {'b': 3, 'c': "yes"}, a python object. It can be bound to the key 'd' in a dictionary {'a': 5, 'c': 90, 5: 50}
    :feedback_d: key2 is an unbound variable here. d['key2'] would be OK.
    
    Which of the following is a legal assignment statement, after the following code executes?
    
    .. code-block:: python 
    
        d = {'key1': {'a': 5, 'c': 90, 5: 50}, 'key2':{'b': 3, 'c': "yes"}} 

Nested Iteration
----------------

When you have nested data structures, especially lists and/or dictionaries, you will frequently need nested for loops
to traverse them.

.. activecode:: nested_data_10

    nested1 = [['a', 'b', 'c'],['d', 'e'],['f', 'g', 'h']]
    for x in nested1:
        print "level1: "
        for y in x:
            print "\tlevel2: " + y

Line 3 executes once for each top-level list, three times in all. With each sub-list,
line 5 executes once for each item in the sub-list. Try stepping through it in Codelens to make sure you understand what the nested iteration does.

.. codelens:: nested_data_11

    nested1 = [['a', 'b', 'c'],['d', 'e'],['f', 'g', 'h']]
    for x in nested1:
        print "level1: "
        for y in x:
            print "\tlevel2: " + y


.. parsonsprob:: nested_data_12

    Now try rearranging these code fragments to make a function that counts all the *leaf* items in a nested list like nested1 above, the items at the lowest level of nesting (8 of them in nested1).
    -----    
    def count_leaves(n):
    =====
        count = 0
    =====
        for L in n:
    =====
            for x in L:
    =====
                count = count + 1
    =====
        return count    
        
