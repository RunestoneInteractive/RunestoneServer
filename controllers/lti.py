import uuid
import six


from rs_grading import _try_to_send_lti_grade
import oauth2


# For some reason, URL query parameters are being processed twice by Canvas and returned as a list, like [23, 23]. So, just take the first element in the list.
def _param_converter(param):
    return param[0] if isinstance(param, list) else param


def index():
    myrecord = None
    consumer = None
    masterapp = None
    userinfo = None

    user_id = request.vars.get('user_id', None)
    last_name = request.vars.get('lis_person_name_family', None)
    first_name = request.vars.get('lis_person_name_given', None)
    full_name = request.vars.get('lis_person_name_full', None)
    if full_name and not last_name:
        names = full_name.strip().split()
        last_name = names[-1]
        first_name = ' '.join(names[:-1])
    email = request.vars.get('lis_person_contact_email_primary', None)
    instructor = ("Instructor" in request.vars.get('roles', [])) or \
                 ("TeachingAssistant" in request.vars.get('roles', []))
    result_source_did=request.vars.get('lis_result_sourcedid', None)
    outcome_url=request.vars.get('lis_outcome_service_url', None)
    assignment_id = _param_converter(request.vars.get('assignment_id', None))
    practice = request.vars.get('practice', None)

    if user_id is None :
        return dict(logged_in=False, lti_errors=["user_id is required for this tool to function", request.vars], masterapp=masterapp)
    elif first_name is None :
        return dict(logged_in=False, lti_errors=["First Name is required for this tool to function", request.vars], masterapp=masterapp)
    elif last_name is None :
        return dict(logged_in=False, lti_errors=["Last Name is required for this tool to function", request.vars], masterapp=masterapp)
    elif email is None :
        return dict(logged_in=False, lti_errors=["Email is required for this tool to function", request.vars], masterapp=masterapp)
    else :
        userinfo = dict()
        userinfo['first_name'] = first_name
        userinfo['last_name'] = last_name
        # In the `Canvas Student View <https://community.canvaslms.com/docs/DOC-13122-415261153>`_ as of 7-Jan-2019, the ``lis_person_contact_email_primary`` is an empty string. In this case, use the userid instead.
        email = email or (user_id + '@junk.com')
        userinfo['email'] = email

    key = request.vars.get('oauth_consumer_key', None)
    if key is not None:
        myrecord = db(db.lti_keys.consumer==key).select().first()
        if myrecord is None :
            return dict(logged_in=False, lti_errors=["Could not find oauth_consumer_key", request.vars],
                        masterapp=masterapp)
        else:
            session.oauth_consumer_key = key
    if myrecord is not None :
        masterapp = myrecord.application
        if len(masterapp) < 1 :
            masterapp = 'welcome'
        session.connect(request, response, masterapp=masterapp, db=db)

        oauth_server = oauth2.Server()
        oauth_server.add_signature_method(oauth2.SignatureMethod_PLAINTEXT())
        oauth_server.add_signature_method(oauth2.SignatureMethod_HMAC_SHA1())

        # Use ``setting.lti_uri`` if it's defined; otherwise, use the current URI (which must be built from its components). Don't include query parameters, which causes a failure in OAuth security validation.
        full_uri = settings.get('lti_uri', '{}://{}{}'.format(
            request.env.wsgi_url_scheme, request.env.http_host, request.url
        ))
        oauth_request = oauth2.Request.from_request(
            'POST', full_uri, None, dict(request.vars),
            query_string=request.env.query_string
        )
        # Fix encoding -- the signed keys are in bytes, but the oauth2 Request constructor translates everything to a string. Therefore, they never compare as equal. ???
        if isinstance(oauth_request.get('oauth_signature'), six.string_types):
            oauth_request['oauth_signature'] = oauth_request['oauth_signature'].encode('utf-8')
        consumer = oauth2.Consumer(myrecord.consumer, myrecord.secret)

        try:
            oauth_server.verify_request(oauth_request, consumer, None)
        except oauth2.Error as err:
            return dict(logged_in=False, lti_errors=["OAuth Security Validation failed:"+err.message, request.vars],
                        masterapp=masterapp)
            consumer = None

    # Time to create / update / login the user
    if userinfo and (consumer is not None):
        userinfo['username'] = email
        # Only assign a password if we're creating the user. The
        # ``get_or_create_user`` method checks for an existing user using both
        # the username and the email.
        update_fields = ['email', 'first_name', 'last_name']
        if not db(
            (db.auth_user.username == userinfo['username']) |
            (db.auth_user.email == userinfo['email'])
        ).select(db.auth_user.id).first():
            pw = db.auth_user.password.validate(str(uuid.uuid4()))[0]
            userinfo['password'] = pw
            update_fields.append('password')
        user = auth.get_or_create_user(userinfo, update_fields=update_fields)
        if user is None:
            return dict(logged_in=False, lti_errors=["Unable to create user record", request.vars],
                        masterapp=masterapp)
        # user exists; make sure course name and id are set based on custom parameters passed, if this is for runestone. As noted for ``assignment_id``, parameters are passed as a two-element list.
        course_id = _param_converter(request.vars.get('custom_course_id', None))
        section_id = _param_converter(request.vars.get('custom_section_id', None))
        if course_id:
            user['course_id'] = course_id
            user['course_name'] = getCourseNameFromId(course_id)    # need to set course_name because calls to verifyInstructor use it
            user['section'] = section_id
            user.update_record()

            # Update instructor status.
            if instructor:
                # Give the instructor free access to the book.
                db.user_courses.update_or_insert(user_id=user.id, course_id=course_id)
                db.course_instructor.update_or_insert(instructor=user.id, course=course_id)
            else:
                db((db.course_instructor.instructor == user.id) &
                   (db.course_instructor.course == course_id)).delete()

            # Before creating a new user_courses record, present payment or donation options.
            if not db((db.user_courses.user_id==user.id) &
                      (db.user_courses.course_id==course_id)).select().first():
                # Store the current URL, so this request can be completed after creating the user.
                session.lti_url_next = full_uri
                auth.login_user(user)
                redirect(URL(c='default'))

        if section_id:
            # set the section in the section_users table
            # test this
            db.section_users.update_or_insert(db.section_users.auth_user == user['id'], auth_user=user['id'], section = section_id)

        auth.login_user(user)

    if assignment_id:
        # If the assignment is released, but this is the first time a student has visited the assignment, auto-upload the grade.
        assignment = db(db.assignments.id == assignment_id).select(
            db.assignments.released).first()
        grade = db(
            (db.grades.auth_user == user.id) &
            (db.grades.assignment == assignment_id)
        ).select(db.grades.lis_result_sourcedid, db.grades.lis_outcome_url).first()
        send_grade = (assignment and assignment.released and grade and
                      not grade.lis_result_sourcedid and
                      not grade.lis_outcome_url)

        # save the guid and url for reporting back the grade
        db.grades.update_or_insert((db.grades.auth_user == user.id) & (db.grades.assignment == assignment_id),
                                   auth_user=user.id,
                                   assignment=assignment_id,
                                   lis_result_sourcedid=result_source_did,
                                   lis_outcome_url=outcome_url)
        if send_grade:
            _try_to_send_lti_grade(user.id, assignment_id)

        redirect(URL('assignments', 'doAssignment', vars={'assignment_id':assignment_id}))

    elif practice:
        if outcome_url and result_source_did:
            db.practice_grades.update_or_insert((db.practice_grades.auth_user == user.id),
                                                auth_user=user.id,
                                                lis_result_sourcedid=result_source_did,
                                                lis_outcome_url=outcome_url,
                                                course_name=getCourseNameFromId(course_id))
        else: # don't overwrite outcome_url and result_source_did
            db.practice_grades.update_or_insert((db.practice_grades.auth_user == user.id),
                                                auth_user=user.id,
                                                course_name=getCourseNameFromId(course_id))
        redirect(URL('assignments', 'settz_then_practice', vars={'course_name':user['course_name']}))

    redirect(get_course_url('index.html'))

