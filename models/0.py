from gluon.storage import Storage
settings = Storage()
# from os import uname

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

# real API key and domain set in gitignore'd 1.py
settings.janrain_api_key = 'a_fake_key'
settings.janrain_domain = 'a-fake-domain'

# if 'local' in uname()[1] or 'Darwin' in uname()[0]:
# 	settings.database_uri = 'sqlite://storage.sqlite'
# elif 'webfaction' in uname()[1]:
#     # the real uri is set in gitignore'd 1.py
# 	settings.database_uri = 'postgres://a_fake_database'
# elif 'luther' in uname()[1]:
# 	settings.database_uri = 'sqlite://storage.sqlite'
# else:
# 	raise RuntimeError('Host unknown, settings not configured')
