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
    app.add_directive('activecode',ActiveCode)
    app.add_directive('actex',ActiveExercise)
    app.add_stylesheet('codemirror.css')
    app.add_stylesheet('activecode.css')

    app.add_javascript('jquery.highlight.js' )
    app.add_javascript('bookfuncs.js' )
    app.add_javascript('codemirror.js' )
    app.add_javascript('python.js' )
    app.add_javascript('javascript.js' )
    app.add_javascript('activecode.js')
    app.add_javascript('skulpt.min.js' )
    app.add_javascript('skulpt-stdlib.js')

    app.add_node(ActivcodeNode, html=(visit_ac_node, depart_ac_node))

    app.connect('doctree-resolved',process_activcode_nodes)
    app.connect('env-purge-doc', purge_activecodes)



START = '''
<div id="cont"></div>
<div id="%(divid)s" lang="%(language)s" class="ac_section alert alert-warning" >
'''


EDIT1 = '''
</div>
<br/>
<div id="%(divid)s_code_div" style="display: %(hidecode)s" class="ac_code_div">
<textarea cols="50" rows="12" id="%(divid)s_code" class="active_code" prefixcode="%(include)s" lang="%(language)s">
%(initialcode)s
</textarea>
</div>
'''

CAPTION = ''' 
<div class="clearfix"></div>
<p class="ac_caption"><span class="ac_caption_text">%(caption)s (%(divid)s)</span> </p>
'''

UNHIDE='''
<span class="ac_sep"></span>
<button class='btn btn-default' id="%(divid)s_showb" onclick="$('#%(divid)s_code_div').toggle();cm_editors['%(divid)s_code'].refresh();$('#%(divid)s_saveb').toggle();$('#%(divid)s_loadb').toggle()">Show/Hide Code</button>
'''

GRADES = '''
<span class="ac_sep"></span>
<input type="button" class='btn btn-default ' id="gradeb" name="Show Feedback" value="Show Feedback" onclick="createGradeSummary('%(divid)s')"/>
'''

AUDIO = '''
<span class="ac_sep"></span>
<input type="button" class='btn btn-default ' id="audiob" name="Play Audio" value="Start Audio Tour" onclick="createAudioTourHTML('%(divid)s','%(argu)s','%(no_of_buttons)s','%(ctext)s')"/>
'''

EDIT2 = '''
<div class="ac_actions">
<button class='btn btn-success' id="%(divid)s_runb">Run</button>
<button class="ac_opt btn btn-default" style="display: inline-block" id="%(divid)s_saveb" onclick="saveEditor('%(divid)s');">Save</button>
<button class="ac_opt btn btn-default" style="display: inline-block" id="%(divid)s_loadb" onclick="requestCode('%(divid)s');">Load</button>
'''

VIZB = '''<button class='btn btn-default' id="%(divid)s_vizb" onclick="injectCodelens('%(divid)s');">Show in Codelens</button>
'''
SCRIPT = '''
<script>
if ('%(hidecode)s' == 'none') {
    // a hack to preserve the inline-block display style. Toggle() will use display: block
    // (instead of inline-block) if the previous display style was 'none'
    $('#%(divid)s_saveb').toggle();
    $('#%(divid)s_loadb').toggle();
}
if ($("#%(divid)s_code_div").parents(".admonition").length == 0 && $("#%(divid)s_code_div").parents("#exercises").length == 0){
	if ($(window).width() > 975){
		$("#%(divid)s_code_div").offset({
			left: $("#%(divid)s .clearfix").offset().left
		});
	}
	$("#%(divid)s_runb").one("click", function(){
		$({})
		.queue(function (next) {
			if ($(window).width() > 975){
				$("#%(divid)s_code_div").animate({
					left: 40
				}, 500, next);
			}
			else{
				next();
			}
		})
		.queue(function (next) {
			$("#%(divid)s_runb").parent().siblings(".ac_output").show();
			runit('%(divid)s',this, undefined);
			$("#%(divid)s_runb").on("click", function(){
				runit('%(divid)s',this, undefined);
			});
		})
		
	});
}
else{
	console.log("inside new if")
	$("#%(divid)s_code_div").css({float : "none", marginLeft : "auto", marginRight : "auto"});
	$("#%(divid)s_runb").parent().siblings(".ac_output").show().css({float : "none", right : "0px"});
	$("#%(divid)s_runb").on("click", function(){
		console.log("button clicked");
		runit('%(divid)s',this, undefined);
	});
}
</script>
'''
OUTPUT_START = '''
<div class="ac_output">'''

CANVAS = '''
<div style="text-align: center">
<canvas id="%(divid)s_canvas" class="ac-canvas" height="400" width="400" style="border-style: solid; display: none; text-align: center"></canvas>
</div>
'''

SUFF = '''<pre id="%(divid)s_suffix" style="display:none">%(suffix)s</pre>'''

PRE = '''<pre id="%(divid)s_pre" class="active_out"></pre>
'''
OUTPUT_END = '''
</div> <!-- end output -->'''

VIZ = '''<div id="%(divid)s_codelens_div" style="display:none"></div>'''

# <iframe id="%(divid)s_codelens" width="800" height="500" style="display:block"src="#">
# </iframe>

END = '''
</div>

'''

AUTO = '''
<script type="text/javascript">
$(document).ready(function() {
    $(window).load(function() {
        var runb = document.getElementById("%(divid)s_runb");
        runit('%(divid)s',runb, %(include)s);
    });
});
</script>
'''

class ActivcodeNode(nodes.General, nodes.Element):
    def __init__(self,content):
        """

        Arguments:
        - `self`:
        - `content`:
        """
        super(ActivcodeNode,self).__init__()
        self.ac_components = content

# self for these functions is an instance of the writer class.  For example
# in html, self is sphinx.writers.html.SmartyPantsHTMLTranslator
# The node that is passed as a parameter is an instance of our node class.
def visit_ac_node(self,node):
    #print self.settings.env.activecodecounter
    res = START
    if 'above' in node.ac_components:
        res += CANVAS
    if 'tour_1' not in node.ac_components:
        res += EDIT2
    else:
        res += EDIT2 + AUDIO
    if node.ac_components['codelens']:
        res += VIZB
    if 'hidecode' not in node.ac_components:
        node.ac_components['hidecode'] = 'block'
    if node.ac_components['hidecode'] == 'none':
        res += UNHIDE
    if 'gradebutton' in node.ac_components:
        res += GRADES
    res += EDIT1
    res += OUTPUT_START
    if 'above' not in node.ac_components:
        if 'nocanvas' not in node.ac_components:
            res += CANVAS
    if 'suffix' in node.ac_components:
        res += SUFF
    if 'nopre' not in node.ac_components:
        res += PRE
    if 'autorun' in node.ac_components:
        res += AUTO
    res += OUTPUT_END
    res += CAPTION

    if node.ac_components['codelens']:
        res += VIZ

    res += SCRIPT
    res += END
    res = res % node.ac_components
    res = res.replace("u'","'")  # hack:  there must be a better way to include the list and avoid unicode strings

    self.body.append(res)

def depart_ac_node(self,node):
    ''' This is called at the start of processing an activecode node.  If activecode had recursive nodes
        etc and did not want to do all of the processing in visit_ac_node any finishing touches could be
        added here.
    '''
    pass


def process_activcode_nodes(app,env,docname):
    pass


def purge_activecodes(app,env,docname):
    pass


class ActiveCode(Directive):
    required_arguments = 1
    optional_arguments = 1
    has_content = True
    option_spec = {
        'nocanvas':directives.flag,
        'nopre':directives.flag,
        'above':directives.flag,  # put the canvas above the code
        'autorun':directives.flag,
        'caption':directives.unchanged,
        'include':directives.unchanged,
        'hidecode':directives.flag,
        'language':directives.unchanged,
        'tour_1':directives.unchanged,
        'tour_2':directives.unchanged,
        'tour_3':directives.unchanged,
        'tour_4':directives.unchanged,
        'tour_5':directives.unchanged,
        'nocodelens':directives.flag
    }

    def run(self):
        env = self.state.document.settings.env
        # keep track of how many activecodes we have.... could be used to automatically make a unique id for them.
        if not hasattr(env,'activecodecounter'):
            env.activecodecounter = 0
        env.activecodecounter += 1

        self.options['divid'] = self.arguments[0]

        if self.content:
            if '====' in self.content:
                idx = self.content.index('====')
                source = "\n".join(self.content[:idx])
                suffix = "\n".join(self.content[idx+1:])
            else:
                source = "\n".join(self.content)
                suffix = "\n"
        else:
            source = '\n'
            suffix = '\n'

        self.options['initialcode'] = source
        self.options['suffix'] = suffix
        str=source.replace("\n","*nline*")
        str0=str.replace("\"","*doubleq*")
        str1=str0.replace("(","*open*")
        str2=str1.replace(")","*close*")
        str3=str2.replace("'","*singleq*")
        self.options['argu']=str3

        complete=""
        no_of_buttons=0
        okeys = self.options.keys()
        for k in okeys:
            if '_' in k:
                x,label = k.split('_')
                no_of_buttons=no_of_buttons+1
                complete=complete+self.options[k]+"*atype*"

        newcomplete=complete.replace("\"","*doubleq*")
        self.options['ctext'] = newcomplete
        self.options['no_of_buttons'] = no_of_buttons

        if 'caption' not in self.options:
            self.options['caption'] = ''

        if 'include' not in self.options:
            self.options['include'] = 'undefined'
        else:
            lst = self.options['include'].split(',')
            lst = [x.strip() for x in lst]
            self.options['include'] = lst

        if 'hidecode' in self.options:
            self.options['hidecode'] = 'none'
        else:
            self.options['hidecode'] = 'block'

        if 'language' not in self.options:
            self.options['language'] = 'python'

        if 'nocodelens' in self.options:
            self.options['codelens'] = False
        else:
            self.options['codelens'] = True

        return [ActivcodeNode(self.options)]


class ActiveExercise(ActiveCode):
    required_arguments = 1
    optional_arguments = 0
    has_content = True

    def run(self):
        self.options['hidecode'] = True
        self.options['gradebutton'] = True
        return super(ActiveExercise,self).run()


if __name__ == '__main__':
    a = ActiveCode()
