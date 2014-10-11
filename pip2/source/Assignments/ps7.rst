:orphan:

..  Copyright (C) Paul Resnick.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. highlight:: python
    :linenothreshold: 500


Week 7: ends October 19
=======================

1. Do the multiple choice questions and exercises in the textbook chapters, including the ones at the bottom of the chapters, below the glossary. Don't forget to click Save for each of the exercises, and always access the textbook by clicking on the link from cTools, so that you'll be logged in.
   
   * Before Thursday's class:
       * Read :ref:`Sorting<sort_chap>`, and do the exercises in that chapter
 
#. Reading responses

   * None this week

#. Problem set

   * None this week
   
#. Exam preparation

   * In CTools you will find a practice midterm exam; another one will be posted closer to the exam time
   
   * Suggested practice for making best use of the problem sets for review
      * Go through all the problem sets, looking at your answers and comparing them to the solution set answers. (The solution sets are all embedded in the problem sets; we have been releasing them when we release the grades for each problem set.)
      * Then make another pass through the problem sets. This time, don't look at your past answer or the solution set. Write new answers from scratch. See how quickly you can solve them. Make a note of any problems that take you a long time to solve. 
      * Repeat as necessary. On later iterations of this process, only redo the problems that you did not solve immediately on the previous iteration.

   * We have also included a bunch of practice problems below. None of these are graded. Some have solutions.      


Practice Problems: Material Prior to Functions
----------------------------------------------

See comments in code for instructions.

.. actex:: rv_1_1

   s = "supercalifragilisticexpialidocious"
   # How many characters are in string s? Write code to print the answer.

   lp = ["hello","arachnophobia","lamplighter","inspirations","ice","amalgamation","programming","Python"]
   # How many characters are in each element of list lp? 
   # Write code to print the length (number of characters) of each element of the list on a separate line. 
   ## Do NOT write 8+ lines of code to do this.

   # The output you get should be:
   # 5
   # 13
   # 11
   # 12
   # 3
   # 12
   # 11
   # 6

#. See comments in code for instructions.

.. actex:: rv_1_2

   ic = 93252759253293024
   # What is the value if you add 5 to the integer in ic?

   dcm = [9, 4, 67, 89, 98324, 23, 34, 67, 89, 34, 56, 67, 90, 3242, 9893, 5]
   # add 14 to each element of the list dcm and print the result

   # The output you get should be:
   # 23
   # 18
   # 81
   # 103
   # 98338
   # 37
   # 48
   # 81
   # 103
   # 48
   # 70
   # 81
   # 104
   # 3256
   # 9907
   # 19

#. See comments in code for instructions.

.. actex:: rv_1_3

   pl = "keyboard smashing: sdgahgkslghgisaoghdwkltewighigohdjdslkfjisdoghkshdlfkdjgdshglsdkfdsgkldhfkdlsfhdsklghdskgdlhgsdklghdsgkdslghdskglsdgkhdskfls"
   # What is the last character of the string value in the variable pl? Find it and print it.

   plts = ["sdsagdsal","sdadfsfsk","dsgsafsal","tomorrow","cooperative","sdgadtx","289,670,452","!)?+)_="]
   # What is the last character of each element in the list plts?
   # Print the last character of each element in the list on a separate line.
   # HINT: You should NOT have to count the length of any of these strings manually/by yourself.

   # Your output should be:
   # l
   # k
   # l
   # w
   # e
   # x
   # 2
   # =


#. See comments in code for instructions.

.. actex:: rv_1_4

   bz = "elementary, my dear watson"
   # Write code to print the fifth character of string bz.
   # Your output should be:
   # e

   # Write code to print the seventh character of string bz.
   # Your output should be:
   # t

#. See comments in code for instructions.

.. actex:: rv_1_5

   nm = "Irene"
   # write code to print out the string "Why hello, Irene" using the variable nm.


   hlt = ['mycroft','Lestrade','gregson','sherlock','Joan','john','holmes','mrs hudson']
   # Write code to print "Nice to meet you," in front of each element in list hlt on a separate line.

   # Your output should look like:
   # Nice to meet you, mycroft
   # Nice to meet you, Lestrade
   # Nice to meet you, gregson
   # Nice to meet you, sherlock
   # Nice to meet you, Joan
   # Nice to meet you, john
   # Nice to meet you, holmes
   # Nice to meet you, mrs hudson


#. See comments in code for instructions.

.. actex:: rv_1_6

   z = True
   # Write code to print the type of the value in the variable z.

   ab = 45.6
   # Write code to print the type of the value in the variable ab.


#. See comments in code for instructions.

.. actex:: rv_1_7

   fancy_tomatoes = ["hello", 6, 4.24, 8, 20, "newspaper", True, "goodbye", "False", False, 5967834, "6578.31"]

   # Write code to print the length of the list fancy_tomatoes.


   # Write code to print out each element of the list fancy_tomatoes on a separate line.
   # (You can do this in just 2 lines of code!)

   # Your output should look like:
   # hello
   # 6
   # 4.24
   # 8
   # 20
   # newspaper
   # True
   # goodbye
   # False
   # False
   # 5967834
   # 6578.31


   # Now write code to print out the type of each element of the list fancy_tomatoes on a separate line.

   # Your output should look like:
   # <type 'str'>
   # <type 'int'>
   # <type 'float'>
   # <type 'int'>
   # <type 'int'>
   # <type 'str'>
   # <type 'bool'>
   # <type 'str'>
   # <type 'str'>
   # <type 'bool'>
   # <type 'int'>
   # <type 'str'>


Functions Practice Problems
---------------------------

We strongly suggest that you try to do the problems yourself before looking at the solutions (which are heavily commented)

1. Define (and call) a function called `` get_vowels `` which takes an **input** of a string and **returns the total number of vowels in the string**.

.. tabbed:: func_review_1

  .. tab:: Problem

      .. actex:: fr_1

          # Write your code here!


          # Here's a sample function call.
          print get_vowels("Hello all") # This should print: 3

  .. tab:: Solution

      .. actex:: fr_1a

          def get_vowels(s):
              vowels = "aeiou"
              total = 0
              for v in vowels:
                  total += s.count(v)
              return total

          print get_vowels("Hello all")

#. Define (and call) a function called `` sum_a_list `` which **takes any list of integers** and **returns the sum of all integers in the list**.

.. tabbed:: func_review_2

  .. tab:: Problem

      .. actex:: fr_2

          # Write your code here!


          # Here's a sample function call.
          print sum_a_list([1,4,7,5]) # this should print: 17

          # Extra practice: 
          # how would you change this function just a LITTLE 
          # so that the function could also take a string of digits
          # and return the sum of all those digits.
          # (Hint: to do this, you only have to type 5 more characters.)

  .. tab:: Solution

      .. actex:: fr_2a

          def sum_a_list(lt):
              tot = 0
              for i in lt:
                  tot = tot + i
              return tot

          print sum_a_list(1,4,7,5])

          # Here's the version of the function that will work
          #   for EITHER a list of integers or a string of digits
          def sum_a_list_or_digitstring(lt):
              tot = 0
              for i in lt:
                  tot = tot + int(i)
              return tot

          print sum_a_list_or_digitstring("1475")


#. Define (and call!) a function called ``common_word`` that **takes a string** and **prints a tuple** of **the most commonly used word in the string** and **the number of times that word is used**. (If there's more than one word that's used most frequently, the function should **print** all of those words.) 

.. tabbed:: func_review_3

  .. tab:: Problem

      .. actex:: fr_3

          # Write your code here!


          # Here's a sample function call.
          common_word("hello hello hello is what they said to the class!") # should print: hello


          # For extra practice: you've done something like this before -- 
          # how would you change this function to print the LONGEST word in the string?



  .. tab:: Solution

      .. actex:: fr_3a

          def common_word(s):
              d = {}
              sp = s.split() # split my string by whitespace, so into 'words'
              for w in sp:
                  if w in d:
                      d[w] = d[w] + 1
                  else:
                      d[w] = 1
              kys = d.keys() # get all the keys from the dict you built, in a list
              most_common = kys[0] # start at the beginning of the list -- this is the most common so far!
              for k in d: # go through the keys in the dictionary
                  if d[k] > d[most_common]: # if the value of the key is bigger than the value of the most common key SO FAR, then you have a new most common key so far
                      most_common = k # so reassign the most_common key
              for ky in d: # now that we know the value of the most common key, go through the keys of the dictionary again
                  if d[ky] == d[most_common]: # for every key that has the same value as the most common one
                      print ky, d[ky] # print the key and its value
                      # note that we do NOT return anything here!
                      # because we asked to print stuff out

          # Think further: what would happen if you put a return statement where that print statement is? why wouldn't that work?


#. Define (and call!) a function called ``smallest_value_name`` that **takes a dictionary** with key-value pairs of names and integer values, like this: ``{"Nick": 56, "Paul":73, "Jackie":42}``, and **returns the name associated with the *lowest integer value**. (So in the case of that example dictionary, the function should return ``Jackie``.)

.. tabbed:: func_review_4

  .. tab:: Problem

      .. actex:: fr_4

          # Write your code here!

          # Here's a sample call
          df = {"Nick": 56, "Paul":73, "Jackie":42}
          pritn smallest_value_name(df) # should print: Jackie

  .. tab:: Solution

      .. actex:: fr_4a

          # Here's one solution
          def smallest_value_name(d):
              kys = d.keys() # returns a list of the keys in the dictionary d
              m = kys[0]
              for k in kys:
                  if d[k] < d[m]:
                      m = k
              return m

          # Here's another solution
          def smallest_val_name_diff(d):
              its = d.items() # returns a list of tuples (key, value) in dictionary d and stores it in its
              tn = its[0]
              for t in its:
                  if t[1] < tn[1]:
                      tn = t
              return tn[0]

          # Sample calls of these solution functions
          d_new = {"Nick": 56, "Paul":73, "Jackie":42, "Ellie":36}
          print smallest_val_name(d_new)

          print smallest_val_name_diff(d_new)
          # both these calls above print "Ellie"!


       