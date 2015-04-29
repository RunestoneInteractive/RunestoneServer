..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Nested Iteration
----------------

When you have nested data structures, especially lists and/or dictionaries, you will frequently need nested for loops
to traverse them.

.. activecode:: nested_data_10

    nested1 = [['a', 'b', 'c'],['d', 'e'],['f', 'g', 'h']]
    for x in nested1:
        print "level1: "
        for y in x:
            print "     level2: " + y

Line 3 executes once for each top-level list, three times in all. With each sub-list,
line 5 executes once for each item in the sub-list. Try stepping through it in Codelens to make sure you understand what the nested iteration does.

.. codelens:: nested_data_11

    nested1 = [['a', 'b', 'c'],['d', 'e'],['f', 'g', 'h']]
    for x in nested1:
        print "level1: "
        for y in x:
            print "    level2: " + y


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
