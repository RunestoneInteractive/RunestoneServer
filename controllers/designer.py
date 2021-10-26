# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
from os import path
import random
import datetime
import logging

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
    import json
    oauth_url = 'https://github.com/login/oauth/access_token'
    oauth_data = {"client_id":"1d31e6dc6ff88f189241", "client_secret":"1ac9570e0d63b075382825454ca3b6e9d7149e39","code": request.vars.code}
    oauth_headers = {"Accept":"application/json"} 
    oauth = requests.post(oauth_url, json=oauth_data,headers=oauth_headers )
    #access_token = oauth.json()['access_token']
    basicvalues = {}
    #session.flash = (f"course name {access_token} has already been used")
    redirect(URL("designer", "book"))
    return basicvalues

@auth.requires_login()
def book():
    basicvalues = {}
    if settings.academy_mode:
        basicvalues["message"] = T("Build a Custom Course")
        basicvalues["descr"] = T(
            """This page allows you to select a book for your own class. You will have access to all student activities in your course.
        To begin, enter a project name below."""
        )
    return basicvalues

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
