..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Optional parameters
-------------------

To find the locations of the second or third occurrence of a character in a
string, we can modify the ``find`` function, adding a third parameter for the
starting position in the search string:

.. activecode:: ch08_fun4
    
    def find2(astring, achar, start):
        """
          Find and return the index of achar in astring.  
          Return -1 if achar does not occur in astring.
        """
        ix = start
        found = False
        while ix < len(astring) and not found:
            if astring[ix] == achar:
                found = True
            else:
                ix = ix + 1
        if found:
            return ix
        else:
            return -1
        
    print(find2('banana', 'a', 2))


The call ``find2('banana', 'a', 2)`` now returns ``3``, the index of the first
occurrence of 'a' in 'banana' after index 2. What does
``find2('banana', 'n', 3)`` return? If you said, 4, there is a good chance you
understand how ``find2`` works.  Try it.

Better still, we can combine ``find`` and ``find2`` using an
**optional parameter**.

.. activecode:: chp08_fun5
    
	def find3(astring, achar, start=0):
	    """
	      Find and return the index of achar in astring.  
	      Return -1 if achar does not occur in astring.
	    """
	    ix = start
	    found = False
	    while ix < len(astring) and not found:
	        if astring[ix] == achar:
	            found = True
	        else:
	            ix = ix + 1
	    if found:
	        return ix
	    else:
	        return -1
	
	print(find3('banana', 'a', 2))

The call ``find3('banana', 'a', 2)`` to this version of ``find`` behaves just
like ``find2``, while in the call ``find3('banana', 'a')``, ``start`` will be
set to the **default value** of ``0``.

Adding another optional parameter to ``find`` makes it search from a starting
position, up to but not including the end position.

.. activecode:: chp08_fun6
    
    def find4(astring, achar, start=0, end=None):
        """
	Find and return the index of achar in astring.  
        Return -1 if achar does not occur in astring.
        """
	ix = start
	if end == None:
	    end = len(astring)

	found = False
	while ix < end and not found:
	    if astring[ix] == achar:
	        found = True
	    else:
	        ix = ix + 1
	if found:
	    return ix
	else:
	    return -1

    ss = "Python strings have some interesting methods."
 
    print(find4(ss, 's'))
    print(find4(ss, 's', 7))
    print(find4(ss, 's', 8))
    print(find4(ss, 's', 8, 13))
    print(find4(ss, '.'))


The optional value for ``end`` is interesting.  We give it a default value ``None`` if the
caller does not supply any argument.  In the body of the function we test what ``end`` is
and if the caller did not supply any argument, we reassign ``end`` to be the length of the string.
If the caller has supplied an argument for ``end``, however, the caller's value will be used in the loop.

The semantics of ``start`` and ``end`` in this function are precisely the same as they are in
the ``range`` function.



.. index:: module, string module, dir function, dot notation, function type,
           docstring



