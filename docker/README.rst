Docker Deployment
====================================

.. note::

    These instructions are for installing Runestone Server using Docker to automate
    much of the work involved in setting up the environment needed to run a server.
    If you would prefer to install all the components directly on a server yourself,
    see the `Manual Installation instructions <../docs/installation.html>`_.


Using Docker, we can bring up the server without needing to install dependencies directly on
the host. Instead, the software required to run the server will be installed in four separate
docker containers (Runestone application, redis cache, postgres DB, jobe code compilation).


.. note::

    These instructions have been tested on Ubuntu 20.04 and should work on any version of Ubuntu 18.04+.
    Installation on older versions of Ubuntu or other Linux distributions may require adjustments.
    These instructions have also been tested on OS X. For Windows, use WSL, VirtualBox, or other similar virtualization software.


Contents
--------
.. contents::


Setup
-----------------------------


1. Run the bootstrap script
****************************

To build a Docker application with the server and all its dependencies, download then run the bootstrap script:

.. code-block:: bash

    curl -fsSLO https://raw.githubusercontent.com/RunestoneInteractive/RunestoneServer/master/docker/docker_tools.py
    # See what build options are available.
    python3 docker_tools.py build --help
    # Run the build.
    python3 docker_tools.py build <your options here>

This will take a while. But once built, you will not need to rebuild the image unless you need to modify settings
inside it. If you do need to modify a built image, you can either `shell into the built container <Shelling Inside>`_
to make changes or rebuild the image.

When this completes, **log out then back in** (reboot if using a VM) to update your group membership. Next, ``cd RunestoneServer``.

.. note::

    All future commands should be run in the ``RunestoneServer`` directory unless instructions specify otherwise.

.. note:: VirtualBox

    To run in VirtualBox, configure the network settings: use NAT, select Advanced, Port forwarding, add:

    =====   ========    =======     =========   ========    ==========
    Name    Protocol    Host IP     Host Port   Guest IP    Guest Port
    =====   ========    =======     =========   ========    ==========
    SSH     TCP                     22                      22
    HTTP    TCP                     80                      80
    HTTPS   TCP                     443                     443
    =====   ========    =======     =========   ========    ==========


2. Configuration
***********************

Most basic configuration can be done via two files you will need to create. These files
are read every time the server is restarted - to see the effects of any changes you will
need to stop the containers and restart them.

Environment Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You may need to set values for environment variables to run Runestone. The easiest
way to do so is to use a ``.env`` file, which Docker will read automatically as it loads
containers. A sample ``.env`` file is provided as ``./.env`` (copied from `docker/.env.prototype <.env.prototype>` on the first build).

If you are running a local test/development instance, you should not need to modify
any of the settings in ``.env``. If you are setting up a production server, you will need to
modify the defaults. See the file for notes about what values are required.

Python Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You also will also likely want to configure some options in the Python code. These options
will be in the file ``models/1.py`` (which is automatically created on the first build).


Again, if you are installing for local development/testing you should not need to modify
any of the settings. If you are installing for production, you will want/need to modify
some of them (so that things like sending students emails for lost passwords work).
See comments in the file for details.


.. warning::

    You will NOT want to check either ``.env`` or ``models/1.py`` into source control. The
    ``.gitignore`` file is set to ignore both of them.


3. Starting/Stopping
**************************

Once your environment is ready to go, you can use ``docker-compose`` to bring the containers up.
This command will create four containers to run different parts of the application stack
(runestone server, redis cache, postgres DB, jobe code testing environment). There are two options:

.. code-block:: bash

    # For debugging, watch the container start up. Stop the container when ctrl-c is pressed.
    docker-compose up
    # Run the container in the background. Use ``docker-compose logs --follow`` to watch.
    docker-compose up -d

The first time you run the command will take a little longer as it installs software into the various
containers. After it is complete, you can go to http://localhost/  to see the application
(if you configured a hostname, substitute it for localhost). If everything so far is set up correctly,
you should see a welcome/login page. Continue in the instructions to add book(s), course(s) and a user account.

To stop all containers use:

.. code-block:: bash

    docker-compose stop


To restart the containers, to reload configuration files or because you have added a new book,
do:

.. code-block:: bash

    docker-compose restart


Or to just restart the Runestone container (which is generally the only one that needs to be updated):

.. code-block:: bash

    docker-compose restart runestone


If you ever want to completely wipe the containers, stop them and then do:

.. code-block:: bash

    docker-compose rm


4. Add Books
**************************

To add a book, you need to add its source code to the ``RunestoneServer/books/`` directory. For an existing
`Runestone book <https://github.com/RunestoneInteractive>`_, that means cloning its source code. For example - to add
`thinkcspy <https://github.com/RunestoneInteractive/thinkcspy>`_ you would do:

.. code-block:: bash

    cd books/
    git clone https://github.com/RunestoneInteractive/thinkcspy.git
    cd ..


.. warning::

   It is important that the folder name for the book matches the ``project_name`` set in its ``pavement.py``.
   This is not always automatically the case. For example, the `ThinkCPP <https://github.com/RunestoneInteractive/ThinkCPP>`_
   repository will normally be cloned into **ThinkCPP** but it has the ``project_name`` set to ``thinkcpp``.
   If there is a mismatch, you will want to rename the folder you cloned the code into so that it
   matches the ``project_name``.

After cloning a book, or after making any edits/updates to it, you need to build the book:

.. code-block:: bash

    docker-tools book-build <book-name>


You will then need to restart the Runestone server to make the new/updated book available. TODO: this is old. rsmanage?

.. code-block:: bash

    docker-compose restart runestone

.. note::

   Most Runestone books set ``master_url`` to ``get_master_url()`` in their ``pavement.py`` file. However, if the book
   you are adding does not, it is **critical** that the ``master_url`` variable in that file is set correctly.
   If you are running docker and doing your development on the same machine then ``http://localhost`` will work.
   If you are running docker on a remote host then make sure to set it to the name of the remote host.


5. Add Courses
**************************

TODO: This scripts needs to be updated. It doesn't work.

To add a course based on a book, run the ``daddcourse`` script:

.. code-block:: bash

    scripts/daddcourse


It will ask for:

**Course Name**: The short name to identify this course/section (do **NOT** include any spaces).  e.g. ``yourname-cs1-fall2021``

**Base Course**: The name of the book to use. This **MUST** match the `project_name` defined
in `pavement.py` of the book. e.g. ``thinkcspy``

**Your institution**: The human readable name of your institution. e.g. ``Some State U``

Then you will be asked whether to allow users to access the course without logging in (defaults to yes) and whether to allow
pair programming (default is no).

You do not have to restart the server to make use of the course.

.. note::

    Some of the default books already have "default" courses with the same name as the book. If you try to create
    a course with a name like ``thinkcspy`` you will be told that the course name is the same as the book.

6. Add a User
**************************

TODO: This scripts needs to be updated. It doesn't work.

To add an initial instructor account to the course you have created, you can either create a new user or add
an existing user as an instructor to the course.

To add a new user, use the ``dmanage`` script to run **inituser**. It asks for what class to add the user to and whether or not
they should be made an instructor.

.. code-block:: bash

    scripts/dmanage inituser


Or, if you already have an account that you want to add as an instructor to the new course, you can use the
``dmanage`` script to execute **addinstructor** which will prompt you for a username and course name:

.. code-block:: bash

    scripts/dmanage addinstructor


Neither of these will require restarting the server.

Once you have logged in as an instructor, you can bulk add students through the web interface.

It is also possible to use a csv file to add multiple instructors or students as you start
up the server. However, this process is brittle (any error loading the information results
in the server entering a restart loop as it fails to load). To do so, make a file named either
`instructors.csv` or `students.csv` in a folder called `configs` in the RunestoneServer folder.
The format of the csv files is to have one person per line with the format of each line as follows:

    username,email,first_name,last_name,pw,course

Once you have started the server, you may have to remove that file to prevent subsequent restarts
trying to load the same records and entering a restart loop because the records already exist.


Other Tips & Tricks
-------------------------------


Rebuilding
***********************

To re-build an image:

.. code-block:: bash

    # See the possibilities
    docker-tools build --help
    # Actually run the build (add options as desired)
    docker-tools build


To force a rebuild, make sure the containers are `stopped <4. Starting/Stopping>`_, then rerun the build
command. The build process caches results from previous builds and should complete much more rapidly. However, the
cache can cause issues if you modify a file that the system is checking for changes. If you need to force a
complete rebuild, use:

.. code-block:: bash

    docker-tools build -- --no-cache


Shelling Inside
**********************************

You can shell into the container to look around, or otherwise test. When you enter,
you'll be in the web2py folder, where runestone is an application under applications. From
the RunestoneServer directory do:

.. code-block:: bash

    docker-tools shell


Remember that the folder under web2py applications/runestone is bound to your host,
so **do not edit files from inside the container** otherwise they will have a change
in permissions on the host.

To run Python-based program, you must first activate a virtual environment:

.. code:: bash

    cd $RUNESTONE_PATH
    poetry shell


Ephemeral filesystem
********************
Data is stored on a Docker containerized application in two distinct places:

-   Volumes, such as the Runestone Server path (`$RUNESTONE_PATH`), the BookServer path, and the Runestone Components path.
-   Layers in a docker image -- which is everything not stored in the volumes listed above.

**Anything written to layers after the Docker build process will be lost.** For example, if you shell into the container then ``apt install`` a package, these changes will be lost if the container is stopped, its configuration changed, etc. This is the nature of Docker. See the `docs <https://docs.docker.com/storage/>`__ for more information.


SSH/VNC access
*********************

To install a VNC client on Linux, execute ``sudo apt install gvncviewer``. Next, run ``gvncviewer localhost:0 &``. This allows you to open a terminal in the container, see Chrome as Selenium tests run, etc.

Execute ``sudo apt install openssh-server`` to install a SSH server. This allows easy access from VSCode, as well as usual SSH access.


Runestone Components / BookServer Development
***********************************************

If you are doing development work on Runestone itself, you will want to install the RunestoneComponents and/or the BookServer from source. To do this, rebuild the image with the ``--single-dev`` option:

.. code-block:: bash

    docker-tools build --single-dev
    docker-compose up

This command automatically clones the `RunestoneComponents <https://github.com/RunestoneInteractive/RunestoneComponents>`_ and/or the `BookServer <https://github.com/bnmnetp/BookServer>`_
as a sibling of the root directory. Use the ``docker-tools build --clone-all/bks/rc/rs`` options to clone your repositories.

As you make changes to Runestone Components or the BookServer, you should not have to restart the Docker containerized application. Any rebuild
of a book should immediately use the new code. This is because the host filesystem is mounted as a `volume <https://docs.docker.com/storage/volumes/>`_ in the container; see the generated ``docker-compose.overrides.yaml`` file.

You can run the unit tests in the container using the ``docker-tools test`` command.

To start or stop the servers, use ``docker-tools start-servers`` / ``docker-tools stop-servers``. While changes to web2py controllers don't require a server restart, any changes to code in the ``modules`` folder does.


Testing the Entrypoint
**********************************

If you want to test the script, the easiest thing
to do is add a command to the docker-compose to disable it, and then run commands
interactively by shelling into the container.

Bring up the containers and then shell inside. Once inside, you can then issue commands
to test the entry point script - since the other containers were started
with docker-compose everything in them is ready to go.


File Permissions
**********************************

File permissions can seem a little strange when you start this container on Linux. Primarily because both
nginx and uwsgi run as the ``www-data`` user. So you will suddenly find your files under RunestoneServer
owned by ``www-data`` . The container's entry point script updates permissions to allow both you and the
container enough privileges to do your work.


Writing Your Own Book
**********************************

If you are writing your own book you will want to get that book set up properly in the runestone
system. You need to do the following:

1. Run the command ``dmanage addcourse`` Use the project name you configured in ``pavement.py`` as
the name of BOTH the course and the basecourse when it asks. The dmanage command is in the scripts
folder of RunestoneServer.

2. Now that your course is registered rebuild it using the command ``docker/docker_tools.py book-build <book_name>`` command. TODO: This is old. rsmanage?

3. If this book is a PreTeXt book you will need to navigate to the directory that contains the
``runestone-manifest.xml`` file and run the command:

.. code-block:: bash

    runestone process-manifest --course <yourcourse> --manifest runestone-manifest.xml

.. note::

    If you are missing ``runestone-manifest.xml`` then you need to rebuild your PreTeXt
    book with ``runestone`` as the publisher. See the PreTeXt docs for how do do this.


Changing dependencies
*********************

If you modify the dependencies of a non-Poetry project (such as the Runestone Components or rsmanage), then ``poetry update`` **will not** see these updates. To force an update, manually delete the ``*.egg-info`` directory before running ``poetry update``.