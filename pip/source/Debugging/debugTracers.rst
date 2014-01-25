..  Copyright (C)  Nick Reid, Jackie Cohen, Paul Resnick.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. _debugging_2:

Don't Guess What Your Program Does
==================================

To build on lessons learned in the first debugging interlude, we are going to talk about practical ways to to debug your program. Our goal in this section is to encourage you to do anything but guess at what is happening in your program. There are two basic steps to not guessing, and while they might seem obvious, even the most professional programmers occasionally skip these steps. These suggestions are similar to the first debugging interlude, but we don't think they can't be emphsized enough.

The two steps are:

1. **Outline first** We are suggesting you frist write down all the steps you want the program to do. You can do this in any manner you like. We are going to show you how to outline using comments, but if you are more visual you might want to sketech on a piece of paper and if you are more spatial try walking around the room.

2. **Print one section at a time** After you outline your program, build each piece one section at a time. The idea here is to test each section to make sure you are getting what you think you should. What you will find is the real challenge of this techinque is keeping these tests neat enough for you to work with.

What you will find is that these steps iterate on eachother, so start with an outline, print what you can, outline the finer details and then test those fine details.

Creating Outlines
-----------------

Sometimes the most difficult part of writing a program is figuring out what you need it to do. For most people trying to describe this in a programming language is daunting because you have to think in a foreign syntax with symbols that aren't obvious. The big trick is to put the program into terms that you can understand.

As we stated earlier, we are going to focus on using comments to outline a program, but there are many other methods, and since the value in outlining is for your own understanding. Feel free to translate this method to another medium, be it a whiteboard or pile of post its. Don't worry about communicating to anyone but yourself.

Start by making a quick outline, focusing on what you have at the start and what you want the program to do at the end. Don't get caught in the details at this point, if you don't know how to do something just vaguely describe what you want the end result to be and move on.

For example, let's work on a program that counts the number of times any word appears in an article.

**Example**

Since we didn't know how to check if a word had already been counted we just skipped over that section with a vague comment.

Our next step is to write the sections that we know how to do, and write simple statements to make sure they are working correctly.


Print First, Ask Questions Later
--------------------------------


Clean It Up Afterwards
----------------------

When you are done with your outlining and testing, delete it. No one really needs to see all the test statments you wrote, and leaving your old test statments in the program might confuse you.

To make sure your program is easy for other people to read, only leave in the comments that you think are most useful. There is an art to having good informative comments, and you can only learn this art by reading other people's programs and having your peers read your programs. As a rule for comments, when in doubt, delete it.

Exercises
---------
