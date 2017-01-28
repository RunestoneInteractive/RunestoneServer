# -*- coding: utf-8 -*-
### required - do not delete
import cgi
import json
import os
import requests
from urllib import unquote
from urllib2 import HTTPError
from gluon.restricted import RestrictedError
def user():
    # this is kinda hacky but it's the only way I can figure out how to pre-populate
    # the course_id field

    if 'everyday' in request.env.http_host:
        redirect('http://interactivepython.org/runestone/everyday')

    if not request.args(0):
        redirect(URL('default', 'user/login'))

    if 'register' in request.args(0):
        # If we can't pre-populate, just set it to blank.
        # This will force the user to choose a valid course name
        db.auth_user.course_id.default = ''

        # Otherwise, use the referer URL to try to pre-populate
        ref = request.env.http_referer
        if ref:
            ref = unquote(ref)
            if '_next' in ref:
                ref = ref.split("_next")
                url_parts = ref[1].split("/")
            else:
                url_parts = ref.split("/")

            for i in range(len(url_parts)):
                if "static" in url_parts[i]:
                    course_name = url_parts[i+1]
                    db.auth_user.course_id.default = course_name
                    break
    try:
        form = auth()
    except HTTPError:
        session.flash = "Sorry, that service failed.  Try a different service or file a bug"
        redirect(URL('default', 'index'))

    if 'profile' in request.args(0):
        try:
            sect = db(db.section_users.auth_user == auth.user.id).select(db.section_users.section).first().section
            sectname = db(db.sections.id == sect).select(db.sections.name).first()
        except:
            sectname = None
        if sectname:
            sectname = sectname.name
        else:
            sectname = 'default'
        my_extra_element = TR(LABEL('Section Name'),
                           INPUT(_name='section', value=sectname, _type='text'))
        form[0].insert(-1, my_extra_element)
        form.element('#auth_user_username')['_readonly']=True

    if 'register' in request.args(0) and request.janrain_form:
        # add the Janrain login form
        form[0][5][2] = ''
        form = (DIV(form, request.janrain_form.login_form()))


    if 'profile' in request.args(0):
        form.vars.course_id = auth.user.course_name
        if form.process().accepted:
            # auth.user session object doesn't automatically update when the DB gets updated
            auth.user.update(form.vars)
            auth.user.course_name = db(db.auth_user.id == auth.user.id).select()[0].course_name
            #problem is that
            inDB = db((db.user_courses.user_id == auth.user.id) & (db.user_courses.course_id == auth.user.course_id)).select()
            DBcheck = []
            for row in inDB:
                DBcheck.append(row)
            if DBcheck == []:
                db.executesql('''
                    INSERT INTO user_courses(user_id, course_id)
                    SELECT %s, %s
                    ''' % (auth.user.id, auth.user.course_id))
            res = db(db.chapters.course_id == auth.user.course_name)
            if res.count() > 0:
                chapter_label = res.select().first().chapter_label
                if db((db.user_sub_chapter_progress.user_id == auth.user.id) &
                      (db.user_sub_chapter_progress.chapter_id == chapter_label)).count() == 0:
                    db.executesql('''
                       INSERT INTO user_sub_chapter_progress(user_id, chapter_id,sub_chapter_id, status)
                       SELECT %s, chapters.chapter_label, sub_chapters.sub_chapter_label, -1
                       FROM chapters, sub_chapters where sub_chapters.chapter_id = chapters.id and chapters.course_id = '%s';
                    ''' % (auth.user.id, auth.user.course_name))
            else:
                session.flash = 'This course is not set up for tracking progress'
            # Add user to default section for course.
            sect = db((db.sections.course_id == auth.user.course_id) &
                      (db.sections.name == form.vars.section)).select(db.sections.id).first()
            if sect:
                x = db.section_users.update_or_insert(auth_user=auth.user.id, section=sect)
                db((auth.user.id == db.section_users.auth_user) & ((db.section_users.section != sect) | (db.section_users.section == None))).delete()
            # select from sections where course_id = auth_user.course_id and section.name = 'default'
            # add a row to section_users for this user with the section selected.
            redirect(URL('default', 'index'))

    if 'login' in request.args(0):
        # add info text re: using local auth. CSS styled to match text on Janrain form
        sign_in_text = TR(TD('Sign in with your Runestone Interactive account', _colspan='3'), _id='sign_in_text')
        usernamewarn = TR(TD('Your username is NOT your email address', _colspan='3') )
        form[0][0].insert(0, usernamewarn)
        form[0][0].insert(0, sign_in_text)

    # this looks horrible but it seems to be the only way to add a CSS class to the submit button
    try:
        form.element(_id='submit_record__row')[1][0]['_class']='btn btn-default'
    except AttributeError: # not all auth methods actually have a submit button (e.g. user/not_authorized)
        pass

    return dict(form=form)

def download(): return response.download(request,db)
def call(): return service()
### end requires

@auth.requires_login()
def index():
    course = db(db.courses.id == auth.user.course_id).select(db.courses.course_name).first()

    if not course or 'boguscourse' in course.course_name:
        # if login was handled by Janrain, user didn't have a chance to choose the course_id;
        # redirect them to the profile page to choose one
        redirect('/%s/default/user/profile?_next=/%s/default/index' % (request.application, request.application))
    else:
        inDB = db((db.user_courses.user_id == auth.user.id) & (db.user_courses.course_id == auth.user.course_id)).select()
        DBcheck = []
        for row in inDB:
            DBcheck.append(row)
        if DBcheck == []:
            db.executesql('''
                    INSERT INTO user_courses(user_id, course_id)
                    SELECT %s, %s
                    ''' % (auth.user.id, auth.user.course_id))
        try:
            chapter_label = db(db.chapters.course_id == auth.user.course_name).select()[0].chapter_label
            if db(db.user_sub_chapter_progress.user_id == auth.user.id).count() == 0:
                if db((db.user_sub_chapter_progress.user_id == auth.user.id) & (
                            db.user_sub_chapter_progress.chapter_id == chapter_label)).count() == 0:
                    db.executesql('''
                       INSERT INTO user_sub_chapter_progress(user_id, chapter_id,sub_chapter_id, status)
                       SELECT %s, chapters.chapter_label, sub_chapters.sub_chapter_label, -1
                       FROM chapters, sub_chapters where sub_chapters.chapter_id = chapters.id and chapters.course_id = '%s';
                    ''' % (auth.user.id, auth.user.course_name))
        except:
            session.flash = "Your course is not set up to track your progress"
        #todo:  check course.course_name make sure it is valid if not then redirect to a nicer page.

        #check number of classes, if more than 1, send to course selection, if only 1, send to book
        courseCheck = db(db.user_courses.user_id == auth.user.id).select()
        numCourses = 0
        for row in courseCheck:
            numCourses += 1
        if numCourses == 1:
            redirect('/%s/static/%s/index.html' % (request.application, course.course_name))
        redirect('/%s/default/courses' % request.application)

    cohortId = db(db.auth_user.id == auth.user.id).select(db.auth_user.cohort_id).first()

def error():
    return dict()

def about():
    return dict()

def ack():
    return dict()


@auth.requires_login()
def bio():
    existing_record = db(db.user_biography.user_id == auth.user.id).select().first()
    db.user_biography.laptop_type.widget = SQLFORM.widgets.radio.widget
    form = SQLFORM(db.user_biography, existing_record,
        showid = False,
        fields=['prefered_name', 'interesting_fact', 'programming_experience', 'laptop_type', 'image'],
        keepvalues = True,
        upload=URL('download'),
        formstyle='table3cols',
        col3={'prefered_name': "Name you would like to be called by in class. Pronunciation hints are also welcome!",
              'interesting_fact': "Tell me something interesting about your outside activities that you wouldn't mind my mentioning in class. For example, are you the goalie for the UM soccer team? An officer in a club or fraternity? An expert on South American insects? Going into the Peace Corps after graduation? Have a company that you started last summer? Have an unusual favorite color?",
              'programming_experience': "Have you ever done any programming before? If so, please describe briefly. (Note: no prior programming experience is required for this course. I just like to know whether you have programmed before.)",
              'image': 'I use a flashcard app to help me learn student names. Please provide a recent photo. (Optional. If you have religious or privacy or other objections to providing a photo, feel free to skip this.)',
              'laptop_type': "Do you have a laptop you can bring to class? If so, what kind?"}
        )
    form.vars.user_id = auth.user.id
    if form.process().accepted:
        session.flash = 'form accepted'
        redirect(URL('default','bio'))
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def bios():
    # go to /default/bios and then click on TSV (not CSV) to export properly with First and Last names showing instead of id
    # get only the people in the course you are instructor for
    q = (db.user_biography.user_id == db.auth_user.id) & (db.auth_user.course_id == auth.user.course_id)
    fields = [db.user_biography.image,
              db.user_biography.prefered_name,
              db.user_biography.user_id,
              db.user_biography.interesting_fact,
              db.user_biography.programming_experience]
    # headers that make it easy to import into Flashcards Deluxe
    headers = {'user_biography.image': 'Picture 1',
              'user_biography.prefered_name': 'Text 2',
              'user_biography.user_id': 'Text 3',
              'user_biography.interesting_fact' : 'Text 4',
              'user_biography.programming_experience' : 'Text 5'}
    bios = SQLFORM.grid(q, fields=fields, headers = headers)
    return dict(bios=bios)


@auth.requires_login()
def courses():
    res = db(db.user_courses.user_id == auth.user.id).select(db.user_courses.course_id)
    classlist = []
    for row in res:
        classes = db(db.courses.id == row.course_id).select()
        for part in classes:
            classlist.append(part.course_name)
    return dict(courses=classlist)


@auth.requires_login()
def remove():
    res = db(db.user_courses.user_id == auth.user.id).select(db.user_courses.course_id)
    classlist = []
    for row in res:
        classes = db(db.courses.id == row.course_id).select()
        for part in classes:
            classlist.append(part.course_name)
    return dict(courses=classlist)


@auth.requires_login()
def coursechooser():
    res = db(db.courses.course_name == request.args[0]).select(db.courses.id)

    if len(res) > 0:
        db(db.auth_user.id == auth.user.id).update(course_id = res[0].id)
        db(db.auth_user.id == auth.user.id).update(course_name = request.args[0])
        auth.user.update(course_name=request.args[0])
        auth.user.update(course_id=res[0].id)
        redirect('/%s/static/%s/index.html' % (request.application,request.args[0]))
    else:
        redirect('/%s/default/user/profile?_next=/%s/default/index' % (request.application, request.application))

@auth.requires_login()
def removecourse():
    courseIdQuery = db(db.courses.course_name == request.args[0]).select(db.courses.id)

    # Check if they're about to remove their currently active course
    authQuery = db(db.auth_user.id == auth.user.id).select()
    for row in authQuery:
        if row.course_name == request.args[0]:
            session.flash = T("Sorry, you cannot remove your current active course.")
        else:
            db((db.user_courses.user_id == auth.user.id) & (db.user_courses.course_id == courseIdQuery[0].id)).delete()

    redirect('/%s/default/courses' % request.application)

def reportabug():
    path = os.path.join(request.folder, 'errors')
    course = request.vars['course']
    uri = request.vars['page']
    username = 'anonymous'
    email = 'anonymous'
    code = None
    ticket = None
    pagerequest = None
    if request.vars.code:
        code = request.vars.code
        ticket = request.vars.ticket.split('/')[1]
        uri = request.vars.requested_uri
        error = RestrictedError()
        error.load(request, request.application, os.path.join(path,ticket))
        ticket = error.traceback

    if auth.user:
        username = auth.user.username
        email = auth.user.email
        course = auth.user.course_name
    return dict(course=course,uri=uri,username=username,email=email,code=code,ticket=ticket)

def sendreport():
    # settings.github_token should be set to a valid Github access token
    # that has full repo access in models/1.py
    if request.vars['nospam'] != '42':
        session.flash = 'Report rejected you are not human'
        redirect('/%s/default/' % request.application)

    if request.vars['bookerror'] == 'on':
        basecourse = db(db.courses.course_name == request.vars['coursename']).select().first().base_course
        if basecourse == None:
            url = 'https://api.github.com/repos/RunestoneInteractive/%s/issues' % request.vars['coursename']
        else:
            url ='https://api.github.com/repos/RunestoneInteractive/%s/issues' % basecourse
    else:
        url = 'https://api.github.com/repos/RunestoneInteractive/RunestoneComponents/issues'
    reqsession = requests.Session()
    reqsession.auth = ('token', settings.github_token)
    coursename = request.vars['coursename'] if request.vars['coursename'] else "None Provided"
    pagename = request.vars['pagename'] if request.vars['pagename'] else "None Provided"
    details = request.vars['bugdetails'] if request.vars['bugdetails'] else "None Provided"
    uname = request.vars['username'] if request.vars['username'] else "anonymous"
    uemail = request.vars['useremail'] if request.vars['useremail'] else "no_email"
    userinfo =  uname + ' ' + uemail

    body = 'Error reported in course ' + coursename + ' on page ' + pagename + ' by user ' + userinfo + '\n' + details
    issue = {'title': request.vars['bugtitle'],
             'body': body}
    r = reqsession.post(url, json.dumps(issue))
    if r.status_code == 201:
        session.flash = 'Successfully created Issue "%s"' % request.vars['bugtitle']
    else:
        session.flash = 'Could not create Issue "%s"' % request.vars['bugtitle']

    courseCheck = 0
    if auth.user:
        courseCheck = db(db.user_courses.user_id == auth.user.id).count()

    if courseCheck == 1 and request.vars['coursename']:
        redirect('/%s/static/%s/index.html' % (request.application, request.vars['coursename']))
    elif courseCheck > 1:
        redirect('/%s/default/courses' % request.application)
    else:
        redirect('/%s/default/' % request.application)
