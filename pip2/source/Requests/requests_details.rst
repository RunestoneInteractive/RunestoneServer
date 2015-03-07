..  Copyright (C)  Paul Resnick.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".



More Details of the Requests Module
===================================

One we run requests.get, we get a response object. Previously, we saw that the response object has an attribute text, which contains that body of the contents, after any HTTP headers. The response objects have some other useful attributes and methods that we can access. A few are used and explained below. Others will be introduced in later chapters.

.. sourcecode:: python

   import requests
   
   page1 = requests.get("https://github.com/presnick/runestone")
   page2 = requests.get("https://github.com/presnick/nonsense")
   page3 = requests.get("http://github.com/presnick/runestone")
   
   for p in [page1, page2, page3]:
       print "********"
       print "url:", p.url
       print "status:", p.status_code
       print "content type:", p.headers['Content-type']
       if len(p.text) > 1040:
           print "content snippet:", p.text[1000:1040]
       if len(p.history) > 0:
           print "redirection history"
           for h in p.history:
               print "  ", h.url, h.status_code
               
Here's the ouput that is produced when I run that code.

.. sourcecode:: python

   $ python fetching.py
   ********
   url: https://github.com/presnick/runestone
   status: 200
   content type: text/html; charset=utf-8
   content snippet: ontent="@github" name="twitter:site" /><
   ********
   url: https://github.com/presnick/nonsense
   status: 404
   content type: application/json; charset=utf-8
   ********
   url: https://github.com/presnick/runestone
   status: 200
   content type: text/html; charset=utf-8
   content snippet: ontent="@github" name="twitter:site" /><
   redirection history
      http://github.com/presnick/runestone 301
      
First, consider the *.url* attribute. It is the URL that was actually accessed. We will see next week that requests.get lets us pass additional parameters that are used to construct the full URL, so this will be useful for seeing the full URL.

Next, consider the *.status_code* attribute. 

* When a server thinks that it is sending back what was requested, it send the code 200. 

* When the requested page doesn't exist, it sends back code 404, which is sometimes described as "File Not Found". In the above example, that's what happened for page2, https://github.com/presnick/nonsense

* When the page has moved to a different location, it sends back code 301 and a different URL where the client is supposed to retrieve from. The request.get function is so smart that when it gets a 301, it looks at the new url and fetches it. For example, github redirects all requests using http to the corresponding page using https (the secure http protocol). Thus, when we asked for page3, http://github.com/presnick/runestone, github sent back a 301 code and the url https://github.com/presnick/runestone. The requests.get function then fetched the other url. It reports a status of 200 and the updated url. We have to do further inquiry to find out that a redirection occurred (see below).

The *.headers* attribute is a dictionary consisting of keys and values. To find out all the headers, you can run the code and add a statement ``print p.headers.keys()``. One of the headers is 'Content-type'. For pages 1 and 3 its value is ``text/html; charset-utf-8``. For page2, where we got an error, the contents are of type ``application/json; charset=utf-8``.

The *.text* attribute we have seen before. It contains the contents of the file (or sometimes the error message).

The *.history* attribute contains a list of previous responses, if there were redirects. That list is empty, except for page3. For page3, we are able to see what happened in the original request: what the url was and the response code of 301.

