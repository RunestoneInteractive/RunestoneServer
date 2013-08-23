# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
from os import path
import uuid
import shutil

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    #response.flash = "Welcome to CourseWare Manager!"

    basicvalues = {}
    basicvalues["message"]=T('Welcome to CourseWare Builder')
    basicvalues["descr"]=T('''This tool allows you to create your own courseware by choosing from a catalog of modules.
    To begin, enter a project name below.''')
    #return dict(message=T('Welcome to CourseWare Manager'))
    return basicvalues

def build():
    buildvalues = {}
    buildvalues['pname']=request.vars.projectname
    buildvalues['pdescr']=request.vars.projectdescription

    existing_course = db(db.courses.course_name == request.vars.projectname).select().first()
    if existing_course:
        return dict(mess='That name has already been used.', building=False)


    db.projects.update_or_insert(projectcode=request.vars.projectname,description=request.vars.projectdescription)

    # if make instructor add row to auth_membership
    if 'instructor' in request.vars:
        gid = db(db.auth_group.role == 'instructor').select(db.auth_group.id).first()
        db.auth_membership.insert(user_id=auth.user.id,group_id=gid)

    if request.vars.coursetype != 'custom':
        # run_sphinx is defined in models/scheduler.py
        row = scheduler.queue_task(run_sphinx, timeout=300, pvars=dict(folder=request.folder,
                                                                       rvars=request.vars,
                                                                       application=request.application,
                                                                       http_host=request.env.http_host))
        uuid = row['uuid']

        if request.vars.startdate == '':
            request.vars.startdate = datetime.date.today()
        else:
            date = request.vars.startdate.split('/')
            request.vars.startdate = datetime.date(int(date[2]), int(date[0]), int(date[1]))

        cid = db.courses.update_or_insert(course_name=request.vars.projectname, term_start_date=request.vars.startdate)

        # enrol the user in their new course
        db(db.auth_user.id == auth.user.id).update(course_id = cid)
        db.course_instructor.insert(instructor=auth.user.id, course=cid)
        auth.user.course_id = cid
        auth.user.course_name = request.vars.projectname

        course_url=path.join('/',request.application,"static",request.vars.projectname,"index.html")

        return(dict(success=False,
                    building=True,
                    task_name=uuid,
                    mess='Building your course.',
                    course_url=course_url))

    else:
        moddata = {}

        rows = db(db.modules.id>0).select()
        for row in rows:
            moddata[row.id]=[row.shortname,row.description,row.pathtofile]

        buildvalues['moddata']=  moddata   #actually come from source files
        buildvalues['startdate'] = request.vars.startdate
        buildvalues['loginreq'] = request.vars.loginreq

        return buildvalues

def build_custom():
    # run_sphinx is defined in models/scheduler.py
    row = scheduler.queue_task(run_sphinx, timeout=300, pvars=dict(folder=request.folder,
                                                                   rvars=request.vars,
                                                                   application=request.application,
                                                                   http_host=request.env.http_host))
    uuid = row['uuid']

    course_url=path.join('/',request.application,"static",request.vars.projectname,"index.html")

    if request.vars.startdate == '':
        request.vars.startdate = datetime.date.today()
    else:
        date = request.vars.startdate.split('/')
        request.vars.startdate = datetime.date(int(date[2]), int(date[0]), int(date[1]))

    cid = db.courses.update_or_insert(course_name=request.vars.projectname, term_start_date=request.vars.startdate)

    # enrol the user in their new course
    db(db.auth_user.id == auth.user.id).update(course_id = cid)
    db.course_instructor.insert(instructor=auth.user.id, course=cid)
    auth.user.course_id = cid
    auth.user.course_name = request.vars.projectname

    return(dict(success=False,
                building=True,
                task_name=uuid,
                mess='Building your course.',
                course_url=course_url))

@auth.requires_membership('instructor')
def delete_course():

    verify_form = FORM(TABLE(TR(LABEL("Really Delete:", INPUT(_name='checkyes', requires=IS_NOT_EMPTY(), _type="checkbox"))),
                       TR(LABEL("Type in the name of the course to verify: ", INPUT(_name='coursename', requires=IS_NOT_EMPTY() ))),
                       TR(INPUT(_type='submit')),
                       labels=''))
    print 'in delete', request.vars
    deleted = False
    if verify_form.process().accepted and request.vars.checkyes == 'on':
        course_name = request.vars.coursename
        cset = db(db.courses.course_name == course_name)
        if not cset.isempty():
            courseid = cset.select(db.courses.id).first()
            print 'courseid = ', courseid
            qset = db((db.course_instructor.course == courseid) & (db.course_instructor.instructor == auth.user.id) )
            if not qset.isempty():
                qset.delete()
                students = db(db.auth_user.course_id == courseid)
                students.update(course_id=1)
                db(db.courses.id == courseid).delete()
                try:
                    shutil.rmtree(path.join('applications',request.application,'static', course_name))
                    shutil.rmtree(path.join('applications',request.application,'custom_courses', course_name))
                    deleted = True
                except:
                    response.flash = 'Error, %s does not appear to exist' % course_name
            else:
                response.flash = 'You are not the instructor of %s' % course_name
        else:
            response.flash = 'course, %s, not found' % course_name
    else:
        response.flash = 'Must Check the checkbox'


    return dict(verify_form=verify_form, deleted=deleted)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

