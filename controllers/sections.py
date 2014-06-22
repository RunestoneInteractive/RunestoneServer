@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def index():
    course = db(db.courses.id == auth.user.course_id).select().first()
    sections = db(db.sections.course_id == course.id).select()
    # get all sections - for course, list number of users in each section
    return dict(
        course = course,
        sections = sections
        )

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def create():
    course = db(db.courses.id == auth.user.course_id).select().first()
    form = FORM(
        DIV(
            LABEL("Section Name", _for="section_name"),
            INPUT(_id="section_name" ,_name="name", requires=IS_NOT_EMPTY(),_class="form-control"),
            _class="form-group"
            ),
        INPUT(_type="Submit", _value="Create Section", _class="btn"),
        )
    if form.accepts(request,session):
        section = db.sections.update_or_insert(name=form.vars.name, course_id=course.id)
        session.flash = "Section Created"
        return redirect(URL('sections','update')+'?id=%d' % (section.id))
    return dict(
        form = form,
        )

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def delete():
    course = db(db.courses.id == auth.user.course_id).select().first()
    section = db(db.sections.id == request.vars.id).select().first()
    if not section or section.course_id != course.id:
        return redirect(URL('admin','sections_list'))
    section.clear_users()
    session.flash = "Deleted Section: %s" % (section.name)
    db(db.sections.id == section.id).delete()
    return redirect(URL('sections','index'))

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def update():
    course = db(db.courses.id == auth.user.course_id).select().first()
    section = db(db.sections.id == request.vars.id).select().first()
    if not section or section.course_id != course.id:
        redirect(URL('admin','sections_list'))
    bulk_email_form = FORM(
        DIV(
            TEXTAREA(_name="emails_csv",
                requires=IS_NOT_EMPTY(),
                _class="form-control",
                ),
            _class="form-group",
            ),
        LABEL(
            INPUT(_name="overwrite", _type="Checkbox"),
            "Overwrite Users In Section",
            _class="checkbox",
            ),
        INPUT(_type='Submit', _class="btn", _value="Update Section"),
        )
    if bulk_email_form.accepts(request,session):
        if bulk_email_form.vars.overwrite:
            section.clear_users()
        users_added_count = 0
        for email_address in bulk_email_form.vars.emails_csv.split(','):
            user = db(db.auth_user.email == email_address.lower()).select().first()
            if user:
                if section.add_user(user):
                    users_added_count += 1
        session.flash = "%d Emails Added" % (users_added_count)
        return redirect(URL('sections','update')+'?id=%d' % (section.id))
    elif bulk_email_form.errors:
        response.flash = "Error Processing Request"
    return dict(
        section = section,
        users = section.get_users(),
        bulk_email_form = bulk_email_form,
        )