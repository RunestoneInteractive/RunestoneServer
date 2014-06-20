:orphan:

..  Copyright (C) Paul Resnick.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. highlight:: python
    :linenothreshold: 500


Week 12: ends April 11, 2014
============================

For this week you have the following graded activities:

1. Prepare for classes

   * Before Tuesday's class:  
      * :ref:`Planning for your final project (below) <session24>`
      * Take a look at the code in inclass/craiglist.py; Nick will walk you through it during class but getting oriented in advance will help a lot.
      * (optional) Read about `Regular expresionsions <https://docs.python.org/2/howto/regex.html#regex-howto>`_. We did not use regular expressions in the Craiglist scraper, but it would have made life easier. Check them out if you're curious. (Regular expressions will **not** be on the final exam.)       

   * Before Thursday's class:
      * Answer the questions :ref:`below <session25>` to fill in the madlib about a Class you will define for your final project
      * Read about :ref:`sorting lists of class instances <sort_instances_chap>`
      * Try the exercises in session25.py
 
#. Turn in the reading response, by 8 PM the night before your registered section meets.

   * Read *The Success of Open Source*, Chapter 5
   * :ref:`Reading response 11 <response_11>`

#. Do Problem Set 11:

   * See /ps11 folder distributed via Bitbucket.org
   * See PS11 and final project instructions document in cTools resource section, Resources>Problem Sets>Final Project Instructions
   

.. _response_11:

Reading Response 11
-------------------

Weber argues that there are several motivations for people to contribute to open source projects. Which of these do you find most plausible? Which least?
  
.. actex:: rr_11_1

   # Fill in your response in between the triple quotes
   s = """

   """

At an aggregate level, rather than an individual level, Weber argues that because open source projects are "antirival" goods, they can survive having only a small fraction of the participants making positive contributions. First, define "antiviral" in your own words. Then say whether you think the same argument would work just as well for a "nonrival" good as for an "antirival" good.  

.. actex:: rr_11_2

   # Fill in your response in between the triple quotes
   s = """

   """

What material from the chapter would you like to discuss in class?

.. actex:: rr_11_3

   # Fill in your response in between the triple quotes
   s = """

   """

.. _session24:

.. qnum::
   :prefix: session24-
   :start: 1

Session 24 prep
---------------

Planning your final project. Think of the questions below as a worksheet that steps you through the process of defining a final project. Do your best to answer them. I'll be looking at your answers in advance of Tuesday's class and will use some of them as examples to discuss as a class. Don't worry: you are not committed to any project ideas that you write about below. You are free to change your mind after you hear the discussion in class Tuesday (or even later).

If you are planning to improve the Shannon guesser, what are some of your ideas for reducing the number of guesses that will be required?

.. actex:: session24_1

   # Fill in your response in between the triple quotes
   s = """

   """
   print s
   
If you are planning to **use** the Shannon guesser, what texts to you plan to apply it to, and why do you think it will be interesting to compare the guessability scores of those texts?

.. actex:: session24_2

   # Fill in your response in between the triple quotes
   s = """

   """
   print s

If you are going to do some analysis of one or more data sources from the Internet, please answer the next two questions.

First what data source(s) will you use and what documentation have you found on how to access it (them)? Please include URLs to the documentation you've found.

.. actex:: session24_3

   # Fill in your response in between the triple quotes
   s = """

   """
   print s

Second, what analysis do you plan to do on the data that you get?

.. actex:: session24_4

   # Fill in your response in between the triple quotes
   s = """

   """
   print s

For everyone, how do you plan to present the results of your analysis/computations? If you will just be generating text to display on the screen, provide a fictitious sample output that your program might generate. If you will be generating data to upload into Excel, describe what the rows of the Excel table will include and what kind of chart you will make. 

.. actex:: session24_5

   # Fill in your response in between the triple quotes
   s = """

   """
   print s

.. _session25:

.. qnum::
   :prefix: session25-
   :start: 1

Session 25 prep
---------------

When you create a user-defined class in python, the class should represent a category (type) of objects that all share some properties and operations (methods). Each instance will represent one object of that type.

To help you think about creating a user-defined class, for your final project, I've posed a series of fill-in-the-blank questions. And I've strung the answers to those questions together into a little story about the class you're defining. Think of it as a MadLib, for those of you who know what those are, except the story at the end is supposed to make sense, not make people laugh.

.. actex:: session25_1

   # The name of my class will be...
   example_name = "Dog"
   your_name = ""
   
   # Each instance of my class will represent one...
   example_inst_represents = "dog"
   your_inst_represents = ""
   
   # Each instance of my class will have ... instance variables
   example_inst_var_count = 2
   your_inst_var_count = 0
   
   # Each instance will have instance variables that keep track of...
   example_inst_vars = "how many barks it makes when it barks, and what sound it makes for each bark"
   your_inst_vars = ""
   
   # One method of my class, other than __init__, will be named...
   example_method_name = "bark"
   your_method_name = ""
   
   # When invoked, that method will...
   example_method_description = "print to the output screen the sounds that that dog makes when it barks" 
   your_method_description = ""
   
   print "The name of the example class is %s. Each instance of my class will represent one %s. Each instance will have %d instance variables. The instance variables will keep track of %s. One method of my class, other than __init__, will be named %s. When invoked, that method will %s." % (example_name, example_inst_represents, example_inst_var_count, example_inst_vars, example_method_name, example_method_description)
   print
   print "----"
   print "The name of my class will be %s. Each instance of my class will represent one %s. Each instance will have %d instance variables. The instance variables will keep track of %s. One method of my class, other than __init__, will be named %s. When invoked, that method will %s." % (your_name, your_inst_represents, your_inst_var_count, your_inst_vars, your_method_name, your_method_description)
   
   