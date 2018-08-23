=========
Test book
=========
This book generates data for use with the test suite.

.. toctree::
   :maxdepth: 2

   test_chapter_1/toctree


ActiveCode
----------
.. activecode:: test_activecode_1
   :coach:
   :caption: This is a caption

   print("My first program adds a list of numbers")
   myList = [2, 4, 6, 8, 10]
   total = 0
   for num in myList:
       total = total + num
   print(total)


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
