# *************************
# |docname| - Runestone API
# *************************
# This module implements the API that the Runestone Components use to communicate with a Runestone Server.
#
# Imports
# =======
# These are listed in the order prescribed by `PEP 8
# <http://www.python.org/dev/peps/pep-0008/#imports>`_.
from collections import Counter
import datetime
from io import open
import json
import logging
from lxml import html
import math
import os
import random
import re
import subprocess
from textwrap import dedent
import uuid

# Third-party imports
# -------------------
from bleach import clean
from dateutil.parser import parse

# Local application imports
# -------------------------
from feedback import is_server_feedback, fitb_feedback, lp_feedback
from rs_practice import _get_qualified_questions

logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)


EVENT_TABLE = {
    "mChoice": "mchoice_answers",
    "fillb": "fitb_answers",
    "dragNdrop": "dragndrop_answers",
    "clickableArea": "clickablearea_answers",
    "parsons": "parsons_answers",
    "codelensq": "codelens_answers",
    "shortanswer": "shortanswer_answers",
    "fillintheblank": "fitb_answers",
    "mchoice": "mchoice_answers",
    "dragndrop": "dragndrop_answers",
    "clickablearea": "clickablearea_answers",
    "parsonsprob": "parsons_answers",
}

COMMENT_MAP = {
    "sql": "--",
    "python": "#",
    "java": "//",
    "javascript": "//",
    "c": "//",
    "cpp": "//",
}


def compareAndUpdateCookieData(sid: str):
    if (
        "ipuser" in request.cookies
        and request.cookies["ipuser"].value != sid
        and request.cookies["ipuser"].value.endswith("@" + request.client)
    ):
        db.useinfo.update_or_insert(
            db.useinfo.sid == request.cookies["ipuser"].value, sid=sid
        )


# Endpoints
# =========
#
# .. _hsblog endpoint:
#
# hsblog endpoint
# ---------------
# Given a JSON record of a clickstream event record the event in the ``useinfo`` table.
# If the event is an answer to a runestone question record that answer in the database in
# one of the xxx_answers tables.
#
def hsblog():
    setCookie = False
    if auth.user:
        if request.vars.course != auth.user.course_name:
            return json.dumps(
                dict(
                    log=False,
                    message="You appear to have changed courses in another tab.  Please switch to this course",
                )
            )
        sid = auth.user.username
        compareAndUpdateCookieData(sid)
        setCookie = True  # we set our own cookie anyway to eliminate many of the extraneous anonymous
        # log entries that come from auth timing out even but the user hasn't reloaded
        # the page.
    else:
        if request.vars.clientLoginStatus == "true":
            logger.error("Session Expired")
            return json.dumps(dict(log=False, message="Session Expired"))

        if "ipuser" in request.cookies:
            sid = request.cookies["ipuser"].value
            setCookie = True
        else:
            sid = str(uuid.uuid1().int) + "@" + request.client
            setCookie = True
    act = request.vars.get("act", "")
    div_id = request.vars.div_id
    event = request.vars.event
    course = request.vars.course
    # Get the current time, rounded to the nearest second -- this is how time time will be stored in the database.
    ts = datetime.datetime.utcnow()
    ts -= datetime.timedelta(microseconds=ts.microsecond)
    tt = request.vars.time
    if not tt:
        tt = 0

    try:
        db.useinfo.insert(
            sid=sid,
            act=act[0:512],
            div_id=div_id,
            event=event,
            timestamp=ts,
            course_id=course,
        )
    except Exception as e:
        logger.error(
            "failed to insert log record for {} in {} : {} {} {}".format(
                sid, course, div_id, event, act
            )
        )
        logger.error("Details: {}".format(e))

    if event == "timedExam" and (act == "finish" or act == "reset" or act == "start"):
        logger.debug(act)
        if act == "reset":
            r = "T"
        else:
            r = None

        try:
            db.timed_exam.insert(
                sid=sid,
                course_name=course,
                correct=int(request.vars.correct or 0),
                incorrect=int(request.vars.incorrect or 0),
                skipped=int(request.vars.skipped or 0),
                time_taken=int(tt),
                timestamp=ts,
                div_id=div_id,
                reset=r,
            )
        except Exception as e:
            logger.debug(
                "failed to insert a timed exam record for {} in {} : {}".format(
                    sid, course, div_id
                )
            )
            logger.debug(
                "correct {} incorrect {} skipped {} time {}".format(
                    request.vars.correct,
                    request.vars.incorrect,
                    request.vars.skipped,
                    request.vars.time,
                )
            )
            logger.debug("Error: {}".format(e.message))

    # Produce a default result.
    res = dict(log=True, timestamp=str(ts))
    try:
        pct = float(request.vars.percent)
    except ValueError:
        pct = None
    except TypeError:
        pct = None

    # Process this event.
    if event == "mChoice" and auth.user:
        answer = request.vars.answer
        correct = request.vars.correct
        db.mchoice_answers.insert(
            sid=sid,
            timestamp=ts,
            div_id=div_id,
            answer=answer,
            correct=correct,
            course_name=course,
            percent=pct,
        )
    elif event == "fillb" and auth.user:
        answer_json = request.vars.answer
        correct = request.vars.correct
        # Grade on the server if needed.
        do_server_feedback, feedback = is_server_feedback(div_id, course)
        if do_server_feedback:
            correct, res_update = fitb_feedback(answer_json, feedback)
            res.update(res_update)
            pct = res["percent"]

        # Save this data.
        db.fitb_answers.insert(
            sid=sid,
            timestamp=ts,
            div_id=div_id,
            answer=answer_json,
            correct=correct,
            course_name=course,
            percent=pct,
        )

    elif event == "dragNdrop" and auth.user:
        answers = request.vars.answer
        minHeight = request.vars.minHeight
        correct = request.vars.correct

        db.dragndrop_answers.insert(
            sid=sid,
            timestamp=ts,
            div_id=div_id,
            answer=answers,
            correct=correct,
            course_name=course,
            min_height=minHeight,
            percent=pct,
        )
    elif event == "clickableArea" and auth.user:
        correct = request.vars.correct
        db.clickablearea_answers.insert(
            sid=sid,
            timestamp=ts,
            div_id=div_id,
            answer=act,
            correct=correct,
            course_name=course,
            percent=pct,
        )

    elif event == "parsons" and auth.user:
        correct = request.vars.correct
        answer = request.vars.answer
        source = request.vars.source
        db.parsons_answers.insert(
            sid=sid,
            timestamp=ts,
            div_id=div_id,
            answer=answer,
            source=source,
            correct=correct,
            course_name=course,
            percent=pct,
        )

    elif event == "codelensq" and auth.user:
        correct = request.vars.correct
        answer = request.vars.answer
        source = request.vars.source
        db.codelens_answers.insert(
            sid=sid,
            timestamp=ts,
            div_id=div_id,
            answer=answer,
            source=source,
            correct=correct,
            course_name=course,
            percent=pct,
        )

    elif event == "shortanswer" and auth.user:
        db.shortanswer_answers.insert(
            sid=sid,
            answer=act,
            div_id=div_id,
            timestamp=ts,
            course_name=course,
        )

    elif event == "unittest" and auth.user:
        statslist = act.split(":")
        if "undefined" not in act:
            pct = float(statslist[1])
            passed = int(statslist[3])
            failed = int(statslist[5])
            if math.isnan(pct):
                pct = 0
        else:
            pct = passed = failed = 0
            logger.error(f"Got undefined unittest results for {div_id} {sid}")
        if pct >= 99.99999:
            correct = "T"
        else:
            correct = "F"
        db.unittest_answers.insert(
            sid=sid,
            timestamp=ts,
            div_id=div_id,
            correct=correct,
            passed=passed,
            failed=failed,
            course_name=course,
            percent=pct,
        )

    elif event == "lp_build" and auth.user:
        ret, new_fields = db.lp_answers._validate_fields(
            dict(sid=sid, timestamp=ts, div_id=div_id, course_name=course)
        )
        if not ret.errors:
            do_server_feedback, feedback = is_server_feedback(div_id, course)
            if do_server_feedback:
                try:
                    code_snippets = json.loads(request.vars.answer)["code_snippets"]
                except Exception:
                    code_snippets = []
                result = lp_feedback(code_snippets, feedback)
                # If an error occurred or we're not testing, pass the answer through.
                res.update(result)

                # Record the results in the database.
                correct = result.get("correct")
                answer = result.get("answer", {})
                answer["code_snippets"] = code_snippets
                ret = db.lp_answers.validate_and_insert(
                    sid=sid,
                    timestamp=ts,
                    div_id=div_id,
                    answer=json.dumps(answer),
                    correct=correct,
                    course_name=course,
                )
                if ret.errors:
                    res.setdefault("errors", []).append(ret.errors.as_dict())
            else:
                res["errors"] = ["No feedback provided."]
        else:
            res.setdefault("errors", []).append(ret.errors.as_dict())

    response.headers["content-type"] = "application/json"
    if setCookie:
        response.cookies["ipuser"] = sid
        response.cookies["ipuser"]["expires"] = 24 * 3600 * 90
        response.cookies["ipuser"]["path"] = "/"
        if auth.user:
            response.cookies["last_course"] = auth.user.course_name
            response.cookies["last_course"]["expires"] = 24 * 3600 * 90
            response.cookies["last_course"]["path"] = "/"

    return json.dumps(res)


# .. _runlog endpoint:
#
# runlog endpoint
# ---------------
# The `logRunEvent` client-side function calls this endpoint to record TODO...
def runlog():  # Log errors and runs with code
    # response.headers['content-type'] = 'application/json'
    setCookie = False
    if auth.user:
        if request.vars.course != auth.user.course_name:
            return json.dumps(
                dict(
                    log=False,
                    message="You appear to have changed courses in another tab.  Please switch to this course",
                )
            )
        sid = auth.user.username
        setCookie = True
    else:
        if request.vars.clientLoginStatus == "true":
            logger.error("Session Expired")
            return json.dumps(dict(log=False, message="Session Expired"))
        if "ipuser" in request.cookies:
            sid = request.cookies["ipuser"].value
            setCookie = True
        else:
            sid = str(uuid.uuid1().int) + "@" + request.client
            setCookie = True
    div_id = request.vars.div_id
    course = request.vars.course
    code = request.vars.code if request.vars.code else ""
    ts = datetime.datetime.utcnow()
    error_info = request.vars.errinfo
    pre = request.vars.prefix if request.vars.prefix else ""
    post = request.vars.suffix if request.vars.suffix else ""
    if error_info != "success":
        event = "ac_error"
        act = str(error_info)[:512]
    else:
        act = "run"
        if request.vars.event:
            event = request.vars.event
        else:
            event = "activecode"
    num_tries = 3
    done = False
    while num_tries > 0 and not done:
        try:
            db.useinfo.insert(
                sid=sid,
                act=act,
                div_id=div_id,
                event=event,
                timestamp=ts,
                course_id=course,
            )
            done = True
        except Exception as e:
            logger.error(
                "probable Too Long problem trying to insert sid={} act={} div_id={} event={} timestamp={} course_id={} exception={}".format(
                    sid, act, div_id, event, ts, course, e
                )
            )
            num_tries -= 1
    if num_tries == 0:
        raise Exception("Runlog Failed to insert into useinfo")

    if auth.user:
        if "to_save" in request.vars and (
            request.vars.to_save == "True" or request.vars.to_save == "true"
        ):
            num_tries = 3
            done = False
            dbcourse = (
                db(db.courses.course_name == course).select(**SELECT_CACHE).first()
            )
            while num_tries > 0 and not done:
                try:
                    db.code.insert(
                        sid=sid,
                        acid=div_id,
                        code=code,
                        emessage=error_info,
                        timestamp=ts,
                        course_id=dbcourse,
                        language=request.vars.lang,
                    )
                    if request.vars.partner:
                        if _same_class(sid, request.vars.partner):
                            comchar = COMMENT_MAP.get(request.vars.lang, "#")
                            newcode = (
                                "{} This code was shared by {}\n\n".format(comchar, sid)
                                + code
                            )
                            db.code.insert(
                                sid=request.vars.partner,
                                acid=div_id,
                                code=newcode,
                                emessage=error_info,
                                timestamp=ts,
                                course_id=dbcourse,
                                language=request.vars.lang,
                            )
                        else:
                            res = {
                                "message": "You must be enrolled in the same class as your partner"
                            }
                            return json.dumps(res)
                    done = True
                except Exception as e:
                    num_tries -= 1
                    logger.error("INSERT into code FAILED retrying -- {}".format(e))
            if num_tries == 0:
                raise Exception("Runlog Failed to insert into code")

    res = {"log": True}
    if setCookie:
        response.cookies["ipuser"] = sid
        response.cookies["ipuser"]["expires"] = 24 * 3600 * 90
        response.cookies["ipuser"]["path"] = "/"
    return json.dumps(res)


# Ajax Handlers for saving and restoring active code blocks


def gethist():

    """
    return the history of saved code by this user for a particular acid
    :Parameters:
        - `acid`: id of the active code block
        - `user`: optional identifier for the owner of the code
    :Return:
        - json object containing a list/array of source texts
    """
    codetbl = db.code
    acid = request.vars.acid

    # if vars.sid then we know this is being called from the grading interface
    if request.vars.sid:
        sid = request.vars.sid
        if auth.user and verifyInstructorStatus(
            auth.user.course_name, auth.user.id
        ):  # noqa: F405
            course_id = auth.user.course_id
        else:
            course_id = None
    elif auth.user:
        sid = auth.user.username
        course_id = auth.user.course_id
    else:
        sid = None
        course_id = None

    res = {}
    if sid:
        query = (
            (codetbl.sid == sid)
            & (codetbl.acid == acid)
            & (codetbl.course_id == course_id)
            & (codetbl.timestamp != None)  # noqa: E711
        )
        res["acid"] = acid
        res["sid"] = sid
        # get the code they saved in chronological order; id order gets that for us
        r = db(query).select(orderby=codetbl.id)
        res["history"] = [row.code for row in r]
        res["timestamps"] = [
            row.timestamp.replace(tzinfo=datetime.timezone.utc).isoformat() for row in r
        ]

    response.headers["content-type"] = "application/json"
    return json.dumps(res)


# @auth.requires_login()
# This function is deprecated as of June 2019
# We need to keep it in place as long as we continue to serve books
# from runestone/static/  When that period is over we can eliminate
def getuser():
    response.headers["content-type"] = "application/json"

    if auth.user:
        try:
            # return the list of courses that auth.user is registered for to keep them from
            # accidentally wandering into courses they are not registered for.
            cres = db(
                (db.user_courses.user_id == auth.user.id)
                & (db.user_courses.course_id == db.courses.id)
            ).select(db.courses.course_name)
            clist = []
            for row in cres:
                clist.append(row.course_name)
            res = {
                "email": auth.user.email,
                "nick": auth.user.username,
                "donated": auth.user.donated,
                "isInstructor": verifyInstructorStatus(  # noqa: F405
                    auth.user.course_name, auth.user.id
                ),
                "course_list": clist,
            }
            session.timezoneoffset = request.vars.timezoneoffset
            logger.debug(
                "setting timezone offset in session %s hours" % session.timezoneoffset
            )
        except Exception:
            res = dict(redirect=auth.settings.login_url)  # ?_next=....
    else:
        res = dict(redirect=auth.settings.login_url)  # ?_next=....
    if session.readings:
        res["readings"] = session.readings
    logger.debug("returning login info: %s" % res)
    return json.dumps([res])


def set_tz_offset():
    session.timezoneoffset = request.vars.timezoneoffset
    logger.debug("setting timezone offset in session %s hours" % session.timezoneoffset)
    return "done"


#
#  Ajax Handlers to update and retrieve the last position of the user in the course
#
def updatelastpage():
    lastPageUrl = request.vars.lastPageUrl
    lastPageScrollLocation = request.vars.lastPageScrollLocation
    if lastPageUrl is None:
        return  # todo:  log request.vars, request.args and request.env.path_info
    course = request.vars.course
    completionFlag = request.vars.completionFlag
    lastPageChapter = lastPageUrl.split("/")[-2]
    lastPageSubchapter = ".".join(lastPageUrl.split("/")[-1].split(".")[:-1])
    if auth.user:
        done = False
        num_tries = 3
        while not done and num_tries > 0:
            try:
                db(
                    (db.user_state.user_id == auth.user.id)
                    & (db.user_state.course_id == course)
                ).update(
                    last_page_url=lastPageUrl,
                    last_page_chapter=lastPageChapter,
                    last_page_subchapter=lastPageSubchapter,
                    last_page_scroll_location=lastPageScrollLocation,
                    last_page_accessed_on=datetime.datetime.utcnow(),
                )
                done = True
            except Exception:
                num_tries -= 1
        if num_tries == 0:
            raise Exception("Failed to save the user state in update_last_page")

        done = False
        num_tries = 3
        while not done and num_tries > 0:
            try:
                db(
                    (db.user_sub_chapter_progress.user_id == auth.user.id)
                    & (db.user_sub_chapter_progress.chapter_id == lastPageChapter)
                    & (
                        db.user_sub_chapter_progress.sub_chapter_id
                        == lastPageSubchapter
                    )
                    & (
                        (db.user_sub_chapter_progress.course_name == course)
                        | (
                            db.user_sub_chapter_progress.course_name == None
                        )  # Back fill for old entries without course
                    )
                ).update(
                    status=completionFlag,
                    end_date=datetime.datetime.utcnow(),
                    course_name=course,
                )
                done = True
            except Exception:
                num_tries -= 1
        if num_tries == 0:
            raise Exception("Failed to save sub chapter progress in update_last_page")

        practice_settings = db(db.course_practice.course_name == auth.user.course_name)
        if (
            practice_settings.count() != 0
            and practice_settings.select().first().flashcard_creation_method == 0
        ):
            # Since each authenticated user has only one active course, we retrieve the course this way.
            course = (
                db(db.courses.id == auth.user.course_id).select(**SELECT_CACHE).first()
            )

            # We only retrieve questions to be used in flashcards if they are marked for practice purpose.
            questions = _get_qualified_questions(
                course.base_course, lastPageChapter, lastPageSubchapter, db
            )
            if len(questions) > 0:
                now = datetime.datetime.utcnow()
                now_local = now - datetime.timedelta(
                    hours=float(session.timezoneoffset)
                    if "timezoneoffset" in session
                    else 0
                )
                existing_flashcards = db(
                    (db.user_topic_practice.user_id == auth.user.id)
                    & (db.user_topic_practice.course_name == auth.user.course_name)
                    & (db.user_topic_practice.chapter_label == lastPageChapter)
                    & (db.user_topic_practice.sub_chapter_label == lastPageSubchapter)
                    & (db.user_topic_practice.question_name == questions[0].name)
                )
                # There is at least one qualified question in this subchapter, so insert a flashcard for the subchapter.
                if completionFlag == "1" and existing_flashcards.isempty():
                    db.user_topic_practice.insert(
                        user_id=auth.user.id,
                        course_name=auth.user.course_name,
                        chapter_label=lastPageChapter,
                        sub_chapter_label=lastPageSubchapter,
                        question_name=questions[0].name,
                        # Treat it as if the first eligible question is the last one asked.
                        i_interval=0,
                        e_factor=2.5,
                        next_eligible_date=now_local.date(),
                        # add as if yesterday, so can practice right away
                        last_presented=now - datetime.timedelta(1),
                        last_completed=now - datetime.timedelta(1),
                        creation_time=now,
                        timezoneoffset=float(session.timezoneoffset)
                        if "timezoneoffset" in session
                        else 0,
                    )
                if completionFlag == "0" and not existing_flashcards.isempty():
                    existing_flashcards.delete()


def getCompletionStatus():
    if auth.user:
        lastPageUrl = request.vars.lastPageUrl
        lastPageChapter = lastPageUrl.split("/")[-2]
        lastPageSubchapter = ".".join(lastPageUrl.split("/")[-1].split(".")[:-1])
        result = db(
            (db.user_sub_chapter_progress.user_id == auth.user.id)
            & (db.user_sub_chapter_progress.chapter_id == lastPageChapter)
            & (db.user_sub_chapter_progress.sub_chapter_id == lastPageSubchapter)
            & (
                (db.user_sub_chapter_progress.course_name == auth.user.course_name)
                | (
                    db.user_sub_chapter_progress.course_name == None
                )  # for backward compatibility
            )
        ).select(db.user_sub_chapter_progress.status)
        rowarray_list = []
        if result:
            for row in result:
                res = {"completionStatus": row.status}
                rowarray_list.append(res)
                # question: since the javascript in user-highlights.js is going to look only at the first row, shouldn't
                # we be returning just the *last* status? Or is there no history of status kept anyway?
            return json.dumps(rowarray_list)
        else:
            # haven't seen this Chapter/Subchapter before
            # make the insertions into the DB as necessary

            # we know the subchapter doesn't exist
            db.user_sub_chapter_progress.insert(
                user_id=auth.user.id,
                chapter_id=lastPageChapter,
                sub_chapter_id=lastPageSubchapter,
                status=-1,
                start_date=datetime.datetime.utcnow(),
                course_name=auth.user.course_name,
            )
            # the chapter might exist without the subchapter
            result = db(
                (db.user_chapter_progress.user_id == auth.user.id)
                & (db.user_chapter_progress.chapter_id == lastPageChapter)
            ).select()
            if not result:
                db.user_chapter_progress.insert(
                    user_id=auth.user.id, chapter_id=lastPageChapter, status=-1
                )
            return json.dumps([{"completionStatus": -1}])


def getAllCompletionStatus():
    if auth.user:
        result = db(
            (db.user_sub_chapter_progress.user_id == auth.user.id)
            & (db.user_sub_chapter_progress.course_name == auth.user.course_name)
        ).select(
            db.user_sub_chapter_progress.chapter_id,
            db.user_sub_chapter_progress.sub_chapter_id,
            db.user_sub_chapter_progress.status,
            db.user_sub_chapter_progress.status,
            db.user_sub_chapter_progress.end_date,
        )
        rowarray_list = []
        if result:
            for row in result:
                if row.end_date is None:
                    endDate = 0
                else:
                    endDate = row.end_date.strftime("%d %b, %Y")
                res = {
                    "chapterName": row.chapter_id,
                    "subChapterName": row.sub_chapter_id,
                    "completionStatus": row.status,
                    "endDate": endDate,
                }
                rowarray_list.append(res)
            return json.dumps(rowarray_list)


@auth.requires_login()
def getlastpage():
    course = request.vars.course
    course = db(db.courses.course_name == course).select(**SELECT_CACHE).first()

    result = db(
        (db.user_state.user_id == auth.user.id)
        & (db.user_state.course_id == course.course_name)
        & (db.chapters.course_id == course.base_course)
        & (db.user_state.last_page_chapter == db.chapters.chapter_label)
        & (db.sub_chapters.chapter_id == db.chapters.id)
        & (db.user_state.last_page_subchapter == db.sub_chapters.sub_chapter_label)
    ).select(
        db.user_state.last_page_url,
        db.user_state.last_page_hash,
        db.chapters.chapter_name,
        db.user_state.last_page_scroll_location,
        db.sub_chapters.sub_chapter_name,
    )
    rowarray_list = []
    if result:
        for row in result:
            res = {
                "lastPageUrl": row.user_state.last_page_url,
                "lastPageHash": row.user_state.last_page_hash,
                "lastPageChapter": row.chapters.chapter_name,
                "lastPageSubchapter": row.sub_chapters.sub_chapter_name,
                "lastPageScrollLocation": row.user_state.last_page_scroll_location,
            }
            rowarray_list.append(res)
        return json.dumps(rowarray_list)
    else:
        db.user_state.insert(user_id=auth.user.id, course_id=course.course_name)


def _getCorrectStats(miscdata, event):
    # TODO: update this to use the xxx_answer table
    # select and count grouping by the correct column
    # this version can suffer from division by zero error
    sid = None
    dbtable = EVENT_TABLE[event]  # translate event to correct table

    if auth.user:
        sid = auth.user.username
    else:
        if "ipuser" in request.cookies:
            sid = request.cookies["ipuser"].value

    if sid:
        course = (
            db(db.courses.course_name == miscdata["course"])
            .select(**SELECT_CACHE)
            .first()
        )
        tbl = db[dbtable]

        count_expr = tbl.correct.count()
        rows = db((tbl.sid == sid) & (tbl.timestamp > course.term_start_date)).select(
            tbl.correct, count_expr, groupby=tbl.correct
        )
        total = 0
        correct = 0
        for row in rows:
            count = row[count_expr]
            total += count
            if row[dbtable].correct:
                correct = count
        if total > 0:
            pctcorr = round(float(correct) / total * 100)
        else:
            pctcorr = "unavailable"
    else:
        pctcorr = "unavailable"

    miscdata["yourpct"] = pctcorr


def _getStudentResults(question: str):
    """
    Internal function to collect student answers
    """
    cc = db(db.courses.id == auth.user.course_id).select().first()
    qst = (
        db(
            (db.questions.name == question)
            & (db.questions.base_course == cc.base_course)
        )
        .select()
        .first()
    )
    tbl_name = EVENT_TABLE[qst.question_type]
    tbl = db[tbl_name]

    res = db(
        (tbl.div_id == question)
        & (tbl.course_name == cc.course_name)
        & (tbl.timestamp >= cc.term_start_date)
    ).select(tbl.sid, tbl.answer, orderby=tbl.sid)

    resultList = []
    if len(res) > 0:
        currentSid = res[0].sid
        currentAnswers = []

        for row in res:
            if row.answer:
                answer = clean(row.answer)
            else:
                answer = None

            if row.sid == currentSid:
                if answer is not None:
                    currentAnswers.append(answer)
            else:
                currentAnswers.sort()
                resultList.append((currentSid, currentAnswers))
                currentAnswers = [answer] if answer is not None else []
                currentSid = row.sid

        currentAnswers.sort()
        resultList.append((currentSid, currentAnswers))

    return resultList


def getaggregateresults():
    course = request.vars.course
    question = request.vars.div_id
    # select act, count(*) from useinfo where div_id = 'question4_2_1' group by act;
    response.headers["content-type"] = "application/json"

    if not auth.user:
        return json.dumps([dict(answerDict={}, misc={}, emess="You must be logged in")])

    is_instructor = verifyInstructorStatus(course, auth.user.id)  # noqa: F405
    # Yes, these two things could be done as a join.  but this **may** be better for performance
    if course in (
        "thinkcspy",
        "pythonds",
        "fopp",
        "csawesome",
        "apcsareview",
        "StudentCSP",
    ):
        start_date = datetime.datetime.utcnow() - datetime.timedelta(days=90)
    else:
        start_date = (
            db(db.courses.course_name == course)
            .select(db.courses.term_start_date)
            .first()
            .term_start_date
        )
    count = db.useinfo.id.count()
    try:
        result = db(
            (db.useinfo.div_id == question)
            & (db.useinfo.course_id == course)
            & (db.useinfo.timestamp >= start_date)
        ).select(db.useinfo.act, count, groupby=db.useinfo.act)
    except Exception:
        return json.dumps(
            [dict(answerDict={}, misc={}, emess="Sorry, the request timed out")]
        )

    tdata = {}
    tot = 0
    for row in result:
        tdata[clean(row.useinfo.act)] = row[count]
        tot += row[count]

    tot = float(tot)
    rdata = {}
    miscdata = {}
    correct = ""
    if tot > 0:
        for key in tdata:
            all_a = key.split(":")
            try:
                answer = all_a[1]
                if "correct" in key:
                    correct = answer
                count = int(tdata[key])
                if answer in rdata:
                    count += rdata[answer] / 100.0 * tot
                pct = round(count / tot * 100.0)

                if answer != "undefined" and answer != "":
                    rdata[answer] = pct
            except Exception as e:
                logger.error("Bad data for %s data is %s -- %s" % (question, key, e))

    miscdata["correct"] = correct
    miscdata["course"] = course

    _getCorrectStats(miscdata, "mChoice")

    returnDict = dict(answerDict=rdata, misc=miscdata)

    if auth.user and is_instructor:
        resultList = _getStudentResults(question)
        returnDict["reslist"] = resultList

    return json.dumps([returnDict])


def getpollresults():
    course = request.vars.course
    div_id = request.vars.div_id

    response.headers["content-type"] = "application/json"

    query = """select act from useinfo
        join (select sid,  max(id) mid
        from useinfo where event='poll' and div_id = %s and course_id = %s group by sid) as T
        on id = T.mid"""

    rows = db.executesql(query, (div_id, course))

    result_list = []
    for row in rows:
        val = row[0].split(":")[0]
        result_list.append(int(val))

    # maps option : count
    opt_counts = Counter(result_list)

    if result_list:
        for i in range(max(result_list)):
            if i not in opt_counts:
                opt_counts[i] = 0
    # opt_list holds the option numbers from smallest to largest
    # count_list[i] holds the count of responses that chose option i
    opt_list = sorted(opt_counts.keys())
    count_list = []
    for i in opt_list:
        count_list.append(opt_counts[i])

    user_res = None
    if auth.user:
        user_res = (
            db(
                (db.useinfo.sid == auth.user.username)
                & (db.useinfo.course_id == course)
                & (db.useinfo.div_id == div_id)
            )
            .select(db.useinfo.act, orderby=~db.useinfo.id)
            .first()
        )

    if user_res:
        my_vote = user_res.act
    else:
        my_vote = -1

    return json.dumps([len(result_list), opt_list, count_list, div_id, my_vote])


def gettop10Answers():
    course = request.vars.course
    question = request.vars.div_id
    response.headers["content-type"] = "application/json"
    rows = []

    try:
        dbcourse = db(db.courses.course_name == course).select(**SELECT_CACHE).first()
        count_expr = db.fitb_answers.answer.count()
        rows = db(
            (db.fitb_answers.div_id == question)
            & (db.fitb_answers.course_name == course)
            & (db.fitb_answers.timestamp > dbcourse.term_start_date)
        ).select(
            db.fitb_answers.answer,
            count_expr,
            groupby=db.fitb_answers.answer,
            orderby=~count_expr,
            limitby=(0, 10),
        )
        res = [
            {"answer": clean(row.fitb_answers.answer), "count": row[count_expr]}
            for row in rows
        ]
    except Exception as e:
        logger.debug(e)
        res = "error in query"

    miscdata = {"course": course}
    _getCorrectStats(
        miscdata, "fillb"
    )  # TODO: rewrite _getCorrectStats to use xxx_answers

    if auth.user and verifyInstructorStatus(course, auth.user.id):  # noqa: F405
        resultList = _getStudentResults(question)
        miscdata["reslist"] = resultList

    return json.dumps([res, miscdata])


def getassignmentgrade():
    response.headers["content-type"] = "application/json"
    if not auth.user:
        return json.dumps([dict(message="not logged in")])

    divid = request.vars.div_id

    ret = {
        "grade": "Not graded yet",
        "comment": "No Comments",
        "avg": "None",
        "count": "None",
        "released": False,
    }

    # check that the assignment is released
    #
    a_q = (
        db(
            (db.assignments.course == auth.user.course_id)
            & (db.assignment_questions.assignment_id == db.assignments.id)
            & (db.assignment_questions.question_id == db.questions.id)
            & (db.questions.name == divid)
        )
        .select(
            db.assignments.released, db.assignments.id, db.assignment_questions.points
        )
        .first()
    )

    # if there is no assignment_question
    # try new way that we store scores and comments
    # divid is a question; find question_grades row
    result = (
        db(
            (db.question_grades.sid == auth.user.username)
            & (db.question_grades.course_name == auth.user.course_name)
            & (db.question_grades.div_id == divid)
        )
        .select(db.question_grades.score, db.question_grades.comment)
        .first()
    )
    logger.debug(result)
    if result:
        # say that we're sending back result styles in new version, so they can be processed differently without affecting old way during transition.
        ret["version"] = 2
        ret["released"] = a_q.assignments.released if a_q else False
        if a_q and not a_q.assignments.released:
            ret["grade"] = "Not graded yet"
        elif a_q and a_q.assignments.released:
            ret["grade"] = result.score or "Written Feedback Only"

        if a_q and a_q.assignments.released == True:
            ret["max"] = a_q.assignment_questions.points
        else:
            ret["max"] = ""

        if result.comment:
            ret["comment"] = result.comment

    return json.dumps([ret])


def _canonicalize_tz(tstring):
    x = re.search(r"\((.*)\)", tstring)
    x = x.group(1)
    y = x.split()
    if len(y) == 1:
        return tstring
    else:
        zstring = "".join([i[0] for i in y])
        return re.sub(r"(.*)\((.*)\)", r"\1({})".format(zstring), tstring)


# .. _getAssessResults:
#
# getAssessResults
# ----------------
def getAssessResults():
    if not auth.user:
        # can't query for user's answers if we don't know who the user is, so just load from local storage
        return ""

    course = request.vars.course
    div_id = request.vars.div_id
    event = request.vars.event
    if (
        verifyInstructorStatus(auth.user.course_name, auth.user) and request.vars.sid
    ):  # retrieving results for grader
        sid = request.vars.sid
    else:
        sid = auth.user.username

    # TODO This whole thing is messy - get the deadline from the assignment in the db
    if request.vars.deadline:
        try:
            deadline = parse(_canonicalize_tz(request.vars.deadline))
            tzoff = session.timezoneoffset if session.timezoneoffset else 0
            deadline = deadline + datetime.timedelta(hours=float(tzoff))
            deadline = deadline.replace(tzinfo=None)
        except Exception:
            logger.error("Bad Timezone - {}".format(request.vars.deadline))
            deadline = datetime.datetime.utcnow()
    else:
        deadline = datetime.datetime.utcnow()

    response.headers["content-type"] = "application/json"

    # Identify the correct event and query the database so we can load it from the server
    if event == "fillb":
        rows = (
            db(
                (db.fitb_answers.div_id == div_id)
                & (db.fitb_answers.course_name == course)
                & (db.fitb_answers.sid == sid)
            )
            .select(
                db.fitb_answers.answer,
                db.fitb_answers.timestamp,
                orderby=~db.fitb_answers.id,
            )
            .first()
        )
        if not rows:
            return ""  # server doesn't have it so we load from local storage instead
        #
        res = {"answer": rows.answer, "timestamp": str(rows.timestamp)}
        do_server_feedback, feedback = is_server_feedback(div_id, course)
        if do_server_feedback:
            correct, res_update = fitb_feedback(rows.answer, feedback)
            res.update(res_update)
        return json.dumps(res)
    elif event == "mChoice":
        rows = (
            db(
                (db.mchoice_answers.div_id == div_id)
                & (db.mchoice_answers.course_name == course)
                & (db.mchoice_answers.sid == sid)
            )
            .select(
                db.mchoice_answers.answer,
                db.mchoice_answers.timestamp,
                db.mchoice_answers.correct,
                orderby=~db.mchoice_answers.id,
            )
            .first()
        )
        if not rows:
            return ""
        res = {
            "answer": rows.answer,
            "timestamp": str(rows.timestamp),
            "correct": rows.correct,
        }
        return json.dumps(res)
    elif event == "dragNdrop":
        rows = (
            db(
                (db.dragndrop_answers.div_id == div_id)
                & (db.dragndrop_answers.course_name == course)
                & (db.dragndrop_answers.sid == sid)
            )
            .select(
                db.dragndrop_answers.answer,
                db.dragndrop_answers.timestamp,
                db.dragndrop_answers.correct,
                db.dragndrop_answers.min_height,
                orderby=~db.dragndrop_answers.id,
            )
            .first()
        )
        if not rows:
            return ""
        res = {
            "answer": rows.answer,
            "timestamp": str(rows.timestamp),
            "correct": rows.correct,
            "minHeight": str(rows.min_height),
        }
        return json.dumps(res)
    elif event == "clickableArea":
        rows = (
            db(
                (db.clickablearea_answers.div_id == div_id)
                & (db.clickablearea_answers.course_name == course)
                & (db.clickablearea_answers.sid == sid)
            )
            .select(
                db.clickablearea_answers.answer,
                db.clickablearea_answers.timestamp,
                db.clickablearea_answers.correct,
                orderby=~db.clickablearea_answers.id,
            )
            .first()
        )
        if not rows:
            return ""
        res = {
            "answer": rows.answer,
            "timestamp": str(rows.timestamp),
            "correct": rows.correct,
        }
        return json.dumps(res)
    elif event == "timedExam":
        rows = (
            db(
                (db.timed_exam.reset == None)  # noqa: E711
                & (db.timed_exam.div_id == div_id)
                & (db.timed_exam.course_name == course)
                & (db.timed_exam.sid == sid)
            )
            .select(
                db.timed_exam.correct,
                db.timed_exam.incorrect,
                db.timed_exam.skipped,
                db.timed_exam.time_taken,
                db.timed_exam.timestamp,
                db.timed_exam.reset,
                orderby=~db.timed_exam.id,
            )
            .first()
        )
        if not rows:
            return ""
        res = {
            "correct": rows.correct,
            "incorrect": rows.incorrect,
            "skipped": str(rows.skipped),
            "timeTaken": str(rows.time_taken),
            "timestamp": str(rows.timestamp),
            "reset": str(rows.reset),
        }
        return json.dumps(res)
    elif event == "parsons":
        rows = (
            db(
                (db.parsons_answers.div_id == div_id)
                & (db.parsons_answers.course_name == course)
                & (db.parsons_answers.sid == sid)
            )
            .select(
                db.parsons_answers.answer,
                db.parsons_answers.source,
                db.parsons_answers.timestamp,
                orderby=~db.parsons_answers.id,
            )
            .first()
        )
        if not rows:
            return ""
        res = {
            "answer": rows.answer,
            "source": rows.source,
            "timestamp": str(rows.timestamp),
        }
        return json.dumps(res)
    elif event == "shortanswer":
        logger.debug(f"Getting shortanswer: deadline is {deadline} ")
        rows = db(
            (db.shortanswer_answers.sid == sid)
            & (db.shortanswer_answers.div_id == div_id)
            & (db.shortanswer_answers.course_name == course)
        ).select(orderby=~db.shortanswer_answers.id)
        if not rows:
            return ""
        last_answer = None
        if not request.vars.deadline:
            row = rows[0]
        else:
            last_answer = rows[0]
            for row in rows:
                if row.timestamp <= deadline:
                    break
            if row.timestamp > deadline:
                row = None

        if row and row == last_answer:
            res = {"answer": row.answer, "timestamp": row.timestamp.isoformat()}
        else:
            if row and row.timestamp <= deadline:
                res = {"answer": row.answer, "timestamp": row.timestamp.isoformat()}
            else:
                res = {
                    "answer": "",
                    "timestamp": None,
                    "last_answer": last_answer.answer,
                    "last_timestamp": last_answer.timestamp.isoformat(),
                }
        srow = (
            db(
                (db.question_grades.sid == sid)
                & (db.question_grades.div_id == div_id)
                & (db.question_grades.course_name == course)
            )
            .select()
            .first()
        )
        if srow:
            res["score"] = srow.score
            res["comment"] = srow.comment

        return json.dumps(res)
    elif event == "lp_build":
        rows = (
            db(
                (db.lp_answers.div_id == div_id)
                & (db.lp_answers.course_name == course)
                & (db.lp_answers.sid == sid)
            )
            .select(
                db.lp_answers.answer,
                db.lp_answers.timestamp,
                db.lp_answers.correct,
                orderby=~db.lp_answers.id,
            )
            .first()
        )
        if not rows:
            return ""  # server doesn't have it so we load from local storage instead
        answer = json.loads(rows.answer)
        correct = rows.correct
        return json.dumps(
            {"answer": answer, "timestamp": str(rows.timestamp), "correct": correct}
        )


def tookTimedAssessment():
    if auth.user:
        sid = auth.user.username
    else:
        return json.dumps({"tookAssessment": False})

    exam_id = request.vars.div_id
    course = request.vars.course_name
    rows = (
        db(
            (db.timed_exam.div_id == exam_id)
            & (db.timed_exam.sid == sid)
            & (db.timed_exam.course_name == course)
        )
        .select(orderby=~db.timed_exam.id)
        .first()
    )
    logger.debug(f"checking {exam_id} {sid} {course} {rows}")
    if rows:
        return json.dumps({"tookAssessment": True})
    else:
        return json.dumps({"tookAssessment": False})


# The request variable ``code`` must contain JSON-encoded RST to be rendered by Runestone. Only the HTML containing the actual Runestone component will be returned.
def preview_question():

    begin = """
.. raw:: html

    <begin_directive>

"""
    end = """

.. raw:: html

    <end_directive>

"""

    try:
        code = begin + dedent(json.loads(request.vars.code)) + end
        with open(
            "applications/{}/build/preview/_sources/index.rst".format(
                request.application
            ),
            "w",
            encoding="utf-8",
        ) as ixf:
            ixf.write(code)

        # Note that ``os.environ`` isn't a dict, it's an object whose setter modifies environment variables. So, modifications of a copy/deepcopy still `modify the original environment <https://stackoverflow.com/questions/13142972/using-copy-deepcopy-on-os-environ-in-python-appears-broken>`_. Therefore, convert it to a dict, where modifications will not affect the environment.
        env = dict(os.environ)
        # Prevent any changes to the database when building a preview question.
        env.pop("DBURL", None)
        # Run a runestone build.
        # We would like to use sys.executable But when we run web2py
        # in uwsgi then sys.executable is uwsgi which doesn't work.
        # Why not just run runestone?
        if "python" not in settings.python_interpreter:
            logger.error(f"Error {settings.python_interpreter} is not a valid python")
            return json.dumps(
                f"Error: settings.python_interpreter must be set to a valid interpreter not {settings.python_interpreter}"
            )
        popen_obj = subprocess.Popen(
            [settings.python_interpreter, "-m", "runestone", "build"],
            # The build must be run from the directory containing a ``conf.py`` and all the needed support files.
            cwd="applications/{}/build/preview".format(request.application),
            # Capture the build output as text in case of an error.
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            # Pass the modified environment which doesn't contain ``DBURL``.
            env=env,
        )
        stdout, stderr = popen_obj.communicate()
        # If there was an error, return stdout and stderr from the build.
        if popen_obj.returncode != 0:
            return json.dumps(
                "Error: Runestone build failed:\n\n" + stdout + "\n" + stderr
            )

        with open(
            "applications/{}/build/preview/build/preview/index.html".format(
                request.application
            ),
            "r",
            encoding="utf-8",
        ) as ixf:
            src = ixf.read()
            tree = html.fromstring(src)
            if len(tree.cssselect(".runestone")) == 0:
                src = ""
            result = re.search(
                "<begin_directive>(.*)<end_directive>", src, flags=re.DOTALL
            )
            if result:
                ctext = result.group(1)
            else:
                component = tree.cssselect(".system-message")
                if len(component) > 0:
                    ctext = html.tostring(component[0]).decode("utf-8")
                    logger.debug("error - ", ctext)
                else:
                    ctext = "Error: Runestone content missing."
            return json.dumps(ctext)
    except Exception as ex:
        return json.dumps("Error: {}".format(ex))


def save_donate():
    if auth.user:
        db(db.auth_user.id == auth.user.id).update(donated=True)


def did_donate():
    if auth.user:
        d_status = (
            db(db.auth_user.id == auth.user.id).select(db.auth_user.donated).first()
        )

        return json.dumps(dict(donate=d_status.donated))
    return json.dumps(dict(donate=False))


def get_datafile():
    """
    course_id - string, the name of the course
    acid -  the acid of this datafile
    """
    course = request.vars.course_id  # the course name
    the_course = db(db.courses.course_name == course).select(**SELECT_CACHE).first()
    acid = request.vars.acid
    file_contents = (
        db(
            (db.source_code.acid == acid)
            & (
                (db.source_code.course_id == the_course.base_course)
                | (db.source_code.course_id == course)
            )
        )
        .select(db.source_code.main_code)
        .first()
    )

    if file_contents:
        file_contents = file_contents.main_code
    else:
        file_contents = None

    return json.dumps(dict(data=file_contents))


@auth.requires(
    lambda: verifyInstructorStatus(auth.user.course_name, auth.user),
    requires_login=True,
)
def broadcast_code():
    """
    Callable by an instructor to send the code in their scratch activecode
    to all students in the class.
    """
    the_course = (
        db(db.courses.course_name == auth.user.course_name)
        .select(**SELECT_CACHE)
        .first()
    )
    cid = the_course.id
    student_list = db(
        (db.user_courses.course_id == cid)
        & (db.auth_user.id == db.user_courses.user_id)
    ).select()
    shared_code = (
        "{} Instructor shared code on {}\n".format(
            COMMENT_MAP.get(request.vars.lang, "#"), datetime.datetime.utcnow().date()
        )
        + request.vars.code
    )
    counter = 0
    for student in student_list:
        if student.auth_user.id == auth.user.id:
            continue
        sid = student.auth_user.username
        try:
            db.code.insert(
                sid=sid,
                acid=request.vars.divid,
                code=shared_code,
                emessage="",
                timestamp=datetime.datetime.utcnow(),
                course_id=cid,
                language=request.vars.lang,
                comment="Instructor shared code",
            )
        except Exception as e:
            logger.error("Failed to insert instructor code! details: {}".format(e))
            return json.dumps(dict(mess="failed"))

        counter += 1

    return json.dumps(dict(mess="success", share_count=counter))


def _same_class(user1: str, user2: str) -> bool:
    user1_course = (
        db(db.auth_user.username == user1).select(db.auth_user.course_id).first()
    )
    user2_course = (
        db(db.auth_user.username == user2).select(db.auth_user.course_id).first()
    )

    return user1_course == user2_course


def login_status():
    if auth.user:
        return json.dumps(dict(status="loggedin", course_name=auth.user.course_name))
    else:
        return json.dumps(dict(status="loggedout", course_name=auth.user.course_name))


auto_gradable_q = [
    "clickablearea",
    "mchoice",
    "parsonsprob",
    "dragndrop",
    "fillintheblank",
    "quizly",
    "khanex",
]


def get_question_source():
    """Called from the selectquestion directive
    There are 4 cases:

    1. If there is only 1 question in the question list then return the html source for it.
    2. If there are multiple questions then choose a question at random
    3. If a proficiency is selected then select a random question that tests that proficiency
    4. If the question is an AB question then see if this student is an A or a B or assign them to one randomly.

    In the last two cases, first check to see if there is a question for this student for this
    component that was previously selected.

    Returns:
        json: html source for this question
    """
    prof = False
    points = request.vars.points
    logger.debug(f"POINTS = {points}")
    min_difficulty = request.vars.min_difficulty
    max_difficulty = request.vars.max_difficulty
    not_seen_ever = request.vars.not_seen_ever
    autogradable = request.vars.autogradable
    is_primary = request.vars.primary
    is_ab = request.vars.AB
    selector_id = request.vars["selector_id"]
    assignment_name = request.vars["timedWrapper"]
    toggle = request.vars["toggleOptions"]

    # If the question has a :points: option then those points are the default
    # however sometimes questions are entered in the web ui without the :points:
    # and points are assigned in the UI instead.  If this is part of an
    # assignment or timed exam AND the points are set in the web UI we will
    # use the points from the UI over the :points:  If this is an assignment
    # or exam that is totally written in RST then  the points in the UI will match
    # the points from the assignment anyway.
    if assignment_name:
        ui_points = (
            db(
                (db.assignments.name == assignment_name)
                & (db.assignments.id == db.assignment_questions.assignment_id)
                & (db.assignment_questions.question_id == db.questions.id)
                & (db.questions.name == selector_id)
            )
            .select(db.assignment_questions.points)
            .first()
        )
        logger.debug(
            f"Assignment Points for {assignment_name}, {selector_id} = {ui_points}"
        )
        if ui_points:
            points = ui_points.points

    if request.vars["questions"]:
        questionlist = request.vars["questions"].split(",")
        questionlist = [q.strip() for q in questionlist]
    elif request.vars["proficiency"]:
        prof = request.vars["proficiency"]

        query = (db.competency.competency == prof) & (
            db.competency.question == db.questions.id
        )
        if is_primary:
            query = query & (db.competency.is_primary == True)
        if min_difficulty:
            query = query & (db.questions.difficulty >= float(min_difficulty))
        if max_difficulty:
            query = query & (db.questions.difficulty <= float(max_difficulty))
        if autogradable:
            query = query & (
                (db.questions.autograde == "unittest")
                | db.questions.question_type.contains(auto_gradable_q, all=False)
            )
        res = db(query).select(db.questions.name)
        logger.debug(f"Query was {db._lastsql}")
        if res:
            questionlist = [row.name for row in res]
        else:
            questionlist = []
            logger.error(f"No questions found for proficiency {prof}")
            return json.dumps(f"<p>No Questions found for proficiency: {prof}</p>")

    if not auth.user:
        # user is not logged in so just give them a random question from questions list
        # and be done with it.
        q = random.choice(questionlist)
        res = db(db.questions.name == q).select(db.questions.htmlsrc).first()
        return json.dumps(res.htmlsrc)

    logger.debug(f"is_ab is {is_ab}")
    if is_ab:

        res = db(
            (db.user_experiment.sid == auth.user.username)
            & (db.user_experiment.experiment_id == is_ab)
        ).select(orderby=db.user_experiment.id)

        if not res:
            exp_group = random.randrange(2)
            db.user_experiment.insert(
                sid=auth.user.username, experiment_id=is_ab, exp_group=exp_group
            )
            logger.debug(f"added {auth.user.username} to {is_ab} group {exp_group}")

        else:
            exp_group = res[0].exp_group

        logger.debug(f"experimental group is {exp_group}")

        prev_selection = (
            db(
                (db.selected_questions.sid == auth.user.username)
                & (db.selected_questions.selector_id == selector_id)
            )
            .select()
            .first()
        )

        if prev_selection:
            questionid = prev_selection.selected_id
        else:
            questionid = questionlist[exp_group]

    if not is_ab:
        poss = set()
        if not_seen_ever:
            seenq = db(
                (db.useinfo.sid == auth.user.username)
                & (db.useinfo.div_id.contains(questionlist, all=False))
            ).select(db.useinfo.div_id)
            seen = set([x.div_id for x in seenq])
            poss = set(questionlist)
            questionlist = list(poss - seen)

        if len(questionlist) == 0 and len(poss) > 0:
            questionlist = list(poss)

        htmlsrc = ""

        prev_selection = (
            db(
                (db.selected_questions.sid == auth.user.username)
                & (db.selected_questions.selector_id == selector_id)
            )
            .select()
            .first()
        )

        if prev_selection:
            questionid = prev_selection.selected_id
        else:
            # Eliminate any previous exam questions for this student
            prev_questions = db(db.selected_questions.sid == auth.user.username).select(
                db.selected_questions.selected_id
            )
            prev_questions = set([row.selected_id for row in prev_questions])
            possible = set(questionlist)
            questionlist = list(possible - prev_questions)
            if questionlist:
                questionid = random.choice(questionlist)
            else:
                # If there are no questions left we should still return a random question.
                questionid = random.choice(list(possible))

    logger.debug(f"toggle is {toggle}")
    if toggle:
        prev_selection = (
            db(
                (db.selected_questions.sid == auth.user.username)
                & (db.selected_questions.selector_id == selector_id)
            )
            .select()
            .first()
        )
        if prev_selection:
            questionid = prev_selection.selected_id
        else:
            questionid = request.vars["questions"].split(",")[0]
    # else:
    #     logger.error(
    #         f"Question ID '{questionid}' not found in select question list of '{selector_id}'."
    #     )
    #     return json.dumps(
    #         f"<p>Question ID '{questionid}' not found in select question list of '{selector_id}'.</p>"
    #     )

    res = db((db.questions.name == questionid)).select(db.questions.htmlsrc).first()

    if res and not prev_selection:
        qid = db.selected_questions.insert(
            selector_id=selector_id,
            sid=auth.user.username,
            selected_id=questionid,
            points=points,
        )
        if not qid:
            logger.error(
                f"Failed to insert a selected question for {selector_id} and {auth.user.username}"
            )
    else:
        logger.debug(
            f"Did not insert a record for {selector_id}, {questionid} Conditions are {res} QL: {questionlist} PREV: {prev_selection}"
        )

    if res and res.htmlsrc:
        htmlsrc = res.htmlsrc
    else:
        logger.error(
            f"HTML Source not found for {questionid} in course {auth.user.course_name} for {auth.user.username}"
        )
        htmlsrc = "<p>No preview available</p>"
    return json.dumps(htmlsrc)


@auth.requires_login()
def update_selected_question():
    """
    This endpoint is used by the selectquestion problems that allow the
    student to select the problem they work on.  For example they may have
    a programming problem that can be solved with writing code, or they
    can switch to a parsons problem if necessary.

    Caller must provide:
    * ``metaid`` -- the id of the selectquestion
    * ``selected`` -- the id of the real question chosen by the student
    """
    sid = auth.user.username
    selector_id = request.vars.metaid
    selected_id = request.vars.selected
    logger.debug(f"USQ - {selector_id} --> {selected_id} for {sid}")
    db.selected_questions.update_or_insert(
        (db.selected_questions.selector_id == selector_id)
        & (db.selected_questions.sid == sid),
        selected_id=selected_id,
        selector_id=selector_id,
        sid=sid,
    )
