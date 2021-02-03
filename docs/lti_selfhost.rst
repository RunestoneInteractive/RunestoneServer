*************************************
Operating Runestone as a LTI Provider
*************************************

#.  Install Runestone Server

    #.  If you would like your installation to be LTI only, set `settings.lti_only_mode = True` in `models/0.py`

#.  Add LTI keys to the database

    1.  Login to postgres

    .. code-block:: bash

     # If you used Docker, you can login to postgres with the following:
     docker exec -ti <postgres-container-name> /bin/bash
     PGPASSWORD=$POSTGRES_PASSWORD psql -U $POSTGRES_USER $POSTGRES_DB

    2.  Insert the LTI Keys

    .. code-block:: bash

     # View tables if desired, we will be modifying the `lti_keys` table
     \dt

     # Description of the `lti_keys` table for reference
     \d lti_keys;
                                           Table "public.lti_keys"
        Column    |          Type          | Collation | Nullable |               Default                
     -------------+------------------------+-----------+----------+--------------------------------------
      id          | integer                |           | not null | nextval('lti_keys_id_seq'::regclass)
      consumer    | character varying(512) |           |          | 
      secret      | character varying(512) |           |          | 
      application | character varying(512) |           |          | 

     # Generate a secret, you can do this in another terminal with openssl
     openssl rand -hex 32

     # Example output from above
     5a239cd6cc27763afc4fe93a87284ea0883546ea3aad77bbee8c4691e0e17870

     # Back on postges, insert the values desired
     INSERT INTO lti_keys VALUES (1,'<yourConsumerName>','<yourSecret>','<yourApplication>');

     # For example
     INSERT INTO lti_keys VALUES (1,'cuboulder_canvas','5a239cd6cc27763afc4fe93a87284ea0883546ea3aad77bbee8c4691e0e17870','cs_runestone');
     INSERT INTO lti_keys VALUES (2,'cuboulder_moodle','5a239cd6cc27763afc4fe93a87284ea0883546ea3aad77bbee8c4691e0e17870','cs_runestone');

     # Verify if desired
     SELECT * FROM lti_keys;

     # To get your course ID's, run the following. Please note that new installs have ~21 placeholder courses.
     # Your first course will have an ID after these.
     SELECT * FROM courses;

     # To get your assignment ID's, run the following.
     SELECT * FROM assignments;

     # Use \q to quit
     \q

#.  Create an LTI generic enrollment link

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


4.  Login to your Runestone instance with the tool just created, and create your class as well as your assignments.

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

6.  Copy the tool as many times as you need to within your Moodle Course and updating the Name and Tool URL

#.  Students can now click on these external tool assignment to be enrolled/logged directly into your runestone course and assignment. The grade should return to Moodle once they are released in Runestone in the instructor interface.

#.  The course instructor must also be an LTI sourced user, so use the "LTI Login Link" URL. This can be hidden for users.
