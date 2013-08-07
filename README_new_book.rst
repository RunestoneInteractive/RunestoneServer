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

``index.rst`` contains information on how to structure the file and include other sources.


``pavement.py``
~~~~~~~~~~~~~~~

This file is used by the Paver build tool to configure the Sphinx build. The only thing you need to change
in this file is the parameter ``project_name``. Set this equal to your <project_name>.


``_templates/``
~~~~~~~~~~~~~~

The templates directory contains the HTML templates that Sphinx uses to generate the HTML pages. This is
where you would change things like colors, fonts, page headers, etc.

Like ``conf.py``, you do not technically have to change anything in here. However, you will probably want
to make at least some customizations to the look and feel of your textbook.

The primary file that you would change to specify the layout of the generated project is
``_templates/sphinx_bootstrap/layout.html``.


``_static/``

This directory is not created automatically. However, if your textbook will contain static resources like images
or other external files, this is where the default configuration will expect such resources to be. If you need
external resources, you should create this directory yourself.


Building Your Project
---------------------

Once you have customized ``conf.py`` to your liking, added your content and any other rST sources to
``index.rst``, and set your course name in ``pavement.py``, you can build your book for the first time.

At a command line in your project directory, run this command:

``$ paver build``

This tells Sphinx to make the HTML files. This will cause the generated HTML to be placed in
``runestone/static/<project_name>``.

Note: If you have not created the ``_static`` directory, the above command will cause a warning that that
directory does not exist. If you aren't using any of your own static resources, you can safely ignore this.


Making It Interactive
---------------------

After building your book, the files generated will reside in ``runestone/static/<project_name>``. If you want,
you can simply open the ``index.html`` file within that directory and start using your course immediately.

ActiveCode blocks, CodeLens visualizers, and many other Runestone Tools will still function in this static,
offline mode. However, if you would like to utilize the full interactive experience, including allowing your
students save and load their work, setting assignments, and getting feedback as to how your students are doing,
you will have to configure web2py to serve your book.

Assuming you followed the original setup instructions, you should already have a web2py user account and be a
member of the instructors group. (If now, do so now!)

1. Start web2py and browse to http://127.0.0.1:8000/runestone/appadmin. Supply the administrative password
you set when you started web2py.

2. Now add your course to the ``courses`` database table. Click the ``[insert new courses]`` link. Enter
<project_name> in the course_name field, and choose a start date for the course (in the format YYYY-MM-DD).
Go back to http://127.0.0.1:8000/runestone/appadmin and click ``db.courses``. Note the Id number of your newly
generated course (under the ``course.id`` column). We will need the ID in the next step.

3. Now you need to set your web2py account to be the instructor for your new course. Go back to
http://127.0.0.1:8000/runestone/appadmin and click the ``[insert new course_instructor]`` link. Type the ID number
you obtained in the previous step into the ``Course`` field, and choose your your web2py username from the
"Instructor" dropdown. Click submit.


Use Your Textbook
-----------------

With web2py running, you can find your new interactive textbook at:
``http://127.0.0.1/runestone/static/<project_name>/index.html.``

There is one option step you may want to perform: to ensure that you web2py redirects you correctly every time,
you may want to enrol your user account in your newly created course. This is slightly different than making your
account an instructor. The enroled course set for your user account determines where web2py redirects you when you
log in.

To enrol yourself, log in to web2py, then go to http://127.0.0.1:8000/runestone/default/user/profile. Enter the
name of your newly created course (<project_name>) into the ``Course Name`` field, and click "Save Profile". You
should be redirected immediately to your course.
