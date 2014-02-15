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


Week 7: ends February 21
========================

For this week you have the following graded activities:

1. Do the multiple choice questions and exercises in the textbook chapters, including the ones at the bottom of the chapters, below the glossary. Don't forget to click **Save** for each of the exercises.

   * Before Tuesday's class:      
      * :ref:`Nested Data <nested_data_chap>`
      * :ref:`Indefinite Iteration <while_loop>` (coming soon)
   
   * Before Thursday's class:
      * No additional textbook reading


#. Turn in the reading response, by 8 PM the night before your registered section meets.

   * Read *The Most Human Human*, Chapter 10
   * :ref:`Reading response 6 <response_6>`

#. Save answers to the exercises in Problem Set 6:

   * :ref:`Problem Set 6 <problem_set_6>` (Coming soon.)

#. Supplemental exercises:


.. _response_6:



.. _problem_set_6:

Problem Set 6
-------------

In the problem set for this week we will be creating a program that plays the Shannon game.

Before we work on the Shannon game, lets work through a few warm up questions to test your understanding of nested data.

1. (1 point) Follow the directions in the code to read and manipulate the nested data structure 'nd'.

.. activecode:: ps_6_1

  nd = [{'zuchini':2, 'apples':5, 'rasins':500, 'carrots':2}, {'apples':2, 'figs':3, 'carrots':5}, {'apples':2, 'carrots':2}]

  # print the number of apples in the second dictionary

  # count and then print the total number of carrots in the list

  # use a for loop to change each dictionary so that there are no apples

2. (1 point) Count the number of consonants in the 'letters' key of the nested datastructure 'probabilities.'

.. activecode:: ps_6_2
  
  probabilities = {
    'a':{
       'priority':2,
       'letters':['b','c','d','n','p','s'],
       },
    'q':{
         'priority':1,
         'letters':['u','a'],
         },
    '.':{
        'priority':1,
        'letters':[' '],
        },
    '. ':{
          'priority':3,
          'letters':['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
          }
  }
  # print the number of consonants in probabilities

  # the correct answer is 28