..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

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

