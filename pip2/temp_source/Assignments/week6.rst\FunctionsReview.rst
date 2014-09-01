..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Functions Review
----------------

These are review problems that we worked on and discussed in section this week. Each problem asks you to define a function, specifies the input that the function takes, and what the function should do.

The problems AND the solutions are provided for you, since you worked on them in class. (Problems and questions you addressed in discussion may vary slightly by section!) We suggest that you try to do the problems again yourself before looking at the solutions (which are heavily commented to address questions that came up in the discussion group work).

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


