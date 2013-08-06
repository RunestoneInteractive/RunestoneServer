Introduction
------------

This folder contains the structure and files you need to create your own custom book using the
Runestone Interactive toolset.


Getting Started
---------------

The simplest project only needs two files: conf.py and index.rst.

A sample conf.py has been provided in this folder. You can (and should) customize it with things
like your project's title, any copyright information, etc. (However, you don't absolutely *have*
to change anything - the defaults in it will at least produce working HTML.)

If your project will not have more than one single page, then you do not need anything more than
an index.rst file. You can customize any content in index.rst, as long as it follows valid
reStructuredText syntax. You can also use directives that have been created as part of the
Runestone Interactive tool set (including ActiveCode, CodeLens, self-check questions, etc).

If you have a more complicated project, with multiple pages, there are instructions in the
index.rst file included in this folder that explain how to structure the file so that HTML
pages and a useful Table Of Contents are generated from your rST source files.


Building Your Book
------------------

Assuming you followed the instructions in the README.md file in the root of the Runestone
git repository, you should have all the dependencies to build your book installed.

At a command line in this directory, run:

$> sphinx-build -b html . <outdir>

<outdir> is the path to the directory that you want the built HTML files to be placed. If you
are serving this book using a web server, you would want to use the directory your web server
expects to find files in as the <outdir>.

The . (period) means that sphinx-build should look for your conf.py and source rST files in
the current directory.