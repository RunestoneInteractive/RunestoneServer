..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

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
