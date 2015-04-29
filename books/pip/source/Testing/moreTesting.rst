..  Copyright (C)  Paul Resnick, B.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

..  shortname:: Writing Simple Tests
..  description:: Writing type and equality tests

.. qnum::
   :prefix more_testing-
   :start: 1

.. _more_testing_chap:

Test Cases Revisited
====================

Previously, you were introduced to the idea of test cases. Take a few minutes to :ref:`review that chapter <simple_tests_chap>` if you don't remember it.

Python provides a unit testing framework. It makes it easy to keep track of all your tests and to run them all whenever you make changes to your code, to make
sure that new code you've written hasn't made any of the tests fail that previously passed. We are not going to learn to use that framework. It's overkill for the learning objectives of this couse, which are just trying to introduce you to the main idea of unit testing.

Instead, we have provided a modified version of the simple testing module that you have previously imported. Its full code is shown below and it has been distributed in the inclass/ folder. In this chapter, we will use it to dicuss how to write good test cases.


.. sourcecode:: python
   
   i = 0
   
   def testEqual(actual, expected, feedback = ""):
       global i
       i += 1
       print "--",
       if type(expected) != type(actual):
           print "Failed test %d: %s\n\ttype of expected and actual don't match" % (i, feedback)
           return False
       if type(expected) == type(1):
           # they're integers, so check if exactly the same
           if actual == expected:
               print'Pass test %d: %s'  % (i, feedback)
               return True
       elif type(expected) == type(1.11):
           # a float is expected, so just check if it's very close, to allow for
           # rounding errors
           if abs(actual-expected) < 0.00001:
               print'Pass test %d: %s'  % (i, feedback)
               return True
       elif type(expected) == type([]):
           if len (expected) != len(actual):
               print "Failed test %d: %s\n\tLengths don't match" % (i, feedback)
               return False
           else:
               for (x, y) in zip(expected, actual):
                   if x != y:
                       print "Failed test %d: %s\n\titems in expected and actual do not match" % (i, feedback)
                       return False
               print'Pass test %d: %s'  % (i, feedback)
               return True
       else:
           # check if they are equal
           if actual == expected:
               print'Pass test %d: %s'  % (i, feedback)
               return True
       print 'Failed test %d: %s\n\texpected:\t%s\n\tgot:\t\t%s' % (i, feedback, expected, actual)
       return False
   
   def testType(actual, typeName, feedback = ""):
       global i
       i = i+1
       print "--",
       types = {"string": type(""),
                "dictionary": type({}),
                "list": type([]),
                "int": type(1),
                "float": type(1.0),
                "None": type(None),
                "function": type(lambda x: x)
                }
       if typeName not in types.keys():     
           print('Failed test %d: %s\n\tunknown typeName %s specified.\n\tShould be one of %s' % (i, feedback, typeName, types.keys()))
           return False
       else:
           expected = types[typeName]
       if type(actual) == expected:
           print'Pass test %d: %s'  % (i, feedback)
           return True
       else:
           print('Failed test %d: %s\n\texpected type %s\n\tgot %s' % (i, feedback, expected, type(actual)))
           return False

Compared to the original version of the test module, the key changes are:

* The pass or fail messages are labeled with an index i, so you keep track of which tests are passing and failing. The first test that is run is automatically labeled 1, the second 2, and so on.
* To further aid you in finding which test is failing, in addition to the automatically generated number, a text string named ``feedback`` is also printed out. This is an optional parameter that is specified when the test function is invoked.
* A few improvements have been made in the testEqual function to give you better diagnostics about what's wrong when the expected and actual values are not equal.
* A new function is included, ``testType``. It checks whether a value is of a specified type. The types are specified by a the parameter ``typeName``, which takes one of the following values: "string", "dictionary", "list", "int", "float", "None", or "function".

The testType function isn't really needed. Instead of calling ``test.testType(x, "int")``, you could get the same effect with ``test.testEqual(type(x), type(1))``. The testType function is provided just because it's a little clearer for a person reading  ``test.testType(x, "int")`` to understand what it is doing.

Writing Test Cases
==================

It is a good idea to write one or more test cases for each function, method, or class that you define. We will start with functions and then move on to classes.

Testing functions
-----------------

A function defines an operation that can be performed. If the function takes one or more parameters, it is supposed to work properly on a variety of possible inputs. Each test case will check whether the function works properly on **one set of possible inputs**. 

A useful function will do some combination of three things, given its input parameters:

* Return a value. For these, you will write **return value tests**.
* Modify the contents of some mutable object, like a list or dictionary. For these you will write **side effect tests**.
* Print something or write something to a file. Tests of whether a function generates the right printed output are beyond the scope of this testing framework; you won't write these tests.

Testing whether a function returns the correct value is the easiest test case to define. You simply check whether the result of invoking the function a particular input produces the particular output that you expect. If f is your function, and you think that it should transform inputs x and y into output z, then you could write a test as ``test.testEqual(f(x, y), z)``. Or, to give a more concrete example, if you have a function ``sqaure``, you could have a test case ``test.testEqual(square(3), 9)``. Call this a **return value test**. 

To test whether a function makes correct changes to a mutable object, you will need more than one line of code. You will first set the mutable object to some value, then run the function, then check whether the object has the expected value. An example follows. Call this a **side effect test** because you are checking to see whether the function invocation has had the correct side effect on the mutable object.

.. sourcecode:: python

   def update_counts(letters, counts_dict):
       for c in letters:
           if c in counts_dict:
               counts_dict[c] = counts_dict[c] + 1
           else:
               counts_dict[c] = 1
   
   counts_dict = {'a': 3, 'b': 2}
   update_counts("aaab", counts_dict)
   test.testEqual(counts_dict['a'], 6)
   test.testEqual(counts_dict['b'], 3)

Because each test checks whether a function works properly on specific inputs, the test cases will never be complete: in principle, a function might work properly on all the inputs that are tested in the test cases, but still not work properly on some other inputs. That's where the art of defining test cases comes in: you try to find specific inputs that are representative of all the important kinds of inputs that might ever be passed to the function.

The first test case that you define for a function should be an "easy" case, one that is prototypical of the kinds of inputs the function is supposed to handle. Additional test cases should handle "extreme" or unusual inputs. For example, if you are defining the "square" function, the first, easy case, might be an input like 3. Additional extreme or unusual inputs around which you create tests cases might be a negative number, 0, a floating point number, and a very, very large number.  

Testing classes
---------------

To test a user-defined class, you will create test cases that check whether instances are created propertly, and you will create test cases for each of the methods as functions, by invoking them on particular instances and seeing whether they produce the correct return values and side effects, especially side effects that change data stored in the instance variables. To illustrate, we will use the Point class that was used in the :ref:`introduction to classes <classes_chap>`.

To test whether the class constructor (the __init__) method is working correctly, create an instance and then ivoke test.testEqual to see whether its instance variables are set correctly.

.. sourcecode:: python

   class Point:
       """ Point class for representing and manipulating x,y coordinates. """
   
       def __init__(self, initX, initY):
   
           self.x = initX
           self.y = initY
   
       def distanceFromOrigin(self):
           return ((self.x ** 2) + (self.y ** 2)) ** 0.5
   
       def move(self, dx, dy):
           self.x = self.x + dx
           self.y = self.y + dy
   
   p = Point(3, 4)
   test.testEqual(p.y, 4)
   test.testEqual(p.x, 3)

A method like distanceFromOrigin does its work by computing a return value, so it needs to be tested with a return value test. A method like move does its work by changing the contents of a mutable object (the point instance has its instance variable changes) so it needs to be tested with a side effect test. 

.. sourcecode:: python

   p = Point(3, 4)
   test.testEqual(p.distanceFromOrigin(), 5.0)
   p.move(-2, 3)
   test.testEqual(p.x, 1)
   test.testEqual(p.y, 7)



**Check your understanding**

.. mchoicemf:: test_questionmore_testing_1
   :answer_a: True
   :answer_b: False
   :correct: b
   :feedback_a: Each test case checks whether the function works correctly on one input. It's a good idea to check several different inputs, including some extreme cases.
   :feedback_b: It's a good idea to check some extreme cases, as well as the typical cases.

   For each function, you should create exactly one test case.
 
.. mchoicemf:: test_questionmore_testing_2
   :answer_a: return value test
   :answer_b: side effect test
   :correct: b
   :feedback_a: The method may return the correct value but not properly change the values of instance variables. See the move method of the Point class above. 
   :feedback_b: The move method of the Point class above is a good example.

   To test a method that changes the value of an instance variable, which kind of test case should you write?

.. mchoicemf:: test_questionmore_testing_3
   :answer_a: return value test
   :answer_b: side effect test
   :correct: a
   :feedback_a: You want to check if maxabs returns the correct value for some input. 
   :feedback_b: The function has no side effects; even though it takes a list L as a parameter, it doesn't alter its contents.

   To test the function maxabs, which kind of test case should you write?

   .. sourcecode:: python
   
      def maxabs(L):
         """L should be a list of numbers (ints or floats). The return value should be the maximum absolute value of the numbers in L."""
         return max(L, key = abs)

.. mchoicemf:: test_questionmore_testing_4
   :answer_a: return value test
   :answer_b: side effect test
   :correct: b
   :feedback_a: The sort method always returns None, so there's nothing to check about whether it is returning the right value. 
   :feedback_b: You want to check whether it has the correct side effect, whether it correctly mutates the list.
      
   We have usually used the sorted function, which takes a list as input and returns a new list containing the same items, possibly in a different order. There is also a method called sort for lists. It changes the order of the items in the list, and returns the value None. Which kind of test case would you use on the sort method?    
   

Glossary
--------

.. glossary::

    return value test
      A return value test invokes a function on a particular set of inputs and checks whether the return value is the correct one for those inputs.
    
    side effect test
      A side effect test invokes a function and then checks whether a mutable object has the correct value. These tests are particularly common for methods of classes that set the values of instance variables.    