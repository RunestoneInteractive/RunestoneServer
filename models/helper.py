from os import path
import os
import shutil
import sys
import json
import logging
import datetime
from psycopg2 import IntegrityError

logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)


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
        results = _scorable_useinfos(course_name, sid, question_name, points, deadline, event_filter, None,
                                     practice_start_time)
        scoring_fn = _score_one_code_run
    elif question_type == 'mchoice':
        results = _scorable_mchoice_answers(course_name, sid, question_name, points, deadline, practice_start_time)
        scoring_fn = _score_one_mchoice
    elif question_type == 'page':
        # question_name does not help us
        results = _scorable_useinfos(course_name, sid, question_name, points, deadline, None, 'page',
                                     practice_start_time)
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
            results = _scorable_useinfos(course_name, sid, question_name, points, deadline, None, None, practice_start_time)
            scoring_fn = _score_one_interaction
        else:
            results = _scorable_codelens_answers(course_name, sid, question_name, points, deadline, practice_start_time)
            scoring_fn = _score_one_codelens
    elif question_type in ['video', 'showeval']:
        # question_name does not help us
        results = _scorable_useinfos(course_name, sid, question_name, points, deadline, None, 'video',
                                     practice_start_time)
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
        _save_question_grade(sid, course_name, question_name, score, id)

    if practice_start_time:
        page_visits = db((db.useinfo.course_id == course_name) & \
                         (db.useinfo.sid == sid) & \
                         (db.useinfo.event == 'page') & \
                         (db.useinfo.timestamp >= practice_start_time)) \
            .select()
        practice_duration = (datetime.datetime.now() - practice_start_time).seconds / 60
        practice_score = 0
        print ("len(page_visits): ", len(page_visits))
        print ("practice_duration: ", practice_duration)
        print ("len(results): ", len(results))
        print ("score: ", score)
        print ("points: ", points)
        if score == points:
            if len(page_visits) <= 1 and len(results) <= 1 and practice_duration <= 2:
                practice_score = 5
            elif len(results) <= 2 and practice_duration <= 2:
                practice_score = 4
            elif len(results) <= 3 and practice_duration <= 3:
                practice_score = 3
            elif len(results) <= 4 and practice_duration <= 4:
                practice_score = 2
            elif len(results) <= 5 and practice_duration <= 5:
                practice_score = 1
        print ("practice_score = ", practice_score)
        return practice_score
    return score


def _scorable_useinfos(course_name, sid, div_id, points, deadline, event_filter=None, question_type=None,
                       practice_start_time=None):
    # look in useinfo, to see if visited (before deadline)
    # sid matches auth_user.username, not auth_user.id
    # if question type is page we must do better with the div_id

    query = ((db.useinfo.course_id == course_name) & \
            (db.useinfo.sid == sid))

    if question_type == 'page':
        quest = db(db.questions.name == div_id).select().first()
        div_id = u"{}/{}".format(quest.chapter, quest.subchapter)
        query = query & (db.useinfo.div_id.contains(div_id))
    else:
        query = query & (db.useinfo.div_id == div_id)

    if event_filter:
        query = query & (db.useinfo.event == event_filter)
    if deadline:
        query = query & (db.useinfo.timestamp < deadline)
    if practice_start_time:
        query = query & (db.useinfo.timestamp >= practice_start_time)
    return db(query).select(orderby=db.useinfo.timestamp)


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


def _score_one_parsons(row, points, autograde):
    # row is from parsons_answers
    # Much like mchoice, parsons_answers currently stores a binary correct value
    # So much like in _score_one_mchoice, the next lines can be altered if a pct_correct value is added to parsons_answers
    if row.correct:
        pct_correct = 100
    else:
        pct_correct = 0
    return _score_from_pct_correct(pct_correct, points, autograde)


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


def _score_one_fitb(row, points, autograde):
    # row is from fitb_answers
    if row.correct:
        pct_correct = 100
    else:
        pct_correct = 0
    return _score_from_pct_correct(pct_correct, points, autograde)


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


def _score_one_clickablearea(row, points, autograde):
    # row is from clickablearea_answers
    if row.correct:
        pct_correct = 100
    else:
        pct_correct = 0
    return _score_from_pct_correct(pct_correct, points, autograde)


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


def _score_one_dragndrop(row, points, autograde):
    # row is from dragndrop_answers
    if row.correct:
        pct_correct = 100
    else:
        pct_correct = 0
    return _score_from_pct_correct(pct_correct, points, autograde)


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


def _score_one_codelens(row, points, autograde):
    # row is from codelens_answers
    if row.correct:
        pct_correct = 100
    else:
        pct_correct = 0
    return _score_from_pct_correct(pct_correct, points, autograde)


def _save_question_grade(sid, course_name, question_name, score, id):
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
            useinfo_id = id
        )
    except IntegrityError:
        logger.error("IntegrityError {} {} {}".format(sid, course_name, question_name))


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


