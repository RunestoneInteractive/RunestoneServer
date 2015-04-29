..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. qnum::
   :prefix: intro-10-
   :start: 1

Experimental Debugging
----------------------

One of the most important skills you will acquire is debugging.  Although it
can be frustrating, debugging is one of the most intellectually rich,
challenging, and interesting parts of programming.

In some ways, debugging is like detective work. You are confronted with clues,
and you have to infer the processes and events that led to the results you see.

Debugging is also like an experimental science. Once you have an idea what is
going wrong, you modify your program and try again. If your hypothesis was
correct, then you can predict the result of the modification, and you take a
step closer to a working program. If your hypothesis was wrong, you have to
come up with a new one. As Sherlock Holmes pointed out, When you have
eliminated the impossible, whatever remains, however improbable, must be the
truth. (A. Conan Doyle, *The Sign of Four*)

For some people, programming and debugging are the same thing. That is,
programming is the process of gradually debugging a program until it does what
you want. The idea is that you should start with a program that does
*something* and make small modifications, debugging them as you go, so that you
always have a working program.

For example, Linux is an operating system kernel that contains millions of
lines of code, but it started out as a simple program Linus Torvalds used to
explore the Intel 80386 chip. According to Larry Greenfield, one of Linus's
earlier projects was a program that would switch between displaying AAAA and
BBBB. This later evolved to Linux (*The Linux Users' Guide* Beta Version 1).

Later chapters will make more suggestions about debugging and other programming
practices.

**Check your understanding**

.. mchoicemf:: question1_9_1
   :answer_a: programming is the process of writing and gradually debugging a program until it does what you want.
   :answer_b: programming is creative and debugging is routine.
   :answer_c: programming is fun and debugging is work.
   :answer_d: there is no difference between them.
   :correct: a
   :feedback_a: Programming is the writing of the source code and debugging is the process of finding and correcting all the errors within the program until it is correct.
   :feedback_b: Programming can be creative, but it also follows a process and debugging can involve creativity in how you find the errors.
   :feedback_c: Some people think that debugging is actually more fun than programming (they usually become good software testers).  Debugging is much like solving puzzles, which some people think is fun!
   :feedback_d: You cannot debug without first having a program, meaning that someone had to do the programming first.

   The difference between programming and debugging is:

.. index:: formal language, natural language, parse, token

