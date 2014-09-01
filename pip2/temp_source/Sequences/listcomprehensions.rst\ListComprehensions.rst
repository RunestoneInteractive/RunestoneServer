..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

List Comprehensions
-------------------

Python provides an alternative way to do map and filter operations, called a **list comprehension**.  Many programmers find them to understand and write. List comprehensions are concise ways to create lists from other lists.  The general syntax is::

   [<expression> for <item> in <sequence> if  <condition>]

where the if clause is optional.  For example,

.. activecode:: listcomp_7

    things = [2, 5, 9]

    yourlist = [value * 2 for value in things]

    print(yourlist)

The expression is ``value * 2``. The item variable is ``value`` and the sequence is ``things``. This is an alternative way to perform a mapping operation. As with ``map``, each item in the sequence is transformed into an item in the new list. Instead of the iteration happening automatically, however, we have adopted the syntax of the for loop which may make it easier to understand. 

Just as in a regular for loop, the part of the statement ``for value in things`` says to execute some code once for each item in things. Each time that code is executed, ``value`` is bound to one item from ``things``. The code that is executed each time is the expression at the beginning, ``value * 2``, rather than a block of code indented underneath the for statement. The other difference from a regular for loop is that each time the expression is evaluated, the resulting value is appended to a list. That happens automatically, without the programmer explicitly initializing an empty list or appending each item.

The ``if`` clause of a list comprehension can be used to do a filter operation. To perform a pure filter operation, the expression can be simply the variable that is bound to each item. For example, the following list comprehension will keep only the positive numbers from the original list.

.. activecode:: listcomp_8

   def keep_evens(nums):
      new_list = [num for num in nums if num % 2 == 0]
      return new_list
      
   print keep_evens([3, 4, 6, 7, 0, 1])

You can also combine map and filter operations by chaining them together, or with a single list comprehension.

.. activecode:: listcomp_9

   things = [3, 4, 6, 7, 0, 1
   #chaining together filter and map:
   # first, filter to keep only the even numbers
   # double each of them
   print map(lambda x: x*2, filter(lambda y: y % 2 == 0, things))
   
   # equivalent version using list comprehension
   print [x*2 for x in things if x % 2 == 0]


**Check your understanding**

.. mchoicemf:: test_question9_20_1
   :answer_a: [4,2,8,6,5]
   :answer_b: [8,4,16,12,10]
   :answer_c: 10
   :answer_d: [10].
   :correct: d
   :feedback_a: Items from alist are doubled before being placed in blist.
   :feedback_b: Not all the items in alist are to be included in blist.  Look at the if clause.
   :feedback_c: The result needs to be a list.
   :feedback_d: Yes, 5 is the only odd number in alist.  It is doubled before being placed in blist.
   
   What is printed by the following statements?
   
   .. code-block:: python

     alist = [4,2,8,6,5]
     blist = [num*2 for num in alist if num%2==1]
     print(blist)

Now try the list comprehension exercises in session22.py

Reduce
======

Another common form of the accumulator pattern is to combine or summarize all the items in a list. 

For example, we can count the items in a list, or add them all up.

.. activecode:: listcomp_10

   nums = [3, 4, 6, 7, 0, 1]
   
   count = 0
   for num in nums:
      count = count + 1
   print count
   
   total = 0
   for num in nums:
      total = total + num
   print total
   
These particular operations, counting and summing, are so commonly performed that python provides built-in functions, ``len`` and ``sum``

.. activecode:: listcomp_11

   nums = [3, 4, 6, 7, 0, 1]

   print len(nums)
   print sum(nums)
 
There's also a built-in function ``max`` that works analogously, aggreating a list of numbers by keeping the largest one.
  
Another common accumulation that combines all the elements is to take a list of strings and concatenate them all together, separating them with some separator such as a comma or, in the example below, --.

.. activecode:: listcomp_12

   strings = ["Hello", "hi", "bye", "wonderful"]
   
   result = strings[0]
   for s in strings[1:]:
      result = result + "--" + s
   print result
   
Again, this way of combining lists of strings is so common that python has a built-in way to do it, in this case the ``join`` method. It's invoked in a slightly strange way because join is a method of string class, not a method of the list class. The string to invoke the method on is the separator to be used in between each of the elements. The list of strings that are to be concatenated together is passed as a parameter.

.. activecode:: listcomp_13

   strings = ["Hello", "hi", "bye", "wonderful"]
   
   print "--".join(strings)
   print ", ".join(strings)
   
More generally, python provides a function ``reduce`` which takes a list and produces a combined value from all the elements. Check out the `documentation <http://docs.python.org/2.7/library/functions.html#reduce>`_. The first parameter is a function that combines a result-so-far with the next element of a list, producing a new result-so-far. The second parameter is the list to be aggregated. An optional third parameter is the initial value for the accumulator variable. If it's not provided, the first element of the list is used as the intitial value.

All of the specific accumulations that you've seen before can be expressed compactly using the ``reduce`` function, though it may take a little decoding to understand exactly what they do.

.. activecode:: listcomp_14

   nums = [3, 4, 6, -7, 0, 1]
   
   # count them; len
   print reduce(lambda x, y: x +1, nums, 0)
   
   # add them up; sum
   print reduce(lambda x, y: x + y, nums)
   
   # find the largest; max
   def greater(x, y):
      if x > y:
         return x
      else:
         return y
   print reduce(greater, nums)
   
   
   strings = ["Hello", "hi", "bye", "wonderful"]
   # join the strings into one big string
   print reduce(lambda x, y: x + "--" + y, strings)   
   
Of course, it's easier to understand code using the more specific functions ``len, sum, max, and join``, so you should use those rather than ``reduce`` whenever you can. But sometimes you want to make a custom aggregator for which there is no built-in. For example, from here's a solution to a question from the Winter 2014 midterm exam.

.. activecode:: listcomp_15

   # manual accumulation         
   def maxabs(nums):
      best_so_far = nums[0]
      for num in nums:
        if abs(num) > abs(best_so_far):
           best_so_far = num
      return best_so_far
   
   # alternative using reduce
   # find the max absolute value
   def greater_abs(x, y):
       if abs(x) > abs(y):
           return x
       else:
           return y
   
   def maxabs2(nums):
     return reduce(greater_abs, nums)
   
   nums = [3, 4, 6, -7, 0, 1]
   print maxabs(nums)
   print maxabs2(nums)
