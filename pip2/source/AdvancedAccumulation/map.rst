..  Copyright (C)  Paul Resnick.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".


Map
---

The following function produces a new list with each item in the original list doubled. It is an example of a mapping, from the original list to a new list of the same length, where each element is doubled.

.. activecode:: listcomp_1
    
    def doubleStuff(a_list):
        """ Return a new list in which contains doubles of the elements in a_list. """
        new_list = []
        for value in a_list:
            new_elem = 2 * value
            new_list.append(new_elem)
        return new_list
    
    things = [2, 5, 9]
    print things
    things = doubleStuff(things)
    print things

The doubleStuff function is an example of the accumulator pattern, in particular the mapping pattern. On line 3, new_list is initialized. On line 5, the doubled value for the current item is produced and on line 6 it is appended to the list we're accumulating. Line 7 executes after we've processrf all the items in the original list: it returns the new_list. Once again, codelens helps us to see the actual references and objects as they are passed and returned.

.. codelens:: listcomp_2

    def doubleStuff(a_list):
        """ Return a new list in which contains doubles of the elements in a_list. """
        new_list = []
        for value in a_list:
            new_elem = 2 * value
            new_list.append(new_elem)
        return new_list

    things = [2, 5, 9]
    things = doubleStuff(things)

This pattern of computation is so common that python offers a more general way to do mappings, the ``map`` function, that makes it more clear what the overall structure of the computation is. map takes two arguments, a function and a sequence. The function is the mapper that transforms items. It is automatically applied to each item in the sequence. You don't have to initialize an accumulator or iterate with a for loop at all.

As we did when passing a function as a parameter to the ``sorted`` function, we can specify a function to pass to ``map`` either by referring to a function by name, or by providing a lambda expression.

.. activecode:: listcomp_3

   def triple(value):
      return 3*value
      
   def tripleStuff(a_list):
      new_list = map(triple, a_list)
      return new_list

   def quadrupleStuff(a_list):
      new_list = map(lambda value: 4*value, a_list)
      return new_list      
      
   things = [2, 5, 9]
   things3 = tripleStuff(things)
   print things3
   things4 = quadrupleStuff(things)
   print things4

Of course, once we get used to using the map function, it's no longer necessary to define functions like tripleStuff and quadrupleStuff.

.. activecode:: listcomp_4

   things = [2, 5, 9]
   
   things4 = map((lambda value: 4*value), things)
   print things4
   
   # or all on one line
   print map((lambda value: 5*value), [1, 2, 3])

