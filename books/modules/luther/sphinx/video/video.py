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
    app.add_directive('video',Video)
    app.add_directive('youtube', Youtube)
    app.add_directive('vimeo', Vimeo)
    app.add_stylesheet('video.css')

CODE = """\
<div id="%(divid)s" class="video_popup" >
<video %(controls)s %(preload)s %(loop)s poster="%(thumb)s">
    %(sources)s
    No supported video types
</video>
</div>
"""

POPUP = """\
<a id="%(divid)s_thumb" style='position:relative;'>
    <img src="%(thumb)s" />
    <div class='video-play-overlay'></div>
</a>
<script>
    jQuery(function ($) {
       $('#%(divid)s_thumb').click(function (e) {
                $('#%(divid)s').modal();
                return false;
        });
    });
</script>

"""

INLINE = """\
<script>
   jQuery(function($) {
      $('#%(divid)s_thumb').click(function(e) {
         $('#%(divid)s').show();
         $('#%(divid)s_thumb').hide();
         logBookEvent({'event':'video','act':'play','div_id': '%(divid)s'});
         // Log the run event
      });
	  $('#%(divid)s video').one("click", function(){
		this.play();
	  });
	  $('#%(divid)s video').one("play", function(){
		logBookEvent({'event':'video','act':'play','div_id': '%(divid)s'});
	  });
   });
</script>
"""
SOURCE = """<source src="%s" type="video/%s"></source>"""


class Video(Directive):
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True
    has_content = True
    option_spec = {'controls':directives.flag,
                   'loop': directives.flag,
                   'thumb': directives.uri,
                   'preload': directives.flag
                   }

    def run(self):
        """
        process the video directive and generate html for output.
        :param self:
        :return:
        """
        mimeMap = {'mov':'mp4','webm':'webm', 'm4v':'m4v'}

        sources = [SOURCE % (directives.uri(line),mimeMap[line[line.rindex(".")+1:]]) for line in self.content]
        self.options['divid'] = self.arguments[0]
        if 'controls' in self.options:
            self.options['controls'] = 'controls'
        if 'loop' in self.options:
            self.options['loop'] = 'loop'
        else:
            self.options['loop'] = ''

        if 'preload' in self.options:
            self.options['preload'] = 'preload="auto"'
        else:
            self.options['preload'] = 'preload="none"'

        self.options['sources'] = "\n    ".join(sources)
        res = CODE % self.options
        if 'popup' in self.options:
            res += POPUP % self.options
        else:
            res += INLINE % self.options
        return [nodes.raw('',res , format='html')]


"""
    ReST directive for embedding Youtube and Vimeo videos.

    There are two directives added: ``youtube`` and ``vimeo``. The only
    argument is the video id of the video to include.

    Both directives have three optional arguments: ``height``, ``width``
    and ``align``. Default height is 281 and default width is 500.

    Example::

        .. youtube:: anwy2MPT5RE
            :height: 315
            :width: 560
            :align: left

    :copyright: (c) 2012 by Danilo Bargen.
    :license: BSD 3-clause
"""

def align(argument):
    """Conversion function for the "align" option."""
    return directives.choice(argument, ('left', 'center', 'right'))


class IframeVideo(Directive):
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'height': directives.nonnegative_int,
        'width': directives.nonnegative_int,
        'align': align,
    }
    default_width = 500
    default_height = 281

    def run(self):
        self.options['video_id'] = directives.uri(self.arguments[0])
        if not self.options.get('width'):
            self.options['width'] = self.default_width
        if not self.options.get('height'):
            self.options['height'] = self.default_height
        if not self.options.get('align'):
            self.options['align'] = 'left'
        return [nodes.raw('', self.html % self.options, format='html')]


class Youtube(IframeVideo):
    html = '<iframe src="http://www.youtube.com/embed/%(video_id)s" \
    width="%(width)u" height="%(height)u" frameborder="0" \
    webkitAllowFullScreen mozallowfullscreen allowfullscreen \
    class="align-%(align)s" seamless ></iframe>'


class Vimeo(IframeVideo):
    html = '<iframe src="http://player.vimeo.com/video/%(video_id)s" \
    width="%(width)u" height="%(height)u" frameborder="0" \
    webkitAllowFullScreen mozallowfullscreen allowFullScreen \
    class="align-%(align)s" seamless ></iframe>'





source = """\
This is some text.

.. video:: divid
   :controls:
   :thumb: _static/turtlestill.png
   :loop:

   http://knuth.luther.edu/~bmiller/foo.mov
   http://knuth.luther.edu/~bmiller/foo.webm

This is some more text.
"""

if __name__ == '__main__':
    from docutils.core import publish_parts

    directives.register_directive('video',Video)

    doc_parts = publish_parts(source,
            settings_overrides={'output_encoding': 'utf8',
            'initial_header_level': 2},
            writer_name="html")

    print doc_parts['html_body']
