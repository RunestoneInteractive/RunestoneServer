import uuid

from applications.runestone.modules import oauth
from applications.runestone.modules import oauth_store

def index():

    #print "In imslti.py"
#    print dict(request.vars)
    
    myrecord = None
    consumer = None
    params = None
    masterapp = None
    oauth_error = None
    userinfo = None
    logged_in = False

    user_id = request.vars.get('user_id', None)
    last_name = request.vars.get('lis_person_name_family', None)
    first_name = request.vars.get('lis_person_name_given', None)
    full_name = request.vars.get('lis_person_name_full', None)
    if full_name and not last_name:
        names = full_name.strip().split()
        last_name = names[-1]
        first_name = ' '.join(names[:-1])
    email = request.vars.get('lis_person_contact_email_primary', None)
    instructor = ("Instructor" in request.vars.get('roles', None)) or \
                 ("TeachingAssistant" in request.vars.get('roles', None))
    result_source_did=request.vars.get('lis_result_sourcedid', None)
    outcome_url=request.vars.get('lis_outcome_service_url', None)
    # print request.vars
    # print result_source_did, outcome_url
    assignment_id=request.vars.get('assignment_id', None)
    if assignment_id and type(assignment_id) == type([]):
        # for some reason, url query parameters are being processed twice by Canvas and returned as a list, like [23, 23]
        # so just take the first element in the list
        assignment_id=assignment_id[0]
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
        userinfo['email'] = email
    
    key = request.vars.get('oauth_consumer_key', None)
    if key is not None:
        myrecord = db(db.lti_keys.consumer==key).select().first()
    #    print myrecord, type(myrecord)
        if myrecord is None :
            return dict(logged_in=False, lti_errors=["Could not find oauth_consumer_key", request.vars],
                        masterapp=masterapp)
        else:
            session.oauth_consumer_key = key
    # print 1, myrecord, userinfo
    if myrecord is not None : 
        masterapp = myrecord.application
        if len(masterapp) < 1 :
            masterapp = 'welcome'
    #    print "masterapp",masterapp
        session.connect(request, response, masterapp=masterapp, db=db)
    
        oauth_server = oauth.OAuthServer(oauth_store.LTI_OAuthDataStore(myrecord.consumer,myrecord.secret))
        oauth_server.add_signature_method(oauth.OAuthSignatureMethod_PLAINTEXT())
        oauth_server.add_signature_method(oauth.OAuthSignatureMethod_HMAC_SHA1())

        full_uri = settings.lti_uri
        oauth_request = oauth.OAuthRequest.from_request('POST', full_uri, None, dict(request.vars),
                                                        query_string=request.env.query_string)
    
        try:
            # print "secret: ", myrecord.secret
            # print "Incoming request from:", full_uri
            consumer, token, params = oauth_server.verify_request(oauth_request)
            # print "Verified."
        except oauth.OAuthError, err:
            return dict(logged_in=False, lti_errors=["OAuth Security Validation failed:"+err.message, request.vars],
                        masterapp=masterapp)
            consumer = None

    # Time to create / update / login the user
    if userinfo and (consumer is not None):
        userinfo['username'] = email
        # print db.auth_user.password.validate('1C5CHFA_enUS503US503')
        # pw = db.auth_user.password.validate('2C5CHFA_enUS503US503')[0];
        pw = db.auth_user.password.validate(str(uuid.uuid4()))[0]
    #    print pw 
        userinfo['password'] = pw
        # print userinfo
        user = auth.get_or_create_user(userinfo, update_fields=['email', 'first_name', 'last_name', 'password'])
        # print user
        if user is None :
            return dict(logged_in=False, lti_errors=["Unable to create user record", request.vars],
                        masterapp=masterapp)
        else:
            # user exists; make sure course name and id are set based on custom parameters passed, if this is for runestone
            course_id = request.vars.get('custom_course_id', None)
            section_id = request.vars.get('custom_section_id', None)
            if course_id:
                user['course_id'] = course_id
                user['course_name'] = getCourseNameFromId(course_id)    # need to set course_name because calls to verifyInstructor use it
                user['section'] = section_id
                user.update_record()
                db.user_courses.update_or_insert(user_id=user.id,course_id=course_id)
                if instructor:
                    db.course_instructor.update_or_insert(instructor = user.id, course = course_id)
                else:
                    db((db.course_instructor.instructor == user.id) & (db.course_instructor.course == course_id)).delete()
            if section_id:
                # set the section in the section_users table
                # test this
                db.section_users.update_or_insert(db.section_users.auth_user == user['id'], auth_user=user['id'], section = section_id)

    #    print user, type(user)
    #    print "Logging in..."
        auth.login_user(user)
    #    print "Logged in..."
        logged_in = True

    if assignment_id:
        # save the guid and url for reporting back the grade
        # print user.id, assignment_id
        db.grades.update_or_insert((db.grades.auth_user == user.id) & (db.grades.assignment == assignment_id),
                                   auth_user=user.id,
                                   assignment=assignment_id,
                                   lis_result_sourcedid=result_source_did,
                                   lis_outcome_url=outcome_url)
        redirect(URL('assignments', 'doAssignment', vars={'assignment_id':assignment_id}))

    elif practice:
        db.practice_grades.update_or_insert((db.practice_grades.auth_user == user.id),
                                   auth_user=user.id,
                                   lis_result_sourcedid=result_source_did,
                                   lis_outcome_url=outcome_url,
                                   course_name=getCourseNameFromId(course_id))
        redirect(URL('assignments', 'settz_then_practice', vars={'course_name':user['course_name']}))

    redirect('/%s/static/%s/index.html' % (request.application, getCourseNameFromId(course_id)))

