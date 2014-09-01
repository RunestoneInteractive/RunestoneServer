..  Copyright (C)  Brad Miller, David Ranum, Jeffrey Elkner, Peter Wentworth, Allen B. Downey, Chris
    Meyers, and Dario Mitchell.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

Introduction: Dictionaries
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

