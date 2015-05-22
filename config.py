import os

DEBUG = True
SECRET_KEY = 'super-secret'

# MongoDB Config
MONGODB_DB = 'runestonedev'
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

# Security configuration
SECURITY_LOGIN_USER_TEMPLATE = "login.html"
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_CONFIRMABLE = False

# Flask-Mail Configuration
MAIL_SERVER = 'localhost'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'username'
MAIL_PASSWORD = 'password'
MAIL_SUPPRESS_SEND = True    # true for local development purposes

