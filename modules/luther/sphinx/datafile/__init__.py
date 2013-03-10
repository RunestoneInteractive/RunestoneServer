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
    app.add_directive('datafile',DataFile)
    app.add_javascript('bookfuncs.js')
    app.add_javascript('skulpt/dist/skulpt.js')
    app.add_javascript('skulpt/dist/builtin.js')

    app.add_node(DataFileNode, html=(visit_df_node, depart_df_node))

    app.connect('doctree-resolved',process_datafile_nodes)
    app.connect('env-purge-doc', purge_datafiles)


PRE = '''
<pre id="%(divid)s" style="display: %(hide)s;">
%(filecontent)s
</pre>
'''

TEXTA = '''
<textarea id="%(divid)s" rows="%(rows)d" cols="%(cols)d">
%(filecontent)s
</textarea>
'''

class DataFileNode(nodes.General, nodes.Element):
    def __init__(self,content):
        """
        Arguments:
        - `self`:
        - `content`:
        """
        super(DataFileNode,self).__init__()
        self.df_content = content

# self for these functions is an instance of the writer class.  For example
# in html, self is sphinx.writers.html.SmartyPantsHTMLTranslator
# The node that is passed as a parameter is an instance of our node class.
def visit_df_node(self,node):
    if node.df_content['edit'] == True:
        res = TEXTA
    else:
        res = PRE
    res = res % node.df_content

    res = res.replace("u'","'")  # hack:  there must be a better way to include the list and avoid unicode strings

    self.body.append(res)

def depart_df_node(self,node):
    ''' This is called at the start of processing an datafile node.  If datafile had recursive nodes
        etc and did not want to do all of the processing in visit_ac_node any finishing touches could be
        added here.
    '''
    pass


def process_datafile_nodes(app,env,docname):
    pass


def purge_datafiles(app,env,docname):
    pass


class DataFile(Directive):
    required_arguments = 1
    optional_arguments = 2
    has_content = True
    option_spec = {
        'hide':directives.flag,
        'edit':directives.flag,
        'rows':directives.positive_int,
        'cols':directives.positive_int
    }

    def run(self):
        env = self.state.document.settings.env

        if not hasattr(env,'datafilecounter'):
            env.datafilecounter = 0
        env.datafilecounter += 1
        
        if 'cols' not in self.options:
            self.options['cols'] = min(65,max([len(x) for x in self.content]))
        if 'rows'not in self.options:
            self.options['rows'] = 20
        
        self.options['divid'] = self.arguments[0]
        if self.content:
            source = "\n".join(self.content)
        else:
            source = '\n'
        self.options['filecontent'] = source
        
        if 'hide' not in self.options:
            self.options['hide'] = 'block'
        else:
            self.options['hide'] = 'none'
            
        if 'edit' not in self.options:
            self.options['edit'] = False
        
        return [DataFileNode(self.options)]

