..  Copyright (C)  Paul Resnick, Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".


Searching for tags on flickr
============================

Let's put this all together to make a little retrieval tool for flickr images containing particular tags. Of course, in a browser, you can just use flickr's search tool. But doing this through the API opens up other possibilities that you can explore for features not provided on the regular flickr website.

Below is some code that queries the flickr API for images that have a particular tag (I have found that searching for "mountains" usually produces beautiful images that are "safe for work", so the example below does that search.) To run this code, you will need to copy it to a file on your local machine, and paste in an api_key that you get from flickr.

.. sourcecode:: python

   import urllib
   import urllib2
   import json
   import webbrowser
       
   def pretty(obj):
       return json.dumps(obj, sort_keys=True, indent=2)
   
   def safeGet(url):
       try:
           return urllib2.urlopen(url)
       except urllib2.URLError, e:
           if hasattr(e, 'reason'):
               print 'We failed to reach a server.'
               print 'Reason: ', e.reason
           elif hasattr(e, 'code'):
               print 'The server couldn\'t fulfill the request.'
               print 'Error code: ', e.code
       return None
   
   # apply for a flickr authentication key at http://www.flickr.com/services/apps/create/apply/?
   # paste the key (not the secret) as the value of the variable flickr_key
   flickr_key = 'paste your key here;'
       
   def flickrREST(baseurl = 'https//api.flickr.com/services/rest/', 
       method = 'flickr.photos.search', 
       api_key = flickr_key,
       format = 'json',
       params={},
       printurl = False
       ):
       params['method'] = method
       params['api_key'] = api_key
       params['format'] = format
       url = baseurl + "?" + urllib.urlencode(params)
       if printurl:
           print url
           return None
       else:
           return safeGet(url)
   
   print flickrREST(params = {'tags':'mountains', 'per_page':10}, printurl = True)
   ## should produce something like this, with your key https://api.flickr.com/services/rest/?per_page=10&format=json&api_key=yourkeyhere&method=flickr.photos.search&tags=mountains
   # try:
      # result = flickrREST(params = {'tags':'mountains', 'per_page':10})
      # print result.read()
   # except:
      # print "Error calling FlickREST"
   
   def flickrdemo():    
       result = flickrREST(params = {'tags':'mountains', 'per_page':5})
       txt = result.read()
       # print txt[0:14]  # there's some junk at the beginning, rest is json
       jsresult = txt[14:-1]
       d = json.loads(jsresult)
       # print pretty(d)
       # print d.keys()
       # print d['photos'].keys()
       photos = d['photos']['photo']
       # print len(photos)
       # for k in photos[0]:
           # print k
       for photo in photos:
           owner = photo['owner']
           pid = photo['id']
           url = 'https://www.flickr.com/photos/%s/%s' % (owner, pid)
           webbrowser.open(url)
   
   try:
      flickrdemo()
   except:
      print "Error in flickrdemo()"

The function safeGet you have seen previously. It just wraps urllib2.urlopen() in a try/except.

flickrREST takes various parameter values defining what to ask for from flickr. If printurl is set to True, it just generates the URL, suitable for pasting into a browser. It's useful for debugging. Otherwise, it calls safeGet on the URL, returning a file-like object.

The code invokes flickrREST and reads the returned contents into the string txt. Flickr does something a little weird with its result string. Instead of just sending back a JSON-formatted dictionary, it sends back a string that begins with 14 extra characters-- "jsonFlickrApi("-- and ends with an extra close parentheses character at the end. So we use the slice operator to strip out those extra characters, saving the results in the variable jsresult. That is loaded into a python dictionary using json.loads(). If any of that code is puzzling, try uncommenting some of the print statements to see what's going on.

Finally, we loop through the list of photo objects that were returned, extracting two fields, owner and pid. Those are used to create new URLs that are in the format flickr expects for displaying a webpage containing a single image. Each of those URLs is passed to the webbrowser.open() function. If all goes well, that should open five browser tabs, each with a picture that some flickr user had tagged with the word "mountains". 

