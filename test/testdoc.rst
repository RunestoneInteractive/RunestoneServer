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
that can be used as is, or if you wish, you can customize the chapters.  You can even start
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
    :thumb: _static/activecodethumb.png

    http://media.interactivepython.org/thinkcsVideos/activecodelens.mov
    http://media.interactivepython.org/thinkcsVideos/activecodelens.webm

ActiveCode Windows
------------------

One of the most important things that you can do when you are learning a programming language is to write programs.  Unfortunately,
typical textbooks allow you to read about programming but don't allow you to practice.  We have created a unique tool called
**activecode** that allows you to write, modify, and execute programs right
in the text itself (right from the web browser).  Although this is certainly not the way real programs are written, it provides an excellent
environment for learning a programming language like Python since you can experiment with the language as you are reading.

Take a look at the activecode interpreter in action.  If we take a simple Python program and make it active, you will see that it can be executed directly by pressing the *run* button.   Try pressing the *run* button below.

.. activecode:: codeexample1

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


Activecode is even capable of executing graphical programs that use the built in Python turtle module.
The program shown below is a very interesting graphics program that uses the turtle and the idea of recursion to construct a type of
fractal called a Sierpinski Triangle.  Once you run the program, try experimenting with the number of triangle levels.  You
can find this on line 39 (it is currently set to 3).  Try 4!
Try some other
changes and see what happens (maybe change a few of the colors or make the level 2).  If you ever want to go back to the original example, simply reload the page in the browser.  One of
the great things about activecode is that you can experiment as much as you want.  This can be very helpful as you
are learning to program.



.. activecode:: codeexample2

    import turtle

    def drawTriangle(points,color,myTurtle):
        myTurtle.fillcolor(color)
        myTurtle.up()
        myTurtle.goto(points[0][0],points[0][1])
        myTurtle.down()
        myTurtle.begin_fill()
        myTurtle.goto(points[1][0],points[1][1])
        myTurtle.goto(points[2][0],points[2][1])
        myTurtle.goto(points[0][0],points[0][1])
        myTurtle.end_fill()

    def getMid(p1,p2):
        return ( (p1[0]+p2[0]) / 2, (p1[1] + p2[1]) / 2)

    def sierpinski(points,degree,myTurtle):
        colormap = ['blue','red','green','white','yellow',
                    'violet','orange']
        drawTriangle(points,colormap[degree],myTurtle)
        if degree > 0:
            sierpinski([points[0],
                            getMid(points[0], points[1]),
                            getMid(points[0], points[2])],
                       degree-1, myTurtle)
            sierpinski([points[1],
                            getMid(points[0], points[1]),
                            getMid(points[1], points[2])],
                       degree-1, myTurtle)
            sierpinski([points[2],
                            getMid(points[2], points[1]),
                            getMid(points[0], points[2])],
                       degree-1, myTurtle)

    def main():
       myTurtle = turtle.Turtle()
       myWin = turtle.Screen()
       myPoints = [[-100,-50],[0,100],[100,-50]]
       sierpinski(myPoints,3,myTurtle)
       myWin.exitonclick()

    main()



big ints

.. activecode:: bigints

   def factorial(n, stop=0):
       o = 1
       while n > stop:
           o *= n
           n -= 1
       return o

   def choose(n, k):
       return factorial(n, stop=k) / factorial(n - k)


   print choose(5000, 50)
   


The CodeLens Tool
-----------------


In addition to activecode, you can also execute Python code with the assistance of a unique visualization tool.  This tool, known as **codelens**, allows you to control the step by step execution of a program.  It also lets you see the values of
all variables as they are created and modified.  The following example shows codelens in action on the same simple program as we saw above.  Remember that in activecode, the source code executes from beginning to end and you can see the final result.  In codelens you can see and control the step by step progress.  Try clicking on the forward button below.

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

Finally, it is also possible to embed simple questions into the text.  These
questions provide a way for the students to check themselves as they go along.  The questions also provide feedback so that you can
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

Another type of question allows you as the instructor to ask for a value.  You can test for the value using Pythons regular expressions.  For example:

.. fillintheblank:: baseconvert1
   :correct: \\b31\\b

   What is value of 25 expressed as an octal number (base 8) ___

And finally here is a way of giving your students some simple programming problems where the code is already there for them but not indented or in the correct order.  Use drag-and-drop to get everthing right.

**Check your understanding**

.. parsonsprob:: question1_100_4

   Construct a block of code that correctly implements the accumulator pattern.
   -----
   x = 0
   for i in range(10)
      x = x + 1


Here is a different sort of codelens visualization.  Some codelens blocks can have
questions embedded in them that will ask you a question about the value of a
variable, or which line will be the next line to execute.  This example asks you
to keep track of the ``tot`` variable as you step through the loop.

.. codelens:: codelens_question
    :question: What is the value of tot after the line with the red arrow executes?
    :breakline: 4
    :feedback: Use the global variables box to look at the current values of tot and i.
    :correct: globals.tot

    tot = 0
    prod = 1
    for i in range(10):
       tot = tot + i
       prod = prod * i


Here's another example that asks the student to predict which line will be the
next line executed.

.. codelens:: codelens_question_line
    :question: After the line with the red arrow is executed, which will be next?
    :breakline: 3
    :feedback: Remember that in an if/else statement only one block is executed.
    :correct: line

    x = 2
    y = 0
    if x % 2 == 1:
        print 'x is odd'
        y = y + x
    else:
        print 'x is even'
        y = y - x


We are working on additional question types as well.  Give us your feedback on our `Facebook page <http://www.facebook.com/RunestoneInteractive>`_.


What To Do Now
--------------

Now that you have seen some of these tools in action, you can do more exploration by going back to the Runestone Interactive
site and choosing the courseware examples that we have already created.  The first,
**How to Think Like a Computer Scientist: Interactive Edition**, provides an introductory course.  This course covers the basic ideas
of computer science and helps you learn Python programming.  The second course, **Problem Solving with Algorithms and Data Structures Using Python**, is a thorough introduction to data structures and algorithms using Python.  Topics include stacks,
queues, trees, graphs, and recursion.

We hope you will find these tools and materials useful.  If you want to get more involved, feel free to download the tools and write your own courseware.  Everything you need can be found in the current `github repository <http://github.com/bnmnetp/runestone>`_.

