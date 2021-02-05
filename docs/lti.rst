***************
LTI Integration
***************

All LMS platforms
=================
Generate a shared/secret key pair for use with Canvas:

#.  Browse to the `Runestone Academy <https://runestone.academy>`_ and log in, then select a course you’re the instructor of.
#.  Browse to the `Instructor's Page <https://runestone.academy/runestone/admin/admin>`_, then click on “LTI Integration” in the Admin tab.
#.  Click on the “Create LTI Key and Secret” button. Click the “Show Secret” button. You will use these in the next step.

After this, follow instructions for your LMS:

.. contents:: Table of Contents
    :local:


Canvas
------
#.  Follow the `Canvas instructions <https://community.canvaslms.com/t5/Instructor-Guide/How-do-I-configure-a-manual-entry-external-app-for-a-course/ta-p/1137>`_ to add an external app:

    :Name: Runestone
    :Consumer key: Enter this from step 1.
    :Shared Secret: Enter this from step 1.
    :Launch URL: Depends on the book/server in use:

        -   Enter the value ``https://csawesome.runestone.academy/runestone/lti`` if you are using the csawesome course and its dedicated server.
        -   Enter the value ``https://runestone.academy/runestone/lti`` for all other cases.

    :Domain: Leave blank.
    :Privacy: Select Public; otherwise, Runestone won’t work.
    :Custom Fields: Depends on the installation type:

        -   For a site-wide installation, or for installing the Runestone external app for use across multiple courses, leave this blank.
        -   If installing for a single course, add ``custom_course_id=xxx``, where ``xxx`` is the ID of the course.
    :Description: Interactive textbooks from Runestone Academy

#.  Add an assignment in Canvas that uses the Runestone external tool:

    #.  At `Runestone Academy`_, create an assignment; be sure you’ve checked the “Visible to Students” box and saved that change.
    #.  Still on the assignments page, copy the LTI link.
    #.  In Canvas, add an assignment. For the submission type, select “External Tool.” For the external tool URL, use the URL you just copied. You’ll have to manually enter the same due date/time and a similar assignment name; these aren’t copied automatically. You must be sure the Load This Tool In A New Tab checkbox is checked.

#.  Students can now click on this assignment and work it. **If they don’t click on the assignment, they won’t receive a grade.**
#.  When the assignment is due, go to Runestone directly from your Canvas course by using an assignment link. Otherwise, grade reporting won’t work.
#.  In the grading tab of the instructor interface, grade the assignment, then click the “Release Grades” button. Doing this will push all grades to Canvas.


Moodle
------
#. The following instructions are for Moodle, but should work for any LMS with LTI Support. Please note that certain items may have naming variations (ie. Moodle External Tool / Canvas External App).

#. In Moodle, create a new external tool called "LTI Login Link".

    :Name: Login to Runestone
    :Tool URL: https://yourHost.blahblah.edu/runestone/lti
    :Consumer key: Enter the key you selected for `consumer` from step 2.2
    :Shared secret: Enter the key you selected for `secret` from step 2.2
    :Icon URL: https://yourHost.blahblah.edu/runestone/static/images/logo_small.png
    :Share Email: True
    :Share Name: True
    :Custom params:

#.  Login to your Runestone instance with the tool just created, and create your class as well as your assignments.

#.  In Moodle, create a new enrollment external app directly to your course and assignment. You will need to repeat this for each assignment. You will also need the database values for your course ID, and assignment ID. Get these from step 2.2. Please note that in order to receive roles and grades. "Accept Grades" must be checked in Moodle. In other LMS's this may be referenced by a "Share IMS Names and Roles" or similar.

    :Name: Assignment 1
    :Tool URL: https://runestone.colorado.edu/runestone/lti?assignment_id=<ID>&custom_course_id=<ID>
    :Consumer key: Enter the key you selected for `consumer` from step 2.2
    :Shared secret: Enter the key you selected for `secret` from step 2.2
    :Icon URL: https://yourHost.blahblah.edu/runestone/static/images/logo_small.png
    :Share Email: True
    :Share Name: True
    :Custom params:
    :Accept Grades: True

#.  Copy the tool as many times as you need to within your Moodle Course and updating the Name and Tool URL

#.  Students can now click on these external tool assignment to be enrolled/logged directly into your runestone course and assignment. The grade should return to Moodle once they are released in Runestone in the instructor interface.

#.  The course instructor must also be an LTI sourced user, so use the "LTI Login Link" URL. This can be hidden for users.
