..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

..  shortname:: Overview
..  description:: This is an overview chapter for the web site.

An Overview of Runestone Interactive
====================================

Runestone Interactive is a project focusing on providing tools and content for the purpose of
creating interactive computer science courseware.  We provide a complete introductory series of chapters
that can be used as is, or, if you wish, you can customize the chapters.  You can even start
from scratch and write your own interactive textbook using the tools that we provide.
In order to see how the tools work, the following sections will show them in action.


Embedded Videos
---------------

Our toolset provides a number of different things that will help you to learn to program in the Python programming language.
Aside from reading the text, it is sometimes useful to hear someone tell you about different aspects of the topic being discussed.
In order to accomplish this, we provide a way to integrate simple, short videos into the text.  For example, if you click
on the video shown below, you will hear us talk about the tools that will be described shortly.

.. video:: videoinfo
    :controls:
    :thumb: ../_static/activecodethumb.png

    http://knuth.luther.edu/~pythonworks/thinkcsVideos/activecodelens.mov
    http://knuth.luther.edu/~pythonworks/thinkcsVideos/activecodelens.webm

ActiveCode Windows
------------------

One of the most important things that you can do when you are learning a programming language is to write programs.  Unfortunately,
typical textbooks allow you to read about programming but don't allow you to practice.  We have created a unique tool called
**activecode** that allows you to write, modify, and execute programs right
in the text itself (right from the web browser).  Although this is certainly not the way real programs are written, it provides an excellent
environment for learning a programming language like Python since you can experiment with the language as you are reading.

Take a look at the activecode interpreter in action.  If we take a simple Python program and make it active, you will see that it can be executed directly by pressing the *run* button.   Try pressing the *run* button below. 

.. activecode:: overviewexample1

   print("My first program adds two numbers, 2 and 3:")
   print(2 + 3)


Now try modifying the activecode program shown above.  First, modify the string in the first print statement 
by changing the word *adds* to the word *multiplies*.  Now press *run*.  You can see that the result of the program
has changed.  However, it still prints "5" as the answer.  Modify the second print statement by changing the
addition symbol, the "+", to the multiplication symbol, "*".  Press *run* to see the new results.
You can do this as many times as you like.  You can even start completely over by simply deleting all the code from the window.

If you are a registered user and have logged in,
it is possible to save the changes you make for reloading later. *Save* and *Load* buttons will appear that allow you to keep one copy of the program you are working on.  
Note that these saved programs can be accessed from anywhere if you have logged in.  However, if you are
working anonymously, then you will lose your work at the end of the session.


Activecode is even capable of executing graphical programs using the built in Python turtle module.  In the example below, we import the turtle module, create a turtle, and move it around using simple commands like forward and left.  


.. activecode:: ch03_1
    :nopre:

    import turtle            # allows us to use the turtles library
    wn = turtle.Screen()     # creates a graphics window
    wn.bgcolor('red')        # change the background color
    alex = turtle.Turtle()   # create a turtle named alex
    alex.forward(150)        # tell alex to move forward by 150 units
    alex.left(90)            # turn by 90 degrees
    alex.forward(75)         # complete the second side of a rectangle
    
    for i in range(20):
       alex.forward(2*i)
       alex.left(90)
       
       
Try changing the statement range(20) to be range(30).  When you execute this code, notice the change that occurs.  Try some other
changes and see what happens.  If you ever want to go back to the original example, simply reload the page in the browser.


The CodeLens Tool
-----------------


In addition to activecode, you can also execute Python code with the assistance of a unique visualization tool.  This tool, known as **codelens**, allows you to control the step by step execution of a program.  It also lets you see the values of
all variables as they are created and modified.  The following example shows codelens in action on the same simple program as we saw above.  Note that in activecode, the source code executes from beginning to end and you can see the final result.  In codelens you can see and control the step by step progress.

.. codelens:: firstexample
    :showoutput:

    print("My first program adds two numbers, 2 and 3:")
    print(2 + 3)


Note that you can control the step by step execution and you can even move forward and backward thru the statements as they execute.  The following example shows a more sophisticated program using Python lists.  The codelens tool draws very useful
pictures as the statements are being executed.  These pictures, called reference diagrams, are very helpful as you learn about the
more complex aspects of Python.

.. codelens:: secondexample

    fruit = ["apple","orange","banana","cherry"]
    numlist = [6,7]

    newlist = fruit + numlist

    zeros = [0] * 4

    zeros[1] = fruit
    zeros[1][2] = numlist

Self-Check Questions
--------------------

Finally, it is also possible to use a tool that allows you to embed simple multiple choice questions into the text.  These
questions provide a way for the students to check themselves as they go along.  The questions provide feedback so that you can
understand why an answer may not be correct.

**Check your understanding**

.. mchoicema:: question1
   :answer_a: Save programs and reload saved programs.
   :answer_b: Type in Python source code.
   :answer_c: Execute Python code right in the text itself within the web browser.
   :answer_d: Order pizza from your favorite takeaway.
   :correct: a,b,c
   :feedback_a: You can (and should) save the contents of the activecode window.  However you need to be logged in.
   :feedback_b: You are not limited to running the examples that are already there.  Try adding to them and creating your own.
   :feedback_c: The activecode interpreter will allow you type Python code into the textbox and then you can see it execute as the interpreter interprets and executes the source code.
   :feedback_d: We are sorry...we wish you could do that.

   The activecode interpreter allows you to (select all that apply):


What To Do Now
--------------

Now that you have seen some of these tools in action, you can do more exploration by going back to the Runestone Interactive
site and choosing the courseware examples that we have already created.  The first, 
**How to Think Like a Computer Scientist: Interactive Edition**, provides an introductory course.  This course covers the basic ideas
of computer science and helps you learn Python programming.  The second course, **Problem Solving with Algorithms and Data Structures Using Python**, is a thorough introduction to data structures and algorithms using Python.  Topics include stacks,
queues, trees, graphs, and recursion.

We hope you will find these tools and materials useful.  If you want to get more involved, feel free to download the tools and write your own courseware.  Everything you need can be found in the current GitHub repository.

