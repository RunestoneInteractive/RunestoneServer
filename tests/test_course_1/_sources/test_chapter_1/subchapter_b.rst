Subchapter B
============


Lets add one activity to this Subchapter!

.. mchoice:: subc_b_1
   :author: test_author
   :answer_a: True
   :answer_b: False
   :correct: b
   :feedback_a: It usually takes longer to read a program because the structure is as important as the content and must be interpreted in smaller pieces for understanding.
   :feedback_b: It usually takes longer to read a program because the structure is as important as the content and must be interpreted in smaller pieces for understanding.
   :practice: T

   True or False:  Reading a program is like reading other kinds of text.


.. poll:: LearningZone_poll
    :option_1: Comfort Zone
    :option_2: Learning Zone
    :option_3: Panic Zone

    During this project I was primarily in my...


.. fillintheblank:: subc_b_fitb
   :author: test_author

   Mary had a |blank| lamb.

   - :little: Is the correct answer
     :big: Is feedback on a specific incorrect
     :x: catchall feedback

.. dragndrop:: subc_b_dd
   :feedback: Feedback that is displayed if things are incorrectly matched--is optional
   :match_1: Drag to Answer A|||Answer A
   :match_2: Drag to Answer B|||Answer B
   :match_3: Drag to Answer C|||Answer C


.. clickablearea:: click1
    :question: Click on all assignment statements.
    :iscode:
    :feedback: Remember, the operator '=' is used for assignment.

    :click-incorrect:def main()::endclick:
        :click-correct:x = 4:endclick:
        for i in range(5):
            :click-correct:y = i:endclick:
            :click-incorrect:if y > 2::endclick:
                print(y)


.. activecode:: units1
    :autograde: unittest
    :practice: T

    def add(a,b):
        return 4

    ====
    from unittest.gui import TestCaseGui

    class myTests(TestCaseGui):

        def testOne(self):
            self.assertEqual(add(2,2),4,"A feedback string when the test fails")
            self.assertAlmostEqual(add(2.0,3.0), 5.0, 5, "Try adding the parameters")

    myTests().main()


.. parsonsprob:: parsons_ag1

   Construct a block of code that correctly implements the accumulator pattern.
   -----
   x = 0
   =====
   for i in range(10)
      x = x + 1


.. youtube:: anwy2MPT5RE
    :divid: yt_vid_ex1
    :height: 315
    :width: 560
    :align: left


.. showeval:: showEval_0
   :trace_mode: true

   eggs = ['dogs', 'cats', 'moose']
   ~~~~

   ''.join({{eggs}}{{['dogs', 'cats', 'moose']}}).upper().join(eggs)
   {{''.join(['dogs', 'cats', 'moose'])}}{{'dogscatsmoose'}}.upper().join(eggs)
   {{'dogscatsmoose'.upper()}}{{'DOGSCATSMOOSE'}}.join(eggs)
   'DOGSCATSMOOSE'.join({{eggs}}{{['dogs', 'cats', 'moose']}})
   {{'DOGSCATSMOOSE'.join(['dogs', 'cats', 'moose'])}}{{'dogsDOGSCATSMOOSEcatsDOGSCATSMOOSEmoose'}}




.. shortanswer:: shorta1

   You can ask your students to answer reflective questions or short essays in the box provided.


The end of subchapter b

