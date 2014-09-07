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

