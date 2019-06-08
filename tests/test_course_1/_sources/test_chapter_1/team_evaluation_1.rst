*****************
Team evaluation 1
*****************

{{ team_name, team_member = get_team_members(email, course_name) }}

Team: **{{ =team_name }}**

If there are fewer than five members in your team, simply leave information for those additional members blank. For example, a team of four would complete information for team members 1-3, and leave team member 4 blank.


Role
----
In the following questions, briefly describe the role each team member has played in all aspects of Senior Design I (ECE 4512/4532) and in preparing content for the design constraints and approach documents (GE 3513). A failure to provide details about team and content preparation roles will not earn full credit for this assignment.

.. for-loop:: 5

    .. raw:: html

        {{{{ if len(teammate_member_list) > {0}: }}}}

    .. shortanswer:: team_eval_role_{0}

        Role - {{{{ =teammate_member_list[{0}] }}}}

    .. raw:: html

        {{{{ pass }}}}


Group dynamics
--------------
.. shortanswer:: team_eval_communication

    Has your group communicated clearly and cooperated successfully? If any group members seem to take charge of all assignments or group members seem uninterested and overly passive in group discussions, detail those issues.


.. shortanswer:: team_eval_participation

    Discuss the reliability and participation of your group members. Has anyone missed a meeting, shown up late, left early, or missed any internal deadlines? If so, please be specific.


Contributions
-------------
Evaluate each team member’s contribution to the **design constraints and approach documents (GE 3513)** by distributing the assignment’s total possible points (100) as you think they should be allocated based on each member’s input. Please note that you are not rating each member on a scale of 0 to 100; rather, you are distributing a total of 100 points across all team members other than yourself (e.g., if everyone has contributed equally on a four-person team, you should give your three team members each a 33.3; if everyone has contributed equally on a five-person team, you should give your four team members each a 25). This rating does not count toward individual grades; rather, it is an opportunity to reveal any problems that might exist within your group. **To aid in transparency, I will make your anonymous ratings available to the entire team.**

.. for-loop:: 5

    .. raw:: html

        {{{{ if len(teammate_member_list) > {0}: }}}}

    .. fillintheblank:: team_eval_ge_contributions_{0}

        {{{{ =teammate_member_list[{0}] }}}}: |blank|

        -   :50 50: Response recorded.
            :x: Please enter a value between 0 and 100 for each team member. The total of all values should sum to 100.

    .. raw:: html

        {{{{ pass }}}}


Repeat the question above, this time evaluating each team member’s contribution to **all aspects of Senior Design I (ECE 4512/4532)**.

.. for-loop:: 5

    .. raw:: html

        {{{{ if len(teammate_member_list) > {0}: }}}}

    .. fillintheblank:: team_eval_sd_contributions_{0}

        {{{{ =teammate_member_list[{0}] }}}}: |blank|

        -   :50 50: Response recorded.
            :x: Please enter a value between 0 and 100 for each team member. The total of all values should sum to 100.

    .. raw:: html

        {{{{ pass }}}}


.. shortanswer:: team_eval_point_explanation

    REQUIRED: If the allocated points above are not equally distributed, you must provide an explanation for your ratings.


Additional information
----------------------
.. shortanswer:: team_eval_additional_info

    Based on any of your answers at this point, please let me know how I can best help your group going forward (meeting with your entire group, meeting with just you, monitoring specific group member contributions/team deadlines, applying a different grading scale, no intervention). Please add any other information that I should know.
