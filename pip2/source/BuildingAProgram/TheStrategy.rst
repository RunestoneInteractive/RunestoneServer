..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Building A Program: A Strategy
==============================

Building on lessons learned in the first debugging interlude, this chapter offers a strategy for writing a program to solve a problem such as those that appear in the exercises at the ends of the chapters in this book. (A similar approach is helpful for writing larger programs, but that will come later.)

.. admonition:: Warning. 

   You may find it tempting to start an exercise by copying and pasting a snippet of code from somewhere in the textbook, and hoping that a small edit will lead to a solution to the current problem. Often this will lead to frustration and confusion; after trying a few code substitutions that feel vaguely familiar to you, you’ll find the code looking kind of complicated and the outputs baffling. 
   
   Copying and editing snippets of code is actually a useful element of the strategy we outline below. But it comes a little later in the process, not as the first thing. And it requires a fair bit of work to make sure you understand the code snippet that you’ve copied. Only then will you be able to find the *right* small edits to the code snippet to make it do what you want.

There are three basic steps to the strategy we recommend: Outline; Code One Section at a Time; Clean Up.

Sketch an Outline
-----------------

We are suggesting you first write down all the steps you want the program to do. You can do this in any manner you like. We are going to show you how to outline using comments, but if you are more visual you might want to sketch on a piece of paper and if you are more spatial try walking around the room. The big trick is to understand everything you want to do first in your own words, so then you are translating them to the computer.

Code One Section at a Time
--------------------------

After you outline your program, you should write code one section at a time, and carefully test that section before you go on. The idea here is to make sure your program is doing what you think it’s doing at each stage.

Translating your English description of a step into code may be the most challenging step for you early in your learning about programming. Later it will come more naturally. Here is a checklist of questions that you may find useful in trying to find the right python code to express your idea, based on what you’ve learned so far:

* Is this operation pulling out an item from a list or string or dictionary? If so, use [] to pull out the item you want.
* Is this operation transforming a string into another string? If so, look at the summary of :ref:`string methods <string_methods>`
* Is this operation modifying a list? If so, look at the material on :ref:`lists <lists>`.
* Is the operation doing something multiple times? If so, you’ll want a ``for`` loop. Start by making a skeleton version of a for loop, and then fill in the parts that are in <brackets>

::

  for <varname> in <seq>:
                  <code block line 1>
                  <code block line 2>
                  ...

* Is the operation something that should only occur in some circumstances and not in others? If so, you’ll want an ``if`` statement. Start by making a skeleton version of an if/then/else code snippet, and then fill in the parts that are in <brackets>

::

  if <boolean exp>:
    <if block here>
    ...
  else:
    <else block here>
    ...

* Is this an accumulator pattern? If so, start by making a skeleton version of it, and then fill it in.

::

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
