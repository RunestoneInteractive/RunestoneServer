import datetime
import logging

def _profile(start, msg):
    delta = datetime.datetime.now() - start
    print "{}: {}.{}".format(msg, delta.seconds, delta.microseconds)


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


def _scorable_mchoice_answers(course_name, sid, question_name, points, deadline, practice_start_time=None):
    query = ((db.mchoice_answers.course_name == course_name) & \
            (db.mchoice_answers.sid == sid) & \
            (db.mchoice_answers.div_id == question_name) \
            )
    if deadline:
        query = query & (db.mchoice_answers.timestamp < deadline)
    if practice_start_time:
        query = query & (db.mchoice_answers.timestamp >= practice_start_time)
    return db(query).select(orderby=db.mchoice_answers.timestamp)


def _scorable_useinfos(course_name, sid, div_id, points, deadline, event_filter=None, question_type=None,
                       practice_start_time=None):
    # look in useinfo, to see if visited (before deadline)
    # sid matches auth_user.username, not auth_user.id
    # if question type is page we must do better with the div_id

    query = ((db.useinfo.course_id == course_name) & \
            (db.useinfo.sid == sid))

    if question_type == 'page':
        quest = db(db.questions.name == div_id).select().first()
        div_id = u"{}/{}.html".format(quest.chapter, quest.subchapter)
        query = query & (db.useinfo.div_id.endswith(div_id))
    else:
        query = query & (db.useinfo.div_id == div_id)

    if event_filter:
        query = query & (db.useinfo.event == event_filter)
    if deadline:
        query = query & (db.useinfo.timestamp < deadline)
    if practice_start_time:
        query = query & (db.useinfo.timestamp >= practice_start_time)
    return db(query).select(db.useinfo.id, db.useinfo.act, orderby=db.useinfo.timestamp)


def _scorable_parsons_answers(course_name, sid, question_name, points, deadline, practice_start_time=None):
    query = ((db.parsons_answers.course_name == course_name) & \
            (db.parsons_answers.sid == sid) & \
            (db.parsons_answers.div_id == question_name) \
            )
    if deadline:
        query = query & (db.parsons_answers.timestamp < deadline)
    if practice_start_time:
        query = query & (db.parsons_answers.timestamp >= practice_start_time)
    return db(query).select(orderby=db.parsons_answers.timestamp)


def _scorable_fitb_answers(course_name, sid, question_name, points, deadline, practice_start_time=None):
    query = ((db.fitb_answers.course_name == course_name) & \
            (db.fitb_answers.sid == sid) & \
            (db.fitb_answers.div_id == question_name) \
            )
    if deadline:
        query = query & (db.fitb_answers.timestamp < deadline)
    if practice_start_time:
        query = query & (db.fitb_answers.timestamp >= practice_start_time)
    return db(query).select(orderby=db.fitb_answers.timestamp)


def _scorable_clickablearea_answers(course_name, sid, question_name, points, deadline, practice_start_time=None):
    query = ((db.clickablearea_answers.course_name == course_name) & \
            (db.clickablearea_answers.sid == sid) & \
            (db.clickablearea_answers.div_id == question_name) \
            )
    if deadline:
        query = query & (db.clickablearea_answers.timestamp < deadline)
    if practice_start_time:
        query = query & (db.clickablearea_answers.timestamp >= practice_start_time)
    return db(query).select(orderby=db.clickablearea_answers.timestamp)


def _scorable_dragndrop_answers(course_name, sid, question_name, points, deadline, practice_start_time=None):
    query = ((db.dragndrop_answers.course_name == course_name) & \
            (db.dragndrop_answers.sid == sid) & \
            (db.dragndrop_answers.div_id == question_name) \
            )
    if deadline:
        query = query & (db.dragndrop_answers.timestamp < deadline)
    if practice_start_time:
        query = query & (db.dragndrop_answers.timestamp >= practice_start_time)
    return db(query).select(orderby=db.dragndrop_answers.timestamp)


def _scorable_codelens_answers(course_name, sid, question_name, points, deadline, practice_start_time=None):
    query = ((db.codelens_answers.course_name == course_name) & \
            (db.codelens_answers.sid == sid) & \
            (db.codelens_answers.div_id == question_name) \
            )
    if deadline:
        query = query & (db.codelens_answers.timestamp < deadline)
    if practice_start_time:
        query = query & (db.codelens_answers.timestamp >= practice_start_time)
    return db(query).select(orderby=db.codelens_answers.timestamp)


def _autograde_one_q(course_name, sid, question_name, points, question_type,
                     deadline=None, autograde=None, which_to_grade=None, save_score=True,
                     practice_start_time = None):
    logger.debug("autograding %s %s %s %s %s %s", course_name, question_name, sid, deadline, autograde, which_to_grade)
    if not autograde:
        logger.debug("autograde not set returning 0")
        return 0

    # If previously manually graded and it is required to save the score, don't overwrite.
    existing = db((db.question_grades.sid == sid) \
       & (db.question_grades.course_name == course_name) \
       & (db.question_grades.div_id == question_name) \
       ).select().first()
    if save_score and existing and (existing.comment != "autograded"):
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
        results = _scorable_useinfos(course_name, sid, question_name, points, deadline, event_filter,
                                     practice_start_time=practice_start_time)
        scoring_fn = _score_one_code_run
    elif question_type == 'mchoice':
        results = _scorable_mchoice_answers(course_name, sid, question_name, points, deadline, practice_start_time)
        scoring_fn = _score_one_mchoice
    elif question_type == 'page':
        # question_name does not help us
        results = _scorable_useinfos(course_name, sid, question_name, points, deadline, question_type='page',
                                     practice_start_time=practice_start_time)
        scoring_fn = _score_one_interaction
    elif question_type == 'parsonsprob':
        results = _scorable_parsons_answers(course_name, sid, question_name, points, deadline, practice_start_time)
        scoring_fn = _score_one_parsons
    elif question_type == 'fillintheblank':
        results = _scorable_fitb_answers(course_name, sid, question_name, points, deadline, practice_start_time)
        scoring_fn = _score_one_fitb
    elif question_type == 'clickablearea':
        results = _scorable_clickablearea_answers(course_name, sid, question_name, points, deadline,
                                                  practice_start_time)
        scoring_fn = _score_one_clickablearea
    elif question_type == 'dragndrop':
        results = _scorable_dragndrop_answers(course_name, sid, question_name, points, deadline, practice_start_time)
        scoring_fn = _score_one_dragndrop
    elif question_type == 'codelens':
        if autograde == 'interact':  # this is probably what we want for *most* codelens it will not be correct when it is an actual codelens question in a reading
            results = _scorable_useinfos(course_name, sid, question_name, points, deadline,
                                         practice_start_time=practice_start_time)
            scoring_fn = _score_one_interaction
        else:
            results = _scorable_codelens_answers(course_name, sid, question_name, points, deadline, practice_start_time)
            scoring_fn = _score_one_codelens
    elif question_type in ['video', 'showeval']:
        # question_name does not help us
        results = _scorable_useinfos(course_name, sid, question_name, points, deadline, question_type='video',
                                     practice_start_time=practice_start_time)
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
            # extract its score and id
            id = row.id
            score = scoring_fn(row, points, autograde)
        elif which_to_grade == 'best_answer':
            # score all rows and take the best one
            best_row = max(results, key = lambda row: scoring_fn(row, points, autograde))
            id = best_row.id
            score = scoring_fn(best_row, points, autograde)
            logger.debug("SCORE = %s by %s", score, scoring_fn)
        else:
            logger.error("Unknown Scoring Scheme %s ", which_to_grade)
            id = 0
            score = 0
    else:
        # no results found, score is 0, not attributed to any row
        id = None
        score = 0

    # Save the score
    if save_score:
        _save_question_grade(sid, course_name, question_name, score, id, deadline)

    if practice_start_time:
        return _score_practice_quality(practice_start_time,
                                       course_name,
                                       sid,
                                       points,
                                       score,
                                       len(results) if results else 0)
    return score


def _save_question_grade(sid, course_name, question_name, score, useinfo_id=None, deadline=None):
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
            useinfo_id = useinfo_id,
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

    # print (student.id, assignment.id)

    # compute the score
    query =  (db.question_grades.sid == student.username) \
             & (db.question_grades.div_id == db.questions.name) \
             & (db.questions.id == db.assignment_questions.question_id) \
             & (db.assignment_questions.assignment_id == assignment.id) \
             & (db.question_grades.course_name == course_name )
    scores = db(query).select(db.question_grades.score)
    logger.debug("List of scores to add for %s is %s",student.username, scores)
    score = sum([row.score for row in scores if row.score])
    # get total points for assignment, so can compute percentage to send to gradebook via LTI
    record = db.assignments(assignment.id)
    if record:
        points = record.points
    else:
        points = 0
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

        if grade and grade.lis_result_sourcedid and grade.lis_outcome_url and session.oauth_consumer_key:
            # send it back to the LMS
            # have to send a percentage of the max score, rather than total points
            pct = score / float(points) if points else 0.0
            lti_record = db(db.lti_keys.consumer == session.oauth_consumer_key).select().first()
            if lti_record:
                # print "score", score, points, pct
                request = OutcomeRequest({"consumer_key": session.oauth_consumer_key,
                                          "consumer_secret": lti_record.secret,
                                          "lis_outcome_service_url": grade.lis_outcome_url,
                                          "lis_result_sourcedid": grade.lis_result_sourcedid})
                resp = request.post_replace_result(pct)
                # print resp

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

def do_autograde(assignment, course_id, course_name, sid, question_name, enforce_deadline, timezoneoffset, thedb, settings):
    global logger
    global db
    db = thedb
    logger = logging.getLogger(settings.logger)
    logger.setLevel(settings.log_level)

    start = datetime.datetime.now()
    if enforce_deadline == 'true':
        # get the deadline associated with the assignment
        deadline = assignment.duedate
    else:
        deadline = None

    if timezoneoffset and deadline:
        deadline = deadline + datetime.timedelta(hours=int(timezoneoffset))
        logger.debug("ASSIGNMENT DEADLINE OFFSET %s",deadline)

    student_rows = _get_students(course_id, sid)
    sids = [row.username for row in student_rows]

    if question_name:
        questions_query = db(
            (db.assignment_questions.assignment_id == assignment.id) &
            (db.assignment_questions.question_id == db.questions.id) &
            (db.questions.name == question_name)
            ).select()
    else:
        # get all qids and point values for this assignment
        questions_query = db((db.assignment_questions.assignment_id == assignment.id) &
                             (db.assignment_questions.question_id == db.questions.id)
                             ).select()
    _profile(start, "after questions fetched")

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
    base_course = db(db.courses.id == course_id).select(db.courses.base_course).first().base_course
    count = 0
    _profile(start, "after readings fetched")
    for (name, chapter, subchapter, points, ar, ag, wtg) in readings:
        count += 1
        for s in sids:
            score = 0
            rows = db((db.questions.chapter == chapter) &
                      (db.questions.subchapter == subchapter) &
                      (db.questions.base_course == base_course)).select()
            # _profile(start, "\t{}. rows fetched for {}/{}".format(count, chapter, subchapter))
            for row in rows:
                score += _autograde_one_q(course_name, s, row.name, 1, row.question_type,
                                          deadline=deadline, autograde=ag, which_to_grade=wtg, save_score=False )
                logger.debug("Score is now %s for %s for %s", score, row.name, sid)
            if score >= ar:
                save_points = points
                logger.debug("full points for %s on %s", sid, name)
            else:
                save_points = 0
                logger.debug("no points for %s on %s", sid, name)
            # _profile(start, "\t\tgraded")
            _save_question_grade(s, course_name, name, save_points, useinfo_id=None, deadline=deadline)
            #_profile(start, "\t\tsaved")

    _profile(start, "after readings graded")

    logger.debug("GRADING QUESTIONS")
    questions = [(row.questions.name,
                  row.assignment_questions.points,
                  row.assignment_questions.autograde,
                  row.assignment_questions.which_to_grade,
                  row.questions.question_type) for row in questions_query
                  if row.assignment_questions.reading_assignment == False or
                     row.assignment_questions.reading_assignment == None]

    _profile(start, "after questions fetched")
    logger.debug("questions to grade = %s", questions)
    for (qdiv, points, autograde, which_to_grade, question_type) in questions:
        for s in sids:
            if autograde != 'manual':
                _autograde_one_q(course_name, s, qdiv, points, question_type,
                                 deadline=deadline, autograde = autograde, which_to_grade = which_to_grade)
                count += 1

    _profile(start, "after calls to _autograde_one_q")
    return count

