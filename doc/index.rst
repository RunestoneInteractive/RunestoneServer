************************************************
Developer documentation for the Runestone server
************************************************
This is the beginning of developer documentation for the Runestone server. To build these documents:

#.  Open a terminal or command prompt and change to the root of this repository.
#.  Execute ``python -m pip install -U -r requirements-dev.txt``. This only needs to be done once.
#.  Execute ``sphinx-build -d _build\doctrees -c doc . _build``.

There's a lot of work left to do. In particular:

-   All comments are interpreted as ReST, per the `CodeChat docs <https://codechat.readthedocs.io/en/master/docs/style_guide.cpp.html>`_. **Read this first!** All the style suggestions should be following when documenting this project.
-   Every source file should start with a title, typically like this:

    .. code-block:: Python

        # ***********************************************
        # |docname| - A one-line description of this file
        # ***********************************************

    As an example, see `/controllers/books.py`.

-   After this, all existing errors and warnings produced by running Sphinx should be fixed.


Architecture
============
.. image:: RunestoneArch.svg


web2py server
=============
.. toctree::
    :maxdepth: 2

    /models/toctree.rst
    /controllers/toctree.rst
    /views/__init__.py
    /modules/__init__.py
    /static/toctree
    /rsmanage/toctree
    /build/toctree


Tests and CI
============
.. toctree::
    :maxdepth: 2

    /.travis.yml
    /.coveralls.yml
    /tests/__init__.py


Containers
==========
.. toctree::

    /docker/README
    /Dockerfile
    /docker-compose.yml
    /docker/entrypoint.sh
    /docker/wsgihandler.py
    /docker/uwsgi/sites/runestone.ini


Other files
===========
.. toctree::
    :maxdepth: 2
    :glob:

    /README
    /CONTRIBUTING
    /ChangeLog
    /scripts/toctree
    /__init__.py
    /.prettierrc.js
    conf.py

Indices and tables
------------------
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
