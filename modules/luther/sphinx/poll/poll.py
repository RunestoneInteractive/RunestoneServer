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
__author__ = 'isaacdontjelindell'

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive


def setup(app):
    app.add_directive('poll', PollDirective)

    app.add_node(PollNode, html=(visit_poll_node, depart_poll_node))


BEGIN = """ <div id='%(divid)s' class='poll alert'> """

# TODO give this form an action!
BEGIN_FORM = """
    <form id='%(divid)s_poll' name='%(divid)s_poll' action="">
        <fieldset>
            <legend>Poll</legend>
            <div class='poll-question'>%(content)s</div>
            <div id='%(divid)s_poll_input'>
                <div class='poll-options'>
"""

POLL_ELEMENT = """
<label for='%(divid)s_%(value)s'> %(value)s </label>
<input type='radio' name='%(divid)s_opt' id='%(divid)s_%(value)s' value='%(value)s'>
"""

END_POLL_OPTIONS = """ </div> """

COMMENT = """ <br><input type='text' name='%(divid)s_comment' placeholder='Any comments?'> <br>"""

END_POLL_INPUT = """
            <button type='button' class='btn btn-small btn-success' onclick="submitPoll('%(divid)s');">Submit</button>
        </div>
"""

END_FORM = """
        </fieldset>
    </form>
"""

RESULTS_DIV = """ <div id='%(divid)s_results'></div> """

END = """ </div> """



class PollNode(nodes.General, nodes.Element):
    def __init__(self, options):
        super(PollNode, self).__init__()
        self.pollnode_components = options

def visit_poll_node(self, node):
    res = BEGIN
    res += BEGIN_FORM

    for i in range(1, node.pollnode_components['scale']+1):
        res += POLL_ELEMENT % {'divid':node.pollnode_components['divid'], 'value':i}

    res += END_POLL_OPTIONS

    if 'allowcomment' in node.pollnode_components:
        res += COMMENT

    res += END_POLL_INPUT
    res += END_FORM
    res += RESULTS_DIV
    res += END

    res = res % node.pollnode_components
    self.body.append(res)

def depart_poll_node(self,node):
    pass


class PollDirective(Directive):
    required_arguments = 1  # the div id
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True
    option_spec = {'scale':directives.positive_int,
                   'allowcomment': directives.flag}

    node_class = PollNode

    def run(self):
        # Raise an error if the directive does not have contents.
        self.assert_has_content()
        
        self.options['divid'] = self.arguments[0]
        self.options['content'] = self.content[0]
        poll_node = PollNode(self.options)

        return [poll_node]


