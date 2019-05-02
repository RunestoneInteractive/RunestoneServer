#!/usr/bin/python
# -*- coding: utf-8 -*-

# default_application, default_controller, default_function
# are used when the respective element is missing from the
# (possibly rewritten) incoming URL
#
default_application = 'runestone'    # ordinarily set in base routes.py
default_controller = 'default'  # ordinarily set in app-specific routes.py
default_function = 'index'      # ordinarily set in app-specific routes.py

# routes_app is a tuple of tuples.  The first item in each is a regexp that will
# be used to match the incoming request URL. The second item in the tuple is
# an applicationname.  This mechanism allows you to specify the use of an
# app-specific routes.py. This entry is meaningful only in the base routes.py.
#
# Example: support welcome, admin, app and myapp, with myapp the default:


routes_app = ((r'/(?P<app>welcome|admin|app)\b.*', r'\g<app>'),
              (r'(.*)', r'runestone'),
              (r'/?(.*)', r'runestone'))

# routes_in is a tuple of tuples.  The first item in each is a regexp that will
# be used to match the incoming request URL. The second item in the tuple is
# what it will be replaced with.  This mechanism allows you to redirect incoming
# routes to different web2py locations
#
# Example: If you wish for your entire website to use init's static directory:
#
#   routes_in=( (r'/static/(?P<file>[\w./-]+)', r'/init/static/\g<file>') )
#

routes_in = ((r'.*:/favicon.ico', r'/runestone/static/favicon.ico'),
             (r'.*:/robots.txt', r'/examples/static/robots.txt'),
             (r'.*/courselib/static/thinkcspy/(?P<any>.*)', r'/runestone/static/thinkcspy/\g<any>'),
             (r'.*/courselib/static/pythonds/(?P<any>.*)', r'/runestone/static/pythonds/\g<any>'),
             (r'.*/courselib/static/everyday/(?P<any>.*)', r'/runestone/static/everyday/\g<any>'),
#             (r'.*/static/(?P<course>[\w+\d+]+)(/)?$','/'+default_application+'/static/\g<course>/index.html'),
             (r'.*http://everydaypython.org$', r'http://everydaypython.org/runestone/everyday'),
             ((r'.*http://otherdomain.com.* (?P<any>.*)', r'/app/ctr\g<any>')))

# 
# routes_out, like routes_in translates URL paths created with the web2py URL()
# function in the same manner that route_in translates inbound URL paths.
#

routes_out = ((r'.*http://otherdomain.com.* /app/ctr(?P<any>.*)', r'\g<any>'),
              (r'/app(?P<any>.*)', r'\g<any>'))

# Specify log level for rewrite's debug logging
# Possible values: debug, info, warning, error, critical (loglevels),
#                  off, print (print uses print statement rather than logging)
# GAE users may want to use 'off' to suppress routine logging.
#
logging = 'debug'

# Error-handling redirects all HTTP errors (status codes >= 400) to a specified
# path.  If you wish to use error-handling redirects, uncomment the tuple
# below.  You can customize responses by adding a tuple entry with the first
# value in 'appName/HTTPstatusCode' format. ( Only HTTP codes >= 400 are
# routed. ) and the value as a path to redirect the user to.  You may also use
# '*' as a wildcard.
#
# The error handling page is also passed the error code and ticket as
# variables.  Traceback information will be stored in the ticket.
#
routes_onerror = [
  ('runestone/static/404', '/runestone/static/fail.html'),
  ('runestone/500', '/runestone/default/reportabug.html'),
]

# routes_onerror = [
#     (r'init/400', r'/init/default/login')
#    ,(r'init/*', r'/init/static/fail.html')
#    ,(r'*/404', r'/init/static/cantfind.html')
#    ,(r'*/*', r'/init/error/index')
# ]

# specify action in charge of error handling
#
# error_handler = dict(application='error',
#                      controller='default',
#                      function='index')

# In the event that the error-handling page itself returns an error, web2py will
# fall back to its old static responses.  You can customize them here.
# ErrorMessageTicket takes a string format dictionary containing (only) the
# "ticket" key.

# error_message = '<html><body><h1>%s</h1></body></html>'
error_message = '''<html><body>
<h1>Sorry, Something went wrong</h1>
<p>The error is: <code>%s</code></p>
<p>We recently reorganized the books, and so some of the chapters have new links.  Please go to the table of contents for your book and navigate to the desired section from there.  <a href="http://dev.runestone.academy">Our Home Page is a good starting point</a></p>
<p>If you got an <code>invalid request</code> were hoping to find a course in /static/mycourse/xxxx.html  That course may need to be rebuilt, or the course may no longer be available.
Please contact your instructor.  If you are an instructor then go to the <a href="/runestone/admin/index">Instructors Page</a> and follow
the instructions to rebuild or create your course.</p>
<p>For any other error, please report this on <a href="http://github.com/bnmnetp/runestone/issues">our github page</a>  (github account required)
Or, tweet us <a href="http://twitter.com/iRunestone">@iRunestone</a>  Please try to include the error message, and the page you were trying to get to.
</p>
</body></html>'''

# error_message_ticket = '<html><body><h1>Internal error</h1>Ticket issued: <a href="/admin/default/ticket/%(ticket)s" target="_blank">%(ticket)s</a></body></html>'

# specify a list of apps that bypass args-checking and use request.raw_args
#
#routes_apps_raw=['myapp']
#routes_apps_raw=['myapp', 'myotherapp']

def __routes_doctest():
    '''
    Dummy function for doctesting routes.py.

    Use filter_url() to test incoming or outgoing routes;
    filter_err() for error redirection.

    filter_url() accepts overrides for method and remote host:
        filter_url(url, method='get', remote='0.0.0.0', out=False)

    filter_err() accepts overrides for application and ticket:
        filter_err(status, application='app', ticket='tkt')

    >>> import os
    >>> import gluon.main
    >>> from gluon.rewrite import regex_select, load, filter_url, regex_filter_out, filter_err, compile_regex
    >>> regex_select()
    >>> load(routes=os.path.basename(__file__))

    >>> os.path.relpath(filter_url('http://domain.com/favicon.ico'))
    'applications/examples/static/favicon.ico'
    >>> os.path.relpath(filter_url('http://domain.com/robots.txt'))
    'applications/examples/static/robots.txt'
    >>> filter_url('http://domain.com')
    '/init/default/index'
    >>> filter_url('http://domain.com/')
    '/init/default/index'
    >>> filter_url('http://domain.com/init/default/fcn')
    '/init/default/fcn'
    >>> filter_url('http://domain.com/init/default/fcn/')
    '/init/default/fcn'
    >>> filter_url('http://domain.com/app/ctr/fcn')
    '/app/ctr/fcn'
    >>> filter_url('http://domain.com/app/ctr/fcn/arg1')
    "/app/ctr/fcn ['arg1']"
    >>> filter_url('http://domain.com/app/ctr/fcn/arg1/')
    "/app/ctr/fcn ['arg1']"
    >>> filter_url('http://domain.com/app/ctr/fcn/arg1//')
    "/app/ctr/fcn ['arg1', '']"
    >>> filter_url('http://domain.com/app/ctr/fcn//arg1')
    "/app/ctr/fcn ['', 'arg1']"
    >>> filter_url('HTTP://DOMAIN.COM/app/ctr/fcn')
    '/app/ctr/fcn'
    >>> filter_url('http://domain.com/app/ctr/fcn?query')
    '/app/ctr/fcn ?query'
    >>> filter_url('http://otherdomain.com/fcn')
    '/app/ctr/fcn'
    >>> regex_filter_out('/app/ctr/fcn')
    '/ctr/fcn'
    >>> filter_url('https://otherdomain.com/app/ctr/fcn', out=True)
    '/ctr/fcn'
    >>> filter_url('https://otherdomain.com/app/ctr/fcn/arg1//', out=True)
    '/ctr/fcn/arg1//'
    >>> filter_url('http://otherdomain.com/app/ctr/fcn', out=True)
    '/fcn'
    >>> filter_url('http://otherdomain.com/app/ctr/fcn?query', out=True)
    '/fcn?query'
    >>> filter_url('http://otherdomain.com/app/ctr/fcn#anchor', out=True)
    '/fcn#anchor'
    >>> filter_err(200)
    200
    >>> filter_err(399)
    399
    >>> filter_err(400)
    400
    >>> filter_url('http://domain.com/welcome', app=True)
    'welcome'
    >>> filter_url('http://domain.com/', app=True)
    'myapp'
    >>> filter_url('http://domain.com', app=True)
    'myapp'
    >>> compile_regex('.*http://otherdomain.com.* (?P<any>.*)', '/app/ctr\g<any>')[0].pattern
    '^.*http://otherdomain.com.* (?P<any>.*)$'
    >>> compile_regex('.*http://otherdomain.com.* (?P<any>.*)', '/app/ctr\g<any>')[1]
    '/app/ctr\\\\g<any>'
    >>> compile_regex('/$c/$f', '/init/$c/$f')[0].pattern
    '^.*?:https?://[^:/]+:[a-z]+ /(?P<c>\\\\w+)/(?P<f>\\\\w+)$'
    >>> compile_regex('/$c/$f', '/init/$c/$f')[1]
    '/init/\\\\g<c>/\\\\g<f>'
    '''
    pass

if __name__ == '__main__':
    import doctest
    doctest.testmod()


