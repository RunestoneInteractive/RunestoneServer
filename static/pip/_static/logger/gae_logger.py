# User activity logger to be deployed on Google App Engine datastore

import datetime
from google.appengine.ext import db


class VisualizerRequest(db.Model):
  user_script = db.TextProperty(required=True) # LONG string
  cumulative_mode = db.BooleanProperty(requred=True)
  user_ip_addr = db.StringProperty(required=True)
  http_referer = db.StringProperty(required=True)
  app_id = db.StringProperty(required=True)
  request_timestamp = db.DateTimeProperty(auto_now_add=True) # always set timestamp to NOW!

x = VisualizerRequest(user_script=db.Text(u'print "hello world"\n', encoding='utf_8'),
                      cumulative_mode=True
                      user_ip_addr='18.239.4.100',
                      http_referer='http://www.google.com/?magic-search',
                      app_id='pgbovine test')

x.put()

