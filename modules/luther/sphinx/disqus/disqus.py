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
    app.add_directive('disqus', Disqus)

CODE = """\
<script type="text/javascript">
    function %(identifier)s(source) { 
        if (window.DISQUS) {

            jQuery('#disqus_thread').insertAfter(source); //append the HTML after the link

            //if Disqus exists, call it's reset method with new parameters
            DISQUS.reset({
                reload: true,
                config: function () {
                    this.page.identifier = '%(identifier)s';
                    this.page.url = 'http://www.%(identifier)s.com/#!';
                }
            });

        } else {

            //insert a wrapper in HTML after the relevant "show comments" link
            jQuery('<div id="disqus_thread"></div>').insertAfter(source);
            disqus_shortname = '%(shortname)s';    
            disqus_identifier = '%(identifier)s'; //set the identifier argument
            disqus_url = 'http://www.%(identifier)s.com/#!'; //set the permalink argument

            //append the Disqus embed script to HTML
            var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
            dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';
            jQuery('head').append(dsq);

        }
    }
</script>
<a href="javascript:void(0)" onclick="%(identifier)s(this);">Show Comments</a>
"""

class Disqus(Directive):
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False
    option_spec = {'shortname':directives.unchanged_required,
                   'identifier':directives.unchanged_required,
                  }


    def run(self):
        """
        generate html to include Disqus box.
        :param self:
        :return:
        """
        res = CODE % self.options
        return [nodes.raw('', res, format='html')]
