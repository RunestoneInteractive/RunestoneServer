# 'Make' support for Online Python Tutor
#
# Copyright (C) 2013 Peter Robinson (pjr@itee.uq.edu.au)
#
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
This program is a 'make' program for embedding traces in web pages.

The process is driven by a .json file (the 'Makefile')

Assuming the file viz_makefile.json is in the cwd which will typically
be where the web pages and python code to be visualized reside, 
and $OPT is the path to the installation of OPT 
(including make_visualizations.py) then

python $OPT/make_visualizations.py viz_makefile.json

will generate all the .js traces and update the web pages as specified
in viz_makefile.json.

python $OPT/make_visualizations.py viz_makefile.json eg1.html 

will do the same thing but only for the given page(s).

Here is an example of the 'Makefile' viz_makefile.json
----------------------------
{       
"visualizer_url": 
      "http://path_to_local_visualizer/visualize.html",


"default_viz_config": 
      {
        "embeddedMode": true, 
        "verticalStack": true
      },

"eg1.html":
      [
        # hash to end of line is a comment
        "js/t1.js",
        {
           "python_scripts/t1a.py": {}
           "python_scripts/t1b.py": {"embeddedMode": false}
        }
      ]
"eg2.html":
      [
        "js/t2.js",
        {
           # verticalStack is removed from the params below
           "python_scripts/t2.py": {"verticalStack": ""}
        }
      ]
}
----------------------------
For each .html file the first argument is the .js file where the traces will go
and the second argument is a dictionary whose keys are the python scripts
to be used to generate the traces.

If "visualizer_url" is not supplied it defaults to 
  "http://pythontutor.com/visualize.html"

If "default_viz_config" is not supplied it defaults to 
  {'heightChangeCallback': 'redrawAllVisualizerArrows', 
   'editCodeBaseURL': viz_url}

where viz_url is the value associated with the "visualizer_url" key.
Note: for this version heightChangeCallback is hard-wired to be 
redrawAllVisualizerArrows.

The dictionary associated with a python script overrides the 
"default_viz_config" dictionary.
In other words, if all visualizations behave the same way then the dictionary 
associated with a python script can be set to {} and so will end up being the 
(supplied) default.

"""

import subprocess
import os
import re
import json
from optparse import OptionParser

# The OPT program for generating traces
GEN_JSON = "generate_json_trace.py"

# The command used to generate traces {0} will be the full path to GEN_JSON
# !! WARNING !! python below might need to be modified to point at the 
# correct version
COMMAND = "python {0} --create_jsvar={1}Trace {2}"

# The possible keys for configuring the visualization and their types
# At the moment changing callbacks are not supported - 
# 'heightChangeCallback' is hard-wired in
VIZ_CONFIG_TYPES = {#'heightChangeCallback': unicode,
                    #'updateOutputCallback': unicode,
                    #'executeCodeWithRawInputFunc': unicode,
                    'embeddedMode': bool,
                    'startingInstruction': int,
                    'verticalStack': bool,
                    'jumpToEnd': bool,
                    'codeDivWidth': int,
                    'codeDivHeight': int,
                    'hideOutput' : bool,
                    'editCodeBaseURL' : unicode,
                    'allowEditAnnotations' : bool,
                    'disableHeapNesting' : bool,
                    'drawParentPointer' : bool,
                    'textualMemoryLabels' : bool,
                    'showOnlyOutputs' : bool,
                    }

CALLBACK_PATTERN_REPL = [
    (r'"heightChangeCallback"\s*:\s*"([^"]*)"', r'"heightChangeCallback":\1'),
    (r'"dateOutputCallback"\s*:\s*"([^"]*)"', r'"OutputCallback":\1'),
    (r'"executeCodeWithRawInputFunc"\s*:\s*"([^"]*)"', 
     r'"executeCodeWithRawInputFunc":\1')
    ]

#  visualize.html in OPT home              
DEFALUT_VIZ_URL = 'http://pythontutor.com/visualize.html'

# The global default visualization configuration
# Note: heightChangeCallback is hard-wired to be redrawAllVisualizerArrows
DEFAULT_VIZ_CONFIG = {'heightChangeCallback': 'redrawAllVisualizerArrows'}
            

# The string used to generate js code for ExecutionVisualizer
VIZ_VAR = \
"""var {0}Visualizer = 
   new ExecutionVisualizer('{0}Div', {0}Trace,
          {1});"""

# The following is used to inject the dependencies and other info
# into the web pages. If this info is already there then it will be replaced.
# If your file already has this info in but does not have the 
# PY_TUTOR_END footer then manually remove this info.
# This information is based on the example from 'http://pythontutor.com'
PY_TUTOR_START = '<!-- dependencies for pytutor.js -->'
PY_TUTOR_END = '<!-- end of dependencies for pytutor.js -->'
PY_TUTOR_DEPEND = PY_TUTOR_START + \
"""

<script type="text/javascript" src="js/d3.v2.min.js"></script>
<script type="text/javascript" src="js/jquery-1.8.2.min.js"></script>
<script type="text/javascript" src="js/jquery.simplemodal.js"></script> <!-- for questions -->
<script type="text/javascript" src="js/jquery.ba-bbq.min.js"></script> <!-- for handling back button and URL hashes -->
<script type="text/javascript" src="js/jquery.jsPlumb-1.3.10-all-min.js "></script> <!-- for rendering SVG connectors 
                                                                                         DO NOT UPGRADE ABOVE 1.3.10 OR ELSE BREAKAGE WILL OCCUR -->
<script type="text/javascript" src="js/jquery-ui-1.8.24.custom.min.js"></script> <!-- for sliders and other UI elements -->
<link type="text/css" href="css/ui-lightness/jquery-ui-1.8.24.custom.css" rel="stylesheet" />
<link type="text/css" href="css/basic.css" rel="stylesheet" />

<!-- Python Tutor frontend code and styles -->
<script type="text/javascript" src="js/pytutor.js"></script>
<link rel="stylesheet" href="css/pytutor.css"/>

<!-- Visualize Script -->
<script type="text/javascript" src="{0}"></script>

<!-- Cut and paste the following lines to the place where the visualizations are to be inserted

{1}
-->

""" + PY_TUTOR_END

# A regular expression used to remove the old info
PY_TUTOR_RE = PY_TUTOR_START + '.*' + PY_TUTOR_END

# Used to inject a comment along with the dependency information so that
# you can cut and paste into the appropriate place in to the page body
DIV_TEXT = '<div id="{0}Div"></div>'

# The ready function to go at the end ot the generated .js file
DOCUMENT_READY_TEXT = \
"""
$(document).ready(function() {{

{0}

    function redrawAllVisualizerArrows() {{
        {1}
    }}
$(window).resize(redrawAllVisualizerArrows);
}});
"""

REDRAW_CONNECTORS_TEXT = "if ({0}Visualizer) {0}Visualizer.redrawConnectors();"

COMMENT_RE = r'#.*$'

def check_viz_config(parent, config):
    """Check that config is a valid visualization configuration"""
    isOK = True
    if type(config) != dict:
        print "In {0}, {1} is not a dictionary".format(parent,config)
        return False
    for key, value in config.iteritems():
        config_field_type = VIZ_CONFIG_TYPES.get(key)
        if config_field_type is None:
            print "Unknown visualizer key:", key
            isOK = False
        elif value != '' and type(value) != config_field_type:
            print "The visualizer configure entry {0}:{1} has the wrong type".format(key,value)
            isOK = False
    return isOK

def check_html_build(html, html_build_info):
    """Check that the build information for this html file is valid."""
    if len(html_build_info) != 2:
        print "The build list for {0} should have 2 entries".format(html)
        return False
    if type(html_build_info[0]) != unicode or \
            not html_build_info[0].endswith('.js'):
        print "The first argument of build list for {0} should be a .js file".format(html)
    if type(html_build_info[1]) != dict:
        print "The html build information must be a dictionary"
        return False
    
    isOK = True
    for key, value in html_build_info[1].iteritems():
        if type(key) != unicode or not key.endswith('.py'):
            print "The key {0} is not a .py file".format(key)
            isOK = False
        isOK = check_viz_config(html_build_info[1], value) and isOK
    return isOK

    
def check_build_info(build_info):
    """Check that the json info is a valid 'Makefile'"""
    isOK = True
    if type(build_info) != dict:
        print "The build information must be a dictionary"
        return False
    for key, value in build_info.iteritems():
        if key == 'default_viz_config':
            isOK = check_viz_config(build_info, value) and isOK
        elif key == 'visualizer_url':
            if type(value) != unicode:
                print 'The visualizer url must be a string'
                isOK = False
        elif key.endswith('.html'):
            isOK = check_html_build(key, value) and isOK
        else:
            print 'Unknown key:', key
            isOK = False
    return isOK

def update_dict(d, defaultd):
    """Update d with key,value pairs in defaultd if the key is not in d.
    If the value is the empty string then that entry is removed from 
    the dictionary"""
    for key, value in defaultd.iteritems():
        if key not in d:
            d[key] = value
        elif value == '':
            d.pop(key)

def get_build_info(json_file):
    """Return the build information in json_file. 
    Check if file is valid.
    """
    try:
        fp = open(json_file, 'rU')
        text = fp.read()
        fp.close()
        text = re.sub(COMMENT_RE, '', text, flags=re.M)
        build_info = json.loads(text)
    except Exception as e:
        print "Error in {0}:\n{1}".format(json_file, str(e))
        return None
    if not check_build_info(build_info):
        return None
    # if necessary add a value for "visualizer_url"
    if "visualizer_url" not in build_info:
        build_info["visualizer_url"] = DEFALUT_VIZ_URL
    # merge DEFAULT_VIZ_CONFIG with the supplied "default_viz_config"
    config = DEFAULT_VIZ_CONFIG
    config["editCodeBaseURL"] = build_info["visualizer_url"]
    config.update(build_info.get("default_viz_config", {}))
    build_info["default_viz_config"] = config
    # update all the 
    for key, value in build_info.iteritems():
        if key.endswith('.html'):
            for py_key, py_dict in value[1].iteritems():
                update_dict(py_dict, build_info.get("default_viz_config", {}))
    return build_info
                
                
def get_vizname_root(py_file):
    """Return the name to be used as the prefix for Trace, Visualizer etc"""
    return os.path.basename(py_file).replace('.', '_')                           
        


def run_command(gen_trace, py_file):
    """ Return the output of generate_json_trace.py on py_file"""
    command = COMMAND.format(gen_trace, get_vizname_root(py_file), py_file)
    return subprocess.check_output(command,bufsize=1,
                                   close_fds=True,
                                   shell=True)

def make_viz(build_info, html_files):
    """Build the visualizations specified in build_info and html_files"""
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    prog = os.path.join(dname, GEN_JSON)
    # if no html files are supplied 'make' all of them
    if not html_files:
        html_files = [h for h in build_info if h.endswith('.html')]

    for html in html_files:
        if html in build_info:
            make_html_viz(prog, html, build_info[html])
        else:
            print "{0} is not in the json file".format(html)

def get_viz_config(conf):
    """Get the configuration params for visualization."""
    text = json.dumps(conf)
    # The callbacks are strings in conf and need to be turned into
    # function relreences by removing the quotes
    for patt, repl in CALLBACK_PATTERN_REPL:
        text = re.sub(patt, repl, text)
    return text

def make_html_viz(prog, html_file, html_info):
    """'Make' the visualizations for html_file"""

    js_out, py_dict = html_info

    # all_traces is a string containing all the js trace datastructures
    # for all the supplied .py files for html_file
    try:
        all_traces = '\n'.join(run_command(prog, py) for py in py_dict)
    except Exception as e:
        print str(e)
        return
    
    # all_viz is the string containing the js code for creating the
    # required instances of ExecutionVisualizer for all the .py files
    # the root of the .py file is used as the root names in ExecutionVisualizer
    all_viz = '\n'.join(VIZ_VAR.format(get_vizname_root(py), 
                                       get_viz_config(pyd)) \
                            for py,pyd in py_dict.iteritems())

    all_redraws = '        \n'.join(REDRAW_CONNECTORS_TEXT.format(get_vizname_root(py)) for py, pyd in py_dict.iteritems() if 'redrawAllVisualizerArrows' in pyd.values())
    
    ready_function = DOCUMENT_READY_TEXT.format(all_viz, all_redraws)

    # all_js is the string of all the require js code
    all_js = all_traces + '\n' + ready_function + '\n'

    fd = open(js_out, 'w')
    fd.write(all_js)
    fd.close()

    # Update html_file
    try:
        fd = open(html_file, 'rU')
        html_text = fd.read()
        fd.close()
    except Exception as e:
        print str(e)
        return
    # strip out the old OPT dependency info
    html_text = re.sub(PY_TUTOR_RE, '', html_text, flags=re.M | re.S)
    end_head_pos = html_text.find('\n</head>')
    if end_head_pos == -1:
        print "Could not find '\n</head>' in {0}".format(html_file)
        return

    # all_divs is the string of all div entries to embed in the html
    # this is added to the header comments for easy cut and pasting
    # to the correct location in the document.
    all_divs = '\n'.join(DIV_TEXT.format(get_vizname_root(py)) for py in py_dict)
    # add the updated dependency info just before </head>
    html_text = html_text[:end_head_pos] +\
        PY_TUTOR_DEPEND.format(js_out, all_divs) + \
        html_text[end_head_pos:]
    fd = open(html_file, 'w')
    fd.write(html_text)
    fd.close()
    

def main(args):
    build_info = get_build_info(args[0])
    if build_info is None:
        print "Make aborted"
    else:
        make_viz(build_info, args[1:])


if __name__ == '__main__': 
    usage = "usage: %prog json_file [py_files]"
    parser = OptionParser(usage = usage)
    options,args = parser.parse_args()
    if len(args) == 0:
        print "Missing arguments - try python make_visualizations.py -h"
    else:
        main(args)
