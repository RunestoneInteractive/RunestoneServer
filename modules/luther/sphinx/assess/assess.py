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
from assessbase import Assessment
from multiplechoice import *
from textfield import *
from blankfill import *
import json
import random

def setup(app):
    app.add_directive('mchoicemf',MChoiceMF)
    app.add_directive('mchoicema',MChoiceMA)
    app.add_directive('fillintheblank',FillInTheBlank)
    app.add_directive('mcmfrandom',MChoiceRandomMF)
    app.add_directive('addbutton',AddButton)
    app.add_directive('qnum',QuestionNumber)    
    app.add_role('textfield',textfield_role)


    app.add_javascript('assess.js')

    app.add_node(MChoiceNode, html=(visit_mc_node, depart_mc_node))
    app.add_node(FITBNode, html=(visit_fitb_node, depart_fitb_node))    

class AddButton(Directive):
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True
    has_content = True
    
    def run(self):
        """
            :param self:
            :return:
            .. addbutton:: bname
            
            ...
            """
        
        TEMPLATE_START = '''
            <div id="%(divid)s" class="alert alert-warning">
            <form name="%(divid)s_form" method="get" action="" onsubmit="return false;">
            '''
        
        TEMPLATE_END = '''
            <button class='btn btn-inverse' name="reset" onclick="resetPage('%(divid)s')">Forget My Answers</button>
            </form>
            </div>
            '''   
        
        self.options['divid'] = self.arguments[0]
        
        res = ""
        res = TEMPLATE_START % self.options
        
        res += TEMPLATE_END % self.options
        return [nodes.raw('',res , format='html')]


class QuestionNumber(Directive):
    """Set Parameters for Question Numbering"""
    required_arguments = 0
    optional_arguments = 3
    has_content = False
    option_spec = { 'prefix': directives.unchanged,
        'suffix': directives.unchanged,
        'start': directives.positive_int
    }

    def run(self):
        env = self.state.document.settings.env

        if 'start' in self.options:
            env.assesscounter = self.options['start'] - 1

        if 'prefix' in self.options:
            env.assessprefix = self.options['prefix']

        if 'suffix' in self.options:
            env.assesssuffix = self.options['suffix']

        return []






#####################





