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


_base_js_escapes = (
    ('\\', r'\u005C'),
    ('\'', r'\u0027'),
    ('"', r'\u0022'),
    ("'", r'\u0027'),
    ('>', r'\u003E'),
    ('<', r'\u003C'),
    ('&', r'\u0026'),
    ('=', r'\u003D'),
    ('-', r'\u002D'),
    (';', r'\u003B'),
    (u'\u2028', r'\u2028'),
    (u'\u2029', r'\u2029')
)

# Escape every ASCII character with a value less than 32.
_js_escapes = (_base_js_escapes +
               tuple([('%c' % z, '\\u%04X' % z) for z in range(32)]))

# escapejs from Django: https://www.djangoproject.com/
def escapejs(value):
    """Hex encodes characters for use in JavaScript strings."""
    if not isinstance(value, basestring):
        value = str(value)

    for bad, good in _js_escapes:
        value = value.replace(bad, good)

    return value


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


