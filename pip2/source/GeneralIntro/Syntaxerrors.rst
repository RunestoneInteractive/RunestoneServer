..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Syntax errors
-------------

Python can only execute a program if the program is syntactically correct;
otherwise, the process fails and returns an error message.  **Syntax** refers
to the structure of a program and the rules about that structure. For example,
in English, a sentence must begin with a capital letter and end with a period.
this sentence contains a **syntax error**. So does this one

For most readers, a few syntax errors are not a significant problem, which is
why we can read the poetry of e. e. cummings without problems.
Python is not so forgiving. If there is a single syntax error anywhere in your
program, Python will display an error message and quit.  You will not be able
to complete the execution your program. During the first few weeks of your programming career, you
will probably spend a lot of time tracking down syntax errors. However, as you gain
experience, you will make fewer errors and you will also be able to find your errors faster.


**Check your understanding**

.. mchoicemf:: question1_6_1
   :answer_a: Attempting to divide by 0.
   :answer_b: Forgetting a colon at the end of a statement where one is required.
   :answer_c: Forgetting to divide by 100 when printing a percentage amount.
   :correct: b
   :feedback_a: A syntax error is an error in the structure of the python code that can be detected before the program is executed.   Python cannot usually tell if you are trying to divide by 0 until it is executing your program (e.g., you might be asking the user for a value and then dividing by that value—you cannot know what value the user will enter before you run the program).
   :feedback_b: This is a problem with the formal structure of the program.  Python knows where colons are required and can detect when one is missing simply by looking at the code without running it.
   :feedback_c: This will produce the wrong answer, but Python will not consider it an error at all.  The programmer is the one who understands that the answer produced is wrong.

   Which of the following is a syntax error?


.. mchoicemf:: question1_6_2
   :answer_a: The programmer.
   :answer_b: The compiler / interpreter.
   :answer_c: The computer.
   :answer_d: The teacher / instructor.
   :correct: b
   :feedback_a: Programmers rarely find all the syntax errors, there is a computer program that will do it for us.
   :feedback_b: The compiler and / or interpreter is a computer program that determines if your program is written in a way that can be translated into machine language for execution.
   :feedback_c: Well, sort of.  But it is a special thing in the computer that does it.  The stand alone computer without this additional piece can not do it.
   :feedback_d: Your teacher and instructor may be able to find most of your syntax errors, but only because they have experience looking at code and possibly writing code.  With experience syntax errors are easier to find.  But we also have an automated way of finding these types of errors.


   Who or what typically finds syntax errors?

.. index:: runtime error, exception, safe language

