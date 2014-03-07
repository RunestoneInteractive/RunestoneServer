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

    app.add_javascript('blockly_compressed.js' )
    app.add_javascript('blocks_compressed.js' )
    app.add_javascript('javascript_compressed.js' )    
    app.add_javascript('python_compressed.js' )        
    app.add_javascript('msg/js/en.js')

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
<p>
    <button onclick="showCode()">Show Code</button>
    <button onclick="runCode()">Run</button>
</p>
<div id="%(divid)s" style="height: 480px; width: 600px;"></div>
'''

CTRL_START = '''<xml id="toolbox" style="display: none">'''
CTRL_END = '''</xml>'''

END = '''
<script>
    Blockly.inject(document.getElementById('%(divid)s'),
        {path: '/runestone/static/_static', toolbox: document.getElementById('toolbox')});

    function showCode() {
      // Generate JavaScript code and display it.
      Blockly.JavaScript.INFINITE_LOOP_TRAP = null;
      var code = Blockly.JavaScript.workspaceToCode();
      alert(code);
    }

    function runCode() {
      // Generate JavaScript code and run it.
      window.LoopTrap = 1000;
      Blockly.JavaScript.INFINITE_LOOP_TRAP = 'if (--window.LoopTrap == 0) throw "Infinite loop.";\\n';
      var code = Blockly.JavaScript.workspaceToCode();
      Blockly.JavaScript.INFINITE_LOOP_TRAP = null;
      try {
        eval(code);
      } catch (e) {
        alert(e);
      }
    }

  </script>
  
'''
# self for these functions is an instance of the writer class.  For example
# in html, self is sphinx.writers.html.SmartyPantsHTMLTranslator
# The node that is passed as a parameter is an instance of our node class.
def visit_block_node(self,node):
    res = START % (node.ac_components)
    res += CTRL_START
    for ctrl in node.ac_components['controls']:
        res += '<block type="%s"></block>\n' % (ctrl)
    res += CTRL_END
    res += END % (node.ac_components)
    self.body.append(res)

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

        self.options['divid'] = self.arguments[0]

        if self.content:
            self.options['controls'] = self.content
        
        return [BlocklyNode(self.options)]



