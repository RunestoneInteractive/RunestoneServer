# Copyright (C) 2013  Bradley N. Miller, Barabara Ericson
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



class MChoiceNode(nodes.General, nodes.Element):
    def __init__(self,content):
        """

        Arguments:
        - `self`:
        - `content`:
        """
        super(MChoiceNode,self).__init__()
        self.mc_options = content


def visit_mc_node(self,node):
    res = ""
    res = node.template_start % node.mc_options

    self.body.append(res)


def depart_mc_node(self,node):
    res = node.template_form_start % node.mc_options
    feedbackStr = "["
    currFeedback = ""
    # Add all of the possible answers
    okeys = node.mc_options.keys()
    okeys.sort()
    for k in okeys:
        if 'answer_' in k:  
            x,label = k.split('_') 
            node.mc_options['alabel'] = label 
            node.mc_options['atext'] = node.mc_options[k]
            res += node.template_option % node.mc_options
            currFeedback = "feedback_" + label
            feedbackStr = feedbackStr + "'" + escapejs(node.mc_options[currFeedback]) + "', "
    
    # store the feedback array with key feedback minus last comma
    node.mc_options['feedback'] = feedbackStr[0:-2] + "]"

    res += node.template_end % node.mc_options

    self.body.append(res)




#####################
# multiple choice question with multiple feedback
# author - Barb Ericson
# author - Anusha 
class MChoiceMF(Assessment):
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True
    has_content = True
    option_spec = {'answer_a':directives.unchanged,
        'answer_b':directives.unchanged,    
        'answer_c':directives.unchanged,
        'answer_d':directives.unchanged,
        'answer_e':directives.unchanged,
        'correct':directives.unchanged,
        'feedback_a':directives.unchanged,
        'feedback_b':directives.unchanged,
        'feedback_c':directives.unchanged,
        'feedback_d':directives.unchanged,
        'feedback_e':directives.unchanged,
        'iscode':directives.flag
    }
    
    def run(self):
        """
            process the multiplechoice directive and generate html for output.
            :param self:
            :return:
            .. mcmfstorage:: qname
            :iscode: boolean
            :answer_a: possible answer  -- what follows _ is label
            :answer_b: possible answer
            ...  
            :answer_e: possible answer                      
            :correct: leter of correct answer
            :feedback_a: displayed if a is picked
            :feedback_b: displayed if b is picked
            :feedback_c: displayed if c is picked
            :feedback_d: displayed if d is picked
            :feedback_e: displayed if e is picked
            
            Question text
            ...
            """
        TEMPLATE_START = '''
            <div id="%(divid)s" class="alert alert-warning">
            '''
        
        OPTION = '''
            <input type="radio" name="group1" value="%(alabel)s" id="%(divid)s_opt_%(alabel)s" />
            <label for= "%(divid)s_opt_%(alabel)s">  %(alabel)s) %(atext)s</label><br />
            '''
        
        TEMPLATE_END = '''

            <script>
            $(document).ready(function(){checkRadio('%(divid)s');});
            </script>
            <button class='btn btn-success' name="do answer" onclick="checkMCMFStorage('%(divid)s','%(correct)s',%(feedback)s)">Check Me</button>
            <button class='btn btn-default' id="%(divid)s_bcomp" disabled name="compare" onclick="compareAnswers('%(divid)s');">Compare Me</button>
            </form><br />
            <div id="%(divid)s_feedback">
            </div>
            </div>
            '''   
        super(MChoiceMF,self).run()


        

        mcNode = MChoiceNode(self.options)
        mcNode.template_start = TEMPLATE_START
        mcNode.template_form_start = '''<form name="%(divid)s_form" method="get" action="" onsubmit="return false;">'''
        mcNode.template_option = OPTION
        mcNode.template_end = TEMPLATE_END

        self.state.nested_parse(self.content, self.content_offset, mcNode)

        return [mcNode]


#####################
# multiple choice question with multiple correct answers
# author - Barb Ericson

class MChoiceMA(Assessment):
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True
    has_content = True
    option_spec = {'answer_a':directives.unchanged,
        'answer_b':directives.unchanged,    
        'answer_c':directives.unchanged,
        'answer_d':directives.unchanged,
        'answer_e':directives.unchanged,
        'correct':directives.unchanged,
        'feedback_a':directives.unchanged,
        'feedback_b':directives.unchanged,
        'feedback_c':directives.unchanged,
        'feedback_d':directives.unchanged,
        'feedback_e':directives.unchanged,
            'iscode':directives.flag
    }
    
    def run(self):
        """
            process the multiplechoice directive and generate html for output.
            :param self:
            :return:
            .. mchoicemf:: qname
            :iscode: boolean
            :answer_a: possible answer  -- what follows _ is label
            :answer_b: possible answer
            ...  
            :answer_e: possible answer                      
            :correct: comma seperated list of correct values a, b, c
            :feedback_a: displayed if a is picked
            :feedback_b: displayed if b is picked
            :feedback_c: displayed if c is picked
            :feedback_d: displayed if d is picked
            :feedback_e: displayed if e is picked
            
            Question text
            ...
            """
        TEMPLATE_START = '''
            <div id="%(divid)s" class="alert alert-warning">
            '''
        
        OPTION = '''
            <input type="checkbox" name="group1" value="%(alabel)s" id="%(divid)s_opt_%(alabel)s" />
            <label for= "%(divid)s_opt_%(alabel)s">  %(alabel)s) %(atext)s</label><br />
            '''
        
        TEMPLATE_END = '''
            <script>
            $(document).ready(function(){checkMultipleSelect('%(divid)s');});
            </script>
            <button class='btn btn-success' name="do answer" onclick="checkMCMAStorage('%(divid)s','%(correct)s',%(feedback)s)">Check Me</button>
            <button class='btn btn-default' id="%(divid)s_bcomp" disabled name="compare" onclick="compareAnswers('%(divid)s');">Compare Me</button>
            </form><br />
            <div id="%(divid)s_feedback">
            </div>
            </div>
            '''   
        

        super(MChoiceMA,self).run()

        mcNode = MChoiceNode(self.options)
        mcNode.template_start = TEMPLATE_START
        mcNode.template_form_start = '''<form name="%(divid)s_form" method="get" action="" onsubmit="return false;">'''
        mcNode.template_option = OPTION
        mcNode.template_end = TEMPLATE_END

        self.state.nested_parse(self.content, self.content_offset, mcNode)

        return [mcNode]



################################


#####################
# display a multiple choice question with feedback that randomizes the answers
class MChoiceRandomMF(Assessment):
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True
    has_content = True
    option_spec = {'answer_a':directives.unchanged,
        'answer_b':directives.unchanged,    
        'answer_c':directives.unchanged,
        'answer_d':directives.unchanged,
        'answer_e':directives.unchanged,
        'correct':directives.unchanged,
        'feedback_a':directives.unchanged,
        'feedback_b':directives.unchanged,
        'feedback_c':directives.unchanged,
        'feedback_d':directives.unchanged,
        'feedback_e':directives.unchanged,
            'iscode':directives.flag
    }
    
    def run(self):
        """
            process the multiplechoice directive and generate html for output.
            :param self:
            :return:
            .. mcmfrandom:: qname
            :iscode: boolean
            :answer_a: possible answer  -- what follows _ is label
            :answer_b: possible answer
            ...  
            :answer_e: possible answer                      
            :correct: leter of correct answer
            :feedback_a: displayed if a is picked
            :feedback_b: displayed if b is picked
            :feedback_c: displayed if c is picked
            :feedback_d: displayed if d is picked
            :feedback_e: displayed if e is picked
            
            Question text
            ...
            """
        TEMPLATE_START = '''
            <div id="%(divid)s" class="alert alert-warning">
            <p>%(qnumber)s: %(bodytext)s</p>
            <form name="%(divid)s_form" method="get" action="" onsubmit="return true;">
            '''
        
        OPTION = '''
            <div id="%(divid)s_op%(opi)s"></div>
            '''
        
        TEMPLATE_END = '''      
            <div id="%(divid)s_bt"></div>
            
            </form>
            <div id="%(divid)s_feedback">
            </div>
            
            <script>
            $(document).ready(function(){createHTML_MCMFRandom("%(divid)s","%(a)s","%(f)s","%(corr)s");});
            </script>
            </div>
            '''   
        
        
        super(MChoiceRandomMF,self).run()

        res = ""
        res = TEMPLATE_START % self.options
        feedbackStr = "["
        currFeedback = ""
        # Add all of the possible answers
        okeys = self.options.keys()
        okeys.sort()
        
        
        answ=""
        feed=""
        ansArr=[]
        feedArray=[]
        for k in okeys:
            if 'answer_' in k:  
                ansArr.append(k)
        for f in ansArr:
            t,flabel=f.split("_")
            feedArray.append(flabel)
        
        i=0
        for k in okeys:
            if 'answer_' in k: 
                answ=answ+self.options[ansArr[i]]+"*separator*"
                feed=feed+self.options["feedback_"+feedArray[i]]+"*separator*"
                self.options['opi']=i+1
                res += OPTION % self.options
            i=i+1
        
        # Store the Answer and Feedback arrays
        self.options['a']=answ
        self.options['f']=feed

        op=self.options['correct']

        if(op=='a'):
            index=0
        elif(op=='b'):
            index=1
        elif(op=='c'):
            index=2
        elif(op=='d'):
            index=3
        elif(op=='e'):
            index=4
        self.options['corr']=self.options[ansArr[index]]
        
        res += TEMPLATE_END % self.options
        return [nodes.raw('',res , format='html')]