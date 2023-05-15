Docker Deployment
====================================

.. TODO

    See https://github.com/RunestoneInteractive/RunestoneServer/issues/1973 for ideas on how to improve this still-complex problem. See https://github.com/RunestoneInteractive/RunestoneServer/pull/1977 for OS X problems and fixes.

.. note::

    These instructions are for installing the Runestone servers using Docker to automate
    much of the work involved in setting up the environment needed to run a server.
    If you would prefer to install all the components directly on a server yourself,
    see the `Manual Installation instructions <../docs/installation.html>`_.

Using Docker, we can bring up the server without needing to install dependencies directly on
the host. Instead, the software required to run the server will be installed in four separate
Docker containers (the Runestone application, redis cache, postgres DB, and Jobe code runner).


**Contents**

.. contents::
    :local:
    :depth: 2


Setup
-----------------------------
To build a Docker application with the server and all its dependencies:

.. note::

    You will need to enter the root user password several times during the following steps. Look for the ``Password:`` prompt, then enter your password. Note that **no characters** will be echoed when you type your password -- this is a normal security precaution built into Unix.


1. Install OS-dependent prerequisites
*************************************

OS X
^^^^
Open a Terminal. In the Terminal:

#.  Edit ``/etc/paths``; add ``/opt/homebrew/bin`` as the first line in that file.
#.  `Install Homebrew <https://brew.sh/#install>`_.
#.  Execute ``brew install python docker md5sha1sum``.
#.  Run the newly-installed Docker Desktop application.

    .. note::

        Expect to wait a few minutes the first time you start the Docker Desktop. Don't proceed until the Docker Desktop's initialization is complete.

Windows
^^^^^^^
If running on Windows, either:

    `Install Ubuntu on WSL2 <https://ubuntu.com/tutorials/install-ubuntu-on-wsl2-on-windows-10#1-overview>`_. Next, install then run
    `Docker Desktop <https://docs.docker.com/desktop/install/windows-install/>`_; see the note above on the initialization process.

    **OR**

    `Install Ubuntu on VirtualBox <https://ubuntu.com/tutorials/how-to-run-ubuntu-desktop-on-a-virtual-machine-using-virtualbox>`_ or on some other virtualization software. You do not need to install the Docker Desktop.

        .. note:: VirtualBox

            To run in VirtualBox, configure the network settings: use NAT, select Advanced, Port forwarding, add:

            =====   ========    =======     =========   ========    ==========
            Name    Protocol    Host IP     Host Port   Guest IP    Guest Port
            =====   ========    =======     =========   ========    ==========
            SSH     TCP                     22                      22
            HTTP    TCP                     80                      80
            HTTPS   TCP                     443                     443
            =====   ========    =======     =========   ========    ==========

Next, run the ``Ubuntu`` program to open a Linux terminal (if using WSL2) or boot up Linux and open a terminal (for VirtualBox or other virtualization software).

Finally, follow the directions for Linux below.

Linux
^^^^^
If running on Linux, you must use Ubuntu 20.04 (although any version of Ubuntu 18.0+ should work). Installation on older versions of Ubuntu or other Linux distributions may require adjustments. I am a fan
of digital ocean droplets and I would recommend starting out with a Docker droplet from their Marketplace.  This will save you a few steps.  You can of course use AWS or Linode or any other provider, but I know DO the best.  **Sizing Virtual Machines:** You will want to make sure that you have at least 1 GB of RAM as parts of the install process do use quite a bit of memory.  If you are going to use this for several classes I would recommend 2 GB.  If you are teaching courses that will involve compiling Java, C, or C++ then I would recommend a configuration that includes 4 cpus as well as 4 GB of RAM.

 Install ``curl`` by opening a terminal then typing:

.. code:: bash

    sudo apt install -y curl

.. warning::

    If this fails, run ``sudo apt update`` then retry the command above.


2. Download the bootstrap script
********************************
.. note::

    On OS X, avoid placing your files in the Documents folder, since security features introduced in OS X 12.4 require you to give Docker `additional permissions <https://support.apple.com/guide/mac-help/control-access-to-files-and-folders-on-mac-mchld5a35146/mac>`_.

Download the bootstrap script. To do this, open a terminal in Ubuntu or OS X then type:

.. code-block:: bash

    curl -fLO https://raw.githubusercontent.com/RunestoneInteractive/RunestoneServer/master/docker/docker_tools.py


3. Run the bootstrap script
***************************
.. warning::

    On Windows using Ubuntu under WSL2: if you see the error message "Docker Desktop not detected..." when running either command below, but you are running the Docker Desktop, then click the gear (settings) icon in Docker Desktop, select Resources then WSL Integration, and make sure the switch next to Ubuntu is turned on.

The next step, which installs required dependencies for the remainder of the process, depends on the two mutually exclusive use cases below. **Remember which use case you select** (either *production* or *development*); many of the following steps vary based on your use case.  **Note** if you are just kicking the tires on a Runestone Server you should use *production* not *test* or *development*.  The *test* mode is for our testing of the server by running 100's of unit tests.

Production use case
^^^^^^^^^^^^^^^^^^^
If your use case is running the server, execute:

.. code-block:: bash

    python3 docker_tools.py init

**OR**

Development use case
^^^^^^^^^^^^^^^^^^^^
If, in addition to running the server, your use case is to change the way Runestone works or change/add to the way `interactive exercises <https://pretextbook.org/doc/guide/html/topic-interactive-exercises.html>`_ behave, then:

#.  `Fork <https://docs.github.com/en/get-started/quickstart/fork-a-repo>`_ the `RunestoneServer <https://github.com/RunestoneInteractive/RunestoneServer.git>`_, `RunestoneComponents <https://github.com/RunestoneInteractive/RunestoneComponents.git>`_, and `BookServer <https://github.com/RunestoneInteractive/BookServer.git>`_ repositories. If you've already forked these repositories, `fetch the latest updates from these upstream repositories <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork>`_.

#.  In the terminal, run:

.. code-block:: bash

    python3 docker_tools.py init --clone-rs <your Github userid>


Post-build
^^^^^^^^^^
This process may take a few minutes to complete. When it does:

#.  **Reboot your computer** to update your group membership.
#.  Run the Docker Desktop if using WSL2 on Windows or using OS X.
#.  Open a terminal.


4. Build the necessary containers
*********************************

In the terminal, type:

.. code-block:: bash

    cd rsdocker/RunestoneServer

.. note::

    All future commands should be run in the ``rsdocker/RunestoneServer`` directory unless instructions specify otherwise.

The next command depends on the use case you chose in the previous step.

Pre-build
^^^^^^^^^
.. note:

    The ``docker-tools build`` command offers many additional options for advanced users, viewable by running ``docker-tools build --help``.

For the production use case, execute:

    .. code-block:: bash

        docker-tools build

**OR**

For the development use case, execute:

    .. code-block:: bash

        docker-tools build --single-dev --clone-all <your Github userid>


.. note::

    The build will take a **long** time (10-20 minutes in many cases). In particular, the last line (``rm -rf $RUNESTONE_PATH``) may seem to hang, but simply takes a long time to complete.


5. Configuration
****************

Most basic configuration can be done via two files you will need to create. These files
are read every time the server is restarted - to see the effects of any changes you will
need to stop the containers and restart them.

Environment Variables
^^^^^^^^^^^^^^^^^^^^^

For the development use case, you do not need to modify any of the default environment variables.

**OR**

For the production use case, you will need to modify these variables. To do so, edit the ``.env`` file, which Docker will read automatically as it loads containers. A sample ``.env`` file is provided as ``./.env`` (copied from `docker/.env.prototype <.env.prototype>` on the first build). See comments in the file for details.

Python Settings
^^^^^^^^^^^^^^^

For the development use case, you do not need to modify any of the default Python settings.

**OR**

For the production use case, you will need to modify these settings to obtain an HTTPS certificate, send the lost password e-mails, etc. These options will be in the file ``models/1.py`` (which is automatically created on the first build).

.. warning::

    You will NOT want to check either ``.env`` or ``models/1.py`` into source control, since these contain passwords. The ``.gitignore`` file is set to ignore both of them.


6. Starting the containerized application
*****************************************

Pre-start
^^^^^^^^^
Once your environment is ready to go, you can use ``docker compose`` to bring the containers up. This command will create four containers to run different parts of the application stack (the Runestone server, redis cache, postgres DB, jobe code testing environment).

For the production use case, execute:

    .. code-block:: bash

        docker compose up -d

    This runs the container in the background (detached mode). Use ``docker compose logs --follow`` to view logging data as the container starts up and runs; open another terminal to execute instructions from the following steps.

**OR**

For the development use case, execute:

    .. code-block:: bash

        docker compose up

    This displays logging data from the container in the terminal. To stop the container, press ctrl-c. Open another terminal to execute the following commands.


Post-start
^^^^^^^^^^
The first time you run the command will take a **lot** longer as it downloads containers then installs software into the various containers. You may ignore the red message ``jobe error`` that appears during this process. After it is complete, you can go to http://localhost/ to see the application (if you configured a hostname, substitute it for localhost). If everything so far is set up correctly, you should see a welcome/login page. Continue in the instructions to add book(s), course(s) and a user account.

Introducing ``rsmanage``
^^^^^^^^^^^^^^^^^^^^^^^^
The ``rsmanage`` command will run many useful commands inside the container for you.  With ``rsmanage`` you can:

*   Add a course - ``rsmanage addcourse``
*   Add a user - ``rsmanage adduser``
*   Get information about a course ``rsmanage courseinfo``
*   Build a book - ``rsmanage build  bookname``
*   Get a database shell in the current database - ``rsmanage db``

...and many other things.  Just type ``rsmanage`` for a list of things it can do.  For a list of options just type ``rsmanage`` and the subcommand you want followed by ``--help``; for example, ``rsmanage build --help``.

If at this stage you type `rsmanage --help` and you get a command not found it is likely that pip installed the command in a different location than the one in your PATH.  It could be in ``~/.local/bin`` or ``/usr/local/bin`` or ``/opt/local/bin``.  You can add that location to your PATH or you can just type the full path to the command.  For example, ``~/.local/bin/rsmanage``


7. Add books
************

No books are installed by default; you must add books using the following process. To add a book, you need to add its source code to the ``RunestoneServer/books/`` directory. Typically, that means cloning its source code. For example, to add
`thinkcspy <https://github.com/RunestoneInteractive/thinkcspy>`_:

.. code-block:: bash

    rsmanage build --clone https://github.com/RunestoneInteractive/thinkcspy.git thinkcspy

After cloning a book, you may need to add it to the database.  Most of the standard books are already there, but you can use ``rsmanage addcourse`` to add it if needed.

.. note::

    PreTeXt authors, see `Publishing to Runestone Academy <https://pretextbook.org/doc/guide/html/sec-publishing-to-runestone-academy.html>`_.  After that, you can build a pretext book just like building a Runestone book ``rsmanage build --ptx coursename``

The following information applies only *authoring* books using the Runestone.

.. warning::

   It is important that the folder name for the book matches the ``project_name`` set in its ``pavement.py``.
   This is not always automatically the case. For example, the `ThinkCPP <https://github.com/RunestoneInteractive/ThinkCPP>`_
   repository will normally be cloned into **ThinkCPP** but it has the ``project_name`` set to ``thinkcpp``.
   If there is a mismatch, you will want to rename the folder you cloned the code into so that it
   matches the ``project_name``.

.. note::

   Most Runestone books set ``master_url`` to ``get_master_url()`` in their ``pavement.py`` file. However, if the book
   you are adding does not, it is **critical** that the ``master_url`` variable in that file is set correctly.
   If you are running docker and doing your development on the same machine then ``http://localhost`` will work.
   If you are running docker on a remote host then make sure to set it to the name of the remote host.


8. Add courses
**************

To add a course based on a book, run the ``rsmanage addcourse`` script. If you run it just like
that it will prompt you for all of the necessary details. Probably the **most important** thing
to point out is that if this is a new book the first time you add it you want to make sure that the basecourse and the course-name are the same.  If you are creating your own course but want it
based on an existing book then make sure to use the correct base course name.

.. code-block:: bash

    rsmanage addcourse

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


9. Add users
************

To add an initial instructor account to the course you have created, you can either create a new user or add an existing user as an instructor to the course. You may use the web interface or the terminal -- the command-line interface, or CLI -- to do this.

Web interface: browse to ``https://<your domain name>/runestone/designer/index`` (production use case) or ``https://localhost/runestone/designer/index`` (development use case). Use this web page to create a new course.

CLI: To add a new user, use the ``rsmanage adduser`` subcommand; it asks for what class to add the user to and whether or not
they should be made an instructor.

.. code-block:: bash

    rsmanage adduser

Or, if you already have an account that you want to add as an instructor to the new course, you can use the
``rsmanage`` command to execute **addinstructor** which will prompt you for a username and course name:

.. code-block:: bash

    rsmanage addinstructor

Neither of these will require restarting the server.

Once you have logged in as an instructor, you can bulk add students through the web interface. After logging in to your running server as an instructor, browse to the Instructor's Page, then click on the Manage Students tab.


Operation
---------
The containerized application is configured to automatically start as soon as Docker / the Docker Desktop is started. Therefore, on OS X or Windows (when using WSL2): after a reboot or after manually shutting down the Docker Desktop, **remember to start the Docker Desktop application**.

Before using ``docker-tools`` or ``rsmanage``:

#.  Run the Docker Desktop if using WSL2 on Windows or using OS X.
#.  Open a terminal.
#.  At the terminal, execute ``cd rsdocker/RunestoneServer``.


Other Tips & Tricks
-------------------


Rebuilding
**********

To re-build an image:

.. code-block:: bash

    # See the possibilities
    docker-tools build --help
    # Actually run the build (add options as desired)
    docker-tools build

To force a rebuild, make sure the containers are stopped by executing ``docker compose stop``, then rerun the build
command. The build process caches results from previous builds and should complete much more rapidly. However, the
cache can cause issues if you modify a file that the system is checking for changes. If you need to force a
complete rebuild, use:

.. code-block:: bash

    docker-tools build -- --no-cache

Shelling Inside
***************

You can shell into the container to look around, or otherwise test. When you enter,
you'll be in the web2py folder, where ``runestone/`` is an application under ``applications/``. From the ``RunestoneServer/`` directory do:

.. code-block:: bash

    docker-tools shell

Remember that the folder under ``web2py/applications/runestone`` is bound to your host,
so **do not edit files from inside the container** otherwise they will have a change
in permissions on the host.

Ephemeral filesystem
********************
Data is stored on a Docker containerized application in two distinct places:

-   Volumes, such as the Runestone Server path (``$RUNESTONE_PATH``), the BookServer path, and the Runestone Components path.
-   Layers in a docker image -- which is everything not stored in the volumes listed above.

**Anything written to layers after the Docker build process will be lost.** For example, if you shell into the container then ``apt install`` a package, these changes will be lost if the container is stopped, its configuration changed, etc. This is the nature of Docker. See the `docs <https://docs.docker.com/storage/>`__ for more information.

SSH/VNC access
**************

To install a VNC client on Linux, execute ``sudo apt install gvncviewer``. Next, run ``gvncviewer localhost:0 &``. This allows you to open a terminal in the container, see Chrome as Selenium tests run, etc.

Execute ``sudo apt install openssh-server`` to install a SSH server. This allows easy access from VSCode, as well as usual SSH access.

Development notes
*****************

If you make changes to the Runestone Components, you must rebuild the bundle of JavaScript bundle produced by webpack using ``npm run build``, then re-build the book (or page of a book) which uses the component you're editing via a ``runestone build`` or ``pretext build``. The unit tests do this automatically; for development, it's easiest to make changes to the test then re-run the test to guarantee the correct builds are done.

If you make changes to the BookServer, you'll need to stop then restart the BookServer. To do this, use ``docker-tools start-servers`` / ``docker-tools stop-servers``.

If you make changes to the Runestone server, most changes will be immediately applied. However, changes in the ``modules`` folder require a stop / start sequence to apply these changes.

You can run the unit tests in the container using the ``docker-tools test`` command.

Testing the Entrypoint
**********************

If you want to test the script, the easiest thing
to do is add a command to the ``docker compose`` to disable it, and then run commands
interactively by shelling into the container.

Bring up the containers and then shell inside. Once inside, you can then issue commands
to test the entry point script - since the other containers were started
with ``docker compose`` everything in them is ready to go.

File Permissions
****************

File permissions can seem a little strange when you start this container on Linux. Primarily because both
nginx and Gunicorn run as the ``www-data`` user. So you will suddenly find your files under RunestoneServer
owned by ``www-data`` . The container's entry point script updates permissions to allow both you and the
container enough privileges to do your work.

Writing Your Own Book
*********************

.. note::

    PreTeXt authors, see `Publishing to Runestone Academy <https://pretextbook.org/doc/guide/html/sec-publishing-to-runestone-academy.html>`_. The following information applies only *authoring* books using the Runestone.

If you are writing your own book you will want to get that book set up properly in the Runestone
system. You need to do the following:

#.  Run the command ``rsmanage addcourse``. Use the project name you configured in ``pavement.py`` as the name of BOTH the course and the basecourse when it asks.

#.  Now that your course is registered, rebuild it using the command ``rsmanage build <book_name>`` command.  If this is a PreTeXt book then build with the command ``rsmanage build --ptx <book_name>`` where the ``book_name`` should match the document-id specified in the docinfo section of the pretext book.  Often found in ``bookinfo.ptx`` but sometimes as a peer of ``<book>`` in the ``main.ptx`` file for the book.


Changing dependencies
*********************

If you modify the dependencies of a non-Poetry project (such as the Runestone Components or rsmanage), then ``poetry update`` **will not** see these updates. To force an update, manually delete the ``*.egg-info`` directory before running ``poetry update``.  Note you **must** be in shelled in to the running docker container to run ``poetry update``.
