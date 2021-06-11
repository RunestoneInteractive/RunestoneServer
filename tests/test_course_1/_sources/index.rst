*********
Test book
*********
This book generates data for use with the test suite.

.. toctree::
   :maxdepth: 2
   :numbered:

   test_chapter_1/toctree
   lp_demo.py
   lp_demo-test.py
   selectquestion
   activecode
   multiquestion


ActiveCode
==========
.. activecode:: test_activecode_1
   :caption: This is a caption

   print("My first program adds a list of numbers")
   myList = [2, 4, 6, 8, 10]
   total = 0
   for num in myList:
       total = total + num
   print(total)


Clickable Area
==============
.. clickablearea:: test_clickablearea_1
    :question: Click the rainbow color(s)
    :feedback: This is incorrect
    :iscode:

    :click-correct:Red:endclick:
    :click-incorrect:Gold:endclick:
    :click-correct:Blue:endclick:
    :click-incorrect:Black:endclick:


.. clickablearea:: test_clickablearea_2
    :question: Click the rainbow color(s)
    :feedback: This is incorrect
    :table:
    :correct: 1,0;2,2;3,1;3,3;4,2
    :incorrect: 2,1;2,3;3,2;4,1;4,3

    +-------+---------+--------+
    |  Red  |  Orange | Yellow |
    +-------+---------+--------+
    | White |  Green  | White  |
    +-------+---------+--------+
    |  Blue |  White  | Indigo |
    +-------+---------+--------+
    | White |  Violet | White  |
    +-------+---------+--------+



Drag and Drop
=============
.. dragndrop:: test_dnd_1
    :feedback: Review your choice
    :match_1: C++|||cpp
    :match_2: Java|||java
    :match_3: Python|||py

    Match the language and the file extension.


Fill in the Blank
=================
.. fillintheblank:: test_fitb_string

    Fill in the blanks to make the following sentence: "The red car drove away."

    The |blank| car drove |blank|.

    -   :red: Correct.
        :x: Incorrect. Try 'red'.
    -   :away: Correct.
        :x: Incorrect. Try 'away'.


.. fillintheblank:: test_fitb_number

    .. If this isn't treated as a comment, then it will cause a **syntax error, thus producing a test failure.

    What is the solution to the following:

    :math:`2 * \pi =` |blank|.

    - :6.28 0.005: Good job.
      :3.27 3: Try higher.
      :9.29 3: Try lower.
      :.*: Incorrect. Try again.


.. fillintheblank:: test_fitb_regex_1
   :casei:

   Complete the sentence: |blank| had a |blank| lamb. One plus one is: (note that if there aren't enough blanks for the feedback given, they're added to the end of the problem. So, we don't **need** to specify a blank here.)

   -   :mary|Mair[a|e|i]: Correct.
       :Sue: Is wrong.
       :wrong: Try again. (Note: the last item of feedback matches anything, regardless of the string it's given.)
   -   :little: That's right.
       :.*: Nope.
   -   :0b10: Right on! Numbers can be given in decimal, hex (0x10 == 16), octal (0o10 == 8), binary (0b10 == 2), or using scientific notation (1e1 == 10), both here and by the user when answering the question.
       :2 1: Close.... (The second number is a tolerance, so this matches 1 or 3.)
       :x: Nope. (As earlier, this matches anything.)


.. fillintheblank:: test_fitb_regex_2
   :casei:

   Windows system files are stored in: |blank|.

   -   :C\:\\Windows\\system: Correct.
       :program files: Third party applications are stored here, not system files.
       :x: Try again.


.. fillintheblank:: test_fitb_regex_3
   :casei:

   Python lists are declared using: |blank|.

   -   :\[\]: Correct.
       :x: Try again.


Multiple Choice
===============
.. mchoice:: test_mchoice_1

    Which colors might be found in a rainbow (check all)?

    -   red

        +   Red it is.

    -   brown

        -   Not brown.

    -   blue

        +   Blue it is.

    -   gray

        -   Not gray.


.. mchoice:: test_mchoice_2

    What color is a stop sign?

    -   red

        +   Red it is.

    -   brown

        -   Not brown.

    -   blue

        -   Not blue.

    -   gray

        -   Not gray.


Parsons
=======
.. parsonsprob:: test_parsons_1
   :adaptive:
   :order: 0 1 2 3 4

   need some text ?
   -----
   def fib(num):
   =====
      if num == 0:
          return 0:
   =====
      if num == 1:
          return 1:
   =====
      return fib(num - 1) + fib(num - 2)
   =====
      return fib(num - 1) * fib(num - 2) #paired


Poll
====
.. poll:: test_poll_1
   :scale: 10
   :allowcomment:

    On a scale from 1 to 10, how important do you think it is to have a polling directive in the Runestone Tools?


Short answers
=============
.. shortanswer:: test_short_answer_1

    Do you like interactive textbooks?


Spreadsheet
===========
.. spreadsheet:: test_spreadsheet_1
    :mindimensions: 6,5
    :colwidths: 200,100,100
    :coltitles: 'name','year','price','foo'

    Google, 1998, 807.80
    Apple, 1976, 116.52
    Yahoo, 1994, 38.66
    ,,=sum(c1:c3)

    ====
    assert A3 == Yahoo
    assert B3 == 1994


.. spreadsheet:: test_spreadsheet_2
    :fromcsv: Iris.csv
    :colwidths: 50,100,100,100,100

    ====
    assert A151 == 150
