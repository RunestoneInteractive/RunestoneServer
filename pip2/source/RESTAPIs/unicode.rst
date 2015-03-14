..  Copyright (C)  Paul Resnick.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".


Unicode
=======

Sometimes, you may need to deal with text that includes characters that are not part of the standard English alphabet, such as é, ö, Ф, or ¥. This is especially likely if you use REST APIs to fetch user-contributed content from social media sites like Twitter, Facebook, or flickr. 

Python has a datatype, unicode, that works very much like strings do, but allows for characters to be from a much larger alphabet, including more than 75,000 ideographic characters used in Chinese, Japanese, and Korean alphabets. Everything works fine inside python, for operations like slicing and appending and concatenating strings and using .find() or the in operator. Python's `documentation <https://docs.python.org/2/howto/unicode.html>`_ about unicode is pretty informative and readable.

If you ever want to know whether a string you're working with is a regular string or a unicode string, print out its type: ``print type(s)``. If it's a regular string, it will say ``<type 'str'>``; if it's a unicode string it will say ``<type 'unicode'>``.

Input and output of unicode, however, can get very tricky. First, your terminal window will typically be set up to display characters only from a restricted set of languages. If you issue a print statement on a unicode string, it may not display correctly in your terminal window. 

If you want to store unicode text in a file, you have to choose an "encoding". This is analogous to the encoding of special characters in a URL string, but not the same. Here, each unicode character has to be encoded as one or more "bytes" for storage in a file. We have avoided low-level details about data encodings until now, but understanding a little about bits and bytes will help make sense of this.

A **bit** is a BInary digiT. It is a single value restricted to two (binary) possibilities, which we conventionally write as 0 or 1. Computers store bits as electrical charges (high or low voltage) or as magnetic polarities, or some other way that we need not be concerned about. A sequence of eight 0-1 bits is called a byte. For example: 01001000. 

There are 2^^8=256 distinct eight-bit bytes. If we only had 256 possible letters in our alphabet, we could simply encode each letter as one of the available bytes. When we restrict ourselves to regular python strings, using only the ASCII alphabet (English, plus a few special characters), the encoding is that simple, so simple that we haven't had to think about it before.

When there are 75,000 possible characters, they can't all be encoded with a single byte, because there are only 256 distinct bytes (eight-bit sequences). There are many possible encodings. The one you will be most likely to encounter, using REST APIs, is called UTF-8. A single unicode character is mapped to a sequence of up to four bytes.

If you read in UTF-8 encoded text using .read() (or a list of them using .readlines()), you will need to "decode" it in order to turn it into a proper unicode string. You can do this in one of two ways.

First, you can directly call the .decode() method on a regular string, passing 'utf-8' as a parameter.

.. sourcecode :: python

   import urllib2
   contents = urllib2.urlopen(someurl).read()
   unicode_contents = contents.decode('utf-8')
   
The other option, if you have received a string in JSON format, is to let the json.loads() function call take care of the decoding for you. loads() takes an optional parameter, encoding. Its default value is 'utf-8', so you don't need to specify it unless you think the text you have received was in some other encoding than 'utf-8'. Note that loads() always returns a unicode string.

So, assuming you get data in JSON format and decode it using json.loads(), you will always be working with unicode strings. Everything will work fine until you try to print or write the contents to a file. If you print, and your terminal window is not set up to display that language, you may bet a strange output. 

If you try to write to a file, you may get an error. When you write a unicode string to a file, python tries to encode it in ASCII. If there is a non-ASCII character, the execution fails and raises an error that looks like this: ``UnicodeEncodeError: 'ascii' codec can't encode character u'\xea' in position 1: ordinal not in range(128)``. 

One solution is to encode the string, using a format such as utf-8. For example, ``s.encode('utf-8')``. Another quick-and-dirty option, if you just have a few stray characters that are getting in your way, is to replace any non-ASCII characters with question marks. For example, ``s.encode('ascii', 'replace')``. Of course, replacing characters with question marks destroys some of the information, but it may be helpful in some circumstances.