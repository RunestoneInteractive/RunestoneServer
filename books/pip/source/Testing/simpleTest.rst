..  Copyright (C)  Paul Resnick, B.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

..  shortname:: SimpleTest
..  description:: Asserting with test.testEqual

.. qnum::
   :prefix: simple_test-
   :start: 1

.. _simple_tests_chap:

Test Cases
==========

In some of the problem sets, you have seen comments that tell you what a program
should output, or what value a function should return when invoked on particular
inputs. A **test case** expresses requirements for a program more formally, in a way
that can be checked automatically. Specifically, a test asserts something about
the state of the program at a particular point in its execution.

We have previously suggested that it's a good idea to first write down comments
about your code is supposed to do, before actually writing the code. It is an 
even better idea to write down some test cases before writing a program. For example,
before writing a function, write a few test cases that check that it returns an
object of the right type and that it returns the correct values when invoked on particular
inputs.

We will return to the idea of test cases towards the end of the course, and make
use of the standard python unit testing module. For now, we introduce a much simpler
unit testing module that consists of just one function.

The module ``test`` can be imported in activecode windows. It consists of just
a single function, ``testEqual``. Below is the code for it.

.. sourcecode:: python

    def testEqual(actual, expected):
        if type(expected) == type(1):
            # they're integers, so check if exactly the same
            if actual == expected:
                print('Pass')
                return True
        elif type(expected) == type(1.11):
            # a float is expected, so just check if it's very close, to allow for
            # rounding errors
            if abs(actual-expected) < 0.00001:
                print('Pass')
                return True
        else:
            # check if they are equal
            if actual == expected:
                print('Pass')
                return True
        print('Test Failed: expected ' + str(expected) + ' but got ' + str(actual))
        return False

Given what you learned in the :ref:`Modules Chapter <modules_chap>`, the way to
put tests in your code is:

.. activecode:: simple_test_1

    import test
    test.testEqual(2, 1+1)
    
The import statement loads the module. test.testEqual looks up the testEqual
within the test module and tries to call it (that's what the parentheses after 
testEqual do). The values 2 and 2 are passed and bound to the formal parameters actual and expected.
The word pass is printed out. The value True is returned, but in this case that value is ignored.

Here's an example with test cases for the `blanked` function that you created 
in Problem Set 4.

.. activecode:: simple_test_2

      # define the function blanked(). 
      # It takes a word and a string of letters that have been revealed.
      # It should return a string with the same number of characters as
      # the original word, but with the unrevealed characters replaced by _ 
            
      def blanked(word, revealed_letters):
          return word 
      
      import test
      test.testEqual(type(blanked("Hello", "el")), type(""))    # make sure it returns a string
      test.testEqual(blanked("Hello", "el"), '_ell_')           # check output particular input
      test.testEqual(blanked("Hellos", "celxb"), '_ell__')      # check output particular input
      test.testEqual(blanked("Goodbye", 'Gwioby'), 'Goo_by_')   # check output particular input

**Check your understanding**

.. mchoicemf:: test_questionsimple_test_1
   :answer_a: True
   :answer_b: False
   :answer_c: It depends
   :correct: b
   :feedback_a: Check the code that defines testEqual
   :feedback_b: A message is printed out, but the program does not stop executing
   :feedback_c: Check the code the defines testEqual

   When test.testEqual is given two values that are not the same, it generates an error and
   stops execution of the program.
 
.. mchoicemf:: test_questionsimple_test_2
   :answer_a: True
   :answer_b: False
   :correct: b
   :feedback_a: You might not notice the error, if the code just produces a wrong output rather generating an error. And it may be difficult to figure out the original cause of an error when you do get one.
   :feedback_b: Test cases let you test some pieces of code as you write them, rather than waiting for problems to show themselves later.

   Test cases are a waste of time, because python interpreter will give an error
   message when the program runs incorrectly.


Glossary
--------

.. glossary::

    test case
        An assertion about the state of the program at particular point in its
        execution, such as the type of a variable or of a value returned by a
        function.    