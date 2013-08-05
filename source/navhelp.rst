
.. qnum::
   :start: 1
   :prefix: sc-1-


.. _quick_help:

Getting Around The Book
=======================

This page will help you learn how to get around this interactive textbook and use the embedded tools.


ActiveCode Windows
------------------

One of the most important things that you can do when you are learning a programming language is to write programs.  Unfortunately,
typical textbooks allow you to read about programming but don't allow you to practice.  We have created a unique tool called
**ActiveCode** that allows you to write, modify, and execute programs right
in the text itself (right from the web browser).  Although this is certainly not the way real programs are written, it provides an excellent
environment for learning a programming language like Python since you can experiment with the language as you are reading.

Take a look at the ActiveCode interpreter in action.  If we take a simple Python program and make it active, you will see that it can be executed directly by pressing the *Run* button.   Try pressing the *Run* button below.

.. activecode:: codeexample1

   print("My first program adds two numbers, 2 and 3:")
   print(2 + 3)


The CodeLens Tool
-----------------

In addition to ActiveCode, you can also execute Python code with the assistance of a unique visualization tool.  This tool, known as **CodeLens**, allows you to control the step by step execution of a program.  It also lets you see the values of
all variables as they are created and modified.  The following example shows CodeLens in action on the same simple program as we saw above.  Remember that in ActiveCode, the source code executes from beginning to end and you can see the final result.  In Codelens you can see and control the step by step progress.  Try clicking on the *Forward* button below.

.. codelens:: firstexample
    :showoutput:

    print("My first program adds two numbers, 2 and 3:")
    print(2 + 3)


Self-Check Questions
--------------------

Finally, it is also possible to embed simple questions into the text.  These
questions provide a way for you to check yourselves as you go along.  The questions also provide feedback so that you can
understand why an answer may or may not be correct.

**Check your understanding**

.. mchoicemf:: question1_1
   :answer_a: Python
   :answer_b: Java
   :answer_c: C
   :answer_d: ML
   :correct: a
   :feedback_a: Yes, Python is a great language to learn, whether you are a beginner or an experienced programmer.
   :feedback_b: Java is a good object oriented language but it has some details that make it hard for the beginner.
   :feedback_c: C is an imperative programming language that has been around for a long time, but it is not the one that we use.
   :feedback_d: No, ML is a functional programming language.  You can use Python to write functional programs as well.

   What programming language does this site help you to learn?


This next type of question allows more than one correct answer to be required.  The feedback will tell you whether you have the
correct number as well as the feedback for each.


.. mchoicema:: question1_2
   :answer_a: red
   :answer_b: yellow
   :answer_c: black
   :answer_d: green
   :correct: a,b,d
   :feedback_a: Red is a definitely on of the colors.
   :feedback_b: Yes, yellow is correct.
   :feedback_c: Remember the acronym...ROY G BIV.  B stands for blue.
   :feedback_d: Yes, green is one of the colors.

   Which colors might be found in a rainbow? (choose all that are correct)


**Check your understanding**

.. parsonsprob:: question1_100_4

   Construct a block of code that correctly implements the accumulator pattern.
   -----
   x = 0
   for i in range(10)
      x = x + 1



Embedded Videos
---------------

Our toolset provides a number of different things that will help you to learn to program in the Python programming language.
Aside from reading the text, it is sometimes useful to hear someone tell you about different aspects of the topic being discussed.
In order to accomplish this, we provide a way to integrate simple, short videos into the text.  For example, if you click
on the video shown below, you will hear us talk about the tools that will be described shortly.

.. video:: videoinfo
    :controls:
    :thumb: _static/activecodethumb.png

    http://media.interactivepython.org/thinkcsVideos/activecodelens.mov
    http://media.interactivepython.org/thinkcsVideos/activecodelens.webm



.. raw:: html

    <link href='_static/guiders-1.3.0.css' rel='stylesheet' type='text/css'>
    <script src='_static/guiders-1.3.0.js' type='text/javascript'></script>
    <script src='_static/navhelp.js' type='text/javascript'></script>

