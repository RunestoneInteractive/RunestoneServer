# Uncomment this to enable `auto-reloading
# <http://web2py.com/books/default/chapter/29/04/the-core?search=import+module#Sharing-the-global-scope-with-modules-using-the-current-object>`_
# of code in the ``modules/`` subdirectory. This is helpful when doing
# development; otherwise, the web2py server must be restarted to reload any
# changes made to ``modules/``.
#from gluon.custom_import import track_changes; track_changes(True)

from gluon.storage import Storage
import logging
from os import environ

settings = Storage()

settings.migrate = True
settings.migprefix = 'runestonebeta_'
settings.title = 'Runestone Interactive'
settings.subtitle = 'eBooks for Python'
settings.author = 'Brad Miller'
settings.author_email = 'info@interactivepython.org'
settings.keywords = ''
settings.description = ''
settings.layout_theme = 'Default'
settings.security_key = '0b734ebc-7a50-4167-99b1-2df09062fde8'
settings.email_server = 'smtp.webfaction.com'
settings.email_sender = 'info@interactivepython.org'
settings.email_login = 'sendmail_bnmnetp@web407.webfaction.com:password'
settings.login_method = 'local'
settings.login_config = ''
settings.course_id = 'devcourse'
settings.plugins = []
settings.server_type = "http://"
settings.academy_mode = True
settings.lti_only_mode = False
settings.coursera_mode = False

# Do not control this with hostnames
config = environ.get("WEB2PY_CONFIG", "NOT SET")

if config == "production":
    settings.database_uri = environ["DBURL"]
    # Set these
    settings.STRIPE_PUBLISHABLE_KEY = environ.get('STRIPE_PUBLISHABLE_KEY')
    settings.STRIPE_SECRET_KEY = environ.get('STRIPE_SECRET_KEY')
elif config == "development":
    settings.database_uri = environ.get("DEV_DBURL")
    settings.STRIPE_PUBLISHABLE_KEY = environ.get('STRIPE_DEV_PUBLISHABLE_KEY')
    settings.STRIPE_SECRET_KEY = environ.get('STRIPE_DEV_SECRET_KEY')
elif config == "test":
    settings.database_uri = environ.get("TEST_DBURL")
    settings.STRIPE_PUBLISHABLE_KEY = environ.get('STRIPE_TEST_PUBLISHABLE_KEY')
    settings.STRIPE_SECRET_KEY = environ.get('STRIPE_TEST_SECRET_KEY')
else:
    print("To configure web2py you should set up both WEB2PY_CONFIG and")
    print("XXX_DBURL values in your environment -- See README for more detail")
    raise ValueError("unknown value for WEB2PY_CONFIG")

# Just for compatibility -- many things use postgresql but web2py removes the ql
settings.database_uri = settings.database_uri.replace('postgresql://', 'postgres://')


settings.logger = "web2py.app.runestone"
settings.sched_logger = settings.logger  # works for production where sending log to syslog but not for dev.
settings.log_level = logging.DEBUG
