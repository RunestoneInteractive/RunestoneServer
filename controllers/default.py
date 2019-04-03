# -*- coding: utf-8 -*-
import json
import os
import requests
from six.moves.urllib.parse import unquote
from six.moves.urllib.error import HTTPError
import logging

from gluon.restricted import RestrictedError
from stripe_form import StripeForm

logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)


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
                    course_name = url_parts[i + 1]
                    db.auth_user.course_id.default = course_name
                    break
    try:
        # After the registration form is submitted the registration is processed here
        # this function will not return in that case, but instead continue on and end up
        # redirecting to index.
        # Additional registration processing can be handled by make_section_entries or another function added
        # through db.auth_user._after_insert.append(some_function)
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
        # Add the section. Taken from ``gluon.tools.addrow`` where ``style='table3cols'``.
        form[0].insert(-1,
            TR(
                TD(LABEL('Section Name: ', _for='auth_user_section', _id='auth_user_section__label'), _class='w2p_fl'),
                TD(INPUT(_name='section', _type='text', _value=sectname, _id='auth_user_section', _class='string'), _class='w2p_fw'),
                TD('', _class='w2p_fc'),
                _id='auth_user_section__row',
            )
        )
        # Make the username read-only.
        form.element('#auth_user_username')['_readonly'] = True

        form.vars.course_id = auth.user.course_name
        if form.validate():
            # Prevent the username from being changed by deleting it before the update. See http://web2py.com/books/default/chapter/29/07/forms-and-validators#SQLFORM-without-database-IO.
            del form.vars.username
            form.record.update_record(**dict(form.vars))
            # auth.user session object doesn't automatically update when the DB gets updated
            auth.user.update(form.vars)
            # TODO: Why is this necessary?
            auth.user.course_name = db(db.auth_user.id == auth.user.id).select()[0].course_name
            # Add user to default section for course.
            sect = db((db.sections.course_id == auth.user.course_id) &
                      (db.sections.name == form.vars.section)).select(db.sections.id).first()
            if sect:
                x = db.section_users.update_or_insert(auth_user=auth.user.id, section=sect)
                db((auth.user.id == db.section_users.auth_user) & (
                   (db.section_users.section != sect) | (db.section_users.section is None))).delete()
            # select from sections where course_id = auth_user.course_id and section.name = 'default'
            # add a row to section_users for this user with the section selected.
            redirect(URL('default', 'index'))

    if 'register' in request.args(0):
        # The validation function ``IS_COURSE_ID`` in ``models/db.py`` changes the course name supplied to a course ID. If the overall form doesn't validate, the value when the form is re-displayed with errors will contain the ID instead of the course name. Change it back to the course name. Note: if the user enters a course for the course name, it will be displayed as the corresponding course name after a failed validation. I don't think this case is important enough to fix.
        try:
            course_id = int(form.vars.course_id)
        except:
            pass
        else:
            # Look up the course name based on the ID.
            form.vars.course_id = getCourseNameFromId(course_id)

    # this looks horrible but it seems to be the only way to add a CSS class to the submit button
    try:
        form.element(_id='submit_record__row')[1][0]['_class'] = 'btn btn-default'
    except (AttributeError, TypeError):  # not all auth methods actually have a submit button (e.g. user/not_authorized)
        pass
    return dict(form=form)


# Can use db.auth_user._after_insert.append(make_section_entries)
# to add a custom function to deal with donation and/or creating a course
# May have to disable auto_login ??

def download(): return response.download(request, db)


def call(): return service()


# Determine the student price for a given ``course_id``. Returns a value in cents, where 0 cents indicates a free book.
def _course_price(course_id):
    # Look for a student price for this course.
    course = db(db.courses.id == course_id).select(db.courses.student_price, db.courses.base_course).first()
    assert course
    price = course.student_price
    # Only look deeper if a price isn't set (even a price of 0).
    if price is None:
        # See if the base course has a student price.
        base_course = db(db.courses.course_name == course.base_course).select(db.courses.student_price).first()
        # If this is already a base course, we're done.
        if base_course:
            price = base_course.student_price
    # If price is ``None`` or negative, return a free course.
    return max(price or 0, 0)


@auth.requires_login()
def payment():
    # The payment will be made for ``auth.user.course_id``. Get the corresponding course name.
    course = db(db.courses.id == auth.user.course_id).select(db.courses.course_name).first()
    assert course.course_name
    form = StripeForm(
        pk=settings.STRIPE_PUBLISHABLE_KEY,
        sk=settings.STRIPE_SECRET_KEY,
        amount=_course_price(auth.user.course_id),
        description="Access to the {} textbook from {}".format(course.course_name, settings.title)
    ).process()
    if form.accepted:
        # Save the payment info, then redirect to the index.
        user_courses_id = db.user_courses.insert(user_id=auth.user.id, course_id=auth.user.course_id)
        db.payments.insert(user_courses_id=user_courses_id, charge_id=form.response['id'])
        db.commit()
        return dict(request=request, course=course, payment_success=True)
    elif form.errors:
        return dict(form=form, payment_success=False)
    # Fix up CSS -- the ``hidden`` attribute hides any error feedback.
    html = form.xml().replace('"payment-errors error hidden"', '"payment-errors error"')
    return dict(html=html, payment_success=None)



@auth.requires_login()
def index():
#    print("REFERER = ", request.env.http_referer)

    course = db(db.courses.id == auth.user.course_id).select(db.courses.course_name).first()

    if not course or 'boguscourse' in course.course_name:
        # if login was handled by Janrain, user didn't have a chance to choose the course_id;
        # redirect them to the profile page to choose one
        redirect('/%s/default/user/profile?_next=/%s/default/index' % (request.application, request.application))
    else:
        in_db = db(
            (db.user_courses.user_id == auth.user.id) & (db.user_courses.course_id == auth.user.course_id)).select()
        db_check = []
        for row in in_db:
            db_check.append(row)
        if not db_check:
            # The user hasn't been enrolled in this course yet. Check the price for the course.
            price = _course_price(auth.user.course_id)
            # If the price is non-zero, then require a payment. Otherwise, ask for a donation.
            if price > 0:
                redirect(URL('payment'))
            else:
                session.request_donation = True
            db.user_courses.insert(user_id=auth.user.id, course_id=auth.user.course_id)
        try:
            logger.debug("INDEX - checking for progress table")
            chapter_label = db(db.chapters.course_id == auth.user.course_name).select()[0].chapter_label
            logger.debug("LABEL = %s user_id = %s course_name = %s", chapter_label, auth.user.id, auth.user.course_name)
            if db((db.user_sub_chapter_progress.user_id == auth.user.id) &
                  (db.user_sub_chapter_progress.chapter_id == chapter_label)).count() == 0:
                if db((db.user_sub_chapter_progress.user_id == auth.user.id) &
                      (db.user_sub_chapter_progress.chapter_id == chapter_label)).count() == 0:
                    db.executesql('''
                       INSERT INTO user_sub_chapter_progress(user_id, chapter_id,sub_chapter_id, status)
                       SELECT %s, chapters.chapter_label, sub_chapters.sub_chapter_label, -1
                       FROM chapters, sub_chapters where sub_chapters.chapter_id = chapters.id and chapters.course_id = '%s';
                    ''' % (auth.user.id, auth.user.course_name))
        except:
            session.flash = "Your course is not set up to track your progress"
        # todo:  check course.course_name make sure it is valid if not then redirect to a nicer page.

        if session.request_donation:
            del session.request_donation
            redirect(URL(c='default', f='donate'))

        if session.build_course:
            del session.build_course
            redirect(URL(c='designer', f='index'))

        # See if we need to do a redirect from LTI.
        if session.lti_url_next:
            # This is a one-time redirect.
            del session.lti_url_next
            redirect(session.lti_url_next)

        # check number of classes, if more than 1, send to course selection, if only 1, send to book
        num_courses = db(db.user_courses.user_id == auth.user.id).count()
        # Don't redirect when there's only one course for testing. Since the static files don't exist, this produces a server error ``invalid file``.
        if num_courses == 1 and os.environ.get('WEB2PY_CONFIG') != 'test':
            redirect('/%s/static/%s/index.html' % (request.application, course.course_name))
        redirect(URL(c='default', f='courses'))


def error():
    # As recommended in http://web2py.com/books/default/chapter/29/04/the-core#Routes-on-error, pass on the error code that brought us here. TODO: This actually returns a 500 (Internal server error). ???
    #response.status = request.vars.code
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
                   showid=False,
                   fields=['prefered_name', 'interesting_fact', 'programming_experience', 'laptop_type', 'image'],
                   keepvalues=True,
                   upload=URL('download'),
                   formstyle='table3cols',
                   col3={
                       'prefered_name': "Name you would like to be called by in class. Pronunciation hints are also welcome!",
                       'interesting_fact': "Tell me something interesting about your outside activities that you wouldn't mind my mentioning in class. For example, are you the goalie for the UM soccer team? An officer in a club or fraternity? An expert on South American insects? Going into the Peace Corps after graduation? Have a company that you started last summer? Have an unusual favorite color?",
                       'programming_experience': "Have you ever done any programming before? If so, please describe briefly. (Note: no prior programming experience is required for this course. I just like to know whether you have programmed before.)",
                       'image': 'I use a flashcard app to help me learn student names. Please provide a recent photo. (Optional. If you have religious or privacy or other objections to providing a photo, feel free to skip this.)',
                       'laptop_type': "Do you have a laptop you can bring to class? If so, what kind?",
                       'confidence': "On a 1-5 scale, how confident are you that you can learn to program?"
                   }
                   )
    form.vars.user_id = auth.user.id
    if form.process().accepted:
        session.flash = 'form accepted'
        redirect(URL('default', 'bio'))
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def bios():
    # go to /default/bios and then click on TSV (not CSV) to export properly with First and Last names showing
    # instead of id get only the people in the course you are instructor for
    q = (db.user_biography.user_id == db.auth_user.id) & (db.auth_user.course_id == auth.user.course_id)
    fields = [db.user_biography.image,
              db.user_biography.prefered_name,
              db.user_biography.user_id,
              db.user_biography.interesting_fact,
              db.user_biography.programming_experience,
              db.user_biography.laptop_type,
              db.auth_user.email]
    # headers that make it easy to import into Flashcards Deluxe
    headers = {'user_biography.image': 'Picture 1',
               'user_biography.prefered_name': 'Text 2',
               'user_biography.user_id': 'Text 3',
               'user_biography.interesting_fact': 'Text 4',
               'user_biography.programming_experience': 'Text 5'}
    bios_form = SQLFORM.grid(q, fields=fields, headers=headers)
    return dict(bios=bios_form)


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
        db(db.auth_user.id == auth.user.id).update(course_id=res[0].id)
        db(db.auth_user.id == auth.user.id).update(course_name=request.args[0])
        auth.user.update(course_name=request.args[0])
        auth.user.update(course_id=res[0].id)
        res = db(db.chapters.course_id == auth.user.course_name)
        logger.debug("COURSECHOOSER checking for progress table %s ", res)
        if res.count() > 0:
            chapter_label = res.select().first().chapter_label
            if db((db.user_sub_chapter_progress.user_id == auth.user.id) &
                  (db.user_sub_chapter_progress.chapter_id == chapter_label)).count() == 0:
                logger.debug("SETTING UP PROGRESS for %s %s", auth.user.username, auth.user.course_name)
                db.executesql('''
                    INSERT INTO user_sub_chapter_progress(user_id, chapter_id,sub_chapter_id, status)
                    SELECT %s, chapters.chapter_label, sub_chapters.sub_chapter_label, -1
                    FROM chapters, sub_chapters where sub_chapters.chapter_id = chapters.id and chapters.course_id = %s;
                ''', (auth.user.id, auth.user.course_name))

        redirect('/%s/static/%s/index.html' % (request.application, request.args[0]))
    else:
        redirect('/%s/default/user/profile?_next=/%s/default/index' % (request.application, request.application))


@auth.requires_login()
def removecourse():
    if not settings.academy_mode:
      course_id_query = db(db.courses.course_name == request.args[0]).select(db.courses.id)
      # todo: properly encode course_names to handle courses with special characters
      # Check if they're about to remove their currently active course
      auth_query = db(db.auth_user.id == auth.user.id).select()
      for row in auth_query:
          if row.course_name == request.args[0] and course_id_query:
              session.flash = T("Sorry, you cannot remove your current active course.")
          else:
              db((db.user_courses.user_id == auth.user.id) &
                 (db.user_courses.course_id == course_id_query[0].id)).delete()

    redirect('/%s/default/courses' % request.application)


def reportabug():
    path = os.path.join(request.folder, 'errors')
    course = request.vars['course']
    uri = request.vars['page']
    username = 'anonymous'
    email = 'anonymous'
    code = None
    ticket = None
    registered_user = False

    if request.vars.code:
        code = request.vars.code
        ticket = request.vars.ticket.split('/')[1]
        uri = request.vars.requested_uri
        error = RestrictedError()
        error.load(request, request.application, os.path.join(path, ticket))
        ticket = error.traceback

    if auth.user:
        username = auth.user.username
        email = auth.user.email
        course = auth.user.course_name
        registered_user = True

    return dict(course=course, uri=uri, username=username, email=email, code=code, ticket=ticket,
                registered_user=registered_user)


@auth.requires_login()
def sendreport():
    if settings.academy_mode:
        if request.vars['bookerror'] == 'on':
            basecourse = db(db.courses.course_name == request.vars['coursename']).select().first().base_course
            if basecourse is None:
                url = 'https://api.github.com/repos/RunestoneInteractive/%s/issues' % request.vars['coursename']
            else:
                url = 'https://api.github.com/repos/RunestoneInteractive/%s/issues' % basecourse
        else:
            url = 'https://api.github.com/repos/RunestoneInteractive/RunestoneComponents/issues'
        reqsession = requests.Session()
        reqsession.auth = ('token', settings.github_token)
        coursename = request.vars['coursename'] if request.vars['coursename'] else "None Provided"
        pagename = request.vars['pagename'] if request.vars['pagename'] else "None Provided"
        details = request.vars['bugdetails'] if request.vars['bugdetails'] else "None Provided"
        uname = request.vars['username'] if request.vars['username'] else "anonymous"
        uemail = request.vars['useremail'] if request.vars['useremail'] else "no_email"
        userinfo = uname + ' ' + uemail

        body = 'Error reported in course ' + coursename + ' on page ' + pagename + ' by user ' + userinfo + '\n' + details
        issue = {'title': request.vars['bugtitle'],
                 'body': body}
        logger.debug("POSTING ISSUE %s ", issue)
        r = reqsession.post(url, json.dumps(issue))
        if r.status_code == 201:
            session.flash = 'Successfully created Issue "%s"' % request.vars['bugtitle']
        else:
            session.flash = 'Could not create Issue "%s"' % request.vars['bugtitle']
        logger.debug("POST STATUS = %s", r.status_code)

        course_check = 0
        if auth.user:
            course_check = db(db.user_courses.user_id == auth.user.id).count()

        if course_check == 1 and request.vars['coursename']:
            redirect('/%s/static/%s/index.html' % (request.application, request.vars['coursename']))
        elif course_check > 1:
            redirect('/%s/default/courses' % request.application)
        else:
            redirect('/%s/default/' % request.application)
    redirect('/%s/default/' % request.application)


def terms():
    return dict(terms={})


def privacy():
    return dict(private={})


def donate():
    if request.vars.donate:
        amt = request.vars.donate
    elif session.donate:
        amt = session.donate
    else:
        amt = None
    return dict(donate=amt)
