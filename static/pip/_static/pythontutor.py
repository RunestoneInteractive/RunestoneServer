# Online Python Tutor
# https://github.com/pgbovine/OnlinePythonTutor/
# 
# Copyright (C) 2010-2013 Philip J. Guo (philip@pgbovine.net)
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# TODO: if we want to enable concurrent requests, then make sure this is threadsafe (e.g., no mutable globals)
# then add this string to app.yaml: 'threadsafe: true'

import webapp2
import pg_logger
import json
import jinja2, os
import sys


# TODO: this croaks for some reason ...
TEST_STR = "import os\nos.chdir('/')"


JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class TutorPage(webapp2.RequestHandler):

  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    template = JINJA_ENVIRONMENT.get_template('visualize.html')
    self.response.out.write(template.render())


class IframeEmbedPage(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    template = JINJA_ENVIRONMENT.get_template('iframe-embed.html')
    self.response.out.write(template.render())


class LessonPage(webapp2.RequestHandler):

  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    template = JINJA_ENVIRONMENT.get_template('lesson.html')
    self.response.out.write(template.render())


class ExecScript(webapp2.RequestHandler):

  def json_finalizer(self, input_code, output_trace):
    ret = dict(code=input_code, trace=output_trace)
    json_output = json.dumps(ret, indent=None) # use indent=None for most compact repr
    self.response.out.write(json_output)

  def get(self):
    self.response.headers['Content-Type'] = 'application/json'
    self.response.headers['Cache-Control'] = 'no-cache'

    pg_logger.exec_script_str(self.request.get('user_script'),
                              self.request.get('raw_input_json'),
                              self.request.get('options_json'),
                              self.json_finalizer)


app = webapp2.WSGIApplication([('/', TutorPage),
                               ('/iframe-embed.html', IframeEmbedPage),
                               ('/lesson.html', LessonPage),
                               ('/exec', ExecScript)],
                              debug=True)

