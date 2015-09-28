# -*- coding: utf-8 -*-
### required - do no delete
import json
from urllib import unquote

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

    form = auth()

    if 'profile' in request.args(0):
        sect = db(db.section_users.auth_user == auth.user.id).select(db.section_users.section).first().section
        sectname = db(db.sections.id == sect).select(db.sections.name).first()
        if sectname:
            sectname = sectname.name
        else:
            sectname = 'default'
        if not sect:
            sect = 'default'
        my_extra_element = TR(LABEL('Section Name'),
                           INPUT(_name='section', value=sectname, _type='text'))
        form[0].insert(-1, my_extra_element)

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

    if 'boguscourse' in course.course_name:
        # if login was handled by Janrain, user didn't have a chance to choose the course_id;
        # redirect them to the profile page to choose one
        redirect('/%s/default/user/profile?_next=/%s/default/index' % (request.application, request.application))
    else:
        try:
            chapter_label = db(db.chapters.course_id == auth.user.course_name).select()[0].chapter_label
            if db(db.user.sub_chapter_progress.user_id == auth.user.id).count() == 0:
                if db((db.user_sub_chapter_progress.user_id == auth.user.id) & (
                            db.user_sub_chapter_progress.chapter_id == chapter_label)).count() == 0:
                    db.executesql('''
                       INSERT INTO user_sub_chapter_progress(user_id, chapter_id,sub_chapter_id, status)
                       SELECT %s, chapters.chapter_label, sub_chapters.sub_chapter_label, -1
                       FROM chapters, sub_chapters where sub_chapters.chapter_id = chapters.id and chapters.course_id = '%s';
                    ''' % (auth.user.id, auth.user.course_name))
                # Add user to default section for course.
                sect = db((db.sections.course_id == auth.user.course_id) & (db.sections.name == form.vars.section)).select(
                    db.sections.id).first()
                if sect:
                    x = db.section_users.update_or_insert(auth_user=auth.user.id, section=sect)
        except:
            session.flash = "Your course is not set up to track your progress"
        #todo:  check course.course_name make sure it is valid if not then redirect to a nicer page.
        redirect('/%s/static/%s/index.html' % (request.application,course.course_name))

    cohortId = db(db.auth_user.id == auth.user.id).select(db.auth_user.cohort_id).first()

def error():
    return dict()

def about():
    return dict()

def ack():
    return dict()

    
