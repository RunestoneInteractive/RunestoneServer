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


Week 4: ends January 31
=======================

For this week you have the following graded activities:

1. Do the multiple choice questions and exercises in the textbook chapters, including the ones at the bottom of the chapters, below the glossary. Don't forget to click **Save** for each of the exercises.

   * Before Tuesday's class:      
      * :ref:`Dictionaries <dictionaries_chap>`
   
   * Before Thursday's class:
      * :ref:`More tips on programming and debugging <debugging_2>` 
      * :ref:`Accumulating results in and from dictionaries <dictionary_accum_chap>`

#. Turn in the reading response, by 8 PM the night before your registered section meets.

   * Read *The Most Human Human*, Chapter 5, "Getting out of Book"
   * :ref:`Reading response 3 <response_3>`

#. Save answers to the exercises in Problem Set 2:

   * :ref:`Problem Set 3 <problem_set_3>`

You also have one optional, ungraded activity, some :ref:`Review Problems <review_problems_1>`

.. _review_problems_1:

Review Problems (Ungraded)
--------------------------

Below are some problems that will help you review the first several concepts we've gone over this semester. 
These probems are *OPTIONAL*, but if you struggled with PS2, we strongly recommend that you
work on these before you attempt PS3. If you are struggling with them, please come to office hours and discuss!
By the time you've done a few of these, the last few should start to come pretty easily.  
(We will release solutions on Thursday night.)

1. See comments in code for instructions.

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

Congratulations, now hit the "That Was Easy" button and go on. You're ready for the rest of this week's reading and the problem set!


.. _response_3:

Reading Response
----------------

**Due 8PM the night before your section meets**

Don't forget to click **save**.
   
   Give an example of when you were interacting with someone where you used "Book" responses.

   .. actex:: rr_3_1

      # Fill in your response in between the triple quotes
      """

      """

   Give an example of when you gave someone an "out of book" response.

   .. actex:: rr_3_2

      # Fill in your response in between the triple quotes
      """

      """

   What would you like to talk about in section this week?
   
   .. actex:: rr_3_3

      # Fill in your response in between the triple quotes
      """

      """

.. _problem_set_3:

Problem Set
-----------

**Due:** **Friday, January 31, 5 pm**

**Instructions:** Write the code you want to save in the provided boxes, and click **save** for each one. 
The last code you have saved for each one by the deadline is what will be graded.


1. (6 points) Old McDonald had a farm. He records the animals on his farm in a dictionary called 'animals'. 
In this problem help Old McDonald manage his farm animals. Be sure to answer all six parts, a-f.

   .. tabbed:: ps_3_1_tabs

      .. tab:: Problem

         .. actex:: ps_3_1

            animals = {
               'cows': 2,
               'chickens': 8,
               'pigs': 4,
               'mice': 72,
               'cats': 9,
               'dogs': 1,
            }

            # a. Print the number of chickens in the farm (by having your code look it up
            # in the animals dictionary. "Print(8)" is cheating...)
            
            # b. Old McDonald was given a yak. Add a yak to to the animals dictionary.

            # c. Old McDonald foud a stray dog. Increase the number of dogs on the farm by 1.

            # d. print out the names and quantities of all animals on his farm, one per line, in any order.
            # For example:
            # 2 cows
            # 9 cats
            # ...

            # e. While giving tours of his farm to children, they often inquire about particular
            # animals. Write code that asks the user to input an animal name, and then
            # prints out how many of that animal he has; or 0 if he has none.
            # For example, output "8 chickens" or "0 elephants"

            # f. Write a statement that tells Old McDonald which animal he has the most of.
            # This statement should print "72 mice", given the current state of the
            # dictionary, but your code should work correctly even if mice aren't the
            # most numerous animal on his farm.

      .. tab:: Solution

         .. actex:: ps_3_1a

            animals = {
               'cows': 2,
               'chickens': 8,
               'pigs': 4,
               'mice': 72,
               'cats': 9,
               'dogs': 1,
            }

            # a. Print the number of chickens in the farm (by having your code look it up
            # in the animals dictionary. "Print(8)" is cheating...)
            
            print(animals['chickens'])
            
            # b. Old McDonald was given a yak. Add a yak to to the animals dictionary.
            
            animals['yak'] = 1

            # c. Old McDonald foud a stray dog. Increase the number of dogs on the farm by 1.

            animals['dogs'] = animals['dogs'] + 1

            # d. print out the names and quantities of all animals on his farm, one per line, in any order.
            # For example:
            # 2 cows
            # 9 cats
            # ...

            for k in animals:
               print(animals[k],k)

            # e. While giving tours of his farm to children, they often inquire about particular
            # animals. Write code that asks the user to input an animal name, and then
            # prints out how many of that animal he has; or 0 if he has none.
            # For example, output "8 chickens" or "0 elephants"

            q = input("How many _____ do you have?")
            if q in animals:
               print(animals[q],q)
            else:
               print(0,q)

            # f. Write a statement that tells Old McDonald which animal he has the most of.
            # This statement should print "72 mice", given the current state of the
            # dictionary, but your code should work correctly even if mice aren't the
            # most numerous animal on his farm.

            keys = animals.keys()
            best_key = keys[0]
            for k in keys:
               if animals[k] > animals[best_key]:
                  best_key = k
            print(animals[best_key], best_key)

For the next three exercises, you will analyze data from our group on Facebook. To 'load' the data you will need to copy and paste it into the python prompt, in between the quotation marks. To maintain confidentiality (i.e., only students in 106 can see it), the data lives in a `file on cTools. <https://ctools.umich.edu/access/content/group/80ba0083-6409-4149-8222-f210f9dc6dd1/Problem%20Sets/PS3/simplefbdata.txt>`_

#. (2 points) For each post or comment in the facebook group, print out the name of the poster.

   .. tabbed:: ps_3_2_tabs

      .. tab:: Problem

         .. actex:: ps_3_2

            fb = """
            # Delete this line and paste file contents here
            """

            x = fb.split("\n")
            # x now refers to a list, with each line of text as one element in the list.
            # If you're not sure, trying printing x, len(x), x[1], and x[1][0] and make sure you understand
            # why you get the output you do

            # Your output should look something like:
            # Paul R.
            # Jackie C.
            # Jackie C.
            # Nick R.
            # Jackie C.

      .. tab:: Solution

         .. actex:: ps_3_2a

            fb = """
            # Delete this line and paste file contents here
            """

            x = fb.split("\n")
            # x now refers to a list, with each line of text as one element in the list.
            # If you're not sure, trying printing x, len(x), x[1], and x[1][0] and make sure you understand
            # why you get the output you do

            for ln in x:
                if ln[:5] == 'from:':
                    print ln[6:].lstrip()

#. (2 points) Use the Facebook data to count the number of posts (or reply comments) each person made in the Facebook group.

   .. tabbed:: ps_3_3_tabs

      .. tab:: Problem

         .. actex:: ps_3_3

            fb = """
            # Delete this line and paste file contents here
            """

            x = fb.split("\n")

            # Your output should look something like this, but with different numbers:
            # Paul R. posted 1 times  (# or, if you're ambitious, make it say 1 time instead of 1 times)
            # Jackie C. posted 3 times
            # Nick R. posted 2 times

      .. tab:: Solution
      
         .. actex:: ps_3_3a

            fb = """
            # Delete this line and paste file contents here
            """

            x = fb.split("\n")

            posters = {}
            for ln in x:
                if ln[:5] == 'from:':
                    name = ln[6:].lstrip()
                    if name not in posters:
                        posters[name] = 1
                    else:
                        posters[name] = posters[name] + 1
            for p in posters:
                print "%s posted %d times" % (p,posters[p])

#. (optional: 1 bonus point; this one is much harder)  Use the Facebook data to determine who made the longest post or comment (most characters); print out the poster's name and the contents.

   .. tabbed:: ps_3_4_tabs

      .. tab:: Problem

         .. actex:: ps_3_4

            fb = """
            # Delete this line and paste file contents here
            """

            x = fb.split("\n")

      .. tab:: Solution

         .. actex:: ps_3_4s

            fb = """
            # Delete this line and paste file contents here
            """

            x = fb.split("\n")

            # use an accumulator pattern, but with two accumulator
            # variables, one for the longest post, and another
            # for the person who made it.
            longest_post = ""   # initialize to empty
            poster = "" #initialize to empty
            
            contents = "" #initialize accumulator for contents of current post
            name = "" # the person who posted the current/prev post
            
            for ln in x:
                # Check if previous post's contents are the longest so far
                if ln[:5] == 'from:':
                    # if a line starting with from
                    
                    # check if previous post should replace longest
                    if len(contents) > len(longest_post):
                        longest_post = contents
                        poster = name
                    
                    # keep track of the name to
                    # use on the next iteration
                    name = ln[6:].lstrip()
                    contents = "" #initialize an accumulator to get the full string for this comment
                else:
                    #it's a content line, but may need to strip off "comment:" or "post:" from beginning
                    if ln[:8] == 'comment:':
                        contents = contents + ln[9:]
                    elif ln[:5] == 'post:':
                        contents = contents = ln[6:]
                    else:
                        # it's a continuation of the comment from previous line
                        contents = contents + '\n' + ln     
            
            # check if last post should replace longest
            if len(contents) > len(longest_post):
                longest_post = contents
                poster = name
            
            print(poster)
            print(longest_post)
            
            #Note: Nick has a more elegant solution for this one, that's
            #a little easier to follow, with fewer special cases, but
            #it uses "nested" data structures, which we won't be
            #covering for a couple more weeks.