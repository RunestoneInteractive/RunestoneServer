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


def setup(app):
    app.add_directive('activecode',ActiveCode)
    app.add_directive('actex',ActiveExercise)
    app.add_stylesheet('codemirror.css')
    app.add_stylesheet('theme/default.css')
    app.add_stylesheet('activecode.css')

    app.add_javascript('jquery.highlight.js')
    app.add_javascript('bookfuncs.js')
    app.add_javascript('codemirror.js')
    app.add_javascript('python.js')
    app.add_javascript('activecode.js')
    app.add_javascript('skulpt/dist/skulpt.js')
    app.add_javascript('skulpt/dist/builtin.js')

    app.add_node(ActivcodeNode, html=(visit_ac_node, depart_ac_node))

    app.connect('doctree-resolved',process_activcode_nodes)
    app.connect('env-purge-doc', purge_activecodes)



START = '''
<div id="%(divid)s" >
'''

EDIT1 = '''
<br/>
<div id="%(divid)s_code_div" style="display: %(hidecode)s">
<textarea cols="50" rows="12" id="%(divid)s_code" class="active_code">
%(initialcode)s
</textarea>
</div>
<p class="ac_caption"><span class="ac_caption_text">%(caption)s (%(divid)s)</span> </p>

<button id="%(divid)s_runb" onclick="runit('%(divid)s',this, %(include)s);">Run</button>
'''
UNHIDE='''
<button id="%(divid)s_showb" onclick="$('#%(divid)s_code_div').toggle();cm_editors['%(divid)s_code'].refresh()">Show/Hide Code</button>
'''

AUDIO = '''
<input type="button" id="audiob" name="Play Audio" value="Start Audio Tour" onclick="createAudioTourHTML('%(divid)s','%(argu)s','%(no_of_buttons)s','%(ctext)s')"/>
'''

EDIT2 = '''
<div id="cont"></div>

<button class="ac_opt" onclick="saveEditor('%(divid)s');">Save</button>
<button class="ac_opt" onclick="requestCode('%(divid)s');">Load</button>
'''

CANVAS = '''
<div style="text-align: center">
<canvas id="%(divid)s_canvas" height="400" width="400" style="border-style: solid; display: none; text-align: center"></canvas>
</div>
'''

PRE = '''
<pre id="%(divid)s_pre" class="active_out">

</pre>

'''

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
    res += EDIT1
    if 'tour_1' not in node.ac_components:
        res += EDIT2
    else:
        res += AUDIO + EDIT2
    if 'above' not in node.ac_components:
        if 'nocanvas' not in node.ac_components:
            res += CANVAS
    if 'hidecode' not in node.ac_components:
        node.ac_components['hidecode'] = 'block'
    if node.ac_components['hidecode'] == 'none':
        res += UNHIDE
    if 'nopre' not in node.ac_components:
        res += PRE
    if 'autorun' in node.ac_components:
        res += AUTO
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
        'tour_1':directives.unchanged,
        'tour_2':directives.unchanged,
        'tour_3':directives.unchanged,
        'tour_4':directives.unchanged,
        'tour_5':directives.unchanged
    }

    def run(self):
        env = self.state.document.settings.env

        # keep track of how many activecodes we have.... could be used to automatically make a unique id for them.
        if not hasattr(env,'activecodecounter'):
            env.activecodecounter = 0
        env.activecodecounter += 1

        self.options['divid'] = self.arguments[0]
        if self.content:
            source = "\n".join(self.content)
        else:
            source = '\n'

        self.options['initialcode'] = source

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

        return [ActivcodeNode(self.options)]


EXEDIT = '''
<button id="butt_%(divid)s" onclick="createActiveCode('%(divid)s','%(source)s'); $('#butt_%(divid)s').hide();">Open Editor</button>
<div id="%(divid)s"></div>
<br />
'''

class ActiveExercise(Directive):
    required_arguments = 1
    optional_arguments = 0
    has_content = True

    def run(self):
        self.options['divid'] = self.arguments[0]
        if self.content:
            source = "\\n".join(self.content)
        else:
            source = ''
        self.options['source'] = source.replace('"','%22').replace("'",'%27')
        res = EXEDIT

        return [nodes.raw('',res % self.options,format='html')]


if __name__ == '__main__':
    a = ActiveCode()
