..  Copyright (C)  Nick Reid, Jackie Cohen, Paul Resnick.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. _debugging_2:

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

Don't Guess What Your Program Does
==================================

To build on lessons learned in the first debugging interlude, we are going to talk about practical ways to to debug your program. Our goal in this section is to encourage you to do anything but guess at what is happening in your program. There are three basic steps to not guessing, and while they might seem obvious, even the most professional programmers occasionally skip these steps. These suggestions are similar to the first debugging interlude, but we don't think they can't be emphasized enough.

The three steps are: Outline, Print, and Clean Up.

What you will find is that these steps iterate on eachother, so start with a general outline, print what you can, and then clean up your code once it works.

Sketch an Outline
-----------------

We are suggesting you first write down all the steps you want the program to do. You can do this in any manner you like. We are going to show you how to outline using comments, but if you are more visual you might want to sketch on a piece of paper and if you are more spatial try walking around the room. The big trick is to understand everything you want to do first in your own words, so then you are translating them to the computer.

Print to Understand
-------------------

After you outline your program, you will want to build one section at a time, and carefully test each section at a time by printing the value of variables. The idea here is to make sure your program is doing what it should be. Writing good print statements can be challenging, but just keep in mind that your goal is to understand how the program is changing.

In the following code block there are some examples of print statements, that can help you understand what is happening in a for loop. In this program we are adding all the even numbers in a list together. You will see a print statement for each loop, and after the loop stops running, which make it easier to see what is happening.

.. activecode:: db2_sample_print
    
    numbers = [1,2,6,4,5,6]

    z = 0
    for num in numbers:
      print("*** LOOP ***")
      print("Num =",num)
      if(0 % 2):
        print("Is even. Adding",num,"to",z)
        z = num + z
      print ("Z =",z)
    print("*** LOOP ***")


Clean Up Afterwards
-------------------

When you are done with outlining and testing your program, delete these statements from your program. No one really needs to see the test statements you wrote, and leaving test statements in the program might confuse you if you add more to the program.

Extra comments do help other people read your code, but try to leave in only the bits that you think are the most useful. There is an art to writing good informative comments, and you can only learn this art by reading other people's programs and having your peers read your programs. As a rule for comments, when in doubt, delete it.

An Example
----------

The rest of this chapter is dedicated to working though an example of this method together. We will write a program that counts the number of different words used in an article. We will then output the most used word.

Our first step is to make a quick outline, just focusing on the broad steps that the program will take. The trick is to not get caught up in small details at this point, and get the entire program written. If you don't know how to do a specific step that you know needs to happen, don't get caught in that detail, and just write a vague comment and move on.

Here is an example of what an outline of our program could look like.

.. activecode:: db2_ex_1_0
    
    # 1 - Open the file

    # 2 - Read each word and store it in a dictionary

    # 3 - Find the most used word

    # 4 - Print the most used word

Notice how there are only two comments with very specific actions. One at the begining and another at the end, these are useful because it tells us where we want to start, and where we are going to end. The other two comments are much more vauge, but thats ok, because we will work our way there after getting comments 1 and 4 working.

.. activecode:: db2_ex_1_1
    
    # 1 - Open the file
    f = open('about_programming.txt', 'r')
    print(f)

    # 2 - Read each word and store it in a dictionary

    # 3 - Find the most used word

    # 4 - Print the most used word
    most_used = '?????'
    print(most_used)

The most important things to notice here is that we tested that our file "f". By immediatly testing it, we know that this part of the program works. We also now know what type of variable we are working with, so we could look up how to work with it if we didn't remember.

The other thing to notice is that we already wrote the end of our program. The value of the variable "most_used" is fake, but we now know that we want our program to set the variable "most_used" in comment number 3.

Filling in Details
------------------

We now have an option of which section of code we want to write next, comment number 2 or 3. You could do either section first, but for the sake of this chapter, we are going to write section 3 first because we have an idea of what section 2 will do.

**Example**

There are many things different in this version of our program than the last. We have deleted the line that set the variable "most_used" in section 4, because we are now actually setting it in section 3 (on line 11).

On line 6 we defined a dictionary called words. This dictionary represents what section 2 is supposed to accomplish, yet we can assume that our dictionary is shorter and simpler than what will be produced in section 2. This is helpful because we can quickly look at the dictionary words and understand that 'something' is the most used word, so we know exactly the value that should be output at the end.

Inside the for loop on line 13, we see many different print statements, which all explain what is happening each time the program loops through a word. This gives us very clear output as to what is happening in our program.

The last section of our code is section 2, where we need to create a dictionary of each word, and count every time the word appears. Our first step should be to clean up our code from section 3 and sketch out the specific tasks we need to accomplish.

**Example**

Now that we have our outline, and only the most relivant print statements, we are ready to start filling in the code.