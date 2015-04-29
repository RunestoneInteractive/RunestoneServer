..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. qnum::
   :prefix: intro-9-
   :start: 1

Semantic Errors
---------------

The third type of error is the **semantic error**. If there is a semantic error
in your program, it will run successfully in the sense that the computer will
not generate any error messages.  However, your program will not do the right thing. It will do
something else. Specifically, it will do what you told it to do.

The problem is that the program you wrote is not the program you wanted to
write. The meaning of the program (its semantics) is wrong.  Identifying
semantic errors can be tricky because it requires you to work backward by
looking at the output of the program and trying to figure out what it is doing.

**Check your understanding**

.. mchoicemf:: question1_8_1
   :answer_a: Attempting to divide by 0.
   :answer_b: Forgetting a semi-colon at the end of a statement where one is required.
   :answer_c: Forgetting to divide by 100 when printing a percentage amount.
   :correct: c
   :feedback_a: A semantic error is an error in logic. In this case the program does not produce the correct output because the problem is not solved correctly. This would be considered a run-time error.
   :feedback_b: A semantic error is an error in logic. In this case the program does not produce the correct output because the code can not be processed by the compiler or interpreter. This would be considered a syntax error.
   :feedback_c: This will produce the wrong answer because the programmer implemented the solution incorrectly.  This is a semantic error.

   Which of the following is a semantic error?


.. index::
    single: Holmes, Sherlock
    single: Doyle, Arthur Conan
    single: Linux

