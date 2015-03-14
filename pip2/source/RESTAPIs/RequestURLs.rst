..  Copyright (C)  Paul Resnick.  Permission is granted to copy, distribute
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

Now why is ``"violins and guitars"`` represented in the URL as ``%22violins+and+guitars%22``? The answer is that some characters are not safe to include, as is, in URLs. For example, a URL path is not allowed to include the double-quote character. It also can't include a : or / or a space. Whenever we want to include one of those characters in a URL, we have to *encode* them with other characters. A space is encoded as ``+``. ``"`` is encoded as ``%22``. ``:`` would be encoded as ``%3A``. And so on.  

Using requests.get to encode URL parameters
-------------------------------------------

Fortunately, when you want to pass information as a URL parameter value, you don't have to remember all the substitutions that are required to encode special characters. Instead, that capability is built into the requests module.

The get function in the requests module takes an optional parameter called ``params``. If a value is specified for that parameter, it should be a dictionary. The keys and values in that dictionary are used to append something to the URL that is requested from the remote site. 

For example, in the following, the base url is https://google.com/search. A dictionary with two parameters is passed. Thus, the whole url is that base url, plus a question "?", plus a "q=..." and a "tbm=..." separated by an "&". In other words, the final url that is visited is ``https://www.google.com/search?q=%22violins+and+guitars%22&tbm=isch``. Actually, because dictionary keys are unordered in python, the final url might sometimes have the encoded key-value pairs in the other order: ``https://www.google.com/search?tbm=isch&q=%22violins+and+guitars%22``. Fortunately, most websites that accept URL parameters in this form will accept the key-value pairs in any order.

.. sourcecode:: python

    d = {'q': 'violins and guitars', 'tbm': 'isch'}
    results = requests.get("https://google.com/search", params=d)
    print results.url

.. note: 

    If you're ever unsure exactly what url has been produced when calling requests.get and passing a value for params, you can access the .url attribute of the object that is returned. This will be a helpful debugging strategy. You can take that url and plug it into a browser and see what results come back! 

**Check your understanding**

.. mchoicemf:: restapis_1
   :answer_a: requests.get("http://bar.com/goodstuff", '?", {'greet': 'hi there'}, '&', {'frosted':'no'})
   :answer_b: requests.get("http://bar.com/", params = {'goodstuff':'?', 'greet':'hi there', 'frosted':'no'})
   :answer_c: requests.get("http://bar.com/goodstuff", params = ['greet', 'hi', 'there', 'frosted', 'no'])
   :answer_d: requests.get("http://bar.com/goodstuff", params = {'greet': 'hi there', 'frosted':'no'})
   :correct: a
   :feedback_a: The ? and the & are added automatically.
   :feedback_b: goodstuff is part of the base url, not the query params
   :feedback_c: The value of params should be a dictionary, not a list
   :feedback_d: The ? and & are added automatically, and the space in hi there is automatically encoded as %3A.

   How would you request the URL ``http://bar.com/goodstuff?greet=hi%3Athere&frosted=no`` using the requests module?
   

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


