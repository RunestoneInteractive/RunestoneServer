# *************************************************
# |docname| - LTI Endpoint for integrating with LMS
# *************************************************
#
# Imports
# =======
# These are listed in the order prescribed by `PEP 8
# <http://www.python.org/dev/peps/pep-0008/#imports>`_.
#
# Standard library
# ----------------
import datetime
import uuid
import json
import html
import time

# Third-party imports
# -------------------
import oauth2

# Local application imports
# -------------------------
from rs_grading import _try_to_send_lti_grade

# Code
# ====
# For some reason, URL query parameters are being processed twice by Canvas and returned as a list, like [23, 23]. So, just take the first element in the list.
def _param_converter(param):
    return param[0] if isinstance(param, list) else param


# Main LTI Launch Endpoint
# ------------------------
def index():

    # Basic processing of the LTI request starts here
    # this first block is about getting the user information provided by the LMS
    myrecord = None
    consumer = None
    masterapp = None
    userinfo = None

    user_id = request.vars.get("user_id", None)
    last_name = request.vars.get("lis_person_name_family", None)
    first_name = request.vars.get("lis_person_name_given", None)
    full_name = request.vars.get("lis_person_name_full", None)
    message_type = request.vars.get("lti_message_type")
    course_id = _param_converter(request.vars.get("custom_course_id", None))

    if course_id:
        # Allow the course_id to be either a number or the name of the course, as a string.
        try:
            course_id = int(course_id)
        except ValueError:
            course_id = (
                db(db.courses.course_name == course_id).select(**SELECT_CACHE).first()
            )
            course_id = course_id.id

    if full_name and not last_name:
        names = full_name.strip().split()
        last_name = names[-1]
        first_name = " ".join(names[:-1])
    email = request.vars.get("lis_person_contact_email_primary", None)
    instructor = ("Instructor" in request.vars.get("roles", [])) or (
        "TeachingAssistant" in request.vars.get("roles", [])
    )
    result_source_did = request.vars.get("lis_result_sourcedid", None)
    outcome_url = request.vars.get("lis_outcome_service_url", None)
    # Deprecated: the use of the non-LTI-compliant name ``assignment_id``. The parameter should be ``custom_assignment_id``.
    assignment_id = _param_converter(
        request.vars.get(
            "custom_assignment_id", request.vars.get("assignment_id", None)
        )
    )
    practice = request.vars.get("practice", None)

    if user_id is None:
        return dict(
            logged_in=False,
            lti_errors=["user_id is required for this tool to function", request.vars],
            masterapp=masterapp,
        )
    elif first_name is None:
        return dict(
            logged_in=False,
            lti_errors=[
                "First Name is required for this tool to function",
                request.vars,
            ],
            masterapp=masterapp,
        )
    elif last_name is None:
        return dict(
            logged_in=False,
            lti_errors=[
                "Last Name is required for this tool to function",
                request.vars,
            ],
            masterapp=masterapp,
        )
    elif email is None:
        return dict(
            logged_in=False,
            lti_errors=["Email is required for this tool to function", request.vars],
            masterapp=masterapp,
        )
    else:
        userinfo = dict()
        userinfo["first_name"] = first_name
        userinfo["last_name"] = last_name
        # In the `Canvas Student View <https://community.canvaslms.com/docs/DOC-13122-415261153>`_ as of 7-Jan-2019, the ``lis_person_contact_email_primary`` is an empty string. In this case, use the userid instead.
        email = email or (user_id + "@junk.com")
        userinfo["email"] = email

    # Now we need to get some security info
    # oauth_consumer_key

    key = request.vars.get("oauth_consumer_key", None)
    if key is not None:
        myrecord = db(db.lti_keys.consumer == key).select().first()
        if myrecord is None:
            return dict(
                logged_in=False,
                lti_errors=["Could not find oauth_consumer_key", request.vars],
                masterapp=masterapp,
            )
        else:
            session.oauth_consumer_key = key
    if myrecord is not None:
        masterapp = myrecord.application
        if len(masterapp) < 1:
            masterapp = "welcome"
        session.connect(request, response, masterapp=masterapp, db=db)

        oauth_server = oauth2.Server()
        oauth_server.add_signature_method(oauth2.SignatureMethod_PLAINTEXT())
        oauth_server.add_signature_method(oauth2.SignatureMethod_HMAC_SHA1())

        # Use ``setting.lti_uri`` if it's defined; otherwise, use the current URI (which must be built from its components). Don't include query parameters, which causes a failure in OAuth security validation.
        full_uri = settings.get(
            "lti_uri",
            "{}://{}{}".format(
                request.env.wsgi_url_scheme, request.env.http_host, request.url
            ),
        )
        oauth_request = oauth2.Request.from_request(
            "POST",
            full_uri,
            None,
            dict(request.vars),
            query_string=request.env.query_string,
        )
        # Fix encoding -- the signed keys are in bytes, but the oauth2 Request constructor translates everything to a string. Therefore, they never compare as equal. ???
        if isinstance(oauth_request.get("oauth_signature"), str):
            oauth_request["oauth_signature"] = oauth_request["oauth_signature"].encode(
                "utf-8"
            )
        consumer = oauth2.Consumer(myrecord.consumer, myrecord.secret)

        try:
            oauth_server.verify_request(oauth_request, consumer, None)
        except oauth2.Error as err:
            return dict(
                logged_in=False,
                lti_errors=[
                    "OAuth Security Validation failed:" + err.message,
                    request.vars,
                ],
                masterapp=masterapp,
            )
            consumer = None
    ###############################################################################
    # I think everything from the beginning to here could/should be refactored into
    # a validate function.  Or make use of the lti package

    # Time to create / update / login the user
    if userinfo and (consumer is not None):
        userinfo["username"] = email
        # Only assign a password if we're creating the user. The
        # ``get_or_create_user`` method checks for an existing user using both
        # the username and the email.
        update_fields = ["email", "first_name", "last_name"]
        if (
            not db(
                (db.auth_user.username == userinfo["username"])
                | (db.auth_user.email == userinfo["email"])
            )
            .select(db.auth_user.id)
            .first()
        ):
            pw = db.auth_user.password.validate(str(uuid.uuid4()))[0]
            userinfo["password"] = pw
            update_fields.append("password")
        user = auth.get_or_create_user(userinfo, update_fields=update_fields)
        if user is None:
            return dict(
                logged_in=False,
                lti_errors=["Unable to create user record", request.vars],
                masterapp=masterapp,
            )
        # user exists; make sure course name and id are set based on custom parameters passed, if this is for runestone. As noted for ``assignment_id``, parameters are passed as a two-element list.
        # course_id = _param_converter(request.vars.get("custom_course_id", None))
        # if the instructor uses their course name instead of its id number then get the number.

        if course_id:
            user["course_id"] = course_id
            user["course_name"] = getCourseNameFromId(
                course_id
            )  # need to set course_name because calls to verifyInstructor use it
            user.update_record()

            # Update instructor status.
            # TODO: this block should be removed.  The only way to become an instructor
            # is through Runestone
            if instructor:
                # Give the instructor free access to the book.
                db.user_courses.update_or_insert(user_id=user.id, course_id=course_id)
                db.course_instructor.update_or_insert(
                    instructor=user.id, course=course_id
                )
            else:
                # Make sure previous instructors are removed from the instructor list.
                db(
                    (db.course_instructor.instructor == user.id)
                    & (db.course_instructor.course == course_id)
                ).delete()

            # Before creating a new user_courses record:
            if (
                not db(
                    (db.user_courses.user_id == user.id)
                    & (db.user_courses.course_id == course_id)
                )
                .select()
                .first()
            ):
                # In academy mode, present payment or donation options, per the discussion at https://github.com/RunestoneInteractive/RunestoneServer/pull/1322.
                if settings.academy_mode:
                    # To do so, store the current URL, so this request can be completed after creating the user.
                    # TODO: this doesn't work, since the ``course_id``` and ``assignment_id`` aren't saved in this redirect. Therefore, these should be stored (perhaps in ``session``) then used after a user pays / donates.
                    session.lti_url_next = full_uri
                    auth.login_user(user)
                    _create_access_token(
                        {"sub": user.username}, expires=datetime.timedelta(days=30)
                    )
                    redirect(URL(c="default"))
                else:
                    # Otherwise, simply create the user.
                    db.user_courses.update_or_insert(
                        user_id=user.id, course_id=course_id
                    )

        auth.login_user(user)
        # At this point the user has logged in
        # add a jwt cookie for compatibility with bookserver
        _create_access_token(
            {"sub": user.username}, expires=datetime.timedelta(days=30)
        )

    if message_type == "ContentItemSelectionRequest":
        return _provide_assignment_list(course_id, consumer)

    elif assignment_id:
        # If the assignment is released, but this is the first time a student has visited the assignment, auto-upload the grade.
        _launch_assignment(assignment_id, user, result_source_did, outcome_url)
        # If we got here, the assignment wasn't launched.
        return dict(
            logged_in=False,
            lti_errors=[
                f"Invalid assignment id {assignment_id}; please contact your instructor.",
                request.vars,
            ],
            masterapp=masterapp,
        )

    elif practice:
        _launch_practice(outcome_url, result_source_did, user, course_id)

    # else just redirect to the book index
    redirect(get_course_url("index.html"))


def _launch_practice(outcome_url, result_source_did, user, course_id):
    if outcome_url and result_source_did:
        db.practice_grades.update_or_insert(
            (db.practice_grades.auth_user == user.id),
            auth_user=user.id,
            lis_result_sourcedid=result_source_did,
            lis_outcome_url=outcome_url,
            course_name=getCourseNameFromId(course_id),
        )
    else:  # don't overwrite outcome_url and result_source_did
        db.practice_grades.update_or_insert(
            (db.practice_grades.auth_user == user.id),
            auth_user=user.id,
            course_name=getCourseNameFromId(course_id),
        )
    redirect(
        URL(
            "assignments",
            "settz_then_practice",
            vars={"course_name": user["course_name"]},
        )
    )


def _launch_assignment(assignment_id, user, result_source_did, outcome_url):
    assignment = (
        db(db.assignments.id == assignment_id).select(db.assignments.released).first()
    )
    # If the assignment isn't valid, return instead of redirecting. The caller will report the error.
    if not assignment:
        return
    grade = (
        db((db.grades.auth_user == user.id) & (db.grades.assignment == assignment_id))
        .select(db.grades.lis_result_sourcedid, db.grades.lis_outcome_url)
        .first()
    )
    send_grade = (
        assignment
        and assignment.released
        and grade
        and not grade.lis_result_sourcedid
        and not grade.lis_outcome_url
    )

    # save the guid and url for reporting back the grade
    db.grades.update_or_insert(
        (db.grades.auth_user == user.id) & (db.grades.assignment == assignment_id),
        auth_user=user.id,
        assignment=assignment_id,
        lis_result_sourcedid=result_source_did,
        lis_outcome_url=outcome_url,
    )
    if send_grade:
        _try_to_send_lti_grade(user.id, assignment_id)

    redirect(URL("assignments", "doAssignment", vars={"assignment_id": assignment_id}))


def _provide_assignment_list(course_id, consumer):
    """Gather all of the assignments for this course package them up
    per https://www.imsglobal.org/specs/lticiv1p0/specification
    and return a form.

    This form is then auto-submitted by javascript
    The key element of the form is the content_items structure which should look like this:
    .. code-block::

        {
        "@context" : "http://purl.imsglobal.org/ctx/lti/v1/ContentItem",
        "@graph" : [
            { "@type" : "LtiLinkItem",
                "@id" : ":item2",
                "icon" : { OPTIONAL
                    "@id" : "http://tool.provider.com/icons/small.png",
                    "width" : 50,
                    "height" : 50
                },
                "thumbnail" : { OPTIONAL
                    "@id" : "http://tool.provider.com/images/thumb.jpg",
                    "width" : 100,
                    "height" : 150
                },
                "title" : "Open sIMSon application",
                "text" : "The &lt;em&gt;sIMSon&lt;/em&gt; application provides a collaborative space for developing semantic modelling skills.",
                "mediaType" : "application/vnd.ims.lti.v1.ltilink",
                "custom" : {
                    "level" : "novice",
                    "mode" : "interactive"
                },
            },
            ]
        }
        keys are to include custom parameters for course_id and assignment_id
        using mediaType as specified will allow the TC to use the usual LTI
        launch mechanism
    """
    rdict = {}
    rdict["oauth_timestamp"] = str(int(time.time()))
    rdict["oauth_nonce"] = str(uuid.uuid1().int)
    rdict["oauth_consumer_key"] = consumer.key
    rdict["oauth_signature_method"] = "HMAC-SHA1"
    rdict["lti_message_type"] = "ContentItemSelection"
    rdict["lti_version"] = "LTI-1p0"
    rdict["oauth_version"] = "1.0"
    rdict["oauth_callback"] = "about:blank"
    extra_data = request.vars.get("data", None)
    if extra_data:
        rdict["data"] = extra_data

    return_url = request.vars.get("content_item_return_url")
    # return_url = "http://dev.runestoneinteractive.org/runestone/lti/fakestore"

    query_res = db(db.assignments.course == course_id).select(
        orderby=~db.assignments.duedate
    )
    result = {
        "@context": "http://purl.imsglobal.org/ctx/lti/v1/ContentItem",
        "@graph": [],
    }
    if query_res:
        for assignment in query_res:
            item = {
                "@type": "LtiLinkItem",
                "mediaType": "application/vnd.ims.lti.v1.ltilink",
                "@id": assignment.id,
                "title": assignment.name,
                "text": assignment.description,
                "custom": {
                    "custom_course_id": course_id,
                    "assignment_id": assignment.id,
                },
            }
            result["@graph"].append(item)

        result = json.dumps(result)
        rdict["content_items"] = result
        # response.view = "/srv/web2py/applications/runestone/views/lti/store.html"
        # req = oauth2.Request("post", return_url, rdict, is_form_encoded=True)
        req = oauth2.Request.from_consumer_and_token(
            consumer,
            token=None,
            http_method="POST",
            http_url=return_url,
            parameters=rdict,
            is_form_encoded=True,
        )
        req.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, None)
        rdict["return_url"] = return_url
        rdict["oauth_signature"] = req["oauth_signature"].decode("utf8")
        rdict["content_items"] = html.escape(result)
        tplate = """
        <!DOCTYPE html>
        <html>
        <body>
        <form name="storeForm" action="{return_url}" method="post" encType="application/x-www-form-urlencoded">
        <input type="hidden" name="lti_message_type" value="ContentItemSelection" />
        <input type="hidden" name="lti_version" value="LTI-1p0" />
        <input type="hidden" name="content_items" value="{content_items}" />
        """
        tplate += (
            """ <input type="hidden" name="data" value="{data}" /> """
            if extra_data
            else ""
        )
        tplate += """
        <input type="hidden" name="oauth_version" value="1.0" />
        <input type="hidden" name="oauth_nonce" value="{oauth_nonce}" />
        <input type="hidden" name="oauth_timestamp" value="{oauth_timestamp}" />
        <input type="hidden" name="oauth_consumer_key" value="{oauth_consumer_key}" />
        <input type="hidden" name="oauth_callback" value="about:blank" />
        <input type="hidden" name="oauth_signature_method" value="HMAC-SHA1" />
        <input type="hidden" name="oauth_signature" value="{oauth_signature}" />
        </form>
        """
        tplate = tplate.format(**rdict)

        scpt = """
        <script type="text/javascript">
            window.onload=function(){
                var auto = setTimeout(function(){ submitform(); }, 1000);

                function submitform(){
                    console.log(document.forms["storeForm"]);
                    document.forms["storeForm"].submit();
                }
            }
        </script>
        </body>
        </html>
        """
        return tplate + scpt


def fakestore():
    # define this function just to show what is coming through
    # I'm going to keep this around as it may be useful for future debugging.
    content = request.vars.get("content_items")
    consumer = oauth2.Consumer("bnm.runestone", "supersecret")
    return_url = "http://dev.runestoneinteractive.org/runestone/lti/fakestore"
    d = dict(request.vars)
    req = oauth2.Request.from_consumer_and_token(
        consumer,
        token=None,
        http_method="POST",
        http_url=return_url,
        parameters=d,
        is_form_encoded=True,
    )
    req.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, None)

    for k, v in req.items():
        print(f"{k} : {v}")
    print(req.method)
    print(req.normalized_url)
    print(req.get_normalized_parameters())

    return f" sent sig = {d['oauth_signature']} computed sig {req['oauth_signature'].decode('utf8')} {d}"
