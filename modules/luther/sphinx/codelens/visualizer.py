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
from pg_logger import exec_script_str_local
import json

def setup(app):
    app.add_directive('codelens',Codelens)
    app.add_stylesheet('codelens/v3/css/pytutor.css')
    app.add_stylesheet('codelens/v3/css/basic.css')
    app.add_stylesheet('codelens/v3/css/ui-lightness/jquery-ui-1.8.24.custom.css')

    app.add_javascript('codelens/v3/js/jquery.simplemodal.js')
    app.add_javascript('codelens/v3/js/d3.v2.min.js')
    app.add_javascript('codelens/v3/js/jquery.ba-bbq.min.js')
    app.add_javascript('codelens/v3/js/jquery.jsPlumb-1.3.10-all-min.js')
    app.add_javascript('codelens/v3/js/jquery-ui-1.8.24.custom.min.js')
    app.add_javascript('codelens/v3/js/pytutor.js')



VIS = '''
<div id="%(divid)s"></div>
<p class="cl_caption"><span class="cl_caption_text">%(caption)s (%(divid)s)</span> </p>'''

QUESTION = '''
<div id="%(divid)s_modal" class="basic-modal-content">
    <h3>Check your understanding</h3>
    %(question)s
    <input id="%(divid)s_textbox" type="textbox" />
    <button id="%(divid)s_tracecheck" onclick="traceQCheckMe('%(divid)s_textbox','%(divid)s','%(correct)s')">Check
    Me</button>
    <button onclick="closeModal('%(divid)s')">Continue...</button>
    <p id="%(divid)s_feedbacktext" class="feedbacktext"></p>
</div>
'''

DATA = '''
<script type="text/javascript">
%(tracedata)s
var %(divid)s_vis;

$(document).ready(function() {
    %(divid)s_vis = new ExecutionVisualizer('%(divid)s',%(divid)s_trace,
                                {embeddedMode: %(embedded)s,
                                verticalStack: true,
                                heightChangeCallback: redrawAllVisualizerArrows,
                                codeDivWidth: 500
                                });
    attachLoggers(%(divid)s_vis,'%(divid)s');
    allVisualizers.push(%(divid)s_vis);
});

$(document).ready(function() {
    $("#%(divid)s_tracecheck").click(function() {
        logBookEvent({'event':'codelens', 'act': 'check', 'div_id':'%(divid)s'});
        });
});

if (allVisualizers === undefined) {
   var allVisualizers = [];
}


$(window).resize(function() {
    %(divid)s_vis.redrawConnectors();
});
</script>
'''


# Some documentation to help the author.
# Here's and example of a single stack frame.
# you might ask a qestion about the value of a global variable
# in which case the correct answer is expressed as:
#
# globals.a
#
# You could ask about a value on the heap
#
# heap.variable
#
# You could ask about a local variable -- not shown here.
#
# locals.variable
#
# You could even ask about what line is going to be executed next
#
# line
# {
#   "ordered_globals": [
#     "a",
#     "b"
#   ],
#   "stdout": "1\n",
#   "func_name": "<module>",
#   "stack_to_render": [],
#   "globals": {
#     "a": 1,
#     "b": 1
#   },
#   "heap": {},
#   "line": 5,
#   "event": "return"
# }


class Codelens(Directive):
    required_arguments = 1
    optional_arguments = 1
    option_spec = {
        'tracedata':directives.unchanged,
        'caption':directives.unchanged,
        'showoutput':directives.flag,
        'question':directives.unchanged,
        'correct':directives.unchanged,
        'feedback':directives.unchanged,
        'breakline':directives.nonnegative_int
    }

    has_content = True

    def run(self):

        self.JS_VARNAME = ""
        self.JS_VARVAL = ""

        def raw_dict(input_code, output_trace):
          ret = dict(code=input_code, trace=output_trace)
          return ret

        def js_var_finalizer(input_code, output_trace):
          global JS_VARNAME
          ret = dict(code=input_code, trace=output_trace)
          json_output = json.dumps(ret, indent=None)
          return "var %s = %s;" % (self.JS_VARNAME, json_output)


        self.options['divid'] = self.arguments[0]
        if self.content:
            source = "\n".join(self.content)
        else:
            source = '\n'

        CUMULATIVE_MODE=False
        self.JS_VARNAME = self.options['divid']+'_trace'
        if 'showoutput' not in self.options:
            self.options['embedded'] = 'true'  # to set embeddedmode to true
        else:
            self.options['embedded'] = 'false'



        if 'question' in self.options:
            curTrace = exec_script_str_local(source, CUMULATIVE_MODE, raw_dict)
            self.inject_questions(curTrace)
            json_output = json.dumps(curTrace, indent=None)
            self.options['tracedata'] = "var %s = %s;" % (self.JS_VARNAME, json_output)
        else:
            self.options['tracedata'] = exec_script_str_local(source, CUMULATIVE_MODE, js_var_finalizer)

        res = VIS
        if 'caption' not in self.options:
            self.options['caption'] = ''
        if 'question' in self.options:
            res += QUESTION
        if 'tracedata' in self.options:
            res += DATA
        return [nodes.raw('',res % self.options,format='html')]

    def inject_questions(self,curTrace):
        if 'breakline' not in self.options:
            raise RuntimeError('Must have breakline option')
        breakline = self.options['breakline']
        for frame in curTrace['trace']:
            if frame['line'] == breakline:
                frame['question'] = dict(text=self.options['question'],
                                      correct = self.options['correct'],
                                      div = self.options['divid']+'_modal',
                                      feedback = self.options['feedback'] )
