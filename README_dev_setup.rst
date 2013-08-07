Creating Your Own Interactive Book
==================================

You can use the Runestone Interactive tools to create your own interactive textbook.


Getting Started
---------------

First, make sure you've followed all the directions in the README to get the Runestone Tools and
web2py up and running on your development machine.

In the root of the ``runestone/`` directory, you will find a folder called ``newproject_copy_me/``.

This folder contains the basic structure and templates you need to create your own course.

You should make a copy of this folder and give it a short (and unique) name.


Project Structure
-----------------

``conf.py``
~~~~~~~~~~~

Inside ``newproject_copy_me`` you will find a file called ``conf.py``. The Runestone Tools use Sphinx
to take the textual source of your textbook and generate HTML that can be displayed in the browser.
This ``conf.py`` file will be the main Sphinx configuration file for your textbook.

You can use the ``conf.py`` file without modification, but you will almost certainly want to customize
it with your own title, author name, copyright notice, etc. Most of the configuration parameters that
you will want to change are in angle brackets with all-caps placeholder text. (E.g. <YOUR TITLE HERE>).

``index.rst``
~~~~~~~~~~~~~

``index.rst`` is the only source file that is required. You can write any amount of reStructuredText
content within this file.

If you are creating a project that will have more than one page, however, ``index.rst`` is where you will
specify what other content source files are included as well as in what order the material appears.

``_templates/``
~~~~~~~~~~~~~~

The templates directory contains the HTML templates that Sphinx uses to generate the HTML pages. This is
where you would change things like colors, fonts, page headers, etc.

Like ``conf.py``, you do not technically have to change anything in here. However, you will probably want
to make at least some customizations to the look and feel of your textbook.

The primary file that you would change to specify the layout of the generated project is
``_templates/sphinx_bootstrap/layout.html``.