Docker Deployment
====================================

.. note::

    These instructions are for installing Runestone Server using docker to automate
    much of the work involved in setting up the environment needed to run a server.
    If you would prefer to install all the components directly on a server yourself,
    see the `Manual Installation instructions <../docs/installation.html>`_.


Using Docker, we can bring up the server without needing to install dependencies directly on
the host. Instead, the software required to run the server will be installed in four separate
docker containers (Runestone application, redis cache, postgres DB, jobe code compilation).


.. note:: 

    These instructions have been tested on Ubuntu 20.04 and should work on any version of Ubuntu 18.04+
    Installation on older versions of Ubuntu or other Linux distributions may require adjustments.
    
    Installing directly on other OS's is likely more trouble than it is worth. 
    If your native OS is Mac or Windows, it is recommended you install in a Linux VM.
    If you are trying to install in a Windows hosted virtual machine, avoid installing into
    a shared folder - permissions issues will likely prevent the deployment from working.


Setup
-----------------------------

0. Install Docker
***********************

#. Follow the `Docker installation guide <https://docs.docker.com/install/#supported-platforms>`_.
    On an updated version of Ubuntu, this should just require:

    .. code-block:: bash

        sudo apt install docker.io


#. On Linux, make sure to also perform the `post-installation steps <https://docs.docker.com/install/linux/linux-postinstall/>`_. 
    On a recent version of Ubuntu this should involve adding yourself to the docker group:

    .. code-block:: bash

        sudo usermod -aG docker $USER

    And then reloading the groups by either logging out and back in,
    restarting your virtual machine, or using this from the command prompt:

    .. code-block:: bash

        su - $USER

#. `Install Docker Compose <https://docs.docker.com/compose/install/>`_. On Ubuntu this should just be:  
    \ 

    .. code-block:: bash

        sudo apt install docker-compose

1. Get Runestone Server
***********************

Make a folder to folder to hold Runestone and install the source code:

.. code-block:: bash

    mkdir Runestone
    cd Runestone/
    git clone https://github.com/RunestoneInteractive/RunestoneServer.git
    cd RunestoneServer/

.. note::

    All future commands should be run in the **RunestoneServer** directory unless instructions specify otherwise.


2. Build
***********************

Next, build the image that will be used for the core Runestone application.

.. code-block:: bash

    docker build -t runestone/server .


This will take a while. But once built, you will not need to rebuild the image unless you need to modify settings
inside it. If you do need to modify a built image, you can either `shell into the built container <Shelling Inside>`_
to make changes or rebuild the image.

To force a rebuild, make sure the containers are `stopped <4. Starting/Stopping>`_, then rerun the ``docker build``
command. The build process caches results from previous builds and should complete much more rapidly. However, the
cache can cause issues if you modify a file that the system is checking for changes. If you need to force a 
complete rebuild, use:

.. code-block:: bash

    docker build -t runestone/server . --no-cache


3. Configuration
***********************

Most basic configuration can be done via two files you will need to create. These files
are read every time the server is restarted - to see the effects of any changes you will
need to stop the containers and restart them.

Environmental Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You will need to set a number of environmental variables to rune Runestone. The easiest
way to do so is to use a ``.env`` file, which docker will read automatically as it loads
containers. A sample ``.env`` file is provided as ``docker/.env.prototype``. Copy
it to the RunestoneServer directory and rename it ``.env``:

.. code-block:: bash

    cp docker/.env.prototype .env


If you are running a local test/development instance, you should not need to modify
any of the settings in .env. If you are setting up a production server, you will need to
modify the defaults. See the file for notes about what values are required.

Python Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You also will also likely want to configure some options in the Python code. These options
will be in a file ``models/1.py`` that you will need to make. You can use the provided 
``1.py.prototype`` file as a starter:

.. code-block:: bash

    cp models/1.py.prototype models/1.py


Again, if you are installing for local development/testing you should not need to modify
any of the settings. If you are installing for production, you will want/need to modify
some of them (so that things like sending students emails for lost passwords work). 
See comments in the file for details.


.. warning::

    You will NOT want to check either ``.env`` or ``models/1.py`` into source control. The
    ``.gitignore`` file is set to ignore both of them.


4. Starting/Stopping
**************************

Once your environment is ready to go, you can use docker-compose to bring the containers up.
This command will create four containers to run different parts of the application stack
(runestone server, redis cache, postgres DB, jobe code testing environment):

.. code-block:: bash

    docker-compose up -d

The first time you run the command will take a little longer as it installs software into the various
containers. After it is complete, you can go to http://localhost/runestone  to see the application 
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


5. Add Books
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


After cloning a book, or after making any edits/updates to it, you need to build the book using the ``dbuild``
command found in the scripts folder. Pass it the name of the book that you wish to build:

.. code-block:: bash

    scripts/dbuild thinkcspy


You will then need to restart the Runestone server to make the new/updated book available.

.. code-block:: bash

    docker-compose restart runestone

.. note:: 

   Most Runestone books set ``master_url`` to ``get_master_url()`` in their ``pavement.py`` file. However, if the book
   you are adding does not, it is **critical** that the ``master_url`` variable in that file is set correctly.
   If you are running docker and doing your development on the same machine then ``http://localhost`` will work.
   If you are running docker on a remote host then make sure to set it to the name of the remote host.


6. Add Courses
**************************

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

7. Add a User
**************************

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


Debugging
*****************

There are a couple of ways to get at the logger output. This can be useful if the server appears
to be failing to start or is exhibiting other errors.

1.  Shell into the container (see below) and then look at ``/srv/web2py/logs/uwsgi.log``

2.  Run ``docker-compose logs --tail 100 --follow`` This will give you the lst 100 lines of information
    already written (between when you started the container and ran this command) and
    will continue to display new information as it is written.



Shelling Inside
**********************************

You can shell into the container to look around, or otherwise test. When you enter,
you'll be in the web2py folder, where runstone is an application under applications. From
the RunestoneServer directory do:

.. code-block:: bash

    scripts/dshell


Remember that the folder under web2py applications/runestone is bound to your host,
so **do not edit files from inside the container** otherwise they will have a change
in permissions on the host.

Maintenance Scripts
**********************************

The ``scripts`` directory has a number of maintenance scripts that will run commands inside the runestone
container to avoid having to shell into it first. In particular the ``dmanage`` script can be used to
`perform a variety of tasks <../rsmanage/toctree.html>`_.

Runestone Components Development
**********************************

If you are doing development work on Runestone itself, you will want to install the RunestoneComponents from source.
First make sure ``npm`` is installed:

.. code-block:: bash

    sudo apt install npm


Then you will need to clone `RunestoneComponents <https://github.com/RunestoneInteractive/RunestoneComponents>`_ 
as a sibling of the RunestoneServer directory. From the ``RunestoneServer`` directory do:

.. code-block:: bash

    cd ..
    git clone https://github.com/RunestoneInteractive/RunestoneComponents.git
    cd RunestoneComponents/
    npm install
    npm run build


Then you will need to tell ``RunestoneServer`` to use this copy of Components instead of the default copy.
In the ``RunestoneServer`` directory create a `docker-compose.override.yml` file. Then add this to it:

.. code-block::
    
    version: "3"

    services:
        runestone:
            volumes:
                - ../RunestoneComponents:/srv/RunestoneComponents

You will then have to restart the runestone container, at which point the entrypoint.sh file will notice that you
have this volume mounted and reinstall the development version of Runestone.

As you make changes to Runestone Components, you should not have to restart the server. Any rebuild
of a book should immediately use the new code.


Developing on Runestone Server
*********************************************

If you look at the docker-compose file, you'll notice that the root of the repository
is bound as a volume to the container:

.. code-block:: bash

    volumes:
      - .:/srv/web2py/applications/runestone
    ...


This means that if you make changes to the repository root
(the Runestone Server application) they will also be made in the container and should
be instantly visible.


Running the Runestone Server Unit Tests
*************************************************

You can run the unit tests in the container using the following command.

.. code-block:: bash

    docker exec -it runestoneserver_runestone_1 bash -c 'cd applications/runestone/tests; python run_tests.py'


The ``scripts`` folder has a nice utility called ``dtest`` that does this for you and also supports 
the ``-k`` option for you to run a single test.


Creating Questions from the Web Interface
*************************************************

If you want to write questions from the web interface you will need to make sure
that ``settings.python_interpreter`` is set to a real python. In the uwsgi environment uwsgi tends to 
replace python in ``sys.executable`` with itself, which is pretty annoying. You can do so
in the ``1.py`` file.


Previous Database
**********************************

Once you create the containers, you'll notice a "databases" subfolder is generated
on the host. This happens after the initialization, as the runestone folder
is bound to the host. If you remove the containers and try to bring them up
without removing this folder, you'll see an error (and the container won't start):

.. code-block::

    docker-compose logs runestone
    /srv/web2py/applications/runestone/databases exists, cannot init until removed from the host.
    sudo rm -rf databases


The message tells you to remove the databases folder. Since the container is restarting
on its own, you should be able to remove it, and then wait, and it will start cleanly.
As an alternative, you can stop and rebuild the container, changing the ``WEB2PY_MIGRATE``
variable to be Fake in ``entrypoint.sh`` and try again:

.. code-block:: bash

    export WEB2PY_MIGRATE=Fake


You would rebuild the container like this:

.. code-block:: bash

    docker build -t runestone/server .


For now, it's recommended to remove the folder. Hopefully we will
develop a cleaner solution to handle migrations.


Testing the Entrypoint
**********************************

If you want to test the [entrypoint.sh](entrypoint.sh) script, the easiest thing
to do is add a command to the docker-compose to disable it, and then run commands
interactively by shelling into the container. For example, add a command line like
this to the "runestone" container:

.. code-block::

    runestone:
      image: runestone/server
      command: tail -F peanutbutter
    ...


Bring up the containers and then shell inside. Once inside, you can then issue commands
to test the entrypoint - since the other containers were started
with docker-compose everything in them is ready to go.

Restarting uwsgi/web2py
**********************************

Controllers are reloaded automatically every time they are used. However if you are making
changes to code in the ``modules`` folder you will need to restart web2py or else it is likely
that a cached version of that code will be used. You can restart web2py easily by first
shelling into the container and then running the command ``touch /srv/web2py/reload_server``

File Permissions
**********************************

File permissions can seem a little strange when you start this container on Linux. Primarily because both
nginx and uwsgi run as the ``www-data`` user. So you will suddenly find your files under RunestoneServer
owned by ``www-data`` . The container's entrypoint script updates permissions to allow both you and the
container enough privileges to do your work.

Writing Your Own Book
**********************************

If you are writing your own book you will want to get that book set up properly in the runestone
system. You need to do the following:

1. Run the command ``dmanage addcourse`` Use the project name you configured in ``pavement.py`` as
the name of BOTH the course and the basecourse when it asks. The dmanage command is in the scripts
folder of RunestoneServer.

2. Now that your course is registered rebuild it using the ``dbuild`` command found in the
RunestoneServer ``scripts`` folder use the command ``dbuild bookname``

3. If this book is a PreTeXt book you will need to navigate to the directory that contains the
``runestone-manifest.xml`` file and run the command:

.. code-block:: bash
    
    runestone process-manifest --course <yourcourse> --manifest runestone-manifest.xml

.. note:: 
    
    If you are missing ``runestone-manifest.xml`` then you need to rebuild your PreTeXt
    book with ``runestone`` as the publisher. See the PreTeXt docs for how do do this.

4. If this book is a PreTeXt book you should put run ``touch NOBUILD`` in the root directory for
this book. Otherwise when the container restarts it will try to build this book using runestone
build and it will fail, causing an endless cycle of container restarts.
