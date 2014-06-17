# Copyright (C) 2011  Bradley N. Miller
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

__author__ = 'bmiller'

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive
import json
import os

# try:
#     import conf
#     version = conf.version
#     staticserver = conf.staticserver
# except:
#     version = '2.1.0'
#     staticserver = 'runestonestatic.appspot.com'

def setup(app):
    app.add_directive('blockly',Blockly)



    app.add_node(BlocklyNode, html=(visit_block_node, depart_block_node))

    app.connect('doctree-resolved',process_activcode_nodes)
    app.connect('env-purge-doc', purge_activecodes)





#'
class BlocklyNode(nodes.General, nodes.Element):
    def __init__(self,content):
        """

        Arguments:
        - `self`:
        - `content`:
        """
        super(BlocklyNode,self).__init__()
        self.ac_components = content


START = '''
<html>
<head>
    <script src='blockly_compressed.js' type="text/javascript"> </script>
    <script src='blocks_compressed.js' type="text/javascript"> </script>
    <script src='javascript_compressed.js' type="text/javascript"> </script>
    <script src='python_compressed.js' type="text/javascript"> </script>
    <script src='msg/js/en.js' type="text/javascript"> </script>
    <link rel="stylesheet" href="bootstrap-3.0.0/css/bootstrap.min.css" type="text/css" />
    <link rel="stylesheet" href="video.css" type="text/css" />
    <script type="text/javascript">
    // Get the objects we need to do logging from the parent frame.
    // This seems better than reloading all of jQuery and bookfuncs into the frame. But
    // Makes this a bit more dependent on the Runestone Environment.
    eBookConfig = parent.eBookConfig
    logBookEvent = parent.logBookEvent
    jQuery = parent.jQuery
    </script>
    <style>
      html, body {
        background-color: #fff;
        margin: 0;
        padding: 0;
      }
      .blocklySvg {
        height: 100%%;
        width: 100%%;
      }
      .active_out {
        margin-top: 5px;
        margin-left: 10px;
        margin-right: 5px;
      }
    </style>
</head>
<body>
<p>
    <button class="btn btn-default" onclick="showCode()">Show Python</button>
    <button class="btn btn-success" onclick="runCode()">Run</button>
</p>
<div id="%(divid)s" style="height: 480px; width: 600px;"></div>
'''

CTRL_START = '''<xml id="toolbox" style="display: none">'''
CTRL_END = '''</xml>'''


END = '''
<script>
    Blockly.inject(document.getElementById('%(divid)s'),
        {path: './', toolbox: document.getElementById('toolbox')});

    function showCode() {
      // Generate JavaScript code and display it.
      Blockly.Python.INFINITE_LOOP_TRAP = null;
      var code = Blockly.Python.workspaceToCode();
      alert(code);
    }

    function runCode() {
      // Generate JavaScript code and run it.
      window.LoopTrap = 1000;
      Blockly.JavaScript.INFINITE_LOOP_TRAP = 'if (--window.LoopTrap == 0) throw "Infinite loop.";\\n';
      var code = Blockly.JavaScript.workspaceToCode();
      Blockly.JavaScript.INFINITE_LOOP_TRAP = null;
      if(logBookEvent) {
          logBookEvent({'event': 'blockly', 'act': 'run', 'div_id': '%(divid)s'});
      } else {
          console.log('logBookEvent is not defined.  This should be defined in the parent frame')
      }
      try {
        eval(code);
      } catch (e) {
        alert(e);
      }
    }

    Blockly.JavaScript['text_print'] = function(block) { 
      // Print statement override. 
      var argument0 = Blockly.JavaScript.valueToCode(block, 'TEXT', 
          Blockly.JavaScript.ORDER_NONE) || '\\'\\''; 
      return 'my_custom_print(' + argument0 + ', "%(divid)s" );\\n'; 
    }; 

    function my_custom_print(text,divid) { 
      var p = document.getElementById(divid+"_pre");
      p.innerHTML += text + "\\n"
      }

    var xmlText = '%(preload)s';
    var xmlDom = Blockly.Xml.textToDom(xmlText);
    Blockly.Xml.domToWorkspace(Blockly.mainWorkspace, xmlDom);

  </script>
  
  <pre class="active_out" id="%(divid)s_pre"></pre>
  </body>
  </html>
'''
# self for these functions is an instance of the writer class.  For example
# in html, self is sphinx.writers.html.SmartyPantsHTMLTranslator
# The node that is passed as a parameter is an instance of our node class.
def visit_block_node(self,node):
    res = START % (node.ac_components)
    res += CTRL_START
    for ctrl in node.ac_components['controls']:
        if ctrl == 'variables':
            res += '<category name="Variables" custom="VARIABLE"></category>'
        elif ctrl == '':
            pass
        elif ctrl[0] == '*':
            res += '<category name="%s">' % (ctrl[2:])
        elif ctrl == '====':
            res += '</category>'
        else:
            res += '<block type="%s"></block>\n' % (ctrl)
    res += CTRL_END
    res += END % (node.ac_components)
    path = os.path.join(node.ac_components['blocklyHomePrefix'],'_static',node.ac_components['divid']+'.html')
    final = '<iframe class="blk-iframe" seamless src="%s" width="600" ' \
            'height="600"></iframe>' % path
    f = open(path, 'w')
    f.write(res)
    f.close()
    self.body.append(final)

def depart_block_node(self,node):
    ''' This is called at the start of processing an activecode node.  If activecode had recursive nodes
        etc and did not want to do all of the processing in visit_ac_node any finishing touches could be
        added here.
    '''
    pass


def process_activcode_nodes(app,env,docname):
    pass


def purge_activecodes(app,env,docname):
    pass


class Blockly(Directive):
    required_arguments = 1
    optional_arguments = 0
    has_content = True
    option_spec = {}

    def run(self):

        document = self.state.document
        rel_filename, filename = document.settings.env.relfn2path(self.arguments[0])
        self.options['divid'] = self.arguments[0]

        pathDepth = rel_filename.count("/")
        self.options['blocklyHomePrefix'] = "../"*pathDepth
        
        plstart = len(self.content)
        if 'preload::' in self.content:
            plstart = self.content.index('preload::')
            self.options['preload'] = " ".join(self.content[plstart+1:])

        if self.content:
            self.options['controls'] = self.content[:plstart]
        
        return [BlocklyNode(self.options)]




'''
    Blockly.JavaScript['text_print'] = function(block) { 
      // Print statement override. 
      var argument0 = Blockly.JavaScript.valueToCode(block, 'TEXT', 
          Blockly.JavaScript.ORDER_NONE) || '\'\''; 
      return 'my_custom_print(' + argument0 + ');\n'; 
    }; 

    function my_custom_print(text) { 
      var p = document.getElementById("blockly1_pre");
      p.innerHTML += text
      }

'''


# to preload blockly with a finished or partial program, do the following
# 
# https://blockly-demo.appspot.com/static/apps/code/index.html?lang=en
# 
# Now save the xml string.  And append something like the following to the script after blockly
# is created:
# 
#       var xmlText = '<xml>  <block type="variables_set" id="1" inline="true" x="25" y="9">    <field name="VAR">X</field>    <value name="VALUE">      <block type="math_number" id="2">        <field name="NUM">10</field>      </block>    </value>  </block></xml>'
#       xmlDom = Blockly.Xml.textToDom(xmlText);
#       Blockly.Xml.domToWorkspace(Blockly.mainWorkspace, xmlDom);
 



