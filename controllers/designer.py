# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
from os import path
import shutil
import random

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
        """
        example action using the internationalization operator T and flash
        rendered by views/default/index.html or views/generic.html
        """
        #response.flash = "Welcome to CourseWare Manager!"

        basicvalues["message"]=T('Build a Custom Course')
        basicvalues["descr"]=T('''This page allows you to select a book for your own class. You will have access to all student activities in your course.
        To begin, enter a project name below.''')
        #return dict(message=T('Welcome to CourseWare Manager'))
    return basicvalues

def build():
    buildvalues = {}
    if settings.academy_mode:
        buildvalues['pname']=request.vars.projectname
        buildvalues['pdescr']=request.vars.projectdescription

        existing_course = db(db.courses.course_name == request.vars.projectname).select().first()
        if existing_course:
            return dict(mess='That name has already been used.', building=False)


        # if make instructor add row to auth_membership
        if 'instructor' in request.vars:
            gid = db(db.auth_group.role == 'instructor').select(db.auth_group.id).first()
            db.auth_membership.insert(user_id=auth.user.id,group_id=gid)

        if request.vars.coursetype != 'custom':
            # todo:  Here we can add some processing to check for an A/B testing course
            if path.exists(path.join(request.folder,'books',request.vars.coursetype+"_A")):
                base_course = request.vars.coursetype + "_" + random.sample("AB",1)[0]
            else:
                base_course = request.vars.coursetype

            if request.vars.startdate == '':
                request.vars.startdate = datetime.date.today()
            else:
                date = request.vars.startdate.split('/')
                request.vars.startdate = datetime.date(int(date[2]), int(date[0]), int(date[1]))

            if not request.vars.institution:
                institution = "Not Provided"
            else:
                institution = request.vars.institution

            if not request.vars.python3:
                python3 = 'false'
            else:
                python3 = 'true'

            if not request.vars.loginreq:
                login_required = 'false'
            else:
                login_required = 'true'

            cid = db.courses.update_or_insert(course_name=request.vars.projectname,
                                              term_start_date=request.vars.startdate,
                                              institution=institution,
                                              base_course=base_course,
                                              login_required = login_required,
                                              python3=python3)


            # enrol the user in their new course
            db(db.auth_user.id == auth.user.id).update(course_id = cid)
            db.course_instructor.insert(instructor=auth.user.id, course=cid)
            auth.user.update(course_name=request.vars.projectname)  # also updates session info
            auth.user.update(course_id=cid)
            db.executesql('''
                INSERT INTO user_courses(user_id, course_id)
                SELECT %s, %s
                ''' % (auth.user.id, cid))

            # Create a default section for this course and add the instructor.
            sectid = db.sections.update_or_insert(name='default',course_id=cid)
            db.section_users.update_or_insert(auth_user=auth.user.id,section=sectid)

            course_url=path.join('/',request.application,"static",request.vars.projectname,"index.html")

            session.flash = "Course Created Successfully"
            redirect(URL('books', 'published', args=[request.vars.projectname, 'index.html']))

        else:
            moddata = {}

            rows = db(db.modules.id>0).select()
            for row in rows:
                moddata[row.id]=[row.shortname,row.description,row.pathtofile]

            buildvalues['moddata']=  moddata   #actually come from source files
            buildvalues['startdate'] = request.vars.startdate
            buildvalues['loginreq'] = request.vars.loginreq

        return buildvalues


@auth.requires_membership('instructor')
def delete_course():
    if settings.academy_mode:
        verify_form = FORM(TABLE(TR(LABEL("Really Delete:", INPUT(_name='checkyes', requires=IS_NOT_EMPTY(), _type="checkbox"))),
                           TR(LABEL("Type in the name of the course to verify: ", INPUT(_name='coursename', requires=IS_NOT_EMPTY() ))),
                           TR(INPUT(_type='submit')),
                           labels=''))

        deleted = False
        if verify_form.process().accepted and request.vars.checkyes == 'on':
            course_name = request.vars.coursename
            cset = db(db.courses.course_name == course_name)
            if not cset.isempty():
                courseid = cset.select(db.courses.id).first()
                print('courseid = ', courseid)
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
                        session.clear()
                    except:
                        response.flash = '%s does not appear to have static content' % course_name
                else:
                    response.flash = 'You are not the instructor of %s' % course_name
            else:
                response.flash = 'course, %s, not found' % course_name
        else:
            response.flash = 'Must Check the checkbox'

    return dict(verify_form=verify_form, deleted=deleted)
