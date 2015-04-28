import os

DEBUG = True
SECRET_KEY = 'super-secret'

SQLALCHEMY_DATABASE_URI = 'sqlite:///devdb.db'

# Security configuration
SECURITY_LOGIN_USER_TEMPLATE = "login.html"
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True