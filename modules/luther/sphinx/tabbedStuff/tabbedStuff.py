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
    app.add_directive('tabbed', TabbedStuffDirective)
    app.add_directive('tab', TabDirective)

    app.add_node(TabNode, html=(visit_tab_node, depart_tab_node))
    app.add_node(TabbedStuffNode, html=(visit_tabbedstuff_node, depart_tabbedstuff_node))

    app.add_stylesheet('tabbedstuff.css')


BEGIN = """<div id='%(divid)s' class='alert alert-warning'>"""

TABLIST_BEGIN = """<ul class='nav nav-tabs' id='%(divid)s_tab'>"""

TABLIST_ELEMENT = """
<li>
    <a data-toggle='tab' href='#%(divid)s-%(tabname)s'><span>%(tabfriendlyname)s</span></a>
</li>
"""

TABLIST_END = """</ul>"""

TABCONTENT_BEGIN = """<div class='tab-content'>"""
TABCONTENT_END = """</div>"""

TABDIV_BEGIN = """<div class='tab-pane' id='%(divid)s-%(tabname)s'>"""

TABDIV_END = """</div>""" 

END = """
    </div>
    <script type='text/javascript'>
        $('#%(divid)s .nav-tabs a').click(function (e) {
            e.preventDefault();
            $(this).tab('show');
        })

        // activate the first tab
        var el = $('#%(divid)s .nav-tabs a')[0];
        $(el).tab('show');

        $('#%(divid)s .nav-tabs a').on('shown.bs.tab', function (e) {
            var content_div = $(e.target.attributes.href.value);
            content_div.find('.disqus_thread_link').each(function() {
                $(this).click();
            });

            content_div.find('.CodeMirror').each(function(i, el) {
                el.CodeMirror.refresh();
            });
        })
    </script>
"""

class TabNode(nodes.General, nodes.Element):
    def __init__(self, content):
        super(TabNode, self).__init__()
        self.tabnode_components = content
        self.tabname = content['tabname']

def visit_tab_node(self, node):
    divid = node.parent.divid 
    tabname = node.tabname

    # remove spaces from tabname to allow it to be used as the div id.
    res = TABDIV_BEGIN % {'divid':divid,
                          'tabname':tabname.replace(" ", "")}
    self.body.append(res)

def depart_tab_node(self,node):
    self.body.append(TABDIV_END)

class TabbedStuffNode(nodes.General, nodes.Element):
    '''A TabbedStuffNode contains one or more TabNodes'''
    def __init__(self,content):
        super(TabbedStuffNode,self).__init__()
        self.tabbed_stuff_components = content
        self.divid = content['divid']

def visit_tabbedstuff_node(self, node):
    divid = node.divid

    # this is all the child tab nodes
    tabs = node.traverse(include_self=False, descend=True, condition=TabNode) 

    res = BEGIN % {'divid':divid}
    res += TABLIST_BEGIN
    
    # make the tab list (<ul>).
    # tabfriendlyname can contain spaces and will be displayed as the name of the tab.
    # tabname is the same as tabfriendlyname but with spaces removed, so it can be 
    # used as the div id.
    for tab in tabs:
        res += TABLIST_ELEMENT % {'divid':divid,
                                  'tabfriendlyname':tab.tabname,  
                                  'tabname':tab.tabname.replace(" ", "")}  

    res += TABLIST_END  # </ul>
    res += TABCONTENT_BEGIN

    self.body.append(res)


def depart_tabbedstuff_node(self,node):
    divid = node.divid

    # close the tab plugin div and init the Bootstrap tabs
    res = TABCONTENT_END
    res += END

    res = res % {'divid':divid}

    self.body.append(res)



class TabDirective(Directive):
    required_arguments = 1  # the name of the tab
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True
    option_spec = {}

    node_class = TabNode

    def run(self):
        # Raise an error if the directive does not have contents.
        self.assert_has_content()
        
        # Create the node, to be populated by "nested_parse".
        self.options['tabname'] = self.arguments[0]
        tab_node = TabNode(self.options)

        # Parse the child nodes (content of the tab)
        self.state.nested_parse(self.content, self.content_offset, tab_node)
        return [tab_node]

class TabbedStuffDirective(Directive):
    required_arguments = 1  # the div to put the tabbed exhibit in
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True

    def run(self):
        # Raise an error if the directive does not have contents.
        self.assert_has_content()

        self.options['divid'] = self.arguments[0]

        # Create the node, to be populated by "nested_parse".
        tabbedstuff_node = TabbedStuffNode(self.options)

        # Parse the directive contents (should be 1 or more tab directives)
        self.state.nested_parse(self.content, self.content_offset, tabbedstuff_node)
        return [tabbedstuff_node]

