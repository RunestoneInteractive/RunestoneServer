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

Building A Program
==================

Building on lessons learned in the first debugging interlude, this chapter offers a strategy for writing a program to solve a problem such as those that appear in the exercises at the ends of the chapters in this book. (A similar approach is helpful for writing larger programs, but that will come later.)

Warning. You may find it tempting to start an exercise by copying and pasting a snippet of code from somewhere in the textbook, and hoping that a small edit will lead to a solution to the current problem. Often this will lead to frustration and confusion; after trying a few code substitutions that feel vaguely familiar to you, you’ll find the code looking kind of complicated and the outputs baffling. Copying and editing snippets of code is actually a useful element of the strategy we outline below. But it comes a little later in the process, not as the first thing. And it requires a fair bit of work to make sure you understand the code snippet that you’ve copied. Only then will you be able to find the *right* small edits to the code snippet to make it do what you want.

There are three basic steps to the strategy we recommend: Outline; Code One Section at a Time; Clean Up.

Sketch an Outline
-----------------

We are suggesting you first write down all the steps you want the program to do. You can do this in any manner you like. We are going to show you how to outline using comments, but if you are more visual you might want to sketch on a piece of paper and if you are more spatial try walking around the room. The big trick is to understand everything you want to do first in your own words, so then you are translating them to the computer.

Code One Section at a Time
--------------------------

After you outline your program, you should write code one section at a time, and carefully test that section before you go on. The idea here is to make sure your program is doing what you think it’s doing at each stage.

Translating your English description of a step into code may be the most challenging step for you early in your learning about programming. Later it will come more naturally. Here is a checklist of questions that you may find useful in trying to find the right python code to express your idea, based on what you’ve learned so far:
* Is this operation pulling out an item from a list or string or dictionary? If so, use [] to pull out the item you want.
* Is this operation transforming a string into another string? If so, look at the summary of ref: string operations
* Is this operation modifying a list? If so, look at the summary of ref: list operations.
* Is the operation doing something multiple times? If so, you’ll want a ``for`` loop. Start by making a skeleton version of a for loop, and then fill in the parts that are in <brackets>

  for <varname> in <seq>:
                  <code block line 1>
                  <code block line 2>
                  ...

* Is the operation something that should only occur in some circumstances and not in others? If so, you’ll want an ``if`` statement. Start by making a skeleton version of an if/then/else code snippet, and then fill in the parts that are in <brackets>

  if <boolean exp>:
    <if block here>
    ...
  else:
    <else block here>
    ...

* Is this an accumulator pattern? If so, start by making a skeleton version of it, and then fill it in.

  #initialize accumulator
  a = <initial value>

  for <varname> in <seq>:
    <some code in for block>
    a = <new_value>
    <other code in for block>
  print a


Finally, you may be reminded of a snippet of code somewhere in the textbook that did something similar to what you want to do. Now is the time to copy and edit that code. **But wait!** Before you start editing that code snippet, make sure you understand it. See the section below on understanding code.

Clean Up
--------

When you are done with outlining and testing your program, delete any diagnostic print statements from your program. No one really needs to see the test statements you wrote, and leaving test statements in the program might confuse you if you add more to the program.

Extra comments do help other people read your code, but try to leave in only the bits that you think are useful. There is an art to writing good informative comments, and you can only learn this art by reading other people's programs and having your peers read your programs. As a rule of thumb for comments, when in doubt, keep it; it you’re worried it won’t make sense to you or someone else later, add more detail to it.

Understanding a Program
=======================

Whether you’re trying to understand a code snippet that someone else wrote or trying to understand your own code that isn’t doing exactly what you wanted, you can avoid a lot of frustration if you slow down and spend the time to fully understand that code. It will reduce your anxiety level as well and make programming more fun!

The basic strategy for understanding code is the explain; predict; check; loop.

Explain (Make a reference diagram)
----------------------------------

To understand what a snippet of code (one or more lines) does, you should first form a hypothesis about the *state* of the program just before your snippet executes.

It’s a good idea to make a reference diagram by hand, the kind of diagram that CodeLens produces for you. In particular, for each of the variable names that are referred to in the code snippet you are trying to understand, you should make a prediction about:
* the type of that variable’s value (integer, string, list, dictionary, etc.)
* the value of that variable

You should also be able to state, in English, what each of the operations in your code snippet does. For example, if your code snippet includes a line ``x.append(4)``, then you should be able to say, “The append operation takes a list, x in this case, and appends an item, 4 in this case, to the end of the list. It changes the actual list, so any other variable that is an alias for the list will also have its value changed.”

Predict
-------

In the predict phase, you will predict the effect of running a snippet of code. Later on in your development, you may make predictions about large snippets of code, but for now you will typically be predicting the effect of executing a single line of code, or at most the net effect of running an entire ``for`` loop. A prediction will either be about what gets printed out, or about the value of a variable, or that an error will occur.

A prediction is not a random guess. It is based on some explanation you have about what the current state of variables is and about what you think certain commands in python do.

Check
-----

To check your understanding or your predictions, you will run a program. 

To check your understanding about the state of variables before your code snippet runs, add diagnostic print statements that print out the types and values of variables. Add these print statements just *before* the code snippet you are trying to understand.

If you made a prediction about the output that will be generated when the code snippet runs, then you can just run the program. If, however, you made a prediction is about a change that occurs in the value of a variable, you will need to add an extra diagnostic print statement right after the line of code that you think should be changing that variable. 

The diagnostic print statements are temporary.  Once you have verified that a program is doing what you think it’s doing, you will remove these extra print statements.

If you get any surprises, then you will want to revise your understanding or your predictions. If you were wrong about the values or types of variables before the code snippet was run, you may to revisit your understanding of the previous code. 

If you were wrong about the effect of an operation, you may need to revisit your understanding of that operation. One good way to do that is to run that operation on some very simple values. For example, if you thought ``x.append([4, 5])`` appended x as the second element of the list that already contains 4 and 5, you might want to try it on even simpler values, like ``x.append(4)`` in order to realize that the item in parentheses in the one being appended, not the list one being appended to.

Example
-------

The following code illustrates what your program might look like after you complete the process above of adding comments that document your understanding and diagnostic print statements that allow you to check your understanding. This is what your code might look like prior to the cleanup phase.

In this program we are adding all the even numbers in a list together, accumulating a sum. You will see a diagnostic print statement inside the code block of the for loop, one inside the if statement, and even a diagnostic else clause that can be deleted entirely. All of these make it easier to check whether it’s doing what it’s supposed to do.
    
.. activecode:: db2_ex_1

    numbers = [1,2,6,4,5,6, 93]

    z = 0
    for num in numbers:
      print("*** LOOP ***")
      print("Num =",num)
      if (num % 2) == 0:
        print("Is even. Adding",num,"to",z)
        z = num + z
      print ("Running sum =",z)
    print("*** DONE ***")
    print ("Total = " , z)