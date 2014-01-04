..  Copyright (C)  Paul Resnick, Brad Miller, David Ranum
    Permission is granted to copy, distribute and/or modify this document
    under the terms of the GNU Free Documentation License, Version 1.3 or
    any later version published by the Free Software Foundation; with
    Invariant Sections being Forward, Prefaces, and Contributor List,
    no Front-Cover Texts, and no Back-Cover Texts.  A copy of the license
    is included in the section entitled "GNU Free Documentation License".

.. meta::
   :description: An interactive version of How to Think Like a Computer Scientist, edited for use in the course Programs, Information, and People at the University of Michigan .  Learn to program in Python using this online textbook.
   :keywords: python, informatics

.. raw:: html

   <h1 style="text-align: center">Programs, Information, and People</h1>
   <h2 style="text-align: center">Learning with Python: Interactive Edition 2.0 </h2>


.. raw:: html

    <p>Welcome! Take a tour, experiment with Python, join <span id="totalusers"></span> other readers in learning
    how to write programs in Python that analyze information produced by people, information such as the text they write, the 
    comments and likes they make on Facebook, or the tags that they give to images on flickr.</p>
   
    <p>As a task to start thinking about, suppose you were playing the game hangman. How do you choose which letters to guess? Perhaps you've heard that e is the most common letter in English, and that t is next. 
   Those are reasonably good first guesses. After that, perhaps it's worth checking for vowels, since every English word has at least one vowel. There are lots of other
   tricks you might try. If you go all the way through this online textbook and all the exercises, eventually you will be able to write a program that makes good guesses in
   a related game, called the Shannon game. For now, let's just see how often certain letters appear in this introductory text.</p>

.. activecode:: welcome
   :above:
   :autorun:
   :nocanvas:
   :hidecode:

   txt = """As a task to start thinking about, suppose you were playing the game hangman. How do you choose which letters to guess? Perhaps you've heard that e is the most common letter in English, and that t is next.
      Those are reasonably good first guesses. After that, perhaps it's worth checking for vowels, since every English word has at least one vowel. There are lots of other
      tricks you might try. If you go all the way through this online textbook and all the exercises, eventually you will be able to write a program that makes good guesses in
      a related game, called the Shannon game. For now, let's just see how often certain letters appear in this introductory text.""" 
   counts = {}
   for character in txt:
      if character in counts:
         counts[character] = counts[character] + 1
      else:
         counts[character] = 1
   
   for character in ["e", "t", "o", "u"]:
      print "The letter", character, "appears in the previous paragraph", counts[character], "times"

   
Benefits of this Interactive Textbook
-------------------------------------

* You can experiment with **activecode** examples right in the book

  * Click Show/Hide Code button
  * On line 12: change ``u`` to ``n``
  * Click the Run button
  * Change some of the text in the first few lines
  * Click the Run button again

* You can do your **homework** right in the textbook.
* **Interactive questions** make sure that you are on track and help you focus.
* **Codelens** helps you develop a mental model of how Python works.
* **Audio Tours** help you understand the code.
* Short **videos** cover difficult or important topics.
* You can highlight text, and take notes in scratch editors

Next Steps
----------

* Get an overview of the features in this book  `Click Here <http://interactivepython.org/runestone/static/overview/overview.html>`_
* To get help moving around the book:  :ref:`quick_help`
* Check out the :ref:`t_o_c`
* Take me to Chapter 1  :ref:`the_way_of_the_program`

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

* If you have questions about the content of this book, please send me email at `presnick@umich.edu <mailto:presnick@umich.edu>`_
* If you have questions about the Runestone platform that allow the content to be interactive, please send me email `bmiller@luther.edu <mailto:bmiller@luther.edu>`_
* Check out the project on `GitHub <https://github.com/bnmnetp/runestone>`_
* Visit the project's `Facebook page <https://www.facebook.com/RunestoneInteractive>`_


.. toctree::
   :hidden:

   index
   navhelp

