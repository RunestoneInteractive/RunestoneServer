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
<div id="disqus_thread"></div>
<script type="text/javascript">
    /* * * CONFIGURATION VARIABLES: EDIT BEFORE PASTING INTO YOUR WEBPAGE * * */
    var disqus_shortname = '%(shortname)s'; // required: replace example with your forum shortname
    var disqus_developer = 1;
    var disqus_identifier = '{{pagename}}';
    /* * * DON'T EDIT BELOW THIS LINE * * */
    if (disqus_identifier.indexOf("index") < 0) {   // dont show the comments index
        (function() {
            var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
            dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';
            (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
        })();
    }
</script>
<noscript>Please enable JavaScript to view the <a href="http://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
<a href="http://disqus.com" class="dsq-brlink">comments powered by <span class="logo-disqus">Disqus</span></a>
"""

class Disqus(Directive):
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
        res = CODE % self.options
        return [nodes.raw('', res, format='html')]
