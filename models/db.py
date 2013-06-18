# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(settings.database_uri,fake_migrate_all=False)
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db = db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db, hmac_key=Auth.get_or_create_key())
crud, service, plugins = Crud(db), Service(), PluginManager()

## Enable captcha's :-(
from gluon.tools import Recaptcha
auth.settings.captcha = Recaptcha(request,
   '6Lfb_t4SAAAAAB9pG_o1CwrMB40YPsdBsD8GsvlD',
   '6Lfb_t4SAAAAAGvAHwmkahQ6s44478AL5Cf-fI-x',
   options="theme:'blackglass'")

auth.settings.login_captcha = False
auth.settings.retrieve_password_captcha	= False
#auth.settings.retrieve_username_captcha	= False


## create all tables needed by auth if not custom tables
db.define_table('courses',
  Field('course_id','string'),
  migrate=settings.migrate
  )
if db(db.courses.id > 0).isempty():
    db.courses.insert(course_id='devcourse')


########################################

def getCourseNameFromId(courseid):
    ''' used to compute auth.user.course_name field '''
    if courseid == 0:
        return ''
    else:
        q = db.courses.id == courseid
        course_name = db(q).select()[0].course_id
        return course_name

class IS_COURSE_ID:
    ''' used to validate that a course name entered (e.g. devcourse) corresponds to a 
        valid course ID (i.e. db.courses.id) '''
    def __init__(self, error_message='Unknown course name. Please see your instructor.'):
        self.e = error_message

    def __call__(self, value):
        if db(db.courses.course_id == value).select():
            return (db(db.courses.course_id == value).select()[0].id, None)
        return (value, self.e)


db.define_table('auth_user',
    Field('username', type='string',
          label=T('Username')),
    Field('first_name', type='string',
          label=T('First Name')),
    Field('last_name', type='string',
          label=T('Last Name')),
    Field('email', type='string',
          requires=IS_EMAIL(banned='^.*shoeonlineblog\.com$'),
          label=T('Email')),
    Field('password', type='password',
          readable=False,
          label=T('Password')),
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    Field('modified_on','datetime',default=request.now,
          label=T('Modified On'),writable=False,readable=False,
          update=request.now),
    Field('registration_key',default='',
          writable=False,readable=False),
    Field('reset_password_key',default='',
          writable=False,readable=False),
    Field('registration_id',default='',
          writable=False,readable=False),
    Field('course_id',db.courses,label=T('Course Name'),
          required=True,
          default=0),
    Field('course_name',compute=lambda row: getCourseNameFromId(row.course_id)),
    format='%(username)s',
    migrate=settings.migrate)


db.auth_user.first_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.auth_user.last_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.auth_user.password.requires = CRYPT(key=auth.settings.hmac_key)
db.auth_user.username.requires = IS_NOT_IN_DB(db, db.auth_user.username)
db.auth_user.registration_id.requires = IS_NOT_IN_DB(db, db.auth_user.registration_id)
db.auth_user.email.requires = (IS_EMAIL(error_message=auth.messages.invalid_email),
                               IS_NOT_IN_DB(db, db.auth_user.email))
db.auth_user.course_id.requires = IS_COURSE_ID()

auth.define_tables(migrate=settings.migrate)


## configure email
mail=auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
#from gluon.contrib.login_methods.rpx_account import use_janrain
#use_janrain(auth,filename='private/janrain.key')
from gluon.contrib.login_methods.rpx_account import RPXAccount

if request.is_local:
    janrain_url = 'http://127.0.0.1:8000/%s/default/user/login' % request.application
else:
    janrain_url = 'http://%s:%s/%s/default/user/login' % (request.env.server_name,
                                                          request.env.server_port,
                                                          request.application)

janrain_form = RPXAccount(request, 
                          api_key=settings.janrain_api_key, # set in 1.py
                          domain='runestoneinteractive',
                          url=janrain_url)

from gluon.contrib.login_methods.extended_login_form import ExtendedLoginForm 
auth.settings.login_form = ExtendedLoginForm(auth, janrain_form)


#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################


mail.settings.server = settings.email_server
mail.settings.sender = settings.email_sender
mail.settings.login = settings.email_login
