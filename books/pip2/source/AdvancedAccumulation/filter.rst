..  Copyright (C)  Paul Resnick.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Filter
------

Now consider another common pattern: going through a list and keeping only those items that meet certain criteria. This is called a filter.

.. activecode:: listcomp_5

   def keep_evens(nums):
      new_list = []
      for num in nums:
         if num % 2 == 0:
            new_list.append(num)
      return new_list
      
   print keep_evens([3, 4, 6, 7, 0, 1])

Again, this pattern of computation is so common that python offers a more compact and general way to do it, the ``filter`` function. filter takes two arguments, a function and a sequence. The function takes one item and return True if the item should. It is automatically called for each item in the sequence. You don't have to initialize an accumulator or iterate with a for loop.

.. activecode:: listcomp_6

   def keep_odds(nums):
      new_list = filter(lambda num: num % 2 == 1, nums)
      return new_list
      
   print keep_odds([3, 4, 6, 7, 0, 1])

Exercises
---------

