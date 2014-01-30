:orphan:

..  Copyright (C) Paul Resnick, Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

..  shortname:: Assignments
..  description:: This chapter is where all the assignments for Umich SI 106 are stored.

.. highlight:: python
    :linenothreshold: 500

Week 5: ends February 7
=======================

For this week you have the following graded activities:

1. Do the multiple choice questions and exercises in the textbook chapters, including the ones at the bottom of the chapters, below the glossary. Don't forget to click **Save** for each of the exercises.

   * Before Tuesday's class:      
      * Functions
   
   * Before Thursday's class:
      * Local and global variables

#. Turn in the reading response, by 8 PM the night before your registered section meets.

   * Read *The Most Human Human*, Chapter 5, "Getting out of Book"
   * :ref:`Reading response 4 <response_4>`

#. Save answers to the exercises in Problem Set 4:

   * :ref:`Problem Set 4 <problem_set_4>`

.. _response_4:

Reading Response
----------------

**Due 8PM the night before your section meets**

Don't forget to click **save**.
   
   Question 1.

   .. actex:: rr_4_1

      # Fill in your response in between the triple quotes
      """

      """

   Question 2.

   .. actex:: rr_4_2

      # Fill in your response in between the triple quotes
      """

      """

   What would you like to talk about in section this week?
   
   .. actex:: rr_4_3

      # Fill in your response in between the triple quotes
      """

      """

.. _problem_set_4:

Problem Set
-----------

**Due:** **Friday, February 7, 5 pm**

**Instructions:** Write the code you want to save in the provided boxes, and click **save** for each one. 
The last code you have saved for each one by the deadline is what will be graded.


1. (2 points) Warm up exercises on calling functions

   .. actex:: ps_4_1

      def add_em_up(L):
         sum = 0
         for x in L:
            sum = sum + x
         return sum
         
      def longer(x, y):
         if len(x) > len(y):
            return x
         elif len(x) < len(y):
            return y
         else:
            return "same length"

      # Write code that invokes add_em_up in order to compute the sum of the
      # numbers from 1 through 20 (hint: try printing range(21))
      
      # Write code that invokes the longer function to determine 
      # whether "supercalifragilisticexpialidocious" or "antidisestablishmentariansim" is longer)

#. (2 points) Warm up exercises on defining functions

   .. actex:: ps_4_2
   
      # Define a function square that takes a number and returns that number multiplied by itself
      
      # Define a function is_prefix that takes two strings and returns True if the 
      # first one is a prefix of the second one, False otherwise.
      
      print(square(3))
      #should be 9
      
      print(prefix("He", "Hello"))
      # should be True
      print(prefix("He", "I said Hello"))
      # should be False
   
#. (2 points) Define the blanked function

   .. actex:: ps_4_3

      # define the function blanked(). 
      # It takes a word and a string of letters that have been revealed.
      # It should return a string with the same number of characters as
      # the original word, but with the unrevealed characters replaced by _ 
            
      def blanked(word, revealed_letters):
      
      print(blanked("Hello", "el"))
      #should output _ell_
   
#. (2 points) Define the health_prompt function

   .. actex:: ps_4_4

      #define the function health_prompt(). The first parameter is the current
      #health and the second the maximum health. It should return a string with + signs for
      #the current health and - signs for the health that has been lost
      
      
      print(health_prompt(3, 7))
      #this should produce the output
      #health: +++----
      
      print(health_prompt(0, 4))
      #this should produce the output
      #health: ----

     
#. (2 points) Cut and paste your two function definitions at the top of this code. Then replace the line with a comment that says to invoke the function game_state_prompt. Run the code to play the game with a friend! Feel free to change max_health if you want to make the game easier or harder to win. For fun, feel free to replace your output_health function with something that produces cool ASCII art of a hangman. (Try Googling "Hangman ASCII art".)

   .. activecode:: ps_4_5

      def game_state_prompt(txt, h, m_h, word, guesses):
          res = txt + "\n"
          res = res + health_prompt(h, m_h) + "\n"
          if guesses != "":
              res = res + "Guesses so far: " + guesses.upper() + "\n"
          else:
              res = res + "No guesses so far" + "\n"
          res = res + "Word: " + blanked(word, guesses) + "\n"
          
          return(res)
      
      def main():
          max_health = 3
          health = max_health
          #to_guess = raw_input("What's the word to guess? (Don't let the player see it!)")
          to_guess = "Reno"
          to_guess = to_guess.upper() # everything in all capitals to avoid confusion
          guesses_so_far = ""
          game_over = False
      
          feedback = "let's get started"

          # Now interactively ask the user to guess
          while not game_over:
              # replace this comment with code that invokes game_state_prompt and assign the return value to the variable prompt
              next_guess = raw_input(prompt)
              next_guess = next_guess.upper()
              feedback = ""
              if len(next_guess) != 1:
                  feedback = "I only understand single letter guesses. Please try again."     
              elif next_guess in guesses_so_far:
                  feedback = "You already guessed that"
              else:
                  guesses_so_far = guesses_so_far + next_guess
                  if next_guess in to_guess:
                      if blanked(to_guess, guesses_so_far) == to_guess:
                          feedback = "Congratulations"
                          game_over = True
                      else:
                          feedback = "Yes, that letter is in the word"
                  else: # next_guess is not in the word to_guess
                      feedback = "Sorry, " + next_guess + " is not in the word."
                      health = health - 1
                      if health <= 0:
                          feedback = " Waah, waah, waah. Game over."
                          game_over= True
      
              # make a call to output_game_state here, with appropriate parameter values
              #output_game_state(feedback, health, max_health, to_guess, guesses_so_far)
          print(feedback)
          print("The word was..." + to_guess)
      
      import sys #don't worry about this line; you'll understand it next week
      sys.setExecutionLimit(60000)     # let the game take up to a minute, 60 * 1000 milliseconds
      main()      
   


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

For the next three exercises, you will analyze data from our group on Facebook. To 'load' the data you will need to copy and paste it into the python prompt, in between the quotation marks. To maintain confidentiality (i.e., only students in 106 can see it), the data lives in a `file on cTools. <https://ctools.umich.edu/access/content/group/80ba0083-6409-4149-8222-f210f9dc6dd1/Problem%20Sets/PS3/simplefbdata.txt>`_

#. (2 points) For each post or comment in the facebook group, print out the name of the poster.

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

#. (2 points) Use the Facebook data to count the number of posts (or reply comments) each person made in the Facebook group.

   .. actex:: ps_3_3

      fb = """
      # Delete this line and paste file contents here
      """

      x = fb.split("\n")

      # Your output should look something like this, but with different numbers:
      # Paul R. posted 1 times  (# or, if you're ambitious, make it say 1 time instead of 1 times)
      # Jackie C. posted 3 times
      # Nick R. posted 2 times

#. (optional: 1 bonus point; this one is much harder)  Use the Facebook data to determine who made the longest post or comment (most characters); print out the poster's name and the contents.

   .. actex:: ps_3_4

      fb = """
      # Delete this line and paste file contents here
      """

      x = fb.split("\n")


Week 3: ends January 24
=======================

For this week, you have the following graded activities:

1. Do the multiple choice questions and exercises in the textbook chapters, including the ones at the bottom of the chapters, below the glossary. Don't forget to click **Save** for each of the exercises.

   * Before Tuesday's class:
      * :ref:`Iteration <iteration_chap>`
   * Before Thursday's class:
      * :ref:`Conditionals <decisions_chap>`
      * :ref:`File Input/Output <files_chap>` (read the Selection/Conditionals chapter first, or you won't be able to do the last exercise...)

#. Turn in the reading response, by 8 PM the night before your registered section meets.
  
   * Read *The Most Human Human*, Chapter 4, "Site-Specificity vs. Pure Technique"
   * :ref:`Reading response 2 <response_2>`

#. Save answers to the exercises in Problem Set 2:

   * :ref:`Problem Set 2 <problem_set_2>`

.. _response_2:

Reading Response
----------------

**Due 8PM the night before your section meets**

Don't forget to click **save**.

1. What did you find particularly interesting in this chapter?  How do you define *site-specificity* based on this reading? When is site-specificity important, and when is it not? What would you like to address in discussion? 

Please write a short paragraph addressing these questions, below.

   .. actex:: rr_2_1
   
      # Fill in your short paragraph answer (about 100-250 words) on the lines between the triple quotes.
      s = """
      
      
      """


.. _problem_set_2:

Problem Set
-----------

.. datafile::  about_programming.txt
   :hide:

   Computer programming (often shortened to programming) is a process that leads from an
   original formulation of a computing problem to executable programs. It involves
   activities such as analysis, understanding, and generically solving such problems
   resulting in an algorithm, verification of requirements of the algorithm including its
   correctness and its resource consumption, implementation (or coding) of the algorithm in
   a target programming language, testing, debugging, and maintaining the source code,
   implementation of the build system and management of derived artefacts such as machine
   code of computer programs. The algorithm is often only represented in human-parseable
   form and reasoned about using logic. Source code is written in one or more programming
   languages (such as C++, C#, Java, Python, Smalltalk, JavaScript, etc.). The purpose of
   programming is to find a sequence of instructions that will automate performing a
   specific task or solve a given problem. The process of programming thus often requires
   expertise in many different subjects, including knowledge of the application domain,
   specialized algorithms and formal logic.
   Within software engineering, programming (the implementation) is regarded as one phase in a software development process. There is an on-going debate on the extent to which
   the writing of programs is an art form, a craft, or an engineering discipline. In
   general, good programming is considered to be the measured application of all three,
   with the goal of producing an efficient and evolvable software solution (the criteria
   for "efficient" and "evolvable" vary considerably). The discipline differs from many
   other technical professions in that programmers, in general, do not need to be licensed
   or pass any standardized (or governmentally regulated) certification tests in order to
   call themselves "programmers" or even "software engineers." Because the discipline
   covers many areas, which may or may not include critical applications, it is debatable
   whether licensing is required for the profession as a whole. In most cases, the
   discipline is self-governed by the entities which require the programming, and sometimes
   very strict environments are defined (e.g. United States Air Force use of AdaCore and
   security clearance). However, representing oneself as a "professional software engineer"
   without a license from an accredited institution is illegal in many parts of the world.
 


**Due:** **Friday, January 24, 5 pm**

**Instructions:** Write the code you want to save in the provided boxes, and click **save** for each one. The last code you have saved for each one by the deadline is what will be graded.

1. (2 points) Print out each element of list ``lbc`` on a separate line. Then print the first character of each element on a separate line.

   .. tabbed:: ps_2_1s

      .. tab:: Problem

         .. actex:: ps_2_1
         
            lbc = ["one","four","two","six","nine","eleven"]
            
            # write code to print each element of list lbc on a separate line
            
            # write code to print the first character of each element of list lbc on a separate line

      .. tab:: Solution

         .. actex:: ps_2_1a
         
            lbc = ["one","four","two","six","nine","eleven"]
            
            # write code to print each element of list lbc on a separate line
            for elem in lbc:
               print elem

            # write code to print the first character of each element of list lbc on a separate line
            for elem in lbc:
               print elem[0]


#. (2 points) See comments for instructions, below. This and the next question deal with the string ``rv``.

   .. tabbed:: ps_2_2s

      .. tab:: Problem

         .. actex:: ps_2_2

            rv = """Once upon a midnight dreary, while I pondered, weak and weary,  
               Over many a quaint and curious volume of forgotten lore,  
               While I nodded, nearly napping, suddenly there came a tapping,   
               As of some one gently rapping, rapping at my chamber door.   
               T is some visitor, I muttered, tapping at my chamber door;           5
               Only this and nothing more."""
            
            # Write code to print the number of characters in the string rv.
            
            # Write code to print the number of words in the string rv. 
            ## Hint: use the split method 

      .. tab:: Solution

         .. actex:: ps_2_a

            rv = """Once upon a midnight dreary, while I pondered, weak and weary,  
               Over many a quaint and curious volume of forgotten lore,  
               While I nodded, nearly napping, suddenly there came a tapping,   
               As of some one gently rapping, rapping at my chamber door.   
               T is some visitor, I muttered, tapping at my chamber door;           5
               Only this and nothing more."""
            
            # Write code to print the number of characters in the string rv.
            print len(rv)

            # Write code to print the number of words in the string rv. 
            ## Hint: use the split method 
            print len(rv.split())


#. (1 point) See comments for instructions, below. 
   
   .. tabbed:: ps_2_3s

      .. tab:: Problem

         .. actex:: ps_2_3
          
            rv = """Once upon a midnight dreary, while I pondered, weak and weary,  
               Over many a quaint and curious volume of forgotten lore,  
               While I nodded, nearly napping, suddenly there came a tapping,   
               As of some one gently rapping, rapping at my chamber door.   
               T is some visitor, I muttered, tapping at my chamber door;           5
               Only this and nothing more."""
            
            # (For these questions, imagine that you couldn't see the whole string value, 
            # but you still needed to answer them.)
            
            # Write code to find out whether the word "raven" is in the string rv. 
            # Print "Yes" if it is, and "No" if it isn't.
            
            # Write code to find out whether the word "rapping" is in the string rv. 
            # Print "Yes" if it is, and "No" if it isn't.

      .. tab:: Solution

         .. actex:: ps_2_3a
          
            rv = """Once upon a midnight dreary, while I pondered, weak and weary,  
               Over many a quaint and curious volume of forgotten lore,  
               While I nodded, nearly napping, suddenly there came a tapping,   
               As of some one gently rapping, rapping at my chamber door.   
               T is some visitor, I muttered, tapping at my chamber door;           5
               Only this and nothing more."""
            
            # (For these questions, imagine that you couldn't see the whole string value, 
            # but you still needed to answer them.)
            
            # Write code to find out whether the word "raven" is in the string rv. 
            # Print "Yes" if it is, and "No" if it isn't.
            if "raven" in rv:
               print "Yes"
            else:
               print "No"

            # also reasonable:
            if "raven" in rv.split():
               print "Yes"
            else:
               print "No"
            
            # Write code to find out whether the word "rapping" is in the string rv. 
            # Print "Yes" if it is, and "No" if it isn't.
            if "rapping" in rv:
               print "Yes"
            else:
               print "No"

            # also reasonable:
            if "rapping" in rv.split():
               print "Yes"
            else:
               print "No"



   The remaining questions in the problem set deal with a file called ``about_programming.txt`` 
   that you can access in an ActiveCode window using the open() function. 
   It is made up of text from the *Computer Programming* article on Wikipedia; ``http://en.wikipedia.org/wiki/Computer_programming``.

#. (1 point) Write code to open the file, about_programming.txt, and print it out, line by line.
   
   .. tabbed:: ps_2_4s

      .. tab:: Problem

         .. actex:: ps_2_4

            # Don't worry about extra blank lines between each of the lines
            # (but if you want to get rid of them, try the .strip() method)

      .. tab:: Solution

         .. actex:: ps_2_4a

            # Don't worry about extra blank lines between each of the lines
            # (but if you want to get rid of them, try the .strip() method)
            f = open("about_programming.txt", 'r')
            # here's the code without the .strip() method
            for orange in f:
               print orange
            # here's the code that'll print without all that extra blank space
            for orange in f:
               print orange.strip()


#. (2 points) Print the number of lines in the file
   
   .. tabbed:: ps_2_5s

      .. tab:: Problem

         .. actex:: ps_2_5

      .. tab:: Solution

         .. actex:: ps_2_5a

            hmf = open("about_programming.txt", 'r')
            total = 0
            for ln in hmf:    # loops the lines in the file, one at a time
               total = total + 1    # ln is bound to the current line of text, but we don't need to refer to it since we only care that it's another line, not what it is

            print total
            
            # alternative solution
            hmf = open("about_programming.txt", 'r')
            ls = hmf.readlines()  # get the text as a list of strings, one for each line
            print len(ls)
            
            # another alternative
            hmf = open("about_programming.txt", 'r')
            t = hmf.read()    # save the whole text in string t
            ls = t.split('\n') # make it into a list of strings, one for each line
            print len(ls)
            # you get a slightly different answer here; try to figure out why
            

#. (2 points) Print the number of lines in the file that include the word "program" or any extension of it (program, programs, programming, programmer).

   .. tabbed:: ps_2_6s

      .. tab:: Problem

         .. actex:: ps_2_6

      .. tab:: Solution

         .. actex:: ps_2_6a

            tot = 0
            ft = open("about_programming.txt", "r")
            for mtfq in ft:
               if "program" in mtfq:       # mtfq is bound to the current line of text, and here we do care what that text is
                  tot = tot + 1
            print tot


#. *1 BONUS POINT* (not required): Write code to find, and print, the number of vowels in the file.
   
   .. tabbed:: ps_2_7a

      .. tab:: Problem

         .. actex:: ps_2_7

            # Write your code here, if you choose to try this problem!
      
      .. tab:: Solution

         .. actex:: ps_2_7a

            # Write your code here, if you choose to try this problem!

            # here is one solution
            f = open("about_programming.txt", 'r')
            whole_file = f.read()
            vowels = ["a","e","i","o","u"]
            amt = 0
            for v in vowels:
               amt = amt + whole_file.count(v)
            print amt




Week 2: ends January 17
=======================

For this week, you have the following graded activities:

1. Do the mutliple choice questions and exercises in the textbook chapters, including the ones at the bottom of the chapters, below the glossary. Don't forget to click Save for each of the exercises.
   
   * Before Tuesday's class: 
      * :ref:`Simple Python Data <simple_python_data>`
      * :ref:`Debugging Interlude <debugging_1>`
   * Before Thursday's class:
      * :ref:`Sequences <sequences_chap>`

#. Turn in the reading response, by 8PM the night before your registered section meets

   * *The Most Human Human*, Chapter 3, "The Migratory Soul"
   * :ref:`Reading response 1 <response_1>`


#. Save answers to the six exercises in Problem Set 1:
   * :ref:`Problem Set 1 <problem_set_1>` 


.. _response_1:

Reading Response
----------------

**Due 8PM the night before your section meets**

Don't forget to click "save" for each of these.

1. If you had to give up either your left-brain functions or your right-brain functions, which would you give up?

   .. actex:: rr_1_1
   
      # Fill in your answer on the lines between the triple quotes
      s = """
      
      
      """
      
#. What's one interesting thing you learned from the chapter? 

   .. actex:: rr_1_2
   
      # Fill in your answer on the lines between the triple quotes
      s = """
      
      
      """

#. What's one question you have or something that you'd like to have discussed during section?

   .. actex:: rr_1_3
   
      # Fill in your answer on the lines between the triple quotes
      s = """
      
      
      """



.. _problem_set_1:

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
            print "Nice to meet you,",nm