=========
Test book
=========
This book generates data for use with the test suite.

.. toctree::
   :maxdepth: 2
   :numbered:

   test_chapter_1/toctree
   lp_demo.py
   lp_demo-test.py


ActiveCode
----------
.. activecode:: test_activecode_1
   :caption: This is a caption

   print("My first program adds a list of numbers")
   myList = [2, 4, 6, 8, 10]
   total = 0
   for num in myList:
       total = total + num
   print(total)

.. activecode:: units2
   :nocodelens:
   :autograde: unittest

   Fix the following code so that it always correctly adds two numbers.
   ~~~~
   def add(a,b):
      return 4

   ====
   from unittest.gui import TestCaseGui

   class myTests(TestCaseGui):

       def testOne(self):
           self.assertEqual(add(2,2),4,"A feedback string when the test fails")
           self.assertAlmostEqual(add(2.0,3.0), 5.0, 5, "Try adding your parameters")

   myTests().main()


Multiple Choice
---------------
.. mchoice:: test_mchoice_1

    What color is a stop sign?

    -   red

        +   Red it is.

    -   brown

        -   Not brown.

    -   blue

        -   Not blue.

    -   gray

        -   Not gray.


Fill in the Blank
-----------------
.. fillintheblank:: test_fitb_1

    Fill in the blanks to make the following sentence: "The red car drove away."

    The |blank| car drove |blank|.

    -   :red: Correct.
        :x: Incorrect. Try 'red'.
    -   :away: Correct.
        :x: Incorrect. Try 'away'.


.. fillintheblank:: test_fitb_numeric

   The answer is 10.

   -  :10: Correct.
      :10 1: Close.
      :x: Nope.


.. fillintheblank:: test_fitb_regex
   :casei:

   Who had a little lamb?

   -   :mary|Mair[a|e|i]: Correct.
       :Sue: Is wrong.
       :x: Nope.


.. fillintheblank:: fitb_dynamic
    :dynamic:
        a = random.randrange(0, 10)
        b = random.randrange(0, 10)

    What is :math:`{{=a}} + {{=b}}`?

    -   :int(ans) == a + b: Correct!
        :int(ans) == a - b: That's :math:`{{=a}} - {{=b}}`.
        :int(ans) == a * b: That's :math:`{{=a}}\cdot{{=b}}`.
        :float(ans) == approx(a / b): That's :math:`{{=a}}/{{=b}}`.
        :x: I don't know what you're doing.


Short answers
-------------
.. shortanswer:: test_short_answer_1

    Do you like interactive textbooks?
