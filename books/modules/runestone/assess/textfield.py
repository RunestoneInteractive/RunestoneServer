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
import random

#    setup is called in assess.py

#    app.add_node(MChoiceNode, html=(visit_mc_node, depart_mc_node))
#    app.add_node(FITBNode, html=(visit_fitb_node, depart_fitb_node))    



def textfield_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    '''
    Usage:

    In your document you can write :textfield:`myid:myvalue:width`

    This will translate to:
        <input type='text' id='myid' class="form-control input-small" style="display:inline; width:width;" value='myvalue'></input>
     
    where width can be specified in pixels or percentage of page width (standard CSS syntax).
    Width can also be specified using relative sizes:
        mini, small, medium, large, xlarge, and xxlarge



    '''
    iid, value, width = text.split(':')

    if 'mini' in width:
        width = '60px'
    elif 'small' in width:
        width = '90px'
    elif 'medium' in width:
        width = '150px'
    elif 'large' in width:
        width = '210px'
    elif 'xlarge' in width:
        width = '270px'
    elif 'xxlarge' in width:
        width = '530px'

    res = '''<input type='text' id='%s' class="form-control" style="display:inline; width: %s;" value="%s"></input>''' % (iid,width,value)

    return [nodes.raw('',res, format='html')],[]

