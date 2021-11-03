# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
from os import path
import random
import datetime
import logging

from requests.sessions import session

logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)

admin_logger(logger)
#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


@auth.requires_login()
def index():
    basicvalues = {}
    if settings.academy_mode:
        basicvalues["message"] = T("Build a Custom Course")
        basicvalues["descr"] = T(
            """This page allows you to select a book for your own class. You will have access to all student activities in your course.
        To begin, enter a project name below."""
        )
    return basicvalues

@auth.requires_login()
def callback():
    import requests
    oauth_url = 'https://github.com/login/oauth/access_token'
    oauth_data = {"client_id":"1d31e6dc6ff88f189241", "client_secret":"1ac9570e0d63b075382825454ca3b6e9d7149e39","code": request.vars.code}
    oauth_headers = {"Accept":"application/json"}
    #print(request.vars.code)
    try:
        oauth = requests.post(oauth_url, json=oauth_data,headers=oauth_headers)
        if oauth.status_code == 200:
            print(oauth.json()['access_token'])
            #session.auth.user['github_oauth_token']=oauth.json()['access_token']
            session.__dict__['github_oauth_token'] = oauth.json()['access_token']
            user = requests.get('https://api.github.com/user', headers = {'Authorization':'token '+oauth.json()['access_token']})
            #session.auth.user['github_user'] = user.json()['login']
            session.__dict__['github_user'] = user.json()['login']
        else:
            session.flash = (f"got {oauth.status_code} from github")
    except:
        print(f"Failure connecting to {oauth_url} There is either a problem with your servers connectivity or githubs")
    basicvalues = {}
    redirect(URL("designer", "book"))
    return basicvalues

@auth.requires_login()
def book():
    #print("loading book page")
    import requests
    #print(session.__dict__.keys())
    github={}
    session.__dict__['github_client_id'] = '1d31e6dc6ff88f189241'
    github['client_id']=session.__dict__['github_client_id']
    # try:
        # if 'github_oauth_token' in session.auth.user.keys():
        #     github['user'] = session.auth.user['github_user']
        #     github['found'] = True
    if 'github_oauth_token' in session.__dict__.keys():
        github['user'] = session.__dict__['github_user']
        github['found'] = True
        user = requests.get('https://api.github.com/user', headers = {'Authorization':'token '+session.__dict__['github_oauth_token']})
        if user.status_code != 200:
            location = "https://github.com/login/oauth/authorize?scope=repo&client_id="+session.__dict__['github_client_id']
            print("token expired, redirecting to refresh token")
            raise HTTP(303,'You are being redirected to refresh your github token', Location=location)
    else:
        github['found'] = False
    # except:
    #     github['found'] =False
    #     print("error getting github username from session variable")
    book_list = os.listdir("applications/{}/books".format(request.application))
    book_list = [book for book in book_list if ".git" not in book]
    res = []
    for book in sorted(book_list):
        # try:
        #     # WARNING: This imports from ``applications.<runestone application name>.books.<book name>``. Since ``runestone/books/<book_name>`` lacks an ``__init__.py``, it will be treated as a `namespace package <https://www.python.org/dev/peps/pep-0420/>`_. Therefore, odd things will happen if there are other modules named ``applications.<runestone application name>.books.<book name>`` in the Python path.
        #     config = importlib.import_module(
        #         "applications.{}.books.{}.conf".format(request.application, book)
        #     )
        # except Exception as e:
        #     logger.error("Error in book list: {}".format(e))
        #     continue
        book_info = {}
        book_info.update(course_description="")
        book_info.update(key_words="")
        if hasattr(config, "navbar_title"):
            book_info["title"] = config.navbar_title
        elif hasattr(config, "html_title"):
            book_info["title"] = config.html_title
        elif hasattr(config, "html_short_title"):
            book_info["title"] = config.html_short_title
        else:
            book_info["title"] = "Runestone Book"
        # update course description if found in the book's conf.py
        if hasattr(config, "course_description"):
            book_info.update(course_description=config.course_description)
        # update course key_words if found in book's conf.py
        if hasattr(config, "key_words"):
            book_info.update(key_words=config.key_words)
        book_info["url"] = "/{}/books/published/{}/index.html".format(
            request.application, book
        )
        book_info["regname"] = book
        res.append(book_info)
        print(book_info)
    return dict(book_list=res,github=github)

@auth.requires_login()
def course():
    basicvalues = {}
    if settings.academy_mode:
        """
        example action using the internationalization operator T and flash
        rendered by views/default/index.html or views/generic.html
        """
        # response.flash = "Welcome to CourseWare Manager!"

        basicvalues["message"] = T("Build a Custom Course")
        basicvalues["descr"] = T(
            """This page allows you to select a book for your own class. You will have access to all student activities in your course.
        To begin, enter a project name below."""
        )
        # return dict(message=T('Welcome to CourseWare Manager'))
    return basicvalues


@auth.requires_login()
def course_build():
    buildvalues = {}
    if settings.academy_mode:
        buildvalues["pname"] = request.vars.projectname
        buildvalues["pdescr"] = request.vars.projectdescription

        existing_course = (
            db(db.courses.course_name == request.vars.projectname).select().first()
        )
        if existing_course:
            session.flash = (
                f"course name {request.vars.projectname} has already been used"
            )
            redirect(URL("designer", "course"))

        if not request.vars.coursetype:
            session.flash = "You must select a base course."
            redirect(URL("designer", "course"))

        # if make instructor add row to auth_membership
        if "instructor" in request.vars:
            gid = (
                db(db.auth_group.role == "instructor").select(db.auth_group.id).first()
            )
            db.auth_membership.insert(user_id=auth.user.id, group_id=gid)

        base_course = request.vars.coursetype

        if request.vars.startdate == "":
            request.vars.startdate = datetime.date.today()
        else:
            date = request.vars.startdate.split("/")
            request.vars.startdate = datetime.date(
                int(date[2]), int(date[0]), int(date[1])
            )

        if not request.vars.institution:
            institution = "Not Provided"
        else:
            institution = request.vars.institution

        if not request.vars.courselevel:
            courselevel = "unknown"
        else:
            courselevel = request.vars.courselevel

        python3 = "true"

        if not request.vars.loginreq:
            login_required = "false"
        else:
            login_required = "true"

        cid = db.courses.update_or_insert(
            course_name=request.vars.projectname,
            term_start_date=request.vars.startdate,
            institution=institution,
            base_course=base_course,
            login_required=login_required,
            python3=python3,
            courselevel=courselevel,
        )

        if request.vars.invoice:
            db.invoice_request.insert(
                timestamp=datetime.datetime.now(),
                sid=auth.user.username,
                email=auth.user.email,
                course_name=request.vars.projectname,
            )

        # enrol the user in their new course
        db(db.auth_user.id == auth.user.id).update(course_id=cid)
        db.course_instructor.insert(instructor=auth.user.id, course=cid)
        auth.user.update(
            course_name=request.vars.projectname
        )  # also updates session info
        auth.user.update(course_id=cid)
        db.executesql(
            """
            INSERT INTO user_courses(user_id, course_id)
            SELECT %s, %s
            """,
            (auth.user.id, cid),
        )

        session.flash = "Course Created Successfully"
        # redirect(
        #     URL("books", "published", args=[request.vars.projectname, "index.html"])
        # )

        return dict(coursename=request.vars.projectname, basecourse=base_course)
