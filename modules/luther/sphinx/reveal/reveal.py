__author__ = 'isaacdontjelindell'

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive

def setup(app):
    app.add_directive('reveal', RevealDirective)
    
    app.add_node(RevealNode, html=(visit_reveal_node, depart_reveal_node))


BEGIN = """
    <button type='button' id='%(divid)s_show' class='btn btn-default' style='margin-bottom:10px;' onclick="$(this).hide();$('#%(divid)s').show();$('#%(divid)s_hide').show();$('#%(divid)s').find('.CodeMirror').each(function(i, el){el.CodeMirror.refresh();});">
        %(showtitle)s
    </button>
    <button type='button' id='%(divid)s_hide' class='btn btn-default' onclick="$(this).hide();$('#%(divid)s').hide();$('#%(divid)s_show').show();" style='display:none'>%(hidetitle)s</button>
    <div id='%(divid)s' style='display:none'>
"""

END = """
    </div>
"""

class RevealNode(nodes.General, nodes.Element):
    def __init__(self,content):
        super(RevealNode,self).__init__()
        self.reveal_components = content


def visit_reveal_node(self, node):
    res = BEGIN % node.reveal_components

    self.body.append(res)

def depart_reveal_node(self,node):
    res = END % node.reveal_components

    self.body.append(res)

class RevealDirective(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True
    option_spec = {"showtitle":directives.unchanged,
                   "hidetitle":directives.unchanged}

    def run(self):
        self.assert_has_content() # an empty reveal block isn't very useful...

        if not 'showtitle' in self.options:
            self.options['showtitle'] = "Show"
        if not 'hidetitle' in self.options:
            self.options['hidetitle'] = "Hide"

        self.options['divid'] = self.arguments[0]

        reveal_node = RevealNode(self.options)

        self.state.nested_parse(self.content, self.content_offset, reveal_node)

        return [reveal_node]

