Select question
---------------
.. selectquestion:: select_question_4
    :fromid: test_clickablearea_1


.. selectquestion:: select_question_5
    :fromid: test_clickablearea_2


.. selectquestion:: select_question_1
    :fromid: test_poll_1


The following spreadsheet ``selectquestion`` components are commented out, since the spreadsheet component doesn't call ``addHTMLToDb``. This means that ``selectquestion`` can't load its HTML.

.. selectquestion::: select_question_2
    :fromid: test_spreadsheet_1


.. selectquestion::: select_question_3
    :fromid: test_spreasheet_2


.. selectquestion:: select_question_6
    :fromid: test_mchoice_1


.. selectquestion:: select_question_7
    :fromid: test_mchoice_2


.. selectquestion:: select_question_8
    :fromid: test_fitb_string


.. selectquestion:: select_question_9
    :fromid: test_fitb_number


.. selectquestion:: select_question_10
    :fromid: test_fitb_regex_1


.. selectquestion:: select_question_11
    :fromid: test_fitb_regex_2


.. selectquestion:: select_question_12
    :fromid: test_fitb_regex_3


.. selectquestion:: select_question_13
    :fromid: test_parsons_1


.. selectquestion:: select_question_14
    :fromid: test_dnd_1


.. selectquestion:: select_question_15
    :fromid: test_activecode_2

There's math in the timed test loaded by the following selectquestion. Add some math here, so Sphinx will include MathJax on this page, enabling the selectquestion to render correctly: :math:`x^2`.

A selectquestion can't contain a timed test; instead, create a timed test from selectquestions.

.. timed:: test_timed_2
    :timelimit: 10

    .. selectquestion:: select_question_17
        :fromid: test_timed_mchoice_1

    .. selectquestion:: select_question_18
        :fromid: test_timed_clickablearea_1

    .. selectquestion:: select_question_19
        :fromid: test_timed_dnd_1

    .. selectquestion:: select_question_20
        :fromid: test_timed_fitb_1

    .. selectquestion:: select_question_21
        :fromid: test_timed_activecode_1

    .. selectquestion:: select_question_22
        :fromid: test_timed_parsons_1

    .. selectquestion:: select_question_23
        :fromid: test_timed_shortanswer_1


.. selectquestion:: select_question_24
    :fromid: test_short_answer_1
