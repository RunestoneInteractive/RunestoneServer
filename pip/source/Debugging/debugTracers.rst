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

To build on lessons learned in the first debugging interlude, we are going to talk about practical ways to to debug your program. Our goal in this section is to encourage you to do anything but guess at what is happening in your program. There are three basic steps to not guessing, and while they might seem obvious, even the most professional programmers occasionally skip these steps. These suggestions are similar to the first debugging interlude, but we don't think they can't be emphsized enough.

The three steps are:

Sketch an Outline
-----------------

We are suggesting you frist write down all the steps you want the program to do. You can do this in any manner you like. We are going to show you how to outline using comments, but if you are more visual you might want to sketech on a piece of paper and if you are more spatial try walking around the room.

Sometimes the most difficult part of writing a program is figuring out what you need it to do. For most people trying to describe this in a programming language is daunting because you have to think in a foreign syntax with symbols that aren't obvious. The big trick is to put the program into terms that you can understand.

As we stated earlier, we are going to focus on using comments to outline a program, but there are many other methods, and since the value in outlining is for your own understanding. Feel free to translate this method to another medium, be it a whiteboard or pile of post its. Don't worry about communicating to anyone but yourself.

Print to Understand
-------------------

After you outline your program, build each piece one section at a time. The idea here is to test each section to make sure you are getting what you think you should. What you will find is the real challenge keeping these tests neat enough for you to work with.

Clean Up Afterwards
-------------------

The last step is to remove the print statements and outline comments as you get sections of your program working. The reason to do this is so it is easy for you to read your program, and the output your program makes.

When you are done with your outlining and testing, delete it. No one really needs to see all the test statments you wrote, and leaving your old test statments in the program might confuse you.

To make sure your program is easy for other people to read, only leave in the comments that you think are most useful. There is an art to having good informative comments, and you can only learn this art by reading other people's programs and having your peers read your programs. As a rule for comments, when in doubt, delete it.

What you will find is that these steps iterate on eachother, so start with a general outline, print what you can, outline the finer details, then test those fine details and once you get a section working clean it up and move to the next section.

The rest of this chapter is dedicated to working though an example of this method together. We will write a program that counts the number of different words used in an article. We will then output the most used word.

An Example
----------

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

-- activecode:: db2_ex_1_2
    
    f = open('about_programming.txt', 'r')

    # 2 - Read each word and store it in a dictionary

    # 3 - Find the most used word
    words = {
      'this':3,
      'something':7,
      'melon':2,
    }
    most_used = words.keys()[0]
    for w in words:
      print("***** LOOP *****")
      print("w=",w," occurs",words[w])
      print("most_used=",most_used," occurs",words[most_used])
      if words[w] > words[most_used]:
        print("Set ",w," as most_used")
        most_used = w
    print("***** END LOOP *****")

    # 4 - Print the most used word
    print(most_used)

There are many things different in this version of our program than the last. We have deleted the line that set the variable "most_used" in section 4, because we are now actually setting it in section 3 (on line 11).

On line 6 we defined a dictionary called words. This dictionary represents what section 2 is supposed to accomplish, yet we can assume that our dictionary is shorter and simpler than what will be produced in section 2. This is helpful because we can quickly look at the dictionary words and understand that 'something' is the most used word, so we know exactly the value that should be output at the end.

Inside the for loop on line 13, we see many different print statements, which all explain what is happening each time the program loops through a word. This gives us very clear output as to what is happening in our program.

The last section of our code is section 2, where we need to create a dictionary of each word, and count every time the word appears. Our first step should be to clean up our code from section 3 and sketch out the specific tasks we need to accomplish.

-- activecode:: db2_ex_1_3
    
    f = open('about_programming.txt', 'r')

    # 2 - Read each word and store it in a dictionary
    # Define a variable to collect the words -- should be called words
    # Loop through each line of the file
    # Break apart each line
    # If the word doesn't exist in 'words', add it to the dictionary and set it to 1
    # Otherwise add 1 to the count of words

    # 3 - Find the most used word
    words = {
      'this':3,
      'something':7,
      'melon':2,
    }
    most_used = words.keys()[0]
    for w in words:
      if words[w] > words[most_used]:
        most_used = w

    # 4 - Print the most used word
    print(most_used)

Now that we have our outline, and only the most relivant print statements, we are ready to start filling in the code.

-- activecode:: db2_ex_1_4
    
    f = open('about_programming.txt', 'r')

    # 2 - Read each word and store it in a dictionary
    # Define a variable to collect the words -- should be called words
    words = {}
    # Loop through each line of the file
    for ln in f:
      # Break apart each line
      bits = ln.split()
      # If the word doesn't exist in 'words', add it to the dictionary and set it to 1
      # Otherwise add 1 to the count of words

    # 3 - Find the most used word
    most_used = words.keys()[0]
    for w in words:
      if words[w] > words[most_used]:
        most_used = w

    # 4 - Print the most used word
    print(most_used)
