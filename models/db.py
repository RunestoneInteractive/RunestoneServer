# *************************************
# |docname| - Core tables and functions
# *************************************
import os
import random
import re

from gluon import current
import logging


logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
# from gluon.contrib.login_methods.rpx_account import use_janrain
# use_janrain(auth,filename='private/janrain.key')
try:
    from gluon.contrib.login_methods.janrain_account import RPXAccount
except ImportError:
    print("Warning you should upgrade to a newer web2py for better janrain support")
    from gluon.contrib.login_methods.rpx_account import RPXAccount  # noqa: F401

from gluon.contrib.login_methods.extended_login_form import (  # noqa: F401
    ExtendedLoginForm,
)

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate  # noqa: F401

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_htps()

table_migrate_prefix = "runestone_"
table_migrate_prefix_test = ""
if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    if os.environ.get("WEB2PY_CONFIG", "") == "test":
        db = DAL(
            settings.database_uri,
            migrate=False,
            pool_size=5,
            adapter_args=dict(logfile="test_runestone_migrate.log"),
        )
        table_migrate_prefix = "test_runestone_"
        table_migrate_prefix_test = table_migrate_prefix
    else:
        # WEB2PY_MIGRATE is either "Yes", "No", "Fake", or missing
        db = DAL(
            settings.database_uri,
            pool_size=30,
            fake_migrate_all=(os.environ.get("WEB2PY_MIGRATE", "Yes") == "Fake"),
            migrate=False,
            migrate_enabled=(
                os.environ.get("WEB2PY_MIGRATE", "Yes") in ["Yes", "Fake"]
            ),
        )
    session.connect(
        request,
        response,
        db,
        masterapp=None,
        migrate=table_migrate_prefix + "web2py_sessions.table",
    )

else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL("google:datastore")
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

# For LTI you may want to open Runestone in an iframe.  This is tricky
# and can run afoul of browser settings that disable 3rd party tracking.
# However this seems to do the trick at least from the test tool at
# https://lti.tools/saltire/tc - More testing with Canvas and Company
# is required.  The Content Request launch also works in an iframe.
if "https" in settings.server_type:
    session.secure()
    if settings.lti_iframes is True:
        session.samesite("None")


# This seems like it should allow us to share the session cookie across subdomains.
# and seems to work for every browser except for Safari
# I'm  not sure what the issue is... So I'm commenting it out until I understand what is gong on.

# if settings.session_domain and "session_id_runestone" in response.cookies:
#    response.cookies["session_id_runestone"]["domain"] = settings.session_domain

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ["*"] if request.is_local else []
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


auth = Auth(db, hmac_key=Auth.get_or_create_key())
crud, service, plugins = Crud(db), Service(), PluginManager()

# Make the settings and database available in modules.
current.db = db
current.settings = settings
current.auth = auth

if settings.enable_captchas:
    ## Enable captcha's :-(
    from gluon.tools import Recaptcha

    auth.settings.captcha = Recaptcha(
        request,
        "6Lfb_t4SAAAAAB9pG_o1CwrMB40YPsdBsD8GsvlD",
        "6Lfb_t4SAAAAAGvAHwmkahQ6s44478AL5Cf-fI-x",
        options="theme:'blackglass'",
    )

auth.settings.login_captcha = False
auth.settings.retrieve_password_captcha = False
auth.settings.retrieve_username_captcha = False

# Set up for `two-factor authentication <http://web2py.com/books/default/chapter/29/09/access-control#Two-step-verification>`_.
# auth.settings.auth_two_factor_enabled = True
# auth.settings.two_factor_methods = [lambda user, auth_two_factor: 'password_here']

if os.environ.get("WEB2PY_CONFIG", "") == "production":
    SELECT_CACHE = dict(cache=(cache.ram, 3600), cacheable=True)
    COUNT_CACHE = dict(cache=(cache.ram, 3600))
else:
    SELECT_CACHE = {}
    COUNT_CACHE = {}

# .. _courses table:
#
# ``courses`` table
# =================
## create all tables needed by auth if not custom tables
db.define_table(
    "courses",
    Field("course_name", "string", unique=True),
    Field("term_start_date", "date"),
    Field("institution", "string"),
    Field("base_course", "string"),
    Field("python3", type="boolean", default=True),
    Field("login_required", type="boolean", default=True),
    Field("allow_pairs", type="boolean", default=False),
    Field("student_price", type="integer"),
    Field("downloads_enabled", type="boolean", default=False),
    Field("courselevel", type="string"),
    migrate=table_migrate_prefix + "courses.table",
)


# Provide a common query. Pass ``db.courses.ALL`` to retrieve all fields; otherwise, only the ``course_name`` and ``base_course`` are selected.
def get_course_row(*args, **kwargs):
    if not args:
        args = db.courses.course_name, db.courses.base_course
    return db(db.courses.id == auth.user.course_id).select(*args).first()


# Make this available to modules.
current.get_course_row = get_course_row


# Provide the correct URL to a book, based on if it's statically or dynamically served. This function return URL(*args) and provides the correct controller/function based on the type of the current course (static vs dynamic).
def get_course_url(*args):
    # Redirect to old-style statically-served books if it exists; otherwise, use the dynamically-served controller.
    if os.path.exists(os.path.join(request.folder, "static", auth.user.course_name)):
        return URL("static", "/".join((auth.user.course_name,) + args))
    else:
        course = (
            db(db.courses.id == auth.user.course_id)
            .select(db.courses.base_course)
            .first()
        )
        args = tuple(x for x in args if x != "")
        if course:
            return URL(c="books", f="published", args=(course.base_course,) + args)
        else:
            return URL(c="default")


########################################


def getCourseNameFromId(courseid):
    """ used to compute auth.user.course_name field """
    q = db.courses.id == courseid
    row = db(q).select().first()
    return row.course_name if row else ""


def getCourseOrigin(base_course):
    res = (
        db(
            (db.course_attributes.course_id == db.courses.id)
            & (db.courses.course_name == base_course)
            & (db.course_attributes.attr == "markup_system")
        )
        .select(db.course_attributes.value, **SELECT_CACHE)
        .first()
    )
    return res


def getCourseAttributesDict(course_id):
    attributes = db(db.course_attributes.course_id == course_id).select(**SELECT_CACHE)
    attrdict = {row.attr: row.value for row in attributes}
    return attrdict

###############################################
#############################################
###########################################

def verifyInstructorStatus(course, instructor):
    """
    Make sure that the instructor specified is actually an instructor for the
    given course.
    """
    res = False
    if type(course) == str:
        course = (
            db(db.courses.course_name == course)
            .select(db.courses.id, **SELECT_CACHE)
            .first()
        )

    try:
        res = (
            db(
                (db.course_instructor.course == course)
                & (db.course_instructor.instructor == instructor)
            ).count(**COUNT_CACHE)
            > 0
        )
    except Exception as e:
        logger.error(f"VIS -- {e}")
        db.rollback()
        res = (
            db(
                (db.course_instructor.course == course)
                & (db.course_instructor.instructor == instructor)
            ).count(**COUNT_CACHE)
            > 0
        )

    return res


def is_editor(userid):
    ed = db(db.auth_group.role == "editor").select(db.auth_group.id).first()
    row = (
        db((db.auth_membership.user_id == userid) & (db.auth_membership.group_id == ed))
        .select()
        .first()
    )

    if row:
        return True
    else:
        return False


class IS_COURSE_ID:
    """used to validate that a course name entered (e.g. devcourse) corresponds to a
    valid course ID (i.e. db.courses.id)"""

    def __init__(
        self, error_message="Unknown course name. Please see your instructor."
    ):
        self.e = error_message

    def __call__(self, value):
        if db(db.courses.course_name == value).select():
            return (db(db.courses.course_name == value).select()[0].id, None)
        return (db(db.courses.course_name == 'boguscourse').select()[0].id, None)



# Do not allow any of the reserved CSS characters in a username.
class HAS_NO_DOTS:
    def __init__(
        self,
        error_message=r"""Your username may not contain spaces or any other special characters: !"#$%&'()*+,./:;<=>?@[\]^`{|}~ just letters and numbers""",
    ):
        self.e = error_message

    def __call__(self, value):
        match = re.search(r"""[!"#$%&'()*+,./:;<=>?@[\]^`{|}~ ]""", value)
        if match:
            exist = db(db.auth_user.username == value).count()
            if exist > 0:  # user already registered give them a pass
                return (value, None)
            self.e = f"""Your username may not contain a {match.group(0).replace(" ","space")} or any other special characters except - or _"""
            return (value, self.e)
        return (value, None)

    def formatter(self, value):
        return value


###############################################################################

db.define_table(
    "auth_user",
    Field("username", type="string", label=T("Username")),
    Field("first_name", type="string", label=T("First Name")),
    Field("last_name", type="string", label=T("Last Name")),
    Field(
        "email",
        type="string",
        requires=IS_EMAIL(banned="^.*shoeonlineblog\\.com$"),
        label=T("Email"),
    ),
    Field("institution", type="string", label=T("Institution Name")),
    Field("faculty_url", type="string", label=T("Faculty URL")),
    Field("password", type="password", readable=False, label=T("Password")),
    Field(
        "created_on",
        "datetime",
        default=request.now,
        label=T("Created On"),
        writable=False,
        readable=False,
    ),
    Field(
        "modified_on",
        "datetime",
        default=request.now,
        label=T("Modified On"),
        writable=False,
        readable=False,
        update=request.now,
    ),
    Field("registration_key", default="", writable=False, readable=False),
    Field("reset_password_key", default="", writable=False, readable=False),
    Field("registration_id", default="", writable=False, readable=False),
    Field(
        "course_id",
        "reference courses",
        label=T("Course Name"),
        required=False,
        default=1,
    ),
    Field(
        "course_name",
        compute=lambda row: getCourseNameFromId(row.course_id),
        readable=False,
        writable=False,
    ),
    Field(
        "accept_tcp", required=True, type="boolean", default=True, label=T("I Accept")
    ),
    Field("active", type="boolean", writable=False, readable=False, default=True),
    Field("donated", type="boolean", writable=False, readable=False, default=False),
    #    format='%(username)s',
    format=lambda u: (u.first_name or "") + " " + (u.last_name or ""),
    migrate=table_migrate_prefix + "auth_user.table",
)


db.auth_user.first_name.requires = IS_NOT_EMPTY(error_message='cannot be empty')
db.auth_user.last_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.auth_user.password.requires = CRYPT(key=auth.settings.hmac_key)
db.auth_user.username.requires = (
    HAS_NO_DOTS(),
    IS_NOT_IN_DB(db, db.auth_user.username),
)
db.auth_user.institution.requires =  IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.auth_user.faculty_url.requires =  IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.auth_user.registration_id.requires = IS_NOT_IN_DB(db, db.auth_user.registration_id)
db.auth_user.email.requires = (
    IS_EMAIL(error_message=auth.messages.invalid_email),
    IS_NOT_IN_DB(db, db.auth_user.email),
)
db.auth_user.course_id.requires = IS_COURSE_ID()

auth.define_tables(username=True, signature=False, migrate=table_migrate_prefix + "")

# Because so many pages rely on `views/_sphinx_static_file.html` it makes
# sense to provide some default values for variables used in the template here
# The latex_preamble attribute can be used for any custom latex macros used in
# the text, that need to be available for grading, assignments, and practice
# This is used in nearly every PreTeXt book.
request.latex_preamble = ""


def set_latex_preamble(base_course: str):
    # See `models/db_ebook.py` for course_attributes table
    bc = db(db.courses.course_name == base_course).select().first()
    res = (
        db(
            (db.course_attributes.course_id == bc.id)
            & (db.course_attributes.attr == "latex_macros")
        )
        .select()
        .first()
    )
    request.latex_preamble = res.value if res else ""


## configure email
mail = auth.settings.mailer
mail.settings.server = settings.email_server
mail.settings.sender = settings.email_sender
mail.settings.login = settings.email_login

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

auth.settings.register_next = URL("default", "index")

# change default session login time from 1 hour to 24 hours
auth.settings.expiration = 3600 * 24


janrain_url = "http://%s/%s/default/user/login" % (
    request.env.http_host,
    request.application,
)

db.define_table(
    "user_courses",
    Field("user_id", db.auth_user, ondelete="CASCADE"),
    Field("course_id", db.courses, ondelete="CASCADE"),
    Field("user_id", db.auth_user),
    Field("course_id", db.courses),
    migrate=table_migrate_prefix + "user_courses.table",
)
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


# mail.settings.server = settings.email_server
# mail.settings.sender = settings.email_sender
# mail.settings.login = settings.email_login
auth.messages.retrieve_username_subject = "Runestone Academy username"
auth.messages.reset_password_subject = "Runestone Academy password"
auth.messages.retrieve_username = """<html>
Hello,
<br>
<p>We received your request to retrieve your username.  According to our files
Your username is: %(username)s </p>

<p>If you have any trouble with this automated system you can also ask your instructor 
and they can help you retrieve your username or reset your password.  If you are
an instructor, you can  (as a last resort) contact Runestone by creating an issue
on  <a href="https://github.com/RunestoneInteractive/RunestoneServer/issues">Github</a>.</p>

<p>This message was generated automatically and comes from an unmonitored email address.  If you reply to this message a human will not see it.  Use the github link above if you need help from a real person.</p>

Thanks for using Runestone!<br><br>

Brad Miller
</html>
"""
auth.messages.reset_password = """<html>
Hello, <br>

<p>If you click on <a href="%(link)s">this link</a> you will reset your password.  Sometimes schools have software that tries to sanitize the previous link and makes it useless.</p>

<p>If you have any trouble with the link you can also ask your instructor 
and they can help you retrieve your username or reset your password.  If you are
an instructor, you can  (as a last resort) contact Runestone by creating an issue
on <a href="https://github.com/RunestoneInteractive/RunestoneServer/issues">Github</a>.</p>

<p>This message was generated automatically and comes from an unmonitored email address.  If you reply to this message a human will not see it.  Use the github link above if you need help from a real person.</p>

Thanks for using Runestone!<br><br>

Brad Miller
</html>
"""

# Make sure the latest version of admin is always loaded.
adminjs = os.path.join("applications", request.application, "static", "js", "admin.js")
try:
    mtime = int(os.path.getmtime(adminjs))
except FileNotFoundError:
    mtime = random.randrange(10000)

request.admin_mtime = str(mtime)

# response.headers["Access-Control-Allow-Origin"] = "*"


def check_for_donate_or_build(field_dict, id_of_insert):
    if "donate" in request.vars:
        session.donate = request.vars.donate

    if "ccn_checkbox" in request.vars:
        session.build_course = True


if "auth_user" in db:
    db.auth_user._after_insert.append(check_for_donate_or_build)


def admin_logger(logger):
    if settings.academy_mode:
        if auth.user:
            sid = auth.user.username
            course = auth.user.course_name
        else:
            sid = "Anonymous"
            course = "Unknown"
        try:
            db.useinfo.insert(
                sid=sid,
                act=request.function,
                div_id=request.env.query_string or "no params",
                event=request.controller,
                timestamp=datetime.datetime.utcnow(),
                course_id=course,
            )
        except Exception as e:
            logger.error(f"failed to insert log record for practice: {e}")


def createUser(username, password, fname, lname, email, institution, faculty_url='', course_name='boguscourse', instructor=False):
    cinfo = db(db.courses.course_name == course_name).select().first()
    if not cinfo:
        raise ValueError("Course {} does not exist".format(course_name))
    pw = CRYPT(auth.settings.hmac_key)(password)[0]
    uid = db.auth_user.insert(
        username=username,
        password=pw,
        first_name=fname,
        last_name=lname,
        email=email,
        institution=institution,
        course_name=course_name,
        faculty_url=faculty_url,
        active="T",
        created_on=datetime.datetime.now(),
        course_id=cinfo.id,
    )
    db.user_courses.insert(user_id=uid, course_id=cinfo.id)
    
    if instructor:
        irole = db(db.auth_group.role == "instructor").select(db.auth_group.id).first()
        db.auth_membership.insert(user_id=uid, group_id=irole)
        auth.login_user(db.auth_user(uid))
    
def validateUser(username, password, fname, lname, email, institution, faculty_url):
    """used to validate user's credentials and create a list of errors"""

    errors = [] 

    match = re.search(r"""[!"#$%&'()*+,./:;<=>?@[\]^`{|}~ ]""", username)
    if match:
        errors.append(
            f"""Username cannot contain a {match.group(0).replace(" ", "space")} on line """
        )
    uinfo = db(db.auth_user.username == username).count()
    if uinfo > 0:
        errors.append("Username {username} already exists on line ")
    if fname == "":
        errors.append("First name cannot be blank on line ")
    if lname == "":
        errors.append(f"Last name cannot be blank on line ")
    if institution == "":
        errors.append(f"Institution name cannot be blank on line ")
    if faculty_url == "":
        errors.append(f"Faculty URL cannot be blank on line ")
    if password == "":
        errors.append(f"Password cannot be blank on line ")
    if "@" not in email:
        errors.append(f"Email address missing @ on line ")

    return errors
