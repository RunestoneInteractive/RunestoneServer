# -*- coding: utf-8 -*-

import os
import random

from gluon import current

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_htps()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    if os.environ.get("WEB2PY_CONFIG","") == 'test':
        db = DAL(settings.database_uri,migrate=False,migrate_enabled=False)
    else:
        # WEB2PY_MIGRATE is either "Yes", "No", "Fake", or missing
        db = DAL(settings.database_uri, fake_migrate_all=(os.environ.get("WEB2PY_MIGRATE", "Yes") == 'Fake'),
                 migrate=False, migrate_enabled=(os.environ.get("WEB2PY_MIGRATE", "Yes") in ['Yes', 'Fake']))
    session.connect(request, response, db, masterapp=None, migrate='runestone_web2py_sessions.table')

else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db = db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

# Make the settings and database available in modules.
current.db = db
current.settings = settings

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

if settings.enable_captchas:
    ## Enable captcha's :-(
    from gluon.tools import Recaptcha
    auth.settings.captcha = Recaptcha(request,
        '6Lfb_t4SAAAAAB9pG_o1CwrMB40YPsdBsD8GsvlD',
        '6Lfb_t4SAAAAAGvAHwmkahQ6s44478AL5Cf-fI-x',
        options="theme:'blackglass'")

auth.settings.login_captcha = False
auth.settings.retrieve_password_captcha	= False
auth.settings.retrieve_username_captcha	= False

# Set up for `two-factor authentication <http://web2py.com/books/default/chapter/29/09/access-control#Two-step-verification>`_.
#auth.settings.auth_two_factor_enabled = True
#auth.settings.two_factor_methods = [lambda user, auth_two_factor: 'password_here']


## create all tables needed by auth if not custom tables
db.define_table('courses',
  Field('course_name', 'string', unique=True),
  Field('term_start_date', 'date'),
  Field('institution', 'string'),
  Field('base_course', 'string'),
  Field('python3', type='boolean', default=True),
  Field('login_required', type='boolean', default=True),
  Field('allow_pairs', type='boolean', default=False),
  Field('student_price', type='integer'),
  migrate='runestone_courses.table'
)


# Provide a common query. Pass ``db.courses.ALL`` to retrieve all fields; otherwise, only the ``course_name`` and ``base_course`` are selected.
def get_course_row(*args, **kwargs):
    if not args:
        args = db.courses.course_name, db.courses.base_course
    return db(db.courses.id == auth.user.course_id).select(*args).first()


# Provide the correct URL to a book, based on if it's statically or dynamically served. This function return URL(*args) and provides the correct controller/function based on the type of the current course (static vs dynamic).
def get_course_url(*args):
    # Redirect to old-style statically-served books if it exists; otherwise, use the dynamically-served controller.
    if os.path.exists(os.path.join(request.folder, 'static', auth.user.course_name)):
        return URL(c='static', args=[auth.user.course_name] + list(args))
    else:
        course = db(db.courses.id == auth.user.course_id).select(db.courses.base_course).first()
        if course:
            return URL(c='books', f='published', args=args)
        else:
            return URL(c='default')

## create cohort_master table
db.define_table('cohort_master',
  Field('cohort_name','string',
  writable=False,readable=False),
  Field('created_on','datetime',default=request.now,
  writable=False,readable=False),
  Field('invitation_id','string',
  writable=False,readable=False),
  Field('average_time','integer', #Average Time it takes people to complete a unit chapter, calculated based on previous chapters
  writable=False,readable=False),
  Field('is_active','integer', #0 - deleted / inactive. 1 - active
  writable=False,readable=False),
  Field('course_name', 'string'),
  migrate='runestone_cohort_master.table'
  )

########################################

def getCourseNameFromId(courseid):
    ''' used to compute auth.user.course_name field '''
    q = db.courses.id == courseid
    row = db(q).select().first()
    return row.course_name if row else ''


def verifyInstructorStatus(course, instructor):
    """
    Make sure that the instructor specified is actually an instructor for the
    given course.
    """
    if type(course) == str:
        course = db(db.courses.course_name == course).select(db.courses.id).first()

    return db((db.course_instructor.course == course) &
             (db.course_instructor.instructor == instructor)
            ).count() > 0

class IS_COURSE_ID:
    ''' used to validate that a course name entered (e.g. devcourse) corresponds to a
        valid course ID (i.e. db.courses.id) '''
    def __init__(self, error_message='Unknown course name. Please see your instructor.'):
        self.e = error_message

    def __call__(self, value):
        if db(db.courses.course_name == value).select():
            return (db(db.courses.course_name == value).select()[0].id, None)
        return (value, self.e)

class HAS_NO_DOTS:
    def __init__(self, error_message='Your username may not contain a \' or space or any other special characters just letters and numbers'):
        self.e = error_message
    def __call__(self, value):
        if "'" not in value and " " not in value:
            return (value, None)
        return (value, self.e)
    def formatter(self, value):
        return value

db.define_table('auth_user',
    Field('username', type='string',
          label=T('Username')),
    Field('first_name', type='string',
          label=T('First Name')),
    Field('last_name', type='string',
          label=T('Last Name')),
    Field('email', type='string',
          requires=IS_EMAIL(banned='^.*shoeonlineblog\\.com$'),
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
    Field('cohort_id','reference cohort_master', requires=IS_IN_DB(db, 'cohort_master.id', 'id'),
          writable=False,readable=False),
    Field('course_id','reference courses',label=T('Course Name'),
          required=True,
          default=1),
    Field('course_name',compute=lambda row: getCourseNameFromId(row.course_id),readable=False, writable=False),
    Field('accept_tcp', required=True, type='boolean', default=True, label=T('I Accept')),
    Field('active',type='boolean',writable=False,readable=False,default=True),
    Field('donated', type='boolean', writable=False, readable=False, default=False),
#    format='%(username)s',
    format=lambda u: (u.first_name or "") + " " + (u.last_name or ''),
    migrate='runestone_auth_user.table')


db.auth_user.first_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.auth_user.last_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.auth_user.password.requires = CRYPT(key=auth.settings.hmac_key)
db.auth_user.username.requires = (HAS_NO_DOTS(), IS_NOT_IN_DB(db, db.auth_user.username))
db.auth_user.registration_id.requires = IS_NOT_IN_DB(db, db.auth_user.registration_id)
db.auth_user.email.requires = (IS_EMAIL(error_message=auth.messages.invalid_email),
                               IS_NOT_IN_DB(db, db.auth_user.email))
db.auth_user.course_id.requires = IS_COURSE_ID()

auth.define_tables(username=True, signature=False, migrate='runestone_')


## configure email
mail=auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

auth.settings.register_next = URL('default', 'index')

# change default session login time from 1 hour to 24 hours
auth.settings.expiration = 3600*24

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
#from gluon.contrib.login_methods.rpx_account import use_janrain
#use_janrain(auth,filename='private/janrain.key')
try:
    from gluon.contrib.login_methods.janrain_account import RPXAccount
except:
    print("Warning you should upgrade to a newer web2py for better janrain support")
    from gluon.contrib.login_methods.rpx_account import RPXAccount
from gluon.contrib.login_methods.extended_login_form import ExtendedLoginForm

janrain_url = 'http://%s/%s/default/user/login' % (request.env.http_host,
                                                   request.application)

db.define_table('user_courses',
                Field('user_id', db.auth_user, ondelete='CASCADE'),
                Field('course_id', db.courses, ondelete='CASCADE'),
                Field('user_id', db.auth_user),
                Field('course_id', db.courses),
                migrate='runestone_user_courses.table')
# For whatever reason the automatic migration of this table failed.  Need the following manual statements
# alter table user_courses alter column user_id type integer using user_id::integer;
# alter table user_courses alter column course_id type integer using course_id::integer;

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
## >>> for row in rows: print(row.id, row.myfield)
#########################################################################


mail.settings.server = settings.email_server
mail.settings.sender = settings.email_sender
mail.settings.login = settings.email_login

# Make sure the latest version of admin is always loaded.
adminjs =  os.path.join('applications',request.application,'static','js','admin.js')
try:
    mtime = int(os.path.getmtime(adminjs))
except:
    mtime = random.randrange(10000)

request.admin_mtime = str(mtime)

def check_for_donate_or_build(field_dict,id_of_insert):
    if 'donate' in request.vars:
        session.donate = request.vars.donate

    if 'ccn_checkbox' in request.vars:
        session.build_course = True

if 'auth_user' in db:
    db.auth_user._after_insert.append(check_for_donate_or_build)
