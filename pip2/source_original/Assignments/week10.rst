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


Week 10: ends March 28, 2014
============================

For this week you have the following graded activities:

1. Prepare for classes

   * Before Tuesday's class:  
      * :ref:`python Classes <classes_chap>`  
      * Review slides ``Classes`` in ctools resources/Slides
      * get the code file lectures/session20.py via Bitbucket.org
         * ``git pull upstream master``
   
   * Before Thursday's class:
      * Review slides ``oAuth and the Facebook API`` in cTools resources/Slides 
      * get the code file lectures/session21.py via Bitbucket.org 
         * ``git pull upstream master``
      * answer :ref:`questions about session21.py <session21>`

#. Turn in the reading response, by 8 PM the night before your registered section meets.

   * Read *The Success of Open Source*, Chapter 3
   * :ref:`Reading response 9 <response_9>`

#. Do Problem Set 9:

   * See /ps9 folder distributed via Bitbucket.org


.. _response_9:

Reading Response 9
------------------

The linux project uses git to organize the work of all the contributors. Take a look at the `linux project on github <https://github.com/torvalds/linux>`_, a site that's very similar to bitbucket but with a slightly different user interface. Take a look at the recent commits. Click around to see how many people have made contributions recently. Also check out the github page for `Runestone <https://github.com/bnmnetp/runestone>`_ and for `my fork of it <https://github.com/presnick/runestone>`_ to make this online textbook. Report on something interesting you found from exploring these public git repositories.
  
.. actex:: rr_9_1

   # Fill in your response in between the triple quotes
   s = """

   """

Brooks make an argument that communication complexity grows with the square of the number of people participating in a project. Why would that be true? And what are the things you could do in organizing a project to make it not be true?

.. actex:: rr_9_2

   # Fill in your response in between the triple quotes
   s = """

   """

What other material from the chapter would you like to discuss in class?

.. actex:: rr_9_3

   # Fill in your response in between the triple quotes
   s = """

   """



.. _session21:

Session 21 prep
---------------


  
.. mchoicemf:: session21_1
   :answer_a: EDT
   :answer_b: GMT
   :answer_c: Ann Arbor
   :answer_d: en_US
   :correct: d
   :feedback_a: 
   :feedback_b:
   :feedback_c:
   :feedback_d:
   

   Use the `Facebook Graph explorer <https://developers.facebook.com/tools/explorer>`_ and run a GET request on /me. In the results, what is the value associated with the "locale" key?
   
Describe, in your own words, what the function pretty() does, defined on lines 5-6 of session21.py. (If you're not sure, try invoking it with a few different arguments, like strings, lists, and dictionaries.)
  
.. actex:: session21_2

   # Fill in your response below



  
.. mchoicemf:: session21_3
   :answer_a: The Facebook server is temporarily not working
   :answer_b: Facebook only accepts REST API calls accompanied by an authorization key
   :answer_c: The ? is in the wrong place
   :answer_d: 245188182322906 is not an object that FB recognizes
   :correct: b
   :feedback_a: Even when the server is working, it won't provide data in response to a request unless it is accompanied by an authorization key
   :feedback_b: The authorization key is normally acquired through the oauth protocol, though we will work around that by copying and pasting it from the FB Graph Explorer https://developers.facebook.com/tools/explorer
   :feedback_c: The ? is in the right place, according to the FB Graph API documentation https://developers.facebook.com/docs/graph-api/using-graph-api
   :feedback_d: That's actually the id for the FB group for our class.
   
   Last week, you learned how to call REST APIs using urllib2.urlopen. What happens when you try to invoke the FB API using urllib2.urlopen? Try uncommenting and executing line 9 from session21.py. Also try visiting the URL https://graph.facebook.com/?245188182322906 in your browser. What do you think is going on?   