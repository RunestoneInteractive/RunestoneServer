Docker Deployment
====================================

.. TODO

    Docs to update:

    Jobe thing turns red?

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

1. Install OS-dependent prerequisites
*************************************

.. TODO

    Enable the script to download and install the Docker Desktop if necessary. Challenge: how to determine if an app in installed in Windows/OS X? On Windows, should we assume WSL2 + Docker Desktop or ask the user if they want to VirtualBox? (I think we should assume -- an advanced user would probably understand to install VirtualBox if they wanted to.)

    Is there any way to download the script without installing curl? It seems like neither curl nor wget is installed by default in Ubuntu. The solution I can see: write OS-specific scripts (Powershell for Windows, bash for Linux and OS X) that can be

Linux
^^^^^
If running on Linux, you must use Ubuntu 20.04 (although any version of Ubuntu 18.0+ should work). Installation on older versions of Ubuntu or other Linux distributions may require adjustments. Install ``curl`` by opening a terminal then typing:

    .. code:: bash

        sudo apt-get install -y curl

OS X
^^^^
If running on OS X, install then run the `Docker Desktop <https://www.docker.com/products/docker-desktop/>`_.

    .. note::

        Expect to wait a few minutes the first time you start the Docker Desktop. Don't proceed until the Docker Desktop's initialization is complete.

Windows
^^^^^^^
If running on Windows, either:

    Install Ubuntu on `WSL2 <https://ubuntu.com/tutorials/install-ubuntu-on-wsl2-on-windows-10#1-overview>`_. Next, install then run
    `Docker Desktop`_; see the note above on the initialization process.

    or

    Install Ubuntu on `VirtualBox <https://ubuntu.com/tutorials/how-to-run-ubuntu-desktop-on-a-virtual-machine-using-virtualbox>`_ or on some other virtualization software. You do not need to install the Docker Desktop.

        .. note:: VirtualBox

            To run in VirtualBox, configure the network settings: use NAT, select Advanced, Port forwarding, add:

            =====   ========    =======     =========   ========    ==========
            Name    Protocol    Host IP     Host Port   Guest IP    Guest Port
            =====   ========    =======     =========   ========    ==========
            SSH     TCP                     22                      22
            HTTP    TCP                     80                      80
            HTTPS   TCP                     443                     443
            =====   ========    =======     =========   ========    ==========

Next, install ``curl`` by opening an Ubuntu terminal then typing:

.. code:: bash

    sudo apt-get install -y curl

2. Run the bootstrap script
***************************
Next, download the bootstrap script. To do this, open a terminal in Ubuntu or OS X then type:

.. code-block:: bash

    curl -fLO https://raw.githubusercontent.com/RunestoneInteractive/RunestoneServer/master/docker/docker_tools.py

This download the bootstrap script. The next step, which installs required dependencies for the remainder of the process, depends on your use case:

Use case: running the server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For the devops use case, execute:

.. code-block:: bash

    python3 docker_tools.py init

Use case: change the way Runestone works or change/add to the way `interactive exercises <https://pretextbook.org/doc/guide/html/topic-interactive-exercises.html>`_ behave
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For the developer use case:

#.  `Fork <https://docs.github.com/en/get-started/quickstart/fork-a-repo>`_ the `RunestoneServer <https://github.com/RunestoneInteractive/RunestoneServer.git>`_, `RunestoneComponents <https://github.com/RunestoneInteractive/RunestoneComponents.git>`_, and `BookServer <https://github.com/RunestoneInteractive/BookServer.git>`_ repositories.

#.  In the terminal, run:

.. code-block:: bash

    python3 docker_tools.py init --clone-rs <your Github userid>

3. Build the necessary containers
*********************************
In the terminal, type:

.. code-block:: bash

    cd RunestoneServer

.. note::

    All future commands should be run in the ``RunestoneServer`` directory unless instructions specify otherwise.

The next command depends on the you case you chose in the previous step:

    For the devops use case, execute:

        .. code-block:: bash

            docker-tools build

    For the developer use case, execute:

        .. code-block:: bash

            docker-tools build --single-dev --clone-all <your Github userid>

    .. note:

        The ``docker-tools build`` command offers many additional options for advanced users, viewable by running ``docker-tools build --help``.

This will take a **long** time (5-10 minutes in many cases). When this completes, **reboot your computer** to update your group membership. Next, open a terminal then ``cd RunestoneServer``.

4. Configuration
***********************

Most basic configuration can be done via two files you will need to create. These files
are read every time the server is restarted - to see the effects of any changes you will
need to stop the containers and restart them.

Environment Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the developer use case, you should not need to modify any of the default environment variables. For the devops use case, you will need to modify these. To do so, edit the ``.env`` file, which Docker will read automatically as it loads containers. A sample ``.env`` file is provided as ``./.env`` (copied from `docker/.env.prototype <.env.prototype>` on the first build). See comments in the file for details.

Python Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the developer use case, you should not need to modify any of the default Python settings. For the devops use case, you will need to modify these to obtain an HTTPS certificate, send the lost password e-mails, etc. These options will be in the file ``models/1.py`` (which is automatically created on the first build).

.. warning::

    You will NOT want to check either ``.env`` or ``models/1.py`` into source control, since these contain passwords. The ``.gitignore`` file is set to ignore both of them.


5. Starting the containerized application
*****************************************

Once your environment is ready to go, you can use ``docker-compose`` to bring the containers up. This command will create four containers to run different parts of the application stack (the Runestone server, redis cache, postgres DB, jobe code testing environment).

For the devops use case:

    .. code-block:: bash

        docker-compose up -d

    This run the container in the background (detached mode). Use ``docker-compose logs --follow`` to view logging data as the container starts up and runs.

For the developer use case use:

    .. code-block:: bash

        docker-compose up

    This displays logging data from the container in the terminal. To Stop the container, press when ctrl-c.


The first time you run the command will take a **lot** longer as it downloads containers then installs software into the various
containers. After it is complete, you can go to http://localhost/ to see the application
(if you configured a hostname, substitute it for localhost). If everything so far is set up correctly,
you should see a welcome/login page. Continue in the instructions to add book(s), course(s) and a user account.

Introducing `rsmanage`
^^^^^^^^^^^^^^^^^^^^^^
The ``rsmanage`` command will run many useful commands inside the container for you.  With ``rsmanage`` you can:

* Add a course - ``rsmanage addcourse``
* Add a user - ``rsmanage adduser``
* Get information about a course ``rsmanage courseinfo``
* Build a book - ``rsmanage build --course bookname``
* Get a database shell in the current database - ``rsmanage db``

...and many other things.  Just type ``rsmanage`` for a list of things it can do.  For a list of options just type ``rsmanage`` and the subcommand you want followed by ``--help``; for example, ``rsmanage build --help``.


6. Add Books
**************************

.. note::

    TODO: Edit/improve the docs from this point forward.

To add a book, you need to add its source code to the ``RunestoneServer/books/`` directory. For an existing
`Runestone book <https://github.com/RunestoneInteractive>`_, that means cloning its source code. For example, to add
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

After cloning a book, you may need to add it to the database.  Most of the standard books are already there, but you can use ``rsmanage addcourse`` to add it if needed.
You also need to rebuild after making any edits/updates to a book.

.. code-block:: bash

    rsmanage build --course mybook

You can also have ``rsmanage`` clone the book for you the first time you want to build it for example:

.. code-block:: bash

    rsmanage build --course thinkcspy --clone https://github.com/RunestoneInteractive/thinkcspy.git

.. note::

   Most Runestone books set ``master_url`` to ``get_master_url()`` in their ``pavement.py`` file. However, if the book
   you are adding does not, it is **critical** that the ``master_url`` variable in that file is set correctly.
   If you are running docker and doing your development on the same machine then ``http://localhost`` will work.
   If you are running docker on a remote host then make sure to set it to the name of the remote host.


7. Add Courses
**************************

To add a course based on a book, run the ``rsmanage addcourse`` script. If you run it just like
that it will prompt you for all of the necessary details. Probably the **most important** thing
to point out is that if this is a new book the first time you add it you want to make sure that the
basecourse and the course-name are the same.  If you are creating your own course but want it
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


8. Add a User
**************************

To add an initial instructor account to the course you have created, you can either create a new user or add
an existing user as an instructor to the course.

To add a new user, use the ``rsmanage adduser`` subcommand  it asks for what class to add the user to and whether or not
they should be made an instructor.

.. code-block:: bash

    rsmanage adduser

Or, if you already have an account that you want to add as an instructor to the new course, you can use the
``rsmanage`` command to execute **addinstructor** which will prompt you for a username and course name:

.. code-block:: bash

    rsmanage addinstructor

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


Operation
---------
To run the containerized application after a stop/reboot/etc.:

#.  On WSL or OS X, run the Docker Desktop.
#.  In a terminal, stop any currently-running containers:

    .. code:: bash

        docker-compose stop

#.  Next, start them by following the directions in `5. Starting the containerized application`_.



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

Ephemeral filesystem
********************
Data is stored on a Docker containerized application in two distinct places:

-   Volumes, such as the Runestone Server path (``$RUNESTONE_PATH``), the BookServer path, and the Runestone Components path.
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

1. Run the command ``rsmanage addcourse`` Use the project name you configured in ``pavement.py`` as
the name of BOTH the course and the basecourse when it asks.


1. Now that your course is registered rebuild it using the command ``rsmanage build --course <book_name>`` command.

2. If this book is a PreTeXt book you will need to navigate to the directory that contains the
``runestone-manifest.xml`` file and run the command:

.. code-block:: bash

    runestone process-manifest --course <yourcourse> --manifest runestone-manifest.xml

.. note::

    If you are missing ``runestone-manifest.xml`` then you need to rebuild your PreTeXt
    book with ``runestone`` as the publisher. See the PreTeXt docs for how do do this.

Changing dependencies
*********************

If you modify the dependencies of a non-Poetry project (such as the Runestone Components or rsmanage), then ``poetry update`` **will not** see these updates. To force an update, manually delete the ``*.egg-info`` directory before running ``poetry update``.  Note you **must** be in shelled in to the running docker container to run ``poetry update``.
