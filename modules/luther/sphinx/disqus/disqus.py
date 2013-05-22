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
    function %(identifier)s_disqus(source) { 
        if (window.DISQUS) {

            $('#disqus_thread').insertAfter(source); //put the DIV for the Disqus box after the link

            //if Disqus exists, call it's reset method with new parameters
            DISQUS.reset({
                reload: true,
                config: function () {
                    this.page.identifier = '%(identifier)s';
                    this.page.url = 'http://%(identifier)s.interactivepython.com/#!';
                }
            });

        } else {
            //insert a wrapper in HTML after the relevant "show comments" link
            $('<div id="disqus_thread"></div>').insertAfter(source);

            // set Disqus required vars
            disqus_shortname = '%(shortname)s';    
            disqus_identifier = '%(identifier)s';
            disqus_url = 'http://%(identifier)s.interactivepython.com/#!'; 

            //append the Disqus embed script to HTML
            var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
            dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';
            $('head').append(dsq);

        }
    }
</script>

    <script type="text/javascript">
    /* * * CONFIGURATION VARIABLES: EDIT BEFORE PASTING INTO YOUR WEBPAGE * * */
    var disqus_shortname = '%(shortname)s'; // required: replace example with your forum shortname
    var disqus_identifier = '%(identifier)s';
    var disqus_url = 'http://%(identifier)s.interactivepython.com/#!'; 

    /* * * DON'T EDIT BELOW THIS LINE * * */
    (function () {
        var s = document.createElement('script'); s.async = true;
        s.type = 'text/javascript';
        s.src = '//' + disqus_shortname + '.disqus.com/count.js';
        (document.getElementsByTagName('HEAD')[0] || document.getElementsByTagName('BODY')[0]).appendChild(s);
    }());
    </script>

<a href="#disqus_thread" data-disqus-identifier="%(identifier)s" onclick="%(identifier)s_disqus(this);">Show Comments</a>
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
