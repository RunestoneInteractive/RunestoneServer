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
    lti_errors = list()
    userinfo = None
    logged_in = False
    
    user_id = request.vars.get('user_id', None)
    last_name = request.vars.get('lis_person_name_family', None)
    first_name = request.vars.get('lis_person_name_given', None)
    email = request.vars.get('lis_person_contact_email_primary', None)
    instructor = "Instructor" in request.vars.get('roles', None)
    result_source_did=request.vars.get('lis_result_sourcedid', None)
    outcome_url=request.vars.get('lis_outcome_service_url', None)
    print result_source_did, outcome_url
    assignment_id=request.vars.get('assignment_id', None)
    # for some reason, url query parameters are being processed twice and returned as a list, like [23, 23]
    if assignment_id:
        # so just take the first element in the list
        assignment_id=assignment_id[0]
    
    if user_id is None :
        lti_errors.append("user_id is required for this tool to function")
    elif first_name is None :
        lti_errors.append("First Name is required for this tool to function")
    elif last_name is None :
        lti_errors.append("Last Name is required for this tool to function")
    elif email is None :
        lti_errors.append("Email is required for this tool to function")
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
            lti_errors.append("Could not find oauth_consumer_key")
    
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
#            print "secret: ", myrecord.secret
#            print "Incoming request from:", full_uri
            consumer, token, params = oauth_server.verify_request(oauth_request)
#            print "Verified."
        except oauth.OAuthError, err:
            oauth_error = "OAuth Security Validation failed:"+err.message
            lti_errors.append(oauth_error)
            print oauth_error
            consumer = None
        # except:
            # print "Unexpected error"
            # oauth_error = "Unexpected Error"
            # consumer = None
    
    # Time to create / update / login the user
    if consumer is not None:
        userinfo['username'] = email
        # print db.auth_user.password.validate('1C5CHFA_enUS503US503')
        # pw = db.auth_user.password.validate('2C5CHFA_enUS503US503')[0];
        pw = db.auth_user.password.validate(str(uuid.uuid4()))[0]
    #    print pw 
        userinfo['password'] = pw
        print userinfo
        user = auth.get_or_create_user(userinfo, update_fields=['email', 'first_name', 'last_name', 'password'])
        print user
        if user is None : 
            lti_errors.append("Unable to create user record")
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
                    print "deleted"
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
        print user.id, assignment_id
        db.grades.update_or_insert((db.grades.auth_user == user.id) & (db.grades.assignment == assignment_id),
                                   auth_user=user.id,
                                   assignment=assignment_id,
                                   lis_result_sourcedid=result_source_did,
                                   lis_outcome_url=outcome_url)
        print("redirecting")
        redirect(URL('assignments', 'doAssignment', vars={'assignment_id':assignment_id}))


    # print(lti_errors)
    redirect('/%s/static/%s/index.html' % (request.application, getCourseNameFromId(course_id)))

    return dict(logged_in=logged_in, lti_errors=lti_errors, masterapp=masterapp)
