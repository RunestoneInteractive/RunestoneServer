**************************
Adding Runestone to Canvas
**************************

Note: Canvas integration is in **beta**.

#.  Generate a shared/secret key pair for use with Canvas:

    #.  Browse to the `Runestone Academy <https://runestone.academy>`_ and log in, then select your course (you must be the Instructor).
    #.  Browse to the `Instructor's Page <https://runestone.academy/runestone/admin/admin>`_, then click on “LTI Integration” in the Admin tab.
    #.  Click on the “Create LTI Key and Secret” button. Click the “Show Secret” button. You will use these in the next step.

#.  Follow the `Canvas instructions <https://community.canvaslms.com/t5/Instructor-Guide/How-do-I-configure-a-manual-entry-external-app-for-a-course/ta-p/1137>`_ to add an external app:

    :Name: Runestone
    :Consumer key: Enter this from Step 1.
    :Shared Secret: Enter this from Step 1.
    :Launch URL: Enter the value `https://runestone.academy/runestone/lti`. Or, it could also be `https://csawesome.runestone.academy/runestone/lti` if you are using the csawesome course and its dedicated server.
    :Domain: Leave blank.
    :Privacy: Select Public; otherwise, Runestone won’t work.
    :Custom Fields: A matter of debate — I leave this blank; Brad prefers ``custom_course_id=xxx``.
    :Description: Interactive textbooks from Runestone Academy

#.  Add an assignment in Canvas that uses the Runestone external tool:

    #.  At `Runestone Academy`_, create an assignment; be sure you’ve checked the “Visible to Students” box and saved that change.
    #.  Still on the assignments page, copy the LTI link.
    #.  In Canvas, add an assignment. For the submission type, select “External Tool.” For the External Tool URL, use the LTI link you just copied. You’ll have to manually enter the same due date/time and a similar assignment name; these aren’t copied automatically. You must be sure the Load This Tool In A New Tab checkbox is checked.

#.  Students can now click on this assignment and work it. **If they don’t click on the assignment, they won’t receive a grade.**
#.  When the assignment is due, go to Runestone directly from your Canvas course by using an assignment link. Otherwise, grade reporting won’t work.
#.  In the grading tab of the instructor interface, grade the assignment, then click the “Release Grades” button. Doing this will push all grades to Canvas.
