# Copyright (C) 2012  Michael Hewner
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
__author__ = 'hewner'

import re
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive

def setup(app):
    app.add_directive('parsonsprob',ParsonsProblem)

    app.add_stylesheet('js-parsons/parsons.css')
    app.add_stylesheet('js-parsons/lib/prettify.css')

    # includes parsons specific javascript headers
    # parsons-noconflict reverts underscore and
    # jquery to their original versions
    app.add_javascript('js-parsons/lib/jquery.min.js')
    app.add_javascript('js-parsons/lib/jquery-ui.min.js')
    app.add_javascript('js-parsons/lib/prettify.js')
    app.add_javascript('js-parsons/lib/underscore-min.js')
    app.add_javascript('js-parsons/lib/lis.js')
    app.add_javascript('js-parsons/parsons.js')
    app.add_javascript('parsons-noconflict.js')


class ParsonsProblem(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}
    has_content = True

    def run(self):
        """

   Instructions for solving the problem should be written and then a line with ----- 
   signals the beginning of the code.  If you want more than one line in a single
   code block, seperate your code blocks with =====.

   Both the instructions sections and code blocks are optional. If you don't include any
   =====, the code will assume you want each line to be its own code block.

Example:

.. parsonsprob:: unqiue_problem_id_here

   Solve my really cool parsons problem...if you can.
   -----
   def findmax(alist):
   =====
      if len(alist) == 0:
         return None
   =====
      curmax = alist[0]
      for item in alist:
   =====
         if item &gt; curmax:
   =====
            curmax = item
   =====
      return curmax


        """


        template_values = {}
        template_values['unique_id'] = self.lineno
        template_values['instructions'] = ""
        code = self.content

        if '-----' in self.content:
            index = self.content.index('-----')
            template_values['instructions'] = "\n".join(self.content[:index])
            code = self.content[index + 1:]

        if '=====' in code:
            template_values['code'] = self.parse_multiline_parsons(code);
        else:
            template_values['code'] = "\n".join(code)

        template_values['divid'] = self.arguments[0]

        TEMPLATE = '''
        %(instructions)s
        <div>
        <div id="parsons-orig-%(unique_id)s" style="display:none;">%(code)s</div>
        <div id="parsons-sortableTrash-%(unique_id)s" class="sortable-code"></div>
        <div id="parsons-sortableCode-%(unique_id)s" class="sortable-code"></div>
	<div style="clear:left;"></div>
        <div id="parsons-message-%(unique_id)s" style="background: pink; padding: 1em;"></div>
        <a href="#" id="newInstanceLink-%(unique_id)s">Reset</a>
        <a href="#" id="feedbackLink-%(unique_id)s">Get feedback</a>
        </div>

    <script>
        $pjQ(document).ready(function(){
            var msgBox = $("#parsons-message-%(unique_id)s");
            msgBox.hide();
	    var displayErrors = function (fb) {
	        if(fb.errors.length > 0) {
                    var hash = pp_%(unique_id)s.getHash("#ul-parsons-sortableCode-%(unique_id)s");
                    msgBox.fadeIn(500);
                    msgBox.css("background-color","pink");
                    msgBox.html(fb.errors[0]);
                    logBookEvent({'event':'parsons', 'act':hash, 'div_id':'%(divid)s'});

	        } else {
                    logBookEvent({'event':'parsons', 'act':'yes', 'div_id':'%(divid)s'});
                    msgBox.css("background-color","white");
                    msgBox.html("Perfect!")
                    msgBox.fadeOut(3000);
                }
	    }
 

        var pp_%(unique_id)s = new ParsonsWidget({
                'sortableId': 'parsons-sortableCode-%(unique_id)s',
		'trashId': 'parsons-sortableTrash-%(unique_id)s',
                'max_wrong_lines': 1,
                'feedback_cb' : displayErrors
        });
        pp_%(unique_id)s.init($pjQ("#parsons-orig-%(unique_id)s").text());
	pp_%(unique_id)s.shuffleLines();
        if(localStorage.getItem('%(divid)s') && localStorage.getItem('%(divid)s-trash')) {
            try {
                var solution = localStorage.getItem('%(divid)s');
                var trash = localStorage.getItem('%(divid)s-trash');
                pp_%(unique_id)s.createHTMLFromHashes(solution,trash);
                pp_%(unique_id)s.getFeedback();
            } catch(err) {
                var text = "An error occured restoring old %(divid)s state.  Error: ";
                console.log(text + err.message);
            }

        }
            $pjQ("#newInstanceLink-%(unique_id)s").click(function(event){
                event.preventDefault();
                pp_%(unique_id)s.shuffleLines();
            });
            $pjQ("#feedbackLink-%(unique_id)s").click(function(event){
                event.preventDefault();

                var hash = pp_%(unique_id)s.getHash("#ul-parsons-sortableCode-%(unique_id)s");
                localStorage.setItem('%(divid)s',hash);
                hash = pp_%(unique_id)s.getHash("#ul-parsons-sortableTrash-%(unique_id)s");
                localStorage.setItem('%(divid)s-trash',hash);

                pp_%(unique_id)s.getFeedback();

            });
            
        });
    </script>

'''


        self.assert_has_content()
        return [nodes.raw('',TEMPLATE % template_values, format='html')]


    def parse_multiline_parsons(self, lines):
        current_block = []
        results = []
        for line in lines:
            if(line == '====='):
                results.append(self.convert_leading_whitespace_for_block(current_block))
                current_block = []
            else:
                current_block.append(line)
        results.append(self.convert_leading_whitespace_for_block(current_block))
        return "\n".join(results)

    def convert_leading_whitespace_for_block(self, block):
        whitespaceMatcher = re.compile("^\s*")
        initialWhitespace = whitespaceMatcher.match(block[0]).end()
        result = block[0]
        for line in block[1:]:
            result += '\\n' # not a line break...the literal characters \n
            result += line[initialWhitespace:]
        return result
