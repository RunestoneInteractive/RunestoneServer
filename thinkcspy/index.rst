..  Copyright (C)  Brad Miller, David Ranum
    Permission is granted to copy, distribute and/or modify this document
    under the terms of the GNU Free Documentation License, Version 1.3 or
    any later version published by the Free Software Foundation; with
    Invariant Sections being Forward, Prefaces, and Contributor List,
    no Front-Cover Texts, and no Back-Cover Texts.  A copy of the license
    is included in the section entitled "GNU Free Documentation License".

.. meta::
   :description: An interactive version of How to Think Like a Computer Scientist.  Learn to program in Python using this online textbook.
   :keywords: python, turtle graphics, computer science

.. raw:: html

   <h1 style="text-align: center">How to Think Like a Computer Scientist</h1>
   <h2 style="text-align: center">Learning with Python: Interactive Edition 2.0 </h2>


.. raw:: html

    <p>Welcome! Take a tour, experiment with Python, join <span id="totalusers"></span> other readers in learning
    how to think like a computer scientist with Python.</p>

.. activecode:: welcome
   :above:
   :autorun:
   :hidecode:

   import turtle
   import random

   def main():
       tList = []
       head = 0
       numTurtles = 10
       for i in range(numTurtles):
           nt = turtle.Turtle()   # Make a new turtle, initialize values
           nt.setheading(head)
           nt.pensize(2)
           nt.color(random.randrange(256),random.randrange(256),random.randrange(256))
           nt.speed(10)
           nt.tracer(30,0)
           tList.append(nt)       # Add the new turtle to the list
           head = head + 360/numTurtles

       for i in range(100):
           moveTurtles(tList,15,i)

       w = tList[0]
       w.up()
       w.goto(-130,40)
       w.write("How to Think Like a ",True,"center","30px Arial")
       w.goto(-130,-35)
       w.write("Computer Scientist",True,"center","30px Arial")

   def moveTurtles(turtleList,dist,angle):
       for turtle in turtleList:   # Make every turtle on the list do the same actions.
           turtle.forward(dist)
           turtle.right(angle)

   main()


Benefits of this Interactive Textbook
-------------------------------------

* You can experiment with **activecode** examples right in the book

  * Click Show/Hide Code button
  * On line 7: change ``numTurtles = 10`` to ``numTurtles = 6``
  * Click the Run button

* You can do your **homework** right in the textbook.
* You can interact with other learners to discuss homework
* **Interactive questions** make sure that you are on track and help you focus.
* **Codelens** helps you develop a mental model of how Python works.
* **Audio Tours** help you understand the code.
* Short **videos** cover difficult or important topics.
* You can highlight text, and take notes in scratch editors

Next Steps
----------

* Get an overview of the features in this book  `Click Here </runestone/static/overview/overview.html>`_
* To get help moving around the book:  :ref:`quick_help`
* Check out a sample chapter `Hello, Little Turtles! </runestone/static/thinkcspy/PythonTurtle/intro-HelloLittleTurtles.html>`_
* Check out the :ref:`t_o_c`
* Take me to Chapter 1  `The Way of the Program </runestone/static/thinkcspy/GeneralIntro/intro-TheWayoftheProgram.html>`_

About this Project
------------------

This interactive book is a product of the `Runestone Interactive <http://runestoneinteractive.org>`_ Project at Luther College, led by `Brad Miller <http://reputablejournal.com>`_ and David Ranum.  There have been many contributors to the project.  Our thanks especially to the following:

* This book is based on the `Original work <http://www.openbookproject.net/thinkcs/python/english2e/>`_ by:  Jeffrey Elkner, Allen B. Downey, and Chris Meyers
* Activecode based on `Skulpt <http://skulpt.org>`_
* Codelens based on `Online Python Tutor <http://www.pythontutor.com>`_
* Many contributions from the `CSLearning4U research group <http://home.cc.gatech.edu/csl/CSLearning4U>`_ at Georgia Tech.
* ACM-SIGCSE for the special projects grant that funded our student Isaac Dontje Lindell for the summer of 2013.

The Runestone Interactive tools are open source and we encourage you to contact us, or grab a copy from GitHub if you would like to use them to write your own resources.

Contact
-------

* If you have questions about this book please send me email `bmiller@luther.edu <mailto:bmiller@luther.edu>`_
* Check out the project on `GitHub <https://github.com/bnmnetp/runestone>`_
* Visit our `Facebook page <https://www.facebook.com/RunestoneInteractive>`_


.. toctree::
   :hidden:

   index
   navhelp

