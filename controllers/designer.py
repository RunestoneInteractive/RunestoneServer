# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
from os import path
import os
import shutil
import sys
import re

from sphinx.application import Sphinx


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
    response.files.append(URL('static','css/dd.css'))
    response.files.append(URL('static','js/dd.js'))

    existing_course = db(db.courses.course_name == request.vars.projectname).select().first()
    if existing_course:
        return dict(mess='That name has already been used.',course_url=None, success=False)

    db.projects.update_or_insert(projectcode=request.vars.projectname,description=request.vars.projectdescription)

    if request.vars.coursetype != 'custom':

        cid = db.courses.update_or_insert(course_name=request.vars.projectname)

        # if make instructor add row to auth_membership
        if request.vars.instructor == "yes":
            gid = db(db.auth_group.role == 'instructor').select(db.auth_group.id).first()
            db.auth_membership.insert(user_id=auth.user.id,group_id=gid)

        # sourcedir holds the all sources temporarily
        # confdir holds the files needed to rebuild the course
        workingdir = request.folder
        sourcedir = path.join(workingdir,request.vars.projectname)

        if not os.path.exists(path.join(workingdir, 'custom_courses')):
            os.mkdir(path.join(workingdir, 'custom_courses'))
        confdir = path.join(workingdir, 'custom_courses', request.vars.projectname)
        if os.path.exists(sourcedir) \
                or re.search(r'[ &]',request.vars.projectname) \
                or os.path.exists(confdir):
            return dict(mess='You may not use %s for your course name'%request.vars.projectname,success=False)

        # copy all the sources into the temporary sourcedir
        shutil.copytree(path.join(workingdir,'source'),sourcedir)

        os.mkdir(confdir)

        # copy the config file. We save it in confdir (to allow rebuilding the course at a later date),
        # and we also copy it to the sourcedir (which will be used for this build and then deleted.
        shutil.copy(path.join(workingdir,request.vars.coursetype,'conf.py'),
            path.join(confdir,'conf.py'))
        shutil.copy(path.join(workingdir,request.vars.coursetype,'conf.py'),
            path.join(sourcedir,'conf.py'))

        # copy the index file. Save in confdir (to allow rebuilding the course at a later date),
        # and copy to sourcedir for this build.
        shutil.copy(path.join(workingdir,request.vars.coursetype,'index.rst'),
            path.join(confdir,'index.rst'))
        shutil.copy(path.join(workingdir,request.vars.coursetype,'index.rst'),
            path.join(sourcedir,'index.rst'))

        # set the courseid
        # set the url
        # build the book
        coursename = request.vars.projectname
        confdir = sourcedir  # the Sphinx build actually gets the conf stuff from the temp sourcedir
        outdir = path.join(request.folder, 'static' , coursename)
        doctreedir = path.join(outdir,'doctrees')
        buildername = 'html'
        confoverrides = {}
        confoverrides['html_context.appname'] = request.application
        confoverrides['html_context.course_id'] = coursename
        confoverrides['html_context.loglevel'] = 10
        confoverrides['html_context.course_url'] = 'http://' + request.env.http_host
        if request.vars.loginreq == 'yes':
            confoverrides['html_context.login_required'] = 'true'
        else:
            confoverrides['html_context.login_required'] = 'false'
        status = sys.stdout
        warning = sys.stdout
        freshenv = True
        warningiserror = False
        tags = []

        sys.path.insert(0,path.join(request.folder,'modules'))
        app = Sphinx(sourcedir, confdir, outdir, doctreedir, buildername,
                    confoverrides, status, warning, freshenv,
                    warningiserror, tags)
        force_all = True
        filenames = []
        app.build(force_all, filenames)

        shutil.copy(path.join(outdir, '_static', 'jquery-1.10.2.min.js'),
                    path.join(outdir, '_static', 'jquery.js'))

        shutil.rmtree(sourcedir)

        # enrol the user in their new course
        db(db.auth_user.id == auth.user.id).update(course_id = cid)
        auth.user.course_id = cid
        auth.user.course_name = request.vars.projectname

        return dict(mess='Your course is ready',course_url='static/'+coursename+'/index.html',success=True )
    else:
        # if make instructor add row to auth_membership
        if request.vars.instructor == "yes":
            gid = db(db.auth_group.role == 'instructor').select(db.auth_group.id).first()
            db.auth_membership.insert(user_id=auth.user.id,group_id=gid)

        moddata = {}

        rows = db(db.modules.id>0).select()
        for row in rows:
            moddata[row.id]=[row.shortname,row.description,row.pathtofile]

        buildvalues['moddata']=  moddata   #actually come from source files

        return buildvalues

def makefile():

    p = request.vars.toc

    pcode = request.vars.projectname
    row = db(db.projects.projectcode==pcode).select()
    title = row[0].description

    workingdir = request.folder
    sourcedir = path.join(workingdir ,pcode)
    confdir = path.join(workingdir, 'custom_courses', pcode)

    os.mkdir(sourcedir)
    os.mkdir(confdir)

    # The conf and index files will be archived in custom_courses/coursename
    # so that the course can be rebuilt at a later date.
    # Copy the conf.py file from devcourse into our custom course.
    shutil.copy(path.join(workingdir, 'devcourse', 'conf.py'),
                path.join(confdir, 'conf.py'))
    shutil.copy(path.join(workingdir, 'devcourse', 'conf.py'),
                path.join(sourcedir, 'conf.py'))

    # generate index.rst and copy modules from source
    f = open(path.join(sourcedir,"index.rst"),"w")

    f.write('''.. Copyright (C)  Brad Miller, David Ranum
   Permission is granted to copy, distribute and/or modify this document
   under the terms of the GNU Free Documentation License, Version 1.3 or
   any later version published by the Free Software Foundation; with
   Invariant Sections being Forward, Prefaces, and Contributor List,
   no Front-Cover Texts, and no Back-Cover Texts.  A copy of the license
   is included in the section entitled "GNU Free Documentation License".''' + "\n\n")


    f.write("="*len(title) + "\n")
    f.write(title + "\n")
    f.write("="*len(title) + "\n\n")

    toc = request.vars.toc
    parts = toc.split(" ")

    idx = 0
    while idx<len(parts):
        item = parts[idx]
        if ".rst" in item:
            f.write("   "+item+"\n")
            idx=idx+1
            moduleDir = item.split('/')[0]
            try:
                shutil.copytree(path.join(workingdir,'source',moduleDir),
                                path.join(sourcedir,moduleDir))
            except:
                print 'copying %s again' % moduleDir
        else:
            topic = ""
            while idx<len(parts) and ".rst" not in parts[idx]:
                if topic != "":
                   topic =topic + " " + parts[idx]
                else:
                    topic = topic + parts[idx]
                idx=idx+1
                    #realitem = item[5:]
            f.write("\n" + topic + "\n" + ":"*len(topic) + "\n\n")
            f.write('''.. toctree::
   :maxdepth: 2 \n\n''')



    f.write('''\nAcknowledgements
::::::::::::::::

.. toctree::
   :maxdepth: 1

   FrontBackMatter/copyright.rst
   FrontBackMatter/prefaceinteractive.rst
   FrontBackMatter/foreword.rst
   FrontBackMatter/preface.rst
   FrontBackMatter/preface2e.rst
   FrontBackMatter/contrib.rst
   FrontBackMatter/fdl-1.3.rst''' + "\n")


    f.close()

    # archive the index file so the course can be rebuilt later
    shutil.copy(path.join(sourcedir, 'index.rst'), path.join(confdir, 'index.rst'))

    shutil.copytree(path.join(workingdir,'source','FrontBackMatter'),
                                path.join(sourcedir,'FrontBackMatter'))

    coursename = pcode
    outdir = path.join(request.folder, 'static' , coursename)
    confdir = sourcedir
    doctreedir = path.join(outdir,'doctrees')
    buildername = 'html'
    confoverrides = {}
    confoverrides['html_context.appname'] = request.application
    confoverrides['html_context.course_id'] = coursename
    confoverrides['html_context.loglevel'] = 10
    confoverrides['html_context.course_url'] = 'http://' + request.env.http_host
    confoverrides['html_context.login_required'] = 'true'
    status = sys.stdout
    warning = sys.stdout
    freshenv = True
    warningiserror = False
    tags = []
    app = Sphinx(sourcedir, confdir, outdir, doctreedir, buildername,
                confoverrides, status, warning, freshenv,
                warningiserror, tags)
    force_all = True
    filenames = []
    app.build(force_all, filenames)

    shutil.copy(path.join(outdir, '_static', 'jquery-1.10.2.min.js'),
                path.join(outdir, '_static', 'jquery.js'))

    shutil.rmtree(sourcedir)

    yoururlpath=path.join('/',request.application,"static",coursename,"index.html")

    # enrol the user in their new course
    cid = db.courses.update_or_insert(course_name=request.vars.projectname)
    db(db.auth_user.id == auth.user.id).update(course_id = cid)
    auth.user.course_id = cid
    auth.user.course_name = request.vars.projectname

    return dict(message=T("Here is the link to your new eBook"),yoururl=yoururlpath)

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

