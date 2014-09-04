# -*- coding: utf-8 -*-

import sys, os

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('../modules'))

# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.mathjax',
              'luther.sphinx.video',
              'luther.sphinx.reveal',
              'luther.sphinx.poll',
              'luther.sphinx.tabbedStuff',
              'luther.sphinx.disqus',
              'luther.sphinx.codelens',
              'luther.sphinx.activecode',
              'luther.sphinx.assess',
              'luther.sphinx.animation',
              'luther.sphinx.meta',
              'gatech.parsons']


# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'<ENTER YOUR PROJECT NAME HERE>' # e.g. How To Think Like a Computer Scientist
copyright = u'<ENTER YOUR COPYRIGHT NOTICE HERE>' # e.g. "2013, Brad Miller and David Ranum"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['ActiveIndexFiles/*']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the Sphinx documentation
# for a list of builtin themes.
html_theme = 'sphinx_bootstrap'

# Theme options are theme-specific and customize the look and feel of a theme
html_theme_options = {
    # Navigation bar title. (Default: ``project`` value)
    'navbar_title': "<INSERT YOUR PROJECT NAME OR OTHER TITLE HERE>",

    # Tab name for entire site. (Default: "Site")
    'navbar_site_name': "Chapters",

    # Global TOC depth for "site" navbar tab. (Default: 1)
    # Switching to -1 shows all levels.
    'globaltoc_depth': 1,

    # Include hidden TOCs in Site navbar?
    #
    # Note: If this is "false", you cannot have mixed ``:hidden:`` and
    # non-hidden ``toctree`` directives in the same page, or else the build
    # will break.
    #
    # Values: "true" (default) or "false"
    'globaltoc_includehidden': "true",

    # HTML navbar class (Default: "navbar") to attach to <div> element.
    # For dark navbar, do "navbar navbar-inverse"
    'navbar_class': "navbar",

    # Fix navigation bar to top of page?
    # Values: "true" (default) or "false"
    'navbar_fixed_top': "true",

    # Location of link to source.
    # Options are "nav" (default), "footer" or anything else to exclude.
    'source_link_position': "nav",
}

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = ["_templates/plugin_layouts"]

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = '<INSERT YOUR PROJECT NAME HERE>'

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title ='<INSERT YOUR PROJECT NAME OR OTHER SHORT TITLE HERE>'

# Logo is currently included as CSS background in default layout file. If you remove
# it there, you should specify an alternative image here.
#html_logo = "../source/_static/logo_small.png"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".

module_paths = [x.replace('.','/') for x in extensions]
module_static_js = ['../modules/%s/js' % x for x in module_paths if os.path.exists('../modules/%s/js' % x)]
module_static_css = ['../modules/%s/css' % x for x in module_paths if os.path.exists('../modules/%s/css' % x)]

html_static_path = ['_static',
                    '../common/js',
                    '../common/css',
                    '../common/bootstrap',
                    '../common/images'] + module_static_js + module_static_css

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = True

# Output file base name for HTML help builder.
htmlhelp_basename = 'PythonCoursewareProjectdoc'
