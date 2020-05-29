Runestone System Architecture
=============================

.. raw:: html

    <object data="RunestoneArch.svg" type="image/svg+xml"></object>


An author creates a runestone book by editing some restructuredText files.
The ``runestone build`` process creates a set of output files formatted as
html.  The html files can be viewed directly in the browser (when ``dynamic_pages == False``).  In this mode runestone produces a static site.
or served through the :ref:`Runestone Server` (``dynamic_pages == True``).  when the content is served through the runestone server each page is an html template and some page content can be dynamically populated when the page is loaded.  The build process also relies on the :ref:`Trace Server` to provide data for CodeLens.


Runestone Server
----------------


Trace Server
------------

