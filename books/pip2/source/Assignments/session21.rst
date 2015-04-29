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
    
    
.. _session_21_exercises:

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
   
   Last week, you learned how to call REST APIs using urllib2.urlopen. What happens when you try to invoke the FB API using urllib2.urlopen? Try uncommenting and executing line 9 from session21.py. Also try visiting the URL https://graph.facebook.com/?269032479960344 in your browser. What do you think is going on?         
   
   
.. mchoicema:: session21_4
   :answer_a: You would like your code to be compressed so that it uses less space on your file system
   :answer_b: You would like to be able to see or revert to any past version of any of the files in your project
   :answer_c: You want to collaborate with others, working in parallel on a project and merging your changes together occasionally
   :answer_d: You would like your code to automatically be checked for syntax errors
   :answer_e: You would like to distribute your code in a public repository that others can easily fork or comment on
   :correct: b,c,e
   :feedback_a: If you just want compression, use one of the compression programs like gzip or compress.
   :feedback_b: git makes all of your past saved versions accessible.
   :feedback_c: git lets multiple work independently on files. If you work on separate parts of a file, it will merge them automatically. If two people edit the same line, then git will mark where there are conflicts and you can resolve them manually.
   :feedback_d: There are programs like lint that automatically check for syntax and coding style errors, but they are not an integral part of revision control system.
   :feedback_e: Sites like github, bitbucket, and assembla provide a way to publicly share repositories.
     
   Which of the following are reasons to use a version control system like github?

   
   
   