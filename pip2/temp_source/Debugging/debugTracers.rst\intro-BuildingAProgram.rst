..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Introduction: Building A Program
==================

Building on lessons learned in the first debugging interlude, this chapter offers a strategy for writing a program to solve a problem such as those that appear in the exercises at the ends of the chapters in this book. (A similar approach is helpful for writing larger programs, but that will come later.)

.. admonition:: Warning. 

   You may find it tempting to start an exercise by copying and pasting a snippet of code from somewhere in the textbook, and hoping that a small edit will lead to a solution to the current problem. Often this will lead to frustration and confusion; after trying a few code substitutions that feel vaguely familiar to you, you’ll find the code looking kind of complicated and the outputs baffling. 
   
   Copying and editing snippets of code is actually a useful element of the strategy we outline below. But it comes a little later in the process, not as the first thing. And it requires a fair bit of work to make sure you understand the code snippet that you’ve copied. Only then will you be able to find the *right* small edits to the code snippet to make it do what you want.

There are three basic steps to the strategy we recommend: Outline; Code One Section at a Time; Clean Up.

