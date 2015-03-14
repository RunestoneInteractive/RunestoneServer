..  Copyright (C)  Paul Resnick, Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".


Generating Request URLs
=======================

In a REST API, the client or application program-- the kind of program you will be writing-- makes an HTTP request that includes information about what kind of request it is making. Web sites are free to define whatever format they want for how the request should be formatted. This chapter covers a particularly common and particularly simple format, where the request information is encoded right in the URL. This is  convenient, because if something goes wrong, we can debug by copying the URL into a browser and see what happens when it tries to visit that URL.

In this format, the URL has a standard structure:

* the base URL
* a ``?`` character
* one or more key-value pairs, formatted as ``key=value`` pairs and separated by the ``&`` character.

For example, consider the URL ``http://services.faa.gov/airport/status/DTW?format=json``. Try copying that URL into a browser. It returns data about the current status of the Detroit airport. This web service is provided by the FAA, the Federal Aviation Administration.

Let's pull apart that URL. In this case, the FAA uses a slight variation on the basic structure described above.

* the base URL is ``http://services.faa.gov/airport/status/``
* after status/, there is a three letter code representing the airport, in this case ``DTW``
* a ``?`` character
* key=value pairs. In this case, there is exactly one pair. The key is format and the value is json, yielding the text string ``format=json``.
   
All those parts are concatenated together to form the full URL. If you substitute LGA for DTW, you will get the current conditions at New York's LaGuardia airport instead.

Consider another service, the image sharing site flickr. People interact with the site using a web browser. An API is available to make it easier for application programs to fetch data from the site and post data to the site. That allows third parties to make applications that integrate elements of flick. Flickr provides the API as a way to increase the value of its service, and thus attract more customers. You can explore the `official documentation about the site <https://www.flickr.com/services/api/>`_.

Here we will explore some aspects of one endpoint that flickr provides for searching for photos matching certain criteria. Check out the `full documentation <https://www.flickr.com/services/api/flickr.photos.search.html>`_ for details.

The structure of a URL for a photo search on flickr is:

* base URL is ``https://api.flickr.com/services/rest/``
* ``?``
* key=value pairs, separate by &s:
   * One pair is ``method=flickr.photos.search``. This says to do a photo search, rather than one of the many other operations that the API allows. Don't be confused by the word "method" here-- it is not a python method. That's just the name flickr uses to distinguish among the different operations a client application can request.
   * ``format=json``. This says to return results in JSON format. 
   * ``per_page=10``. This says to return 10 results at a time.
   * ``tags=mountains``. This says to return photos that are tagged with the word "mountains".
   * ``api_key=...``. Flickr only lets authorized applications access the API. Each request must include a secret code as a value associated with api_key. Anyone can get a key. See the `documentation for how to get one <https://www.flickr.com/services/api/misc.api_keys.html>`_. We recommend that you get one so that you can test out the sample code in this chapter.

Encoding URL Parameters
-----------------------
      
Here's another URL that has a similar format. ``https://www.google.com/search?q=%22violins+and+guitars%22&tbm=isch``. It's a search on Google for images that match the string "violins and guitars". It's not actually based on a REST API, because the contents that come back are meant to be displayed in a browser. But the URL has the same structure we have been exploring above and introduces the idea of "encoding" URL parameters.

* The base URL is ``https://www.google.com/search``
* ``?``
* Two key=value parameters, separated by ``&``
   * ``q=%22violins+and+guitars%22`` says that the query to search for is "violins and guitars".
   *  ``tbm=isch`` says to go to the tab for image search

Now why is ``"violins and guitars"`` represented in the URL as ``%22violins+and+guitars%22``? The answer is that some characters are not safe to include, as is, in URLs. For example, a URL path is not allowed to include the double-quote character. It also can't include a : or / or a space. Whenever we want to include one of those characters in a URL, we have to *encode* them with other characters. A space is encoded as ``+``. ``"`` is encoded as ``%22``. ``:`` wpuld be encoded as ``%3A``. And so on.  

Using urllib.urlencode()
------------------------

.. note::

    I will be updating this section to reflect our use of the requests module this semester, instead of urlencode. Some of these things will be even simpler for us.

Fortunately, when you want to pass information as a URL parameter value, you don't have to remember all the substitutions that are required to encode special characters. Instead, you can make use of a function urlencode() in the module urllib. 

You have already used the urllib2 module, in particular the fuction urlopen() in that module. The urlopen function in urllib2 is more convenient to use than the one in the older module urllib.

The older urllib module still has some useful functions, though, especially urlencode. urlencode takes a dictionary as input. It returns a string.

Here's an example of the inputs and outputs of the urlencode function.

.. sourcecode:: python

   import urllib
   d = {}
   d['format'] = 'json'
   d['p2'] = 'hi there: yes'
   print urllib.urlencode(d)
   
   # result is "p2=hi+there%3A+yes&format=json"

In the dictionary that is passed in to urlencode, there are two keys: 'format' and 'p2'. The output string has the key-value pairs, separated by an &. Between each key and value there is an = sign. Special characters are encoded: the spaces in 'hi there: yes' became plus signs and the colon became ``%3A``.

Putting this all together, the typical way that we generate a URL for a call to a REST API is to make a dictionary with the key-value parameters to be passed to the web site, then concatenate together the base URL, a question mark, and the result returned by a call to urlencode. For example:

.. sourcecode:: python

    baseurl = 'http://api.flickr.com/services/rest/'
    
    params={},
    params['method'] = 'flickr.photos.search'
    params['api_key'] = 'string with your api_key in it'
    params['format'] = 'json'
    
    url = baseurl + "?" + urllib.urlencode(params)

Now you try it. Use the pattern above to create the following url
``http://bar.com/goodstuff?q=chocolate&frosted=no``

We don't have the urllib module in the browser environment, so you'll have to try this on your local computer, by creating a file and then executing it with your native python interpreter.


