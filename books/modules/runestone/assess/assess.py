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
    app.add_directive('timedmchoicemf',timedMChoiceMF)
    app.add_directive('starttimer',StartTimer)
    app.add_directive('finishtimer',FinishTimer)	
    app.add_directive('fillintheblank',FillInTheBlank)
    app.add_directive('mcmfrandom',MChoiceRandomMF)
    app.add_directive('addbutton',AddButton)
    app.add_directive('qnum',QuestionNumber)
    app.add_directive('revealquestions',RevealQuestions)	    
    app.add_role('textfield',textfield_role)


    app.add_javascript('assess.js')

    app.add_node(MChoiceNode, html=(visit_mc_node, depart_mc_node))
    app.add_node(FITBNode, html=(visit_fitb_node, depart_fitb_node))
    app.add_node(RevealQNode, html=(visit_reveal_qnode, depart_reveal_qnode))    

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

class StartTimer(Directive):
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True
    has_content = True
    option_spec = {"duration":directives.unchanged}
    
    def run(self):
        """
            :param self:
            :return:
            .. addbutton:: bname
            
            ...
            """
        
        if not 'duration' in self.options:
		TEMPLATE_START = '''

		    	


		    
		    <p id="output"></p>
		    <div id="controls">
			<button class='btn btn-inverse' id ="start" onclick="start(30)">Start</button>
			<button class='btn btn-inverse' id ="pause" onclick="pause()">Pause</button>
			

		    '''
	if 'duration' in self.options:
		TEMPLATE_START = '''

		    	


		    <div id="startWrapper">
		    <p id="output"></p>
		    </div>
		    <div id="controls" style="text-align: center;">
			<button class='btn btn-inverse' id ="start" onclick="start()">Start</button>
			<button class='btn btn-inverse' id ="pause" onclick="pause()">Pause</button>
			
		    '''
        
        TEMPLATE_END = '''
	            <script>
			var time = %(duration)s * 60;
		    showTime(%(duration)s * 60);
            </script>

            </div>
		



            '''   
        
        self.options['divid'] = self.arguments[0]
        
        res = ""
        res = TEMPLATE_START % self.options
        
        res += TEMPLATE_END % self.options
        return [nodes.raw('',res , format='html')]

################################################################################################

class FinishTimer(Directive):
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

            '''
        
        TEMPLATE_END = '''
	
	<div style="text-align: center;">
	<button class='btn btn-inverse' id ="finish" onclick="checkTimedMCMFStorage()">Submit Answers</button>
	</div>
	<p id="results"></p>
	<script>
	    $(document).ready(function() {checkIfFinished()});
	</script>


            '''   
        
        self.options['divid'] = self.arguments[0]
        
        res = ""
        res = TEMPLATE_START % self.options
        
        res += TEMPLATE_END % self.options
        return [nodes.raw('',res , format='html')]

#########################################################################

BEGIN = """

    <div id='%(divid)s' style='display:none'>
"""
    #<button type='button' id='button_show' class='btn btn-default reveal_button' style='margin-bottom:10px;' onclick="">
     #  %(showtitle)s
    #</button>
    #<button type='button' id='button_hide' class='btn btn-default reveal_button' onclick="" style='display:none'>
	#%(hidetitle)s
    #</button>
END = """
    </div> <!-- end reveal -->
"""


class RevealQNode(nodes.General, nodes.Element):
    def __init__(self,content):
        super(RevealQNode,self).__init__()
        self.reveal_components = content


def visit_reveal_qnode(self, node):
    res = BEGIN % node.reveal_components

    self.body.append(res)

def depart_reveal_qnode(self,node):
    res = END % node.reveal_components

    self.body.append(res)



class RevealQuestions(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True
    option_spec = {"showtitle":directives.unchanged,
                   "hidetitle":directives.unchanged}

    def run(self):
        self.assert_has_content() # an empty reveal block isn't very useful...

        if not 'showtitle' in self.options:
            self.options['showtitle'] = "Timed Quiz Paused/Not Started"
        if not 'hidetitle' in self.options:
            self.options['hidetitle'] = "Currently Taking Timed Quiz"

        self.options['divid'] = self.arguments[0]

        reveal_node = RevealQNode(self.options)

        self.state.nested_parse(self.content, self.content_offset, reveal_node)

        return [reveal_node]


