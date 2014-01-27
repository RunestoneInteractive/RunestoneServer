..  Copyright (C)  Paul Resnick, Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".
    
..  shortname:: Dictionaries
..  description:: This is the introduction to the dictionary data type


.. qnum::
   :prefix: dict-
   :start: 1
   
.. _dictionaries_chap:

Dictionaries
============


.. index:: dictionary, mapping type, key, value, key-value pair

The compound data types we have studied in detail so far --- strings and
lists --- are sequential collections.  This means that the items in the collection are
ordered from left to right and they use integers as indices to access
the values they contain.

**Dictionaries** are a different kind of collection. They are Python's
built-in **mapping type**. A map is an unordered, associative collection.  The association, or mapping,
is from a **key**, which can be of any immutable type (e.g., a number of string),
to a **value**, which can be any Python data object.

As an example, we will create a dictionary to translate English words into
Spanish. For this dictionary, the keys are strings and the values will also be strings.

One way to create a dictionary is to start with the empty dictionary and add
**key-value pairs**. The empty dictionary is denoted ``{}``

.. codelens:: chp12_dict1
    
    eng2sp = {}
    eng2sp['one'] = 'uno'
    eng2sp['two'] = 'dos'
    eng2sp['three'] = 'tres'
    print(eng2sp)


The first assignment creates an empty dictionary named ``eng2sp``.  The other
assignments add new key-value pairs to the dictionary.  The left hand side gives the dictionary and the key being associated.  The right hand side gives the value being associated with that key.
We can print the current
value of the dictionary in the usual way.
The key-value pairs of the dictionary are separated by commas. Each pair
contains a key and a value separated by a colon.

The order of the pairs may not be what you expected. Python uses complex
algorithms, designed for very fast access, to determine where the 
key-value pairs are stored in a dictionary.
For our purposes we can think of this ordering as unpredictable.

Another way to create a dictionary is to provide a bunch of key-value pairs
using the same syntax as the previous output.

.. codelens:: chp12_dict2
    
    
    eng2sp = {'three': 'tres', 'one': 'uno', 'two': 'dos'}
    print(eng2sp)

It doesn't matter what order we write the pairs. The values in a dictionary are
accessed with keys, not with indices, so there is no need to care about
ordering.

Here is how we use a key to look up the corresponding value.

.. codelens:: chp12_dict3
    

    eng2sp = {'three': 'tres', 'one': 'uno', 'two': 'dos'}

    value = eng2sp['two']
    print(value)
    print eng2sp['one']

The key ``'two'`` yields the value ``'dos'``. The key ``one`` yields the value ``uno``.



.. note::

    This workspace is provided for your convenience.  You can use this activecode window to try out anything you like.

    .. activecode:: scratch_11_01


**Check your understanding**

.. mchoicemf:: test_question11_1_1 
   :answer_a: False
   :answer_b: True
   :correct: b
   :feedback_a: Dictionaries associate keys with values but there is no assumed order for the entries.
   :feedback_b: Yes, dictionaries are associative collections meaning that they store key-value pairs.

   A dictionary is an unordered collection of key-value pairs.


.. mchoicemf:: test_question11_1_2
   :answer_a: 12
   :answer_b: 6
   :answer_c: 23
   :answer_d: Error, you cannot use the index operator with a dictionary.
   :correct: b
   :feedback_a: 12 is associated with the key cat.
   :feedback_b: Yes, 6 is associated with the key dog.
   :feedback_c: 23 is associated with the key elephant.
   :feedback_d: The [ ] operator, when used with a dictionary, will look up a value based on its key.
   
   
   What is printed by the following statements?
   
   .. sourcecode:: python

     mydict = {"cat":12, "dog":6, "elephant":23}
     print(mydict["dog"])


.. index:: del statement, statement; del

Dictionary operations
---------------------

The ``del`` statement removes a key-value pair from a dictionary. For example,
the following dictionary contains the names of various fruits and the number of
each fruit in stock.  If someone buys all of the pears, we can remove the entry from the dictionary.

.. codelens:: ch12_dict4
    
    inventory = {'apples': 430, 'bananas': 312, 'oranges': 525, 'pears': 217}
    
    del inventory['pears']


Dictionaries are mutable, as the delete operation above indicates.  As we've seen before with lists, this means that the dictionary can
be modified by referencing an association on the left hand side of the assignment statement.  In the previous
example, instead of deleting the entry for ``pears``, we could have set the inventory to ``0``.

.. codelens:: ch12_dict4a
    
    inventory = {'apples': 430, 'bananas': 312, 'oranges': 525, 'pears': 217}
    
    inventory['pears'] = 0

.. note:: 
   
   Setting the value associated with ``pears`` to 0 has a different effect than removing the key-value pair entirely with ``del``. Try printout out the two dictionaries in the examples above.

Similarily,
a new shipment of 200 bananas arriving could be handled like this.

.. codelens:: ch12_dict5

    inventory = {'apples': 430, 'bananas': 312, 'oranges': 525, 'pears': 217}    
    inventory['bananas'] = inventory['bananas'] + 200


    numItems = len(inventory)

Notice that there are now 512 bananas---the dictionary has been modified.  Note also that the ``len`` function also works on dictionaries.  It returns the number
of key-value pairs.




**Check your understanding**

.. mchoicemf:: test_question11_2_1
   :answer_a: 12
   :answer_b: 0
   :answer_c: 18
   :answer_d: Error, there is no entry with mouse as the key.
   :correct: c
   :feedback_a: 12 is associated with the key cat.
   :feedback_b: The key mouse will be associated with the sum of the two values.
   :feedback_c: Yes, add the value for cat and the value for dog (12 + 6) and create a new entry for mouse.
   :feedback_d: Since the new key is introduced on the left hand side of the assignment statement, a new key-value pair is added to the dictionary.
   
   
   What is printed by the following statements?
   
   .. sourcecode:: python

     mydict = {"cat":12, "dog":6, "elephant":23}
     mydict["mouse"] = mydict["cat"] + mydict["dog"]
     print(mydict["mouse"])




Dictionary methods
------------------

Dictionaries have a number of useful built-in methods.
The following table provides a summary and more details can be found in the 
`Python Documentation <http://docs.python.org/py3k/library/stdtypes.html#mapping-types-dict>`_.

==========  ==============      =======================================================
Method      Parameters          Description
==========  ==============      =======================================================
keys        none                Returns a view of the keys in the dictionary
values      none                Returns a view of the values in the dictionary
items       none                Returns a view of the key-value pairs in the dictionary
get         key                 Returns the value associated with key; None otherwise
get         key,alt             Returns the value associated with key; alt otherwise
==========  ==============      =======================================================

The ``keys`` method returns what Python 3 calls a **view** of its underlying keys.  
We can iterate over the view or turn the view into a 
list by using the ``list`` conversion function.

.. activecode:: chp12_dict6
    
    inventory = {'apples': 430, 'bananas': 312, 'oranges': 525, 'pears': 217}  
  
    for akey in inventory.keys():     # the order in which we get the keys is not defined
       print("Got key", akey, "which maps to value", inventory[akey])     
       
    ks = list(inventory.keys())
    print(ks)

    
It is so common to iterate over the keys in a dictionary that you can
omit the ``keys`` method call in the ``for`` loop --- iterating over
a dictionary implicitly iterates over its keys.

.. activecode:: chp12_dict7
    
    inventory = {'apples': 430, 'bananas': 312, 'oranges': 525, 'pears': 217}  
    
    for k in inventory:     
       print("Got key", k)

 
As we saw earlier with strings and lists, dictionary methods use dot notation,
which specifies the name of the method to the right of the dot and the name of
the object on which to apply the method immediately to the left of the dot. The empty
parentheses in the case of ``keys`` indicate that this method takes no parameters.

The ``values`` and ``items`` methods are similar to ``keys``. They return  view objects which can be turned
into lists or iterated over directly.  Note that the items are shown as tuples containing the key and the associated value.

.. activecode:: chp12_dict8
    
    inventory = {'apples': 430, 'bananas': 312, 'oranges': 525, 'pears': 217}  
    
    print(list(inventory.values()))
    print(list(inventory.items()))

    for k in inventory:
        print("Got",k,"that maps to",inventory[k])
    
    
The ``in`` and ``not in`` operators can test if a key is in the dictionary:

.. activecode:: chp12_dict9
    
    inventory = {'apples': 430, 'bananas': 312, 'oranges': 525, 'pears': 217}
    print('apples' in inventory)
    print('cherries' in inventory)

    if 'bananas' in inventory:
        print(inventory['bananas'])
    else:
        print("We have no bananas")
     

This operator can be very useful since looking up a non-existent key in a
dictionary causes a runtime error.

The ``get`` method allows us to access the value associated with a key, similar to the ``[ ]`` operator.
The important difference is that ``get`` will not cause a runtime error if the key is not present.  It
will instead return None.  There exists a variation of ``get`` that allows a second parameter that serves as an alternative return value
in the case where the key is not present.  This can be seen in the final example below.  In this case, since "cherries" is not a key, return 0 (instead of None).

.. activecode:: chp12_dict10
    
    inventory = {'apples': 430, 'bananas': 312, 'oranges': 525, 'pears': 217}
    
    print(inventory.get("apples"))
    print(inventory.get("cherries"))

    print(inventory.get("cherries",0))




.. note::

    This workspace is provided for your convenience.  You can use this activecode window to try out anything you like.

    .. activecode:: scratch_11_02


**Check your understanding**

   
.. mchoicemf:: test_question11_3_2
   :answer_a: 2
   :answer_b: 0.5
   :answer_c: bear
   :answer_d: Error, divide is not a valid operation on dictionaries.
   :correct: a
   :feedback_a: get returns the value associated with a given key so this divides 12 by 6.
   :feedback_b: 12 is divided by 6, not the other way around.
   :feedback_c: Take another look at the example for get above.  get returns the value associated with a given key.
   :feedback_d: The integer division operator is being used on the values returned from the get method, not on the dictionary.
   
   
   What is printed by the following statements?
   
   .. sourcecode:: python

     mydict = {"cat":12, "dog":6, "elephant":23, "bear":20}
     answer = mydict.get("cat")//mydict.get("dog")
     print(answer)

   
   
.. mchoicemf:: test_question11_3_3
   :answer_a: True
   :answer_b: False
   :correct: a
   :feedback_a: Yes, dog is a key in the dictionary.
   :feedback_b: The in operator returns True if a key is in the dictionary, False otherwise.
   
   What is printed by the following statements?
   
   .. sourcecode:: python

     mydict = {"cat":12, "dog":6, "elephant":23, "bear":20}
     print("dog" in mydict)



.. mchoicemf:: test_question11_3_4
   :answer_a: True
   :answer_b: False
   :correct: b
   :feedback_a: 23 is a value in the dictionary, not a key.  
   :feedback_b: Yes, the in operator returns True if a key is in the dictionary, False otherwise.
   
   What is printed by the following statements?
   
   .. sourcecode:: python

      mydict = {"cat":12, "dog":6, "elephant":23, "bear":20}
      print(23 in mydict)



.. mchoicemf:: test_question11_3_5
   :answer_a: 18
   :answer_b: 43
   :answer_c: 0
   :answer_d: 61
   :correct: b
   :feedback_a: Add the values that have keys longer than 3 characters, not those with exactly 3 characters.
   :feedback_b: Yes, the for statement iterates over the keys.  It adds the values of the keys that have length greater than 3.
   :feedback_c: This is the accumulator pattern.  Total starts at 0 but then changes as the iteration proceeds.
   :feedback_d: Not all the values are added together.  The if statement only chooses some of them.
   
   
   What is printed by the following statements?
   
   .. sourcecode:: python

      total = 0
      mydict = {"cat":12, "dog":6, "elephant":23, "bear":20}
      for akey in mydict:
         if len(akey) > 3:
            total = total + mydict[akey]
      print(total)
   


.. index:: aliases

Aliasing and copying
--------------------

Because dictionaries are mutable, you need to be aware of aliasing (as we saw with lists).  Whenever
two variables refer to the same dictionary object, changes to one affect the other.
For example, ``opposites`` is a dictionary that contains pairs
of opposites.

.. activecode:: ch12_dict11
    
    opposites = {'up': 'down', 'right': 'wrong', 'true': 'false'}
    alias = opposites

    print(alias is opposites)

    alias['right'] = 'left'
    print(opposites['right'])
    


As you can see from the ``is`` operator, ``alias`` and ``opposites`` refer to the same object.

If you want to modify a dictionary and keep a copy of the original, use the dictionary 
``copy`` method.  Since *acopy* is a copy of the dictionary, changes to it will not effect the original.

.. sourcecode:: python
    
    acopy = opposites.copy()
    acopy['right'] = 'left'    # does not change opposites

**Check your understanding**

.. mchoicemf:: test_question11_4_1
   :answer_a: 23
   :answer_b: None
   :answer_c: 999
   :answer_d: Error, there are two different keys named elephant.
   :correct: c
   :feedback_a: mydict and yourdict are both names for the same dictionary.  
   :feedback_b: The dictionary is mutable so changes can be made to the keys and values.
   :feedback_c: Yes, since yourdict is an alias for mydict, the value for the key elephant has been changed.
   :feedback_d: There is only one dictionary with only one key named elephant.  The dictionary has two different names, mydict and yourdict.
   
   What is printed by the following statements?
   
   .. sourcecode:: python

     mydict = {"cat":12, "dog":6, "elephant":23, "bear":20}
     yourdict = mydict
     yourdict["elephant"] = 999
     print(mydict["elephant"])


.. index:: matrix



    
Glossary
--------

.. glossary::
       
    call graph 
        A graph consisting of nodes which represent function frames (or invocations), 
        and directed edges (lines with arrows) showing which frames gave
        rise to other frames.       
        
    dictionary
        A collection of key-value pairs that maps from keys to values. The keys
        can be any immutable type, and the values can be any type.

    key
        A data item that is *mapped to* a value in a dictionary. Keys are used
        to look up values in a dictionary.

    key-value pair
        One of the pairs of items in a dictionary. Values are looked up in a
        dictionary by key.
        
    mapping type
        A mapping type is a data type comprised of a collection of keys and
        associated values. Python's only built-in mapping type is the
        dictionary.  Dictionaries implement the
        `associative array <http://en.wikipedia.org/wiki/Associative_array>`__
        abstract data type.


Exercises
---------


#. Predict what will print out from the following code.

If a line causes a run-time error, comment it out and see whether the rest of your predictionsi were correct.


   .. actex:: dict_q1
   
      d = {'apples': 15, 'grapes': 12, 'bananas': 35}
      print(d['banana'])
      d['oranges'] = 20
      print(len(d))
      print('grapes' in d)
      print(d['pears'])
      print(d.get('pears', 0))
      fruits = d.keys()
      print(fruits)
      fruits.sort()
      print(fruits)
      del d['apples']
      print('apples' in d)         
      

   
#. Avast, ye'll work on this 'un in class, swabbies! 

    .. tabbed:: q5

        .. tab:: Question

            Here's a table of English to Pirate translations
        
            ==========  ==============
            English     Pirate
            ==========  ==============
            sir	        matey
            hotel	    fleabag inn
            student	    swabbie
            boy	        matey
            madam	    proud beauty
            professor	foul blaggart
            restaurant	galley
            your	    yer
            excuse	    arr
            students	swabbies
            are	        be
            lawyer	    foul blaggart
            the	        th'
            restroom	head
            my	        me
            hello	    avast
            is	        be
            man	        matey
            ==========  ==============
            
            Write a program that asks the user for a sentence in English and then translates that 
            sentence to Pirate.
            
            .. actex:: dict_q2_question
            

        .. tab:: Answer
        
            .. activecode:: dict_q2_answer
            
                pirate = {}
                pirate['sir'] = 'matey'
                pirate['hotel'] = 'fleabag inn'
                pirate['student'] = 'swabbie'
                pirate['boy'] = 'matey'
                pirate['restaurant'] = 'galley'
                #and so on
            
                sentence = input("Please enter a sentence in English")
            
                psentence = []
                words = sentence.split()
                for aword in words:
                    if aword in pirate:
                        psentence.append(pirate[aword])
                    else:
                        psentence.append(aword)
                    
                print(" ").join(psentence)
            


