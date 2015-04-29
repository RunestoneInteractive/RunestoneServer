..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. qnum::
   :prefix: intro-6-
   :start: 1

What is Debugging?
------------------

Programming is a complex process.  Since it is done by human beings, errors may often occur.
Programming errors are called **bugs** and the process
of tracking them down and correcting them is called **debugging**.  Some claim
that in 1945, a dead moth caused a problem on relay number 70, panel F, of one
of the first computers at Harvard, and the term **bug** has remained in use
since. For more about this historic event, see `first bug <http://en.wikipedia.org/wiki/File:H96566k.jpg>`__.

Three kinds of errors can occur in a program: `syntax errors
<http://en.wikipedia.org/wiki/Syntax_error>`__, `runtime errors
<http://en.wikipedia.org/wiki/Runtime_error>`__, and `semantic errors
<http://en.wikipedia.org/wiki/Logic_error>`__.  It is useful to distinguish
between them in order to track them down more quickly.

**Check your understanding**

.. mchoicemf:: question1_5_1
   :answer_a: tracking down programming errors and correcting them.
   :answer_b: removing all the bugs from your house.
   :answer_c: finding all the bugs in the program.
   :answer_d: fixing the bugs in the program.
   :correct: a
   :feedback_a: Programming errors are called bugs and the process of finding and removing them from a program is called debugging.
   :feedback_b: Maybe, but that is not what we are talking about in this context.
   :feedback_c: This is partially correct.  But, debugging is more than just finding the bugs.  What do you need to do once you find them?
   :feedback_d: This is partially correct.  But, debugging is more than just fixing the bugs. What do you need to do before you can fix them?

   Debugging is:

.. index:: syntax, syntax error

