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
**Due:** **Friday, January 17, 5 pm**

**Instructions:** Write the code you want to save in the provided boxes, and click **save** for each one. The last code you have saved for each one by the deadline is what will be graded.

1. (1 pt) Given the following code, write a print statement that will pick out the letter ``"o"``, from the string ``s``. 

   .. actex:: ps_1_1

       s = "Hello, all"
      
      

#. (1 pt) Write code to print this string WITHOUT any ``&`` signs.

      This is a really fun&& homework assign&ment. And & I love&& &&Python.

   .. actex:: ps_1_2
   
         # Here's the string provided for you
         nst = "This is a really fun&& homework assign&ment. And & I love&& &&Python."
      
      # Write your code to print this string without any "&s", below:
      

#. (1 pt) What is the index of the first letter "h" in this sentence? Write code to find it, and print it. (Remember, an index is the __th element of a string or a list, for example.)

      This is a really fun homework assigment, and I love Python.

   .. actex:: ps_1_3
   
         # Here's the sentence, provided for you
         st = "This is a really fun homework assigment, and I love Python."
      
      ## Write your code to find the first index of the letter "h" below:
   

#. (3 pts) See comments for instructions.

   .. actex:: ps_1_4
      
      abc = [1,2,3,4,5,6,7]
      
      # What is the type of value is in the variable abc? 
      # Write code to find out what type the value of abc is.
      
      ## Write the type here: _______
      
      # write code to extract and print the first three elements of abc
      
      # write code to extract and print the last element of abc
      
      # write code to extract and print the number 4 from abc
      
      # write code to extract and print the number 6 from abc
      
      # write code to find out what type the first element of abc is, and print it.



#. (2 pts) See the comments for instructions.

   .. actex:: ps_1_5
   
      xy_lst = ["hello","goodbye","welcome","106","si 106"]
      abc_sentence = "Welcome to SI 106, everyone."
      
      # write code to extract and print the first element of xy_lst
      
      # write code to extract and print the last element of xy_lst
      
      # write code to extract and print the first character of abc_sentence
      
      # write code to extract and print the last character of abc_sentence

         
#. (2 pts) Write code to ask the user for their name and print out ``"Nice to meet you, <THEIR NAME>"``

   .. actex:: ps_1_6
   
      # For example, if you enter "Nick", your code should then print "Nice to meet you, Nick" abc
            print abc[:3]
            ## other possibilities include:
            # print a[0], a[1], a[2]
            
            # write code to extract and print the last element of abc
            print abc[-1]
            
            # write code to extract and print the number 4 from abc
            print abc[3]
            
            # write code to extract and print the number 6 from abc
            print abc[5]
            
            # write code to find out what type the first element of abc is, and print it.
            print type(abc[0])



#. (2 pts) See the comments for instructions.

   .. tabbed:: ps_1_5s

      .. tab:: Problem

         .. actex:: ps_1_5
         
            xy_lst = ["hello","goodbye","welcome","106","si 106"]
            abc_sentence = "Welcome to SI 106, everyone."
            
            # write code to extract and print the first element of xy_lst
            
            # write code to extract and print the last element of xy_lst
            
            # write code to extract and print the first character of abc_sentence
            
            # write code to extract and print the last character of abc_sentence

      .. tab:: Solution

         .. actex:: ps_1_5_a
         
            xy_lst = ["hello","goodbye","welcome","106","si 106"]
            abc_sentence = "Welcome to SI 106, everyone."
            
            # write code to extract and print the first element of xy_lst
            print xy_lst[0]
            
            # write code to extract and print the last element of xy_lst
            print xy_lst[-1]
            
            # write code to extract and print the first character of abc_sentence
            print abc_sentence[0]
            
            # write code to extract and print the last character of abc_sentence
            print abc_sentence[-1]

            ## note that "first" and "last" for sequences are easy when you program! 

         
#. (2 pts) Write code to ask the user for their name and print out ``"Nice to meet you, <THEIR NAME>"``
   
   .. tabbed:: ps_1_6s

      .. tab:: Problem

         .. actex:: ps_1_6
         
            # For example, if you enter "Nick", your code should then print "Nice to meet you, Nick"

      .. tab:: Solution

         .. actex:: ps_1_6_a
         
            # For example, if you enter "Nick", your code should then print "Nice to meet you, Nick"
            nm = raw_input("Please enter your name: ")
