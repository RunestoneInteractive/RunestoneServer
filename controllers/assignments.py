from os import path
import os
import shutil
import sys
import json
import logging
import datetime
from psycopg2 import IntegrityError
from db_dashboard import DashboardDataAnalyzer

logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)

# todo: This is a strange place for this function or at least a strange name.
# index is called to show the student progress page from the user menu -- its redundant with studentreport in dashboard
def index():
    if not auth.user:
        session.flash = "Please Login"
        return redirect(URL('default','index'))
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
        return redirect(URL('assignments','index'))

    if auth.user.course_name in ['thinkcspy','pythonds','JavaReview','webfundamentals','StudentCSP','apcsareview']:
        session.flash = "{} is not a graded course".format(auth.user.course_name)
        return redirect(URL('default','user'))

    data_analyzer = DashboardDataAnalyzer(db, auth, auth.user.course_id)
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

    return dict(student=student, course_id=auth.user.course_id, course_name=auth.user.course_name, user=data_analyzer.user, chapters=chapters, activity=activity, assignments=data_analyzer.grades)


def _score_from_pct_correct(pct_correct, points, autograde):
    # ALL_AUTOGRADE_OPTIONS = ['all_or_nothing', 'pct_correct', 'interact']
    if autograde == 'interact' or autograde == 'visited':
        return points
    elif autograde == 'pct_correct':
        # prorate credit based on percentage correct
        return int(round((pct_correct * points)/100.0))
    elif autograde == 'all_or_nothing' or autograde == 'unittest':
        # 'unittest' is legacy, now deprecated
        # have to get *all* tests to pass in order to get any credit
        if pct_correct == 100:
            return points
        else:
            return 0


def _score_one_code_run(row, points, autograde):
    # row is one row from useinfo table
    # second element of act is the percentage of tests that passed
    if autograde == 'interact':
        return _score_one_interaction(row, points, autograde)

    try:
        (ignore, pct, ignore, passed, ignore, failed) = row.act.split(':')
        pct_correct = 100 * float(passed)/(int(failed) + int(passed))
    except:
        pct_correct = 0 # can still get credit if autograde is 'interact' or 'visited'; but no autograded value
    return _score_from_pct_correct(pct_correct, points, autograde)

def _score_one_mchoice(row, points, autograde):
    # row is from mchoice_answers
    ## It appears that the mchoice_answers is only storing a binary correct_or_not
    ## If that is updated to store a pct_correct, the next few lines can change
    if row.correct:
        pct_correct = 100
    else:
        pct_correct = 0
    return _score_from_pct_correct(pct_correct, points, autograde)

def _score_one_interaction(row, points, autograde):
    # row is from useinfo
    if row:
        return points
    else:
        return 0

def _score_one_parsons(row, points, autograde):
    # row is from parsons_answers
    # Much like mchoice, parsons_answers currently stores a binary correct value
    # So much like in _score_one_mchoice, the next lines can be altered if a pct_correct value is added to parsons_answers
    if row.correct:
        pct_correct = 100
    else:
        pct_correct = 0
    return _score_from_pct_correct(pct_correct, points, autograde)

def _score_one_fitb(row, points, autograde):
    # row is from fitb_answers
    if row.correct:
        pct_correct = 100
    else:
        pct_correct = 0
    return _score_from_pct_correct(pct_correct, points, autograde)

def _score_one_clickablearea(row, points, autograde):
    # row is from clickablearea_answers
    if row.correct:
        pct_correct = 100
    else:
        pct_correct = 0
    return _score_from_pct_correct(pct_correct, points, autograde)

def _score_one_dragndrop(row, points, autograde):
    # row is from dragndrop_answers
    if row.correct:
        pct_correct = 100
    else:
        pct_correct = 0
    return _score_from_pct_correct(pct_correct, points, autograde)

def _score_one_codelens(row, points, autograde):
    # row is from codelens_answers
    if row.correct:
        pct_correct = 100
    else:
        pct_correct = 0
    return _score_from_pct_correct(pct_correct, points, autograde)


def _scorable_mchoice_answers(course_name, sid, question_name, points, deadline):
    query = ((db.mchoice_answers.course_name == course_name) & \
            (db.mchoice_answers.sid == sid) & \
            (db.mchoice_answers.div_id == question_name) \
            )
    if deadline:
        query = query & (db.mchoice_answers.timestamp < deadline)
    return db(query).select(orderby=db.mchoice_answers.timestamp)

def _scorable_useinfos(course_name, sid, div_id, points, deadline, event_filter = None, question_type=None):
    # look in useinfo, to see if visited (before deadline)
    # sid matches auth_user.username, not auth_user.id
    # if question type is page we must do better with the div_id

    query = ((db.useinfo.course_id == course_name) & \
            (db.useinfo.sid == sid))

    if question_type == 'page':
        quest = db(db.questions.name == div_id).select().first()  #todo cache this translation somehow
        div_id = u"{}/{}".format(quest.chapter, quest.subchapter)
        query = query & (db.useinfo.div_id.contains(div_id))
    else:
        query = query & (db.useinfo.div_id == div_id)

    if event_filter:
        query = query & (db.useinfo.event == event_filter)
    if deadline:
        query = query & (db.useinfo.timestamp < deadline)
    return db(query).select(orderby=db.useinfo.timestamp)

def _scorable_parsons_answers(course_name, sid, question_name, points, deadline):
    query = ((db.parsons_answers.course_name == course_name) & \
            (db.parsons_answers.sid == sid) & \
            (db.parsons_answers.div_id == question_name) \
            )
    if deadline:
        query = query & (db.parsons_answers.timestamp < deadline)
    return db(query).select(orderby=db.parsons_answers.timestamp)

def _scorable_fitb_answers(course_name, sid, question_name, points, deadline):
    query = ((db.fitb_answers.course_name == course_name) & \
            (db.fitb_answers.sid == sid) & \
            (db.fitb_answers.div_id == question_name) \
            )
    if deadline:
        query = query & (db.fitb_answers.timestamp < deadline)
    return db(query).select(orderby=db.fitb_answers.timestamp)

def _scorable_clickablearea_answers(course_name, sid, question_name, points, deadline):
    query = ((db.clickablearea_answers.course_name == course_name) & \
            (db.clickablearea_answers.sid == sid) & \
            (db.clickablearea_answers.div_id == question_name) \
            )
    if deadline:
        query = query & (db.clickablearea_answers.timestamp < deadline)
    return db(query).select(orderby=db.clickablearea_answers.timestamp)

def _scorable_dragndrop_answers(course_name, sid, question_name, points, deadline):
    query = ((db.dragndrop_answers.course_name == course_name) & \
            (db.dragndrop_answers.sid == sid) & \
            (db.dragndrop_answers.div_id == question_name) \
            )
    if deadline:
        query = query & (db.dragndrop_answers.timestamp < deadline)
    return db(query).select(orderby=db.dragndrop_answers.timestamp)

def _scorable_codelens_answers(course_name, sid, question_name, points, deadline):
    query = ((db.codelens_answers.course_name == course_name) & \
            (db.codelens_answers.sid == sid) & \
            (db.codelens_answers.div_id == question_name) \
            )
    if deadline:
        query = query & (db.codelens_answers.timestamp < deadline)

    return db(query).select(orderby=db.codelens_answers.timestamp)

def _autograde_one_q(course_name, sid, question_name, points, question_type, deadline=None, autograde=None, which_to_grade=None, save_score=True):


    logger.debug("autograding %s %s %s %s %s %s", course_name, question_name, sid, deadline, autograde, which_to_grade)
    if not autograde:
        logger.debug("autograde not set returning 0")
        return 0

    # if previously manually graded, don't overwrite
    existing = db((db.question_grades.sid == sid) \
       & (db.question_grades.course_name == course_name) \
       & (db.question_grades.div_id == question_name) \
       ).select().first()
    if existing and (existing.comment != "autograded"):
        logger.debug("skipping; previously manually graded, comment = {}".format(existing.comment))
        return 0


    # For all question types, and values of which_to_grade, we have the same basic structure:
    # 1. Query the appropriate table to get rows representing student responses
    # 2. Apply a scoring function to the first, last, or all rows
    #   2a. if scoring 'best_answer', take the max score
    #   Note that the scoring function will take the autograde parameter as an input, which might
    #      affect how the score is determined.

    # get the results from the right table, and choose the scoring function
    if question_type in ['activecode', 'actex']:
        if autograde in ['pct_correct', 'all_or_nothing', 'unittest']:
            event_filter = 'unittest'
        else:
            event_filter = None
        results = _scorable_useinfos(course_name, sid, question_name, points, deadline, event_filter)
        scoring_fn = _score_one_code_run
    elif question_type == 'mchoice':
        results = _scorable_mchoice_answers(course_name, sid, question_name, points, deadline)
        scoring_fn = _score_one_mchoice
    elif question_type == 'page':
        # question_name does not help us
        results = _scorable_useinfos(course_name, sid, question_name, points, deadline, question_type='page')
        scoring_fn = _score_one_interaction
    elif question_type == 'parsonsprob':
        results = _scorable_parsons_answers(course_name, sid, question_name, points, deadline)
        scoring_fn = _score_one_parsons
    elif question_type == 'fillintheblank':
        results = _scorable_fitb_answers(course_name, sid, question_name, points, deadline)
        scoring_fn = _score_one_fitb
    elif question_type == 'clickablearea':
        results = _scorable_clickablearea_answers(course_name, sid, question_name, points, deadline)
        scoring_fn = _score_one_clickablearea
    elif question_type == 'dragndrop':
        results = _scorable_dragndrop_answers(course_name, sid, question_name, points, deadline)
        scoring_fn = _score_one_dragndrop
    elif question_type == 'codelens':
        if autograde == 'interact':  # this is probably what we want for *most* codelens it will not be correct when it is an actual codelens question in a reading
            results = _scorable_useinfos(course_name, sid, question_name, points, deadline)
            scoring_fn = _score_one_interaction
        else:
            results = _scorable_codelens_answers(course_name, sid, question_name, points, deadline)
            scoring_fn = _score_one_codelens
    elif question_type in ['video', 'showeval']:
        # question_name does not help us
        results = _scorable_useinfos(course_name, sid, question_name, points, deadline, question_type='video')
        scoring_fn = _score_one_interaction

    else:
        logger.debug("skipping; question_type = {}".format(question_type))
        return 0

    # use query results and the scoring function
    if results:
        if which_to_grade in ['first_answer', 'last_answer', None]:
            # get single row
            if which_to_grade == 'first_answer':
                row = results.first()
            elif which_to_grade == 'last_answer':
                row = results.last()
            else:
                # default is last
                row = results.last()
            # extract its score
            score = scoring_fn(row, points, autograde)
        elif which_to_grade == 'best_answer':
            # score all rows and take the best one
            best_row = max(results, key = lambda row: scoring_fn(row, points, autograde))
            score = scoring_fn(best_row, points, autograde)
            logger.debug("SCORE = %s by %s", score, scoring_fn)
        else:
            logger.error("Unknown Scoring Scheme %s ", which_to_grade)
            score = 0
    else:
        # no results found, score is 0, not attributed to any row
        score = 0

    # Save the score
    if save_score:
        _save_question_grade(sid, course_name, question_name, score, deadline)

    return score

def _save_question_grade(sid, course_name, question_name, score, deadline=None):
    try:
        db.question_grades.update_or_insert(
            ((db.question_grades.sid == sid) &
            (db.question_grades.course_name == course_name) &
            (db.question_grades.div_id == question_name)
            ),
            sid=sid,
            course_name=course_name,
            div_id=question_name,
            score = score,
            comment = "autograded",
            useinfo_id=None,
            deadline=deadline
        )
    except IntegrityError:
        logger.error("IntegrityError {} {} {}".format(sid, course_name, question_name))


def _compute_assignment_total(student, assignment, course_name):
    # return the computed score and the manual score if there is one; if no manual score, save computed score
    # student is a row, containing id and username
    # assignment is a row, containing name and id and points

    # Get all question_grades for this sid/assignment_id
    # Retrieve from question_grades table  with right sids and div_ids
    # sid is really a username, so look it up in auth_user
    # div_id is found in questions; questions are associated with assignments, which have assignment_id

    # print(student.id, assignment.id)

    # compute the score
    query =  (db.question_grades.sid == student.username) \
             & (db.question_grades.div_id == db.questions.name) \
             & (db.questions.id == db.assignment_questions.question_id) \
             & (db.assignment_questions.assignment_id == assignment.id) \
             & (db.question_grades.course_name == course_name )
    scores = db(query).select(db.question_grades.score)
    logger.debug("List of scores to add for %s is %s",student.username, scores)
    total = sum([row.score for row in scores if row.score])
    score = total

    grade = db(
        (db.grades.auth_user == student.id) &
        (db.grades.assignment == assignment.id)).select().first()

    if grade and grade.manual_total:
        # don't save it; return the calculated and the previous manual score
        return score, grade.score
    else:
        # Write the score to the grades table
        try:
            db.grades.update_or_insert(
                ((db.grades.auth_user == student.id) &
                 (db.grades.assignment == assignment.id)),
                auth_user = student.id,
                assignment = assignment.id,
                score=score)
        except IntegrityError:
            logger.error("IntegrityError update or insert {} {} with score {}"
                         .format(student.id, assignment.id, score))
        return score, None

def _get_students(course_id, sid = None):
    if sid:
        # sid which is passed in is a username, not a row id
        student_rows = db((db.user_courses.course_id == course_id) &
                          (db.user_courses.user_id == db.auth_user.id) &
                          (db.auth_user.username == sid)
                          ).select(db.auth_user.username, db.auth_user.id)
    else:
        # get all student usernames for this course
        student_rows = db((db.user_courses.course_id == course_id) &
                          (db.user_courses.user_id == db.auth_user.id)
                          ).select(db.auth_user.username, db.auth_user.id)
    return student_rows

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def record_assignment_score():
    score = request.vars.get('score', None)
    assignment_name = request.vars.assignment
    assignment = db((db.assignments.name == assignment_name) & (db.assignments.course == auth.user.course_id)).select().first()
    if assignment:
        assignment_id = assignment.id
    else:
        return json.dumps({'success':False, 'message':"Select an assignment before trying to calculate totals."})

    if score:
        # Write the score to the grades table
        # grades table expects row ids for auth_user and assignment
        sname = request.vars.get('sid', None)
        sid = db((db.auth_user.username == sname)).select(db.auth_user.id).first().id
        db.grades.update_or_insert(
            ((db.grades.auth_user == sid) &
            (db.grades.assignment == assignment_id)),
            auth_user = sid,
            assignment = assignment_id,
            score=score,
            manual_total=True
        )

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def calculate_totals():
    assignment_name = request.vars.assignment
    assignment = db((db.assignments.name == assignment_name) & (db.assignments.course == auth.user.course_id)).select().first()
    if assignment:
        assignment_id = assignment.id
    else:
        return json.dumps({'success':False, 'message':"Select an assignment before trying to calculate totals."})

    sid = request.vars.get('sid', None)

    student_rows = _get_students(auth.user.course_id, sid)

    results = {'success':True}
    if sid:
        computed_total, manual_score = _compute_assignment_total(student_rows[0], assignment, auth.user.course_name)
        results['message'] = "Total for {} is {}".format(sid, computed_total)
        results['computed_score'] = computed_total
        results['manual_score'] = manual_score
    else:
        # compute total score for the assignment for each sid; also saves in DB unless manual value saved
        scores = [_compute_assignment_total(student, assignment, auth.user.course_name)[0] for student in student_rows]
        results['message'] = "Calculated totals for {} students\n\tmax: {}\n\tmin: {}\n\tmean: {}".format(
            len(scores),
            max(scores),
            min(scores),
            sum(scores)/float(len(scores))
        )

    return json.dumps(results)

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def autograde():
    ### This endpoint is hit to autograde one or all students or questions for an assignment

    assignment_name = request.vars.assignment
    assignment = db((db.assignments.name == assignment_name) & (db.assignments.course == auth.user.course_id)).select().first()
    if assignment:
        assignment_id = assignment.id
    else:
        return json.dumps({'success':False, 'message':"Select an assignment before trying to autograde."})

    sid = request.vars.get('sid', None)
    question_name = request.vars.get('question', None)
    enforce_deadline = request.vars.get('enforceDeadline', None)
    if enforce_deadline == 'true':
        # get the deadline associated with the assignment
        deadline = assignment.duedate
    else:
        deadline = None

    if 'timezoneoffset' in session and deadline:
        deadline = deadline + datetime.timedelta(hours=int(session.timezoneoffset))
        logger.debug("ASSIGNMENT DEADLINE OFFSET %s",deadline)

    student_rows = _get_students(auth.user.course_id, sid)
    sids = [row.username for row in student_rows]

    if question_name:
        questions_query = db(
            (db.assignment_questions.assignment_id == assignment_id) &
            (db.assignment_questions.question_id == db.questions.id) &
            (db.questions.name == question_name)
            ).select()
    else:
        # get all qids and point values for this assignment
        questions_query = db((db.assignment_questions.assignment_id == assignment_id) &
                             (db.assignment_questions.question_id == db.questions.id)
                             ).select()

    readings = [(row.questions.name,
                 row.questions.chapter,
                 row.questions.subchapter,
                 row.assignment_questions.points,
                 row.assignment_questions.activities_required,
                 row.assignment_questions.autograde,
                 row.assignment_questions.which_to_grade,
                 ) for row in questions_query if row.assignment_questions.reading_assignment == True]
    logger.debug("GRADING READINGS")
    # Now for each reading, get all of the questions in that subsection
    # call _autograde_one_q using the autograde and which to grade for that section. likely interact
    #
    base_course = row = db(db.courses.id == auth.user.course_id).select(db.courses.base_course).first().base_course
    count = 0
    for (name, chapter, subchapter, points, ar, ag, wtg) in readings:
        count += 1
        for s in sids:
            score = 0
            rows = db((db.questions.chapter == chapter) &
                      (db.questions.subchapter == subchapter) &
                      (db.questions.base_course == base_course)).select()
            for row in rows:
                score += _autograde_one_q(auth.user.course_name, s, row.name, 1, row.question_type,
                                          deadline=deadline, autograde=ag, which_to_grade=wtg, save_score=False )
                logger.debug("Score is now %s for %s for %s", score, row.name, auth.user.username)
            if score >= ar:
                save_points = points
                logger.debug("full points for %s on %s", auth.user.username, name)
            else:
                save_points = 0
                logger.debug("no points for %s on %s", auth.user.username, name)

            _save_question_grade(s, auth.user.course_name, name, save_points,
                                 deadline=deadline)

    logger.debug("GRADING QUESTIONS")
    questions = [(row.questions.name,
                  row.assignment_questions.points,
                  row.assignment_questions.autograde,
                  row.assignment_questions.which_to_grade,
                  row.questions.question_type) for row in questions_query
                  if row.assignment_questions.reading_assignment == False or
                     row.assignment_questions.reading_assignment == None]

    logger.debug("questions to grade = %s", questions)
    for (qdiv, points, autograde, which_to_grade, question_type) in questions:
        for s in sids:
            if autograde != 'manual':
                _autograde_one_q(auth.user.course_name, s, qdiv, points, question_type,
                                 deadline=deadline, autograde = autograde, which_to_grade = which_to_grade)
                count += 1

    return json.dumps({'message': "autograded {} items".format(count)})




@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def record_grade():
    if 'acid' not in request.vars or 'sid' not in request.vars:
        return json.dumps({'success':False, 'message':"Need problem and user."})

    score_str = request.vars.get('grade', 0)
    if score_str == "":
        score = 0
    else:
        score = float(score_str)
    comment = request.vars.get('comment', None)
    if score_str != "" or ('comment' in request.vars and comment != ""):
        try:
            db.question_grades.update_or_insert((\
                (db.question_grades.sid == request.vars['sid']) \
                & (db.question_grades.div_id == request.vars['acid']) \
                & (db.question_grades.course_name == auth.user.course_name) \
                ),
                sid = request.vars['sid'],
                div_id = request.vars['acid'],
                course_name = auth.user.course_name,
                score = score,
                comment = comment)
        except IntegrityError:
            logger.error("IntegrityError {} {} {}".format(request.vars['sid'], request.vars['acid'], auth.user.course_name))
            return json.dumps({'response': 'not replaced'})
        return json.dumps({'response': 'replaced'})
    else:
        return json.dumps({'response': 'not replaced'})

# create a unique index:  question_grades_sid_course_name_div_id_idx" UNIQUE, btree (sid, course_name, div_id)

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def get_problem():
    if 'acid' not in request.vars or 'sid' not in request.vars:
        return json.dumps({'success':False, 'message':"Need problem and user."})

    user = db(db.auth_user.username == request.vars.sid).select().first()
    if not user:
        return json.dumps({'success':False, 'message':"User does not exist. Sorry!"})

    res = {
        'id':"%s-%d" % (request.vars.acid, user.id),
        'acid':request.vars.acid,
        'sid':user.id,
        'username':user.username,
        'name':"%s %s" % (user.first_name, user.last_name),
        'code': ""
    }

    # get the deadline associated with the assignment
    assignment_name = request.vars.assignment
    if assignment_name and auth.user.course_id:
        assignment = db((db.assignments.name == assignment_name) & (db.assignments.course == auth.user.course_id)).select().first()
        deadline = assignment.duedate
    else:
        deadline = None

    offset = datetime.timedelta(0)
    if session.timezoneoffset and deadline:
        offset = datetime.timedelta(hours=int(session.timezoneoffset))
        logger.debug("setting offset %s %s", offset, deadline+offset)

    query =  (db.code.acid == request.vars.acid) & (db.code.sid == request.vars.sid) & (db.code.course_id == auth.user.course_id)
    if request.vars.enforceDeadline == "true" and deadline:
        query = query & (db.code.timestamp < deadline + offset)
        logger.debug("DEADLINE QUERY = %s", query)
    c = db(query).select(orderby = db.code.id).last()

    if c:
        res['code'] = c.code

    # add prefixes, suffix_code and files that are available
    # retrieve the db record
    source = db.source_code(acid = request.vars.acid, course_id = auth.user.course_name)

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
            #logger.debug(res['includes'])
        if source.suffix_code:
            res['suffix_code'] = source.suffix_code
            #logger.debug(source.suffix_code)

        file_divs = [x.strip() for x in source.available_files.split(',') if x != '']
        res['file_includes'] = [{'acid': acid, 'contents': get_source(acid)} for acid in file_divs]
    return json.dumps(res)


def doAssignment():
    if not auth.user:
        session.flash = "Please Login"
        return redirect(URL('default','index'))

    course = db(db.courses.id == auth.user.course_id).select().first()
    assignment_id = request.vars.assignment_id
    if not assignment_id or assignment_id.isdigit() == False:
        logger.error("BAD ASSIGNMENT = %s assignment %s", course, assignment_id)
        session.flash = "Bad Assignment ID"
        return redirect(URL("assignments","chooseAssignment"))

    logger.debug("COURSE = %s assignment %s", course, assignment_id)
    assignment = db((db.assignments.id == assignment_id) & (db.assignments.course == auth.user.course_id)).select().first()

    if not assignment:
        logger.error("NO ASSIGNMENT assign_id = %s course = %s user = %s",assignment_id, course, auth.user.username)
        session.flash = "Could not find login and try again."
        return redirect(URL('default','index'))

    if assignment.visible == 'F' or assignment.visible == None:
        if verifyInstructorStatus(auth.user.course_name, auth.user) == False:
            session.flash = "That assignment is no longer available"
            return redirect(URL('assignments','chooseAssignment'))


    questions_html = db((db.assignment_questions.assignment_id == assignment.id) & \
                        (db.assignment_questions.question_id == db.questions.id) & \
                        (db.assignment_questions.reading_assignment == None or db.assignment_questions.reading_assignment != 'T')) \
                        .select(db.questions.htmlsrc, db.questions.id, db.questions.chapter, db.questions.subchapter, db.questions.name, orderby=db.assignment_questions.sorting_priority)

    readings = db((db.assignment_questions.assignment_id == assignment.id) &
                  (db.assignment_questions.question_id == db.questions.id) &
                  (db.assignment_questions.reading_assignment == 'T'))\
        .select(db.questions.base_course, db.questions.name,
                db.questions.chapter, db.questions.subchapter,
                orderby=db.assignment_questions.sorting_priority)

    questions_scores = db((db.assignment_questions.assignment_id == assignment.id) &
                    (db.assignment_questions.question_id == db.questions.id) &
                    (db.assignment_questions.reading_assignment == None or db.assignment_questions.reading_assignment != 'T') & \
                    (db.question_grades.sid == auth.user.username) &
                    (db.question_grades.div_id == db.questions.name)) \
        .select(db.questions.id, db.question_grades.score, db.question_grades.comment, db.assignment_questions.points, orderby=db.assignment_questions.sorting_priority)

    questionslist = []
    readingsDict = {}

    # The next for loop formats the readings information into readingsDict
    # The keys of readingsDict are ids in the chapters table
    # Each value is a list of lists detailing the information about each section within the assigned chapter
    # Chapter ids are used as keys so the dictionary can be iterated in the correct order within doAssignment.html

    # Once the questions table starts recording chapters for readings, a dictionary may not be needed anymore,
    # and the labels query won't be needed at all

    for r in readings:
        logger.debug("READING = %s",r.name)
        # todo: eliminate this query
        labels = db((db.chapters.chapter_label == r.chapter) &
                    (db.chapters.course_id == auth.user.course_name) &
                    (db.chapters.id == db.sub_chapters.chapter_id) &
                    (db.sub_chapters.sub_chapter_label == r.subchapter)) \
            .select(db.sub_chapters.chapter_id, db.sub_chapters.sub_chapter_name,
                    db.sub_chapters.sub_chapter_label, db.chapters.chapter_name, db.chapters.chapter_label,
                    db.chapters.id).first()
        logger.debug("LABELS = %s",labels)
        logger.debug("user_id = %s labels[chapters] = %s labels[sub_chapters] = %s",auth.user.id,labels['chapters'].chapter_label,labels['sub_chapters'].sub_chapter_label)
        chapter_name = labels.chapters.chapter_name
        subchapter_name = labels.sub_chapters.sub_chapter_name
        completion = db((db.user_sub_chapter_progress.user_id == auth.user.id) &
            (db.user_sub_chapter_progress.chapter_id == labels['chapters'].chapter_label) &
            (db.user_sub_chapter_progress.sub_chapter_id == labels['sub_chapters'].sub_chapter_label)).select().first()

        # Sometimes when a sub-chapter is added to the book after the user has registerd and the
        # subchapter tables have been created you need to catch that and insert.
        if not completion:
            newid = db.user_sub_chapter_progress.insert(chapter_id=labels['chapters'].chapter_label,
                                                        sub_chapter_id=labels['sub_chapters'].sub_chapter_label,
                                                        status=-1,
                                                        user_id=auth.user.id)
            completion = db(db.user_sub_chapter_progress.id == newid).select().first()

        logger.debug("COMPLETION = %s",completion)
        chapterPath = (completion.chapter_id + '/toctree.html')
        sectionPath = (completion.chapter_id + '/' + completion.sub_chapter_id + '.html')

        if labels['chapters'].id not in readingsDict:
            readingsDict[labels['chapters'].id] = []

        if completion.status == 1:
            readingsDict[labels['chapters'].id].append([chapter_name, chapterPath, subchapter_name, sectionPath, 'completed'])
        elif completion.status == 0:
            readingsDict[labels['chapters'].id].append([chapter_name, chapterPath, subchapter_name, sectionPath, 'started'])
        else:
            readingsDict[labels['chapters'].id].append([chapter_name, chapterPath, subchapter_name, sectionPath, 'notstarted'])

    # This is to get the chapters' completion states based on the completion of sections of the readings in assignments
    # The completion of chapters in reading assignments means that all the assigned sections for that specific chapter have been completed
    # This means chapter completion states within assignments will not always match up with chapter completion states in the ToC,
    # So the DB is not queried and instead the readingsDict is iterated through after it's been built.
    # Each chapter's completion gets appended to the first list within the list of section information for each chapter in the readingsDict
    for chapter in readingsDict:
        hasStarted = False
        completionState = 'completed'
        for s in readingsDict[chapter]:
            if s[4] == 'completed':
                hasStarted = True
            if s[4] == 'started':
                hasStarted = True
                completionState = 'started'
        if hasStarted:
            readingsDict[chapter][0].append(completionState)
        else:
            readingsDict[chapter][0].append('notstarted')

    currentqScore = 0

    # This formats questionslist into a list of lists.
    # Each list within questionslist represents a question and holds the question's html string to be rendered in the view and the question's scoring information
    # If scores have not been released for the question or if there are no scores yet available, the scoring information will be recorded as empty strings
    for q in questions_html:

        # It there is no html recorded, the question can't be rendered
        if q.htmlsrc != None:

            # This replacement is to render images
            q.htmlsrc = bytes(q.htmlsrc).decode('utf8').replace('src="../_static/', 'src="../static/' + course['course_name'] + '/_static/')
            q.htmlsrc = q.htmlsrc.replace("../_images","/{}/static/{}/_images".format(request.application,course.course_name))
            try:
                if q.id == questions_scores[currentqScore]['questions'].id  and assignment['released']:
                    questioninfo = [q.htmlsrc,
                                    questions_scores[currentqScore]['question_grades'].score,
                                    questions_scores[currentqScore]['assignment_questions'].points,
                                    questions_scores[currentqScore]['question_grades'].comment,
                                    q.chapter,
                                    q.subchapter,
                                    q.name]
                    currentqScore += 1
                else:
                    questioninfo  = [q.htmlsrc, '', '','',q.chapter,q.subchapter,q.name]
            except:
                # There are still questions, but no more recorded grades
                questioninfo  = [q.htmlsrc, '', '','',q.chapter,q.subchapter,q.name]

            questionslist.append(questioninfo)

    return dict(course=course, course_name=auth.user.course_name, assignment=assignment, questioninfo=questionslist, course_id=auth.user.course_name, readings=readingsDict)

def chooseAssignment():
    if not auth.user:
        session.flash = "Please Login"
        return redirect(URL('default','index'))

    course = db(db.courses.id == auth.user.course_id).select().first()
    assignments = db((db.assignments.course == course.id) & (db.assignments.visible == 'T')).select(orderby=db.assignments.duedate)
    return(dict(assignments=assignments))
