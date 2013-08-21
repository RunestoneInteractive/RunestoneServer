# Copyright (C) 2013  Bradley N. Miller
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
from assessbase import *
import json
import random



class FITBNode(nodes.General, nodes.Element):
    def __init__(self,content):
        """

        Arguments:
        - `self`:
        - `content`:
        """
        super(FITBNode,self).__init__()
        self.fitb_options = content


def visit_fitb_node(self,node):
    res = node.template_start % node.fitb_options

    self.body.append(res)
        

def depart_fitb_node(self,node):
    fbl = []
    for k in sorted(node.fitb_options.keys()):
        if 'feedback' in k:
            pair = eval(node.fitb_options[k])
            p1 = escapejs(pair[1])
            newpair = (pair[0],p1)
            fbl.append(newpair)
    
    if 'casei' in node.fitb_options:
        node.fitb_options['casei'] = 'true'
    else:
        node.fitb_options['casei'] = 'false'
    node.fitb_options['fbl'] = json.dumps(fbl).replace('"',"'")
    res = ""
    
    res += node.template_end % node.fitb_options

    self.body.append(res)


class FillInTheBlank(Assessment):
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True
    has_content = True
    option_spec = {'correct':directives.unchanged,
        'feedback':directives.unchanged,
        'feedback1':directives.unchanged,
        'feedback2':directives.unchanged,
        'feedback3':directives.unchanged,                   
        'feedback4':directives.unchanged,  
        'blankid':directives.unchanged,
        'iscode':directives.flag,
        'casei':directives.flag  # case insensitive matching
    }
    
    def run(self):
        """
            process the fillintheblank directive and generate html for output.
            :param self:
            :return:
            .. fillintheblank:: qname
            :iscode: boolean
            :correct: somestring
            :feedback: -- displayed if wrong
            :feedback: ('.*', 'this is the message')
            Question text
            ...
            """
        
        TEMPLATE_START = '''
            <div id="%(divid)s" class="alert alert-warning">
            '''
        
        TEMPLATE_END = '''
            <script>
            $(document).ready(function(){checkPreviousFIB('%(divid)s');});
            </script>
            <button class='btn btn-success' name="do answer" onclick="checkFIBStorage('%(divid)s', '%(blankid)s', '%(correct)s',%(fbl)s, %(casei)s)">Check Me</button>
            <button class='btn btn-default' id="%(divid)s_bcomp" disabled name="compare" onclick="compareFITBAnswers('%(divid)s');">Compare Me</button>
            <br />
            <br />
            <div id="%(divid)s_feedback">
            </div>
            </div>
            '''   

        super(FillInTheBlank,self).run()

        fitbNode = FITBNode(self.options)
        fitbNode.template_start = TEMPLATE_START
        fitbNode.template_end = TEMPLATE_END

        self.state.nested_parse(self.content, self.content_offset, fitbNode)

        return [fitbNode]


