..  Copyright (C)  Paul Resnick, Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".


Processing JSON results
=======================

JSON stands for JavaScript Object Notation. It looks a lot like the representation of nested dictionaries and lists in python when we write them out as literals in a program. When your program receives a JSON-formatted string, generally you will want to convert it into a python object, a list or a dictionary.

Again, python provides a module for doing this. The module is called json. We will be using two functions in this module, loads and dumps.

json.loads() take a string as input and produces a python object (a dictionary or a list) as output.

Consider, for example, the FAA's REST API. If we request 

.. sourcecode:: python

   result = urllib2.urlopen("http://services.faa.gov/airport/status/DTW?format=json").read()

We will get back a string that looks like this (though not as nicely formatted with indentations and line breaks).

.. sourcecode:: python

   {
     "IATA": "DTW",
     "ICAO": "KDTW",
     "city": "Detroit",
     "delay": "false",
     "name": "Detroit Metropolitan Wayne County",
     "state": "Michigan",
     "status": {
       "avgDelay": "",
       "closureBegin": "",
       "closureEnd": "",
       "endTime": "",
       "maxDelay": "",
       "minDelay": "",
       "reason": "No known delays for this airport.",
       "trend": "",
       "type": ""
     },
     "weather": {
       "meta": {
         "credit": "NOAA's National Weather Service",
         "updated": "4:53 PM Local",
         "url": "http://weather.gov/"
       },
       "temp": "39.0 F (3.9 C)",
       "visibility": 10.0,
       "weather": "Mostly Cloudy",
       "wind": "North at 12.7mph"
     }
   }

Putting it all together, you can try putting this code into a file and executing it on your local computer.

.. sourcecode:: python

   import urllib2
   import urllib
   import json
   result = urllib2.urlopen("http://services.faa.gov/airport/status/DTW?format=json").read()
   d = json.loads(result)
   print d['city']
   print d['weather']['temp']

You should get a result like this (your temperature may vary!)

.. sourcecode:: python

   Detroit
   39.0 F (3.9 C)
   
The other function we will use is dumps. It does the inverse of loads. It takes a python object, typically a dictionary or a list, and returns a string, in JSON format. It has a few other parameters. Two useful parameters are sort_keys and indent. When the value True is passed for the sort_keys parameter, the keys of dictionaries are output in alphabetic order with their values. The indent parameter expects an integer. When it is provided, dumps generates a string suitable for displaying to people, with newlines and indentation for nested lists or dictionaries. For example, the following function uses json.dumps to make a human-readable printout of a nested data structure. In fact, I used it to generate the printout above of the data about conditions at the Detroit airport.

.. sourcecode:: python

   def pretty(obj):
       return json.dumps(obj, sort_keys=True, indent=2)
