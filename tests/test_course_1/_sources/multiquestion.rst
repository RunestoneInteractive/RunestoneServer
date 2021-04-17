This was copied from the Runestone Components timed test.


A Multi Question Exam
=====================

.. timed:: test_timed_1
   :timelimit: 10

   .. mchoice:: test_timed_mchoice_1
       :answer_a: The value you are searching for is the first element in the array.
       :answer_b: The value you are searching for is the last element in the array
       :answer_c: The value you are searching for is in the middle of the array.
       :answer_d: The value you are searching for is not in the array
       :answer_e: Sequential Search can never be faster than Binary Search.
       :correct: a
       :feedback_a: Only when the search value is the first item in the array, and thus the first value encountered in sequential search, will sequential be faster than binary.
       :feedback_b: In this case a sequential search will have to check every element before finding the correct one, whereas a binary search will not.
       :feedback_c: Results will differ depending on the exact location of the element, but Binary Search will still find the element faster while Sequential will have to check more elements.
       :feedback_d: If the search value is not in the array, a sequential search will have to check every item in the array before failing, a binary search will be faster.
       :feedback_e: When the search value is the first element, Sequential will always be faster, as it will only need to check one element.

       Under which of these conditions will a sequential search be faster than a binary search?

   .. clickablearea:: test_timed_clickablearea_1
       :question: Click on the correct cells.
       :feedback: Remember, the operator '=' is used for assignment.
       :table:
       :correct: 1,1;1,4;2,3;2,4
       :incorrect: 2,1;2,2;3,0

       +------------------------+------------+----------+----------+
       |        correct         |    N-A     |    N-A   | correct  |
       +========================+============+==========+==========+
       | Incorrect              | incorrect  | correct  | correct  |
       +------------------------+------------+----------+----------+
       | This row is incorrect  |   ...      |   ...    |   ...    |
       +------------------------+------------+----------+----------+

   .. dragndrop:: test_timed_dnd_1
       :feedback: This is feedback.
       :match_1: Drag to A|||Answer A
       :match_2: Drag to B|||Answer B
       :match_3: Drag to C|||Answer C

       This is a drag n drop question.

   .. fillintheblank:: test_timed_fitb_1

       Fill in the blanks to make the following sentence: "The red car drove away" The |blank| car drove |blank|.

       -  :red: Correct
          :.*: Try red
       -  :away: Correct
          :.*: where did we say the red car was going?


   .. activecode:: test_timed_activecode_1
       :nocodelens:

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


   .. parsonsprob:: test_timed_parsons_1

      Put the blocks in order to describe a morning routine.
      -----
      get up
      =====
      eat breakfast
      =====
      brush your teeth


   .. shortanswer:: test_timed_shortanswer_1
       :optional:
       :mathjax:

       What are the colors in the rainbow?
       What is meaning of :math:`\pi r^2`
