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


DISQUS_BOX = """\
<script type="text/javascript">
    function %(identifier)s_disqus(source) { 
        if (window.DISQUS) {

            $('#disqus_thread').insertAfter(source); //put the DIV for the Disqus box after the link

            //if Disqus exists, call it's reset method with new parameters
            DISQUS.reset({
                reload: true,
                config: function () {
                    this.page.identifier = '%(identifier)s_' + eBookConfig.course;
                    this.page.url = 'http://%(identifier)s_'+eBookConfig.course+'.interactivepython.com/#!';
                }
            });

        } else {
            //insert a wrapper in HTML after the relevant "show comments" link
            $('<div id="disqus_thread"></div>').insertAfter(source);

            // set Disqus required vars
            disqus_shortname = '%(shortname)s';    
            disqus_identifier = '%(identifier)s_' + eBookConfig.course;
            disqus_url = 'http://%(identifier)s_'+eBookConfig.course+'.interactivepython.com/#!';

            //append the Disqus embed script to HTML
            var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
            dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';
            $('head').append(dsq);

        }
    }
</script>
"""

DISQUS_LINK = """
<a href="#disqus_thread" class='disqus_thread_link' data-disqus-identifier="%(identifier)s" onclick="%(identifier)s_disqus(this);">Show Comments</a>
<script type='text/javascript'>
    $("a[data-disqus-identifier='%(identifier)s']").attr('data-disqus-identifier', '%(identifier)s_' + eBookConfig.course);
</script>
"""


def setup(app):
    app.add_directive('disqus', DisqusDirective)
    
    app.add_node(DisqusNode, html=(visit_disqus_node, depart_disqus_node))
    app.connect('doctree-resolved' ,process_disqus_nodes)
    app.connect('env-purge-doc', purge_disqus_nodes)

class DisqusNode(nodes.General, nodes.Element):
    def __init__(self,content):
        super(DisqusNode,self).__init__()
        self.disqus_components = content


def visit_disqus_node(self, node):
    res = DISQUS_BOX   
    res += DISQUS_LINK

    res = res % node.disqus_components

    self.body.append(res)

def depart_disqus_node(self,node):
    pass

def process_disqus_nodes(app, env, docname):
    pass

def purge_disqus_nodes(app, env, docname):
    pass


class DisqusDirective(Directive):
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False
    option_spec = {'shortname':directives.unchanged_required,
                   'identifier':directives.unchanged_required
                  }


    def run(self):
        """
        generate html to include Disqus box.
        :param self:
        :return:
        """

        return [DisqusNode(self.options)]

