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

class Assessment(Directive):
    """Base Class for assessments"""

    def getNumber(self):
        env = self.state.document.settings.env
        if not hasattr(env,'assesscounter'):
            env.assesscounter = 0
        env.assesscounter += 1

        res = "Q-%d"

        if hasattr(env,'assessprefix'):
            res = env.assessprefix + "%d"

        res = res % env.assesscounter

        if hasattr(env, 'assesssuffix'):
            res += env.assesssuffix

        return res


    def run(self):

        self.options['qnumber'] = self.getNumber()
        
        self.options['divid'] = self.arguments[0]

        if self.content[0][:2] == '..':  # first line is a directive
            self.content[0] = self.options['qnumber'] + ': \n\n' + self.content[0]
        else:
            self.content[0] = self.options['qnumber'] + ': ' + self.content[0]

        if self.content:
            if 'iscode' in self.options:
                self.options['bodytext'] = '<pre>' + "\n".join(self.content) + '</pre>'
            else:
                self.options['bodytext'] = "\n".join(self.content)
        else:
            self.options['bodytext'] = '\n'


