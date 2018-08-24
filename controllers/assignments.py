from os import path
import os
import shutil
import sys
import json
import logging
import datetime
from collections import OrderedDict
from psycopg2 import IntegrityError
from rs_grading import do_autograde, do_calculate_totals, do_check_answer, send_lti_grade

logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)

# todo: This is a strange place for this function or at least a strange name.
# index is called to show the student progress page from the user menu -- its redundant with studentreport in dashboard
def index():
    if not auth.user:
        session.flash = "Please Login"
        return redirect(URL('default', 'index'))
    if 'sid' not in request.vars:
        #return redirect(URL('assignments','index') + '?sid=%s' % (auth.user.username))
        request.vars.sid = auth.user.username

    student = db(db.auth_user.username == request.vars.sid).select(
        db.auth_user.id,
        db.auth_user.username,
        db.auth_user.first_name,
        db.auth_user.last_name,
        db.auth_user.email,
    ).first()
    if not student:
        return redirect(URL('assignments', 'index'))

    if auth.user.course_name in ['thinkcspy', 'pythonds', 'JavaReview', 'webfundamentals', 'StudentCSP', 'apcsareview']:
        session.flash = "{} is not a graded course".format(auth.user.course_name)
        return redirect(URL('default', 'user'))

    data_analyzer = DashboardDataAnalyzer(auth.user.course_id)
    data_analyzer.load_user_metrics(request.vars.sid)
    data_analyzer.load_assignment_metrics(request.vars.sid, studentView=True)

    chapters = []
    for chapter_label, chapter in data_analyzer.chapter_progress.chapters.iteritems():
        chapters.append({
            "label": chapter.chapter_label,
            "status": chapter.status_text(),
            "subchapters": chapter.get_sub_chapter_progress()
        })
    activity = data_analyzer.formatted_activity.activities

    return dict(student=student, course_id=auth.user.course_id, course_name=auth.user.course_name,
                user=data_analyzer.user, chapters=chapters, activity=activity, assignments=data_analyzer.grades)


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def record_assignment_score():
    score = request.vars.get('score', None)
    assignment_name = request.vars.assignment
    assignment = db(
        (db.assignments.name == assignment_name) & (db.assignments.course == auth.user.course_id)).select().first()
    if assignment:
        assignment_id = assignment.id
    else:
        return json.dumps({'success': False, 'message': "Select an assignment before trying to calculate totals."})

    if score:
        # Write the score to the grades table
        # grades table expects row ids for auth_user and assignment
        sname = request.vars.get('sid', None)
        sid = db((db.auth_user.username == sname)).select(db.auth_user.id).first().id
        db.grades.update_or_insert(
            ((db.grades.auth_user == sid) &
             (db.grades.assignment == assignment_id)),
            auth_user=sid,
            assignment=assignment_id,
            score=score,
            manual_total=True
        )

# download a CSV with the student's performance on all assignments so far
@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def download_time_spent():
    course = db(db.courses.id == auth.user.course_id).select().first()
    students = db(db.auth_user.course_id == course.id).select()
    assignments = db(db.assignments.course == course.id)(db.assignments.assignment_type == db.assignment_types.id
                                                         ).select(orderby=db.assignments.assignment_type)
    grades = db(db.grades).select()

    field_names = ['Lastname','Firstname','Email','Total']
    type_names = []
    assignment_names = []

    # datestr should be in format "05-20-13"
    datestr = request.vars.as_of
    try:
        as_of_timestamp = datetime.datetime.strptime(datestr, '%m-%d-%y')
    except:
        return dict(error="Please enter ?as_of=03-24-16")
    # probably broken now; assignment_types is deprecated and maybe not filled in correctly
    # assignment_types = db(db.assignment_types).select(db.assignment_types.ALL, orderby=db.assignment_types.name)
    rows = [CourseGrade(user = student,
                        course=course,
                        assignment_types=[]).csv(type_names,
                                                 assignment_names,
                                                 as_of_timestamp=as_of_timestamp
                                                 ) for student in students]
    response.view='generic.csv'
    return dict(filename='grades_download.csv', csvdata=rows, field_names=field_names+type_names+assignment_names)


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def calculate_totals():
    assignment_name = request.vars.assignment
    sid = request.vars.get('sid', None)
    assignment = db(
        (db.assignments.name == assignment_name) & (db.assignments.course == auth.user.course_id)).select().first()
    if assignment:
        return json.dumps(
            do_calculate_totals(assignment, auth.user.course_id, auth.user.course_name, sid, db, settings))
    else:
        return json.dumps({'success': False, 'message': "Select an assignment before trying to calculate totals."})


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def autograde():
    ### This endpoint is hit to autograde one or all students or questions for an assignment

    sid = request.vars.get('sid', None)
    question_name = request.vars.get('question', None)
    enforce_deadline = request.vars.get('enforceDeadline', None)
    assignment_name = request.vars.assignment
    timezoneoffset = session.timezoneoffset if 'timezoneoffset' in session else None

    assignment = db(
        (db.assignments.name == assignment_name) & (db.assignments.course == auth.user.course_id)).select().first()
    if assignment:
        count = do_autograde(assignment, auth.user.course_id, auth.user.course_name, sid, question_name,
                             enforce_deadline, timezoneoffset, db, settings)
        return json.dumps({'message': "autograded {} items".format(count)})
    else:
        return json.dumps({'success': False, 'message': "Select an assignment before trying to autograde."})

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def record_grade():
    if 'acid' not in request.vars or 'sid' not in request.vars:
        return json.dumps({'success': False, 'message': "Need problem and user."})

    score_str = request.vars.get('grade', 0)
    if score_str == "":
        score = 0
    else:
        score = float(score_str)
    comment = request.vars.get('comment', None)
    if score_str != "" or ('comment' in request.vars and comment != ""):
        try:
            db.question_grades.update_or_insert(( \
                        (db.question_grades.sid == request.vars['sid']) \
                        & (db.question_grades.div_id == request.vars['acid']) \
                        & (db.question_grades.course_name == auth.user.course_name) \
                ),
                sid=request.vars['sid'],
                div_id=request.vars['acid'],
                course_name=auth.user.course_name,
                score=score,
                comment=comment)
        except IntegrityError:
            logger.error(
                "IntegrityError {} {} {}".format(request.vars['sid'], request.vars['acid'], auth.user.course_name))
            return json.dumps({'response': 'not replaced'})
        return json.dumps({'response': 'replaced'})
    else:
        return json.dumps({'response': 'not replaced'})


# create a unique index:  question_grades_sid_course_name_div_id_idx" UNIQUE, btree (sid, course_name, div_id)

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def get_problem():
    if 'acid' not in request.vars or 'sid' not in request.vars:
        return json.dumps({'success': False, 'message': "Need problem and user."})

    user = db(db.auth_user.username == request.vars.sid).select().first()
    if not user:
        return json.dumps({'success': False, 'message': "User does not exist. Sorry!"})

    res = {
        'id': "%s-%d" % (request.vars.acid, user.id),
        'acid': request.vars.acid,
        'sid': user.id,
        'username': user.username,
        'name': "%s %s" % (user.first_name, user.last_name),
        'code': ""
    }

    # get the deadline associated with the assignment
    assignment_name = request.vars.assignment
    if assignment_name and auth.user.course_id:
        assignment = db(
            (db.assignments.name == assignment_name) & (db.assignments.course == auth.user.course_id)).select().first()
        deadline = assignment.duedate
    else:
        deadline = None

    offset = datetime.timedelta(0)
    if session.timezoneoffset and deadline:
        offset = datetime.timedelta(hours=int(session.timezoneoffset))
        logger.debug("setting offset %s %s", offset, deadline + offset)

    query = (db.code.acid == request.vars.acid) & (db.code.sid == request.vars.sid) & (
            db.code.course_id == auth.user.course_id)
    if request.vars.enforceDeadline == "true" and deadline:
        query = query & (db.code.timestamp < deadline + offset)
        logger.debug("DEADLINE QUERY = %s", query)
    c = db(query).select(orderby=db.code.id).last()

    if c:
        res['code'] = c.code

    # add prefixes, suffix_code and files that are available
    # retrieve the db record
    source = db.source_code(acid=request.vars.acid, course_id=auth.user.course_name)

    if source and c and c.code:
        def get_source(acid):
            r = db.source_code(acid=acid)
            if r:
                return r.main_code
            else:
                return ""

        if source.includes:
            # strip off "data-include"
            txt = source.includes[len("data-include="):]
            included_divs = [x.strip() for x in txt.split(',') if x != '']
            # join together code for each of the includes
            res['includes'] = '\n'.join([get_source(acid) for acid in included_divs])
            # logger.debug(res['includes'])
        if source.suffix_code:
            res['suffix_code'] = source.suffix_code
            # logger.debug(source.suffix_code)

        file_divs = [x.strip() for x in source.available_files.split(',') if x != '']
        res['file_includes'] = [{'acid': acid, 'contents': get_source(acid)} for acid in file_divs]
    return json.dumps(res)


def doAssignment():
    if not auth.user:
        session.flash = "Please Login"
        return redirect(URL('default', 'index'))

    course = db(db.courses.id == auth.user.course_id).select().first()
    assignment_id = request.vars.assignment_id
    if not assignment_id or assignment_id.isdigit() == False:
        logger.error("BAD ASSIGNMENT = %s assignment %s", course, assignment_id)
        session.flash = "Bad Assignment ID"
        return redirect(URL("assignments", "chooseAssignment"))

    logger.debug("COURSE = %s assignment %s", course, assignment_id)
    assignment = db(
        (db.assignments.id == assignment_id) & (db.assignments.course == auth.user.course_id)).select().first()

    if not assignment:
        logger.error("NO ASSIGNMENT assign_id = %s course = %s user = %s", assignment_id, course, auth.user.username)
        session.flash = "Could not find login and try again."
        return redirect(URL('default', 'index'))

    if assignment.visible == 'F' or assignment.visible == None:
        if verifyInstructorStatus(auth.user.course_name, auth.user) == False:
            session.flash = "That assignment is no longer available"
            return redirect(URL('assignments', 'chooseAssignment'))

    questions = db((db.assignment_questions.assignment_id == assignment.id) & \
                   (db.assignment_questions.question_id == db.questions.id)) \
        .select(db.questions.name,
                db.questions.htmlsrc,
                db.questions.id,
                db.questions.chapter,
                db.questions.subchapter,
                db.assignment_questions.points,
                db.assignment_questions.activities_required,
                db.assignment_questions.reading_assignment,
                orderby=db.assignment_questions.sorting_priority)


    try:
        db.useinfo.insert(sid=auth.user.username,act='viewassignment',div_id=assignment.name,
                          event='page',
                          timestamp=datetime.datetime.utcnow(),course_id=course.course_name)
    except:
        logger.debug('failed to insert log record for {} in {} : doAssignment '.format(auth.user.username, course.course_name))

    questionslist = []
    questions_score = 0
    readings = OrderedDict()
    readings_score = 0

    # For each question, accumulate information, and add it to either the readings or questions data structure
    # If scores have not been released for the question or if there are no scores yet available, the scoring information will be recorded as empty strings

    for q in questions:
        if q.questions.htmlsrc:
            # This replacement is to render images
            htmlsrc = bytes(q.questions.htmlsrc).decode('utf8').replace('src="../_static/', 'src="../static/' + course[
                'course_name'] + '/_static/')
            htmlsrc = htmlsrc.replace("../_images",
                                      "/{}/static/{}/_images".format(request.application, course.course_name))
        else:
            htmlsrc = None
        if assignment['released']:
            # get score and comment
            grade = db((db.question_grades.sid == auth.user.username) &
                       (db.question_grades.div_id == q.questions.name)).select().first()
            if grade:
                score, comment = grade.score, grade.comment
            else:
                score, comment = 0, 'ungraded'
        else:
            score, comment = 0, 'ungraded'

        info = dict(
            htmlsrc=htmlsrc,
            score=score,
            points=q.assignment_questions.points,
            comment=comment,
            chapter=q.questions.chapter,
            subchapter=q.questions.subchapter,
            name=q.questions.name,
            activities_required=q.assignment_questions.activities_required
        )
        if q.assignment_questions.reading_assignment:
            # add to readings
            if q.questions.chapter not in readings:
                # add chapter info
                completion = db((db.user_chapter_progress.user_id == auth.user.id) & \
                                (db.user_chapter_progress.chapter_id == q.questions.chapter)).select().first()
                if not completion:
                    status = 'notstarted'
                elif completion.status == 1:
                    status = 'completed'
                elif completion.status == 0:
                    status = 'started'
                else:
                    status = 'notstarted'
                readings[q.questions.chapter] = dict(status=status, subchapters=[])

            # add subchapter info
            # add completion status to info
            subch_completion = db((db.user_sub_chapter_progress.user_id == auth.user.id) & \
                                  (
                                          db.user_sub_chapter_progress.sub_chapter_id == q.questions.subchapter)).select().first()
            if not subch_completion:
                status = 'notstarted'
            elif subch_completion.status == 1:
                status = 'completed'
            elif subch_completion.status == 0:
                status = 'started'
            else:
                status = 'notstarted'
            info['status'] = status

            readings[q.questions.chapter]['subchapters'].append(info)
            readings_score += info['score']

        else:
            # add to questions
            questionslist.append(info)
            questions_score += info['score']

    return dict(course=course,
                course_name=auth.user.course_name,
                assignment=assignment,
                questioninfo=questionslist,
                course_id=auth.user.course_name,
                readings=readings,
                questions_score=questions_score,
                readings_score=readings_score)


def chooseAssignment():
    if not auth.user:
        session.flash = "Please Login"
        return redirect(URL('default', 'index'))

    course = db(db.courses.id == auth.user.course_id).select().first()
    assignments = db((db.assignments.course == course.id) & (db.assignments.visible == 'T')).select(
        orderby=db.assignments.duedate)
    return (dict(assignments=assignments))


# The rest of the file is about the the spaced practice:

def _get_lti_record(oauth_consumer_key):
    return db(db.lti_keys.consumer == oauth_consumer_key).select().first()

def _get_course_practice_record(course_name):
    return db(db.course_practice.course_name == course_name).select().first()

def _get_student_practice_grade(sid, course_name):
    return db((db.practice_grades.auth_user==sid) &
              (db.practice_grades.course_name==course_name)).select().first()

def _get_practice_completion_count(user_id, course_name):
    return db((db.user_topic_practice_Completion.course_name == course_name) & \
       (db.user_topic_practice_Completion.user_id == user_id)).count()

# Called when user clicks "I'm done" button.
def checkanswer():
    if not auth.user:
        session.flash = "Please Login"
        return redirect(URL('default', 'index'))

    sid = auth.user.id
    course_name = auth.user.course_name
    # Retrieve the question id from the request object.
    qid = request.vars.get('QID', None)
    username = auth.user.username
    # Retrieve the q (quality of answer) from the request object.
    q = request.vars.get('q', None)

    # If the question id exists:
    if request.vars.QID:
        now = datetime.datetime.utcnow()
        # Use the autograding function to update the flashcard's e-factor and i-interval.
        do_check_answer(sid, course_name, qid, username, q, db, settings, now,
                        datetime.timedelta(hours=int(session.timezoneoffset)))

        # That scored the particular question. So now get the total number completed and send grade back via LTI
        completion_count = _get_practice_completion_count(sid, course_name)

        lti_record = _get_lti_record(session.oauth_consumer_key)
        practice_grade = _get_student_practice_grade(sid, course_name)
        course_settings = _get_course_practice_record(course_name)
        # print "count:", completion_count
        # print "lti_record:", lti_record,
        # print "practice_grade:", practice_grade,
        # print "course_settings:", course_settings
        if lti_record and practice_grade and course_settings:
            send_lti_grade(assignment_points=course_settings.max_practice_days,
                           score=completion_count,
                           consumer=lti_record.consumer,
                           secret=lti_record.secret,
                           outcome_url=practice_grade.lis_outcome_url,
                           result_sourcedid=practice_grade.lis_result_sourcedid)

        # Since the user wants to continue practicing, continue with the practice action.
        redirect(URL('practice'))
    session.flash = "Sorry, your score was not saved. Please try submitting your answer again."
    redirect(URL('practice'))


# Only questions that are marked for practice are eligible for the spaced practice.
def _get_qualified_questions(base_course, chapter_label, sub_chapter_label):
    return db((db.questions.base_course == base_course) & \
              (db.questions.topic == "{}/{}".format(chapter_label, sub_chapter_label)) & \
              (db.questions.practice == True)).select()


# Gets invoked from lti to set timezone and then redirect to practice()
def settz_then_practice():
    return dict(course_name=request.vars.get('course_name', 'UMSI106'))


# Gets invoked when the student requests practicing topics.
def practice():
    if not auth.user:
        session.flash = "Please Login"
        return redirect(URL('default', 'index'))

    now = datetime.datetime.utcnow() - datetime.timedelta(hours=int(session.timezoneoffset))

    # Calculates the remaining days to the end of the semester. If your semester ends at any time other than April 19,
    # 2018, please replace it.
    remaining_days = (datetime.date(2018, 4, 19) - now.date()).days

    # Since each authenticated user has only one active course, we retrieve the course this way.
    course = db(db.courses.id == auth.user.course_id).select().first()

    # Retrieve the existing flashcards in the current course for this user.
    existing_flashcards = db((db.user_topic_practice.course_name == auth.user.course_name) & \
                             (db.user_topic_practice.user_id == auth.user.id))

    # If the user already has flashcards for the current course.
    if existing_flashcards.isempty():
        # new student; create flashcards
        # We only create flashcards for those sections that are marked by the instructor as taught.
        subchaptersTaught = db((db.sub_chapter_taught.course_name == auth.user.course_name) & \
                               (db.sub_chapter_taught.chapter_name == db.chapters.chapter_name) & \
                               (db.sub_chapter_taught.sub_chapter_name == db.sub_chapters.sub_chapter_name) & \
                               (db.chapters.course_id == auth.user.course_name) & \
                               (db.sub_chapters.chapter_id == db.chapters.id)) \
            .select(db.chapters.chapter_label, db.chapters.chapter_name, db.sub_chapters.sub_chapter_label,
                    orderby=db.chapters.id | db.sub_chapters.id)
        for subchapterTaught in subchaptersTaught:
            # We only retrive questions to be used in flashcards if they are marked for practice purpose.
            questions = _get_qualified_questions(course.base_course,
                                                 subchapterTaught.chapters.chapter_label,
                                                 subchapterTaught.sub_chapters.sub_chapter_label)
            if len(questions) > 0:
                # There is at least one qualified question in this subchapter, so insert a flashcard for the subchapter.
                db.user_topic_practice.insert(
                    user_id=auth.user.id,
                    course_name=auth.user.course_name,
                    chapter_label=subchapterTaught.chapters.chapter_label,
                    sub_chapter_label=subchapterTaught.sub_chapters.sub_chapter_label,
                    question_name=questions[0].name,
                    # Treat it as if the first eligible question is the last one asked.
                    i_interval=0,
                    e_factor=2.5,
                    # add as if yesterday, so can practice right away
                    last_presented=now.date() - datetime.timedelta(1),
                    last_completed=now.date() - datetime.timedelta(1),
                    creation_time=now,
                )

    # How many times has this user submitted their practice from the beginning of today (12:00 am) till now?
    practiced_today_count = db((db.user_topic_practice_log.course_name == auth.user.course_name) & \
                               (db.user_topic_practice_log.user_id == auth.user.id) & \
                               (db.user_topic_practice_log.q != 0) & \
                               (db.user_topic_practice_log.q != -1) & \
                               (db.user_topic_practice_log.end_practice >= datetime.datetime(now.year,
                                                                                             now.month,
                                                                                             now.day,
                                                                                             0, 0, 0, 0))).count()
    # Retrieve all the falshcards created for this user in the current course and order them by their order of creation.
    flashcards = db((db.user_topic_practice.course_name == auth.user.course_name) & \
                    (db.user_topic_practice.user_id == auth.user.id)).select(orderby=db.user_topic_practice.id)
    # Select only those where enough time has passed since last presentation.
    presentable_flashcards = [f for f in flashcards if
                              (now.date() - f.last_completed.date()).days >= f.i_interval]

    all_flashcards = db((db.user_topic_practice.course_name == auth.user.course_name) & \
                        (db.user_topic_practice.user_id == auth.user.id) & \
                        (db.user_topic_practice.chapter_label == db.chapters.chapter_label) & \
                        (db.user_topic_practice.sub_chapter_label == db.sub_chapters.sub_chapter_label) & \
                        (db.chapters.course_id == auth.user.course_name) & \
                        (db.sub_chapters.chapter_id == db.chapters.id)) \
            .select(db.chapters.chapter_name, db.sub_chapters.sub_chapter_name, db.user_topic_practice.i_interval,
                db.user_topic_practice.last_completed, orderby=db.user_topic_practice.id)
    for f_card in all_flashcards:
        f_card["remaining_days"] = max(0, f_card.user_topic_practice.i_interval -
                                       (now.date() - f_card.user_topic_practice.last_completed.date()).days)
        f_card["mastery_percent"] = int(100 * f_card["remaining_days"] // 55)
        f_card["mastery_color"] = "danger"
        if f_card["mastery_percent"] >= 75:
            f_card["mastery_color"] = "success"
        elif f_card["mastery_percent"] >= 50:
            f_card["mastery_color"] = "info"
        elif f_card["mastery_percent"] >= 25:
            f_card["mastery_color"] = "warning"

    # Define how many topics you expect your students practice every day.
    practice_times_to_pass_today = 10

    # If the student has any flashcards to practice and has not practiced enough to get their points for today or they
    # have intrinsic motivation to practice beyond what they are expected to do.
    if len(presentable_flashcards) > 0 and (practiced_today_count != practice_times_to_pass_today or
                                            request.vars.willing_to_continue):
        # Present the first one.
        flashcard = presentable_flashcards[0]
        # Get eligible questions.
        questions = _get_qualified_questions(course.base_course,
                                             flashcard.chapter_label,
                                             flashcard.sub_chapter_label)
        # Find index of the last question asked.
        question_names = [q.name for q in questions]
        qIndex = question_names.index(flashcard.question_name)
        # present the next one in the list after the last one that was asked
        question = questions[(qIndex + 1) % len(questions)]

        # This replacement is to render images
        question.htmlsrc = bytes(question.htmlsrc).decode('utf8').replace('src="../_static/',
                                                                          'src="../static/' + course[
                                                                              'course_name'] + '/_static/')
        question.htmlsrc = question.htmlsrc.replace("../_images",
                                                    "/{}/static/{}/_images".format(request.application,
                                                                                   course.course_name))

        autogradable = 1
        # If it is possible to autograde it:
        if ((question.autograde is not None) or
                (question.question_type is not None and question.question_type in
                 ['mchoice', 'parsonsprob', 'fillintheblank', 'clickablearea', 'dragndrop'])):
            autogradable = 2

        questioninfo = [question.htmlsrc, question.name, question.id, autogradable]

        # This is required to check the same question in do_check_answer().
        flashcard.question_name = question.name
        # This is required to only check answers after this timestamp in do_check_answer().
        flashcard.last_presented = now
        flashcard.update_record()

    else:
        questioninfo = None

        # Add a practice completion record for today, if there isn't one already.
        practice_completion_today = db((db.user_topic_practice_Completion.course_name == auth.user.course_name) & \
                                       (db.user_topic_practice_Completion.user_id == auth.user.id) & \
                                       (db.user_topic_practice_Completion.practice_completion_time == now.date()))
        if practice_completion_today.isempty():
            db.user_topic_practice_Completion.insert(
                user_id=auth.user.id,
                course_name=auth.user.course_name,
                practice_completion_time=now.date()
            )

    # The number of days the student has completed their practice.
    practice_completion_count = db((db.user_topic_practice_Completion.course_name == auth.user.course_name) & \
                                   (db.user_topic_practice_Completion.user_id == auth.user.id)).count()

    # Calculate the number of times left for the student to practice today to get the completion point.
    practice_today_left = min(len(presentable_flashcards), max(0, practice_times_to_pass_today - practiced_today_count))

    return dict(course=course, course_name=auth.user.course_name,
                course_id=auth.user.course_name,
                q=questioninfo, all_flashcards=all_flashcards,
                flashcard_count=len(presentable_flashcards),
                # The number of days the student has completed their practice.
                practice_completion_count=practice_completion_count,
                remaining_days=remaining_days, max_days=45,
                # The number of times remaining to practice today to get the completion point.
                practice_today_left=practice_today_left,
                # The number of times this user has submitted their practice from the beginning of today (12:00 am) till now.
                practiced_today_count=practiced_today_count)


# Called when user clicks like or dislike icons.
def like_dislike():
    if not auth.user:
        session.flash = "Please Login"
        return redirect(URL('default', 'index'))

    sid = auth.user.id
    course_name = auth.user.course_name
    likeVal = request.vars.get('likeVal', None)

    if likeVal:
        db.user_topic_practice_survey.insert(
            user_id=sid,
            course_name=course_name,
            like_practice=likeVal,
            response_time=datetime.datetime.now(),
        )
        return json.dumps(dict(complete=True))
    session.flash = "Sorry, your request was not saved. Please login and try again."
    redirect(URL('practice'))
