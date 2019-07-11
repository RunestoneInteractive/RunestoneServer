import json
import datetime
import logging
import subprocess
import uuid
from bleach import clean
from collections import Counter
from diff_match_patch import *
import os
import sys
from io import open
from lxml import html
from feedback import is_server_feedback, fitb_feedback, lp_feedback

logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)

response.headers['Access-Control-Allow-Origin'] = '*'

EVENT_TABLE = {'mChoice':'mchoice_answers',
               'fillb':'fitb_answers',
               'dragNdrop':'dragndrop_answers',
               'clickableArea':'clickablearea_answers',
               'parsons':'parsons_answers',
               'codelens1':'codelens_answers',
               'shortanswer':'shortanswer_answers',
               'fillintheblank': 'fitb_answers',
               'mchoice': 'mchoice_answers',
               'dragndrop': 'dragndrop_answers',
               'clickablearea':'clickablearea_answers',
               'parsonsprob': 'parsons_answers' }


def compareAndUpdateCookieData(sid):
    if 'ipuser' in request.cookies and request.cookies['ipuser'].value != sid and request.cookies['ipuser'].value.endswith("@"+request.client):
        db.useinfo.update_or_insert(db.useinfo.sid == request.cookies['ipuser'].value, sid=sid)

def hsblog():
    setCookie = False
    if auth.user:
        sid = auth.user.username
        compareAndUpdateCookieData(sid)
        setCookie = True    # we set our own cookie anyway to eliminate many of the extraneous anonymous
                            # log entries that come from auth timing out even but the user hasn't reloaded
                            # the page.
    else:
        if 'ipuser' in request.cookies:
            sid = request.cookies['ipuser'].value
            setCookie = True
        else:
            sid = str(uuid.uuid1().int)+"@"+request.client
            setCookie = True
    act = request.vars.get('act', '')
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
        db.useinfo.insert(sid=sid,act=act[0:512],div_id=div_id,event=event,timestamp=ts,course_id=course)
    except:
        logger.debug('failed to insert log record for {} in {} : {} {} {}'.format(sid, course, div_id, event, act))

    if event == 'timedExam' and (act == 'finish' or act == 'reset'):
        logger.debug(act)
        if act == 'reset':
            r = 'T'
        else:
            r = None

        try:
            db.timed_exam.insert(sid=sid, course_name=course, correct=int(request.vars.correct),
                             incorrect=int(request.vars.incorrect), skipped=int(request.vars.skipped),
                             time_taken=int(tt), timestamp=ts,
                             div_id=div_id,reset=r)
        except Exception as e:
            logger.debug('failed to insert a timed exam record for {} in {} : {}'.format(sid, course, div_id))
            logger.debug('correct {} incorrect {} skipped {} time {}'.format(request.vars.correct, request.vars.incorrect, request.vars.skipped, request.vars.time))
            logger.debug('Error: {}'.format(e.message))

    # Produce a default result.
    res = dict(log=True, timestamp=str(ts))

    # Process this event.
    if event == 'mChoice' and auth.user:
        # # has user already submitted a correct answer for this question?
        # if db((db.mchoice_answers.sid == sid) &
        #       (db.mchoice_answers.div_id == div_id) &
        #       (db.mchoice_answers.course_name == auth.user.course_name) &
        #       (db.mchoice_answers.correct == 'T')).count() == 0:
            answer = request.vars.answer
            correct = request.vars.correct
            db.mchoice_answers.insert(sid=sid,timestamp=ts, div_id=div_id, answer=answer, correct=correct, course_name=course)
    elif event == "fillb" and auth.user:
        answer_json = request.vars.answer
        correct = request.vars.correct
        # Grade on the server if needed.
        do_server_feedback, feedback = is_server_feedback(div_id, course)
        if do_server_feedback:
            correct, res_update = fitb_feedback(answer_json, feedback)
            res.update(res_update)

        # Save this data.
        db.fitb_answers.insert(sid=sid, timestamp=ts, div_id=div_id, answer=answer_json, correct=correct, course_name=course)

    elif event == "dragNdrop" and auth.user:
        # if db((db.dragndrop_answers.sid == sid) &
        #       (db.dragndrop_answers.div_id == div_id) &
        #       (db.dragndrop_answers.course_name == auth.user.course_name) &
        #       (db.dragndrop_answers.correct == 'T')).count() == 0:
            answers = request.vars.answer
            minHeight = request.vars.minHeight
            correct = request.vars.correct

            db.dragndrop_answers.insert(sid=sid, timestamp=ts, div_id=div_id, answer=answers, correct=correct, course_name=course, minHeight=minHeight)
    elif event == "clickableArea" and auth.user:
        # if db((db.clickablearea_answers.sid == sid) &
        #       (db.clickablearea_answers.div_id == div_id) &
        #       (db.clickablearea_answers.course_name == auth.user.course_name) &
        #       (db.clickablearea_answers.correct == 'T')).count() == 0:
            correct = request.vars.correct
            db.clickablearea_answers.insert(sid=sid, timestamp=ts, div_id=div_id, answer=act, correct=correct, course_name=course)

    elif event == "parsons" and auth.user:
        # if db((db.parsons_answers.sid == sid) &
        #       (db.parsons_answers.div_id == div_id) &
        #       (db.parsons_answers.course_name == auth.user.course_name) &
        #       (db.parsons_answers.correct == 'T')).count() == 0:
            correct = request.vars.correct
            answer = request.vars.answer
            source = request.vars.source
            db.parsons_answers.insert(sid=sid, timestamp=ts, div_id=div_id, answer=answer, source=source, correct=correct, course_name=course)

    elif event == "codelensq" and auth.user:
        # if db((db.codelens_answers.sid == sid) &
        #       (db.codelens_answers.div_id == div_id) &
        #       (db.codelens_answers.course_name == auth.user.course_name) &
        #       (db.codelens_answers.correct == 'T')).count() == 0:
            correct = request.vars.correct
            answer = request.vars.answer
            source = request.vars.source
            db.codelens_answers.insert(sid=sid, timestamp=ts, div_id=div_id, answer=answer, source=source, correct=correct, course_name=course)

    elif event == "shortanswer" and auth.user:
        # for shortanswers just keep the latest?? -- the history will be in useinfo
        db.shortanswer_answers.update_or_insert((db.shortanswer_answers.sid == sid) & (db.shortanswer_answers.div_id == div_id) & (db.shortanswer_answers.course_name == course),
            sid=sid, answer=act, div_id=div_id, timestamp=ts, course_name=course)

    elif event == "lp_build" and auth.user:
        ret, new_fields = db.lp_answers._validate_fields(dict(
            sid=sid, timestamp=ts, div_id=div_id, course_name=course
        ))
        if not ret.errors:
            do_server_feedback, feedback = is_server_feedback(div_id, course)
            if do_server_feedback:
                try:
                    code_snippets = json.loads(request.vars.answer)['code_snippets']
                except:
                    code_snippets = []
                result = lp_feedback(code_snippets, feedback)
                # If an error occurred or we're not testing, pass the answer through.
                res.update(result)

                # Record the results in the database.
                correct = result.get('correct')
                answer = result.get('answer', {})
                answer['code_snippets'] = code_snippets
                ret = db.lp_answers.validate_and_insert(sid=sid, timestamp=ts, div_id=div_id,
                    answer=json.dumps(answer), correct=correct, course_name=course)
                if ret.errors:
                    res.setdefault('errors', []).append(ret.errors.as_dict())
            else:
                res['errors'] = ['No feedback provided.']
        else:
            res.setdefault('errors', []).append(ret.errors.as_dict())

    response.headers['content-type'] = 'application/json'
    if setCookie:
        response.cookies['ipuser'] = sid
        response.cookies['ipuser']['expires'] = 24*3600*90
        response.cookies['ipuser']['path'] = '/'
    return json.dumps(res)

def runlog():    # Log errors and runs with code
    response.headers['content-type'] = 'application/json'
    setCookie = False
    if auth.user:
        sid = auth.user.username
        setCookie = True
    else:
        if 'ipuser' in request.cookies:
            sid = request.cookies['ipuser'].value
            setCookie = True
        else:
            sid = str(uuid.uuid1().int)+"@"+request.client
            setCookie = True
    div_id = request.vars.div_id
    course = request.vars.course
    code = request.vars.code if request.vars.code else ""
    ts = datetime.datetime.utcnow()
    error_info = request.vars.errinfo
    pre = request.vars.prefix if request.vars.prefix else ""
    post = request.vars.suffix if request.vars.suffix else ""
    if error_info != 'success':
        event = 'ac_error'
        act = str(error_info)[:512]
    else:
        act = 'run'
        if request.vars.event:
            event = request.vars.event
        else:
            event = 'activecode'
    num_tries = 3
    done = False
    while num_tries > 0 and not done:
        try:
            db.useinfo.insert(sid=sid, act=act, div_id=div_id, event=event, timestamp=ts, course_id=course)
            done = True
        except Exception as e:
            logger.error("probable Too Long problem trying to insert sid={} act={} div_id={} event={} timestamp={} course_id={} exception={}".format(sid, act, div_id, event, ts, course, e))
            num_tries -= 1
    if num_tries == 0:
        raise Exception("Runlog Failed to insert into useinfo")

    num_tries = 3
    done = False
    while num_tries > 0 and not done:
        try:
            dbid = db.acerror_log.insert(sid=sid,
                                        div_id=div_id,
                                        timestamp=ts,
                                        course_id=course,
                                        code=pre+code+post,
                                        emessage=error_info)
            done = True
        except:
            logger.error("INSERT into acerror_log FAILED retrying")
            num_tries -= 1
    if num_tries == 0:
        raise Exception("Runlog Failed to insert into acerror_log")

    #lintAfterSave(dbid, code, div_id, sid)
    if auth.user:
        if 'to_save' in request.vars and (request.vars.to_save == "True" or request.vars.to_save == "true"):
            num_tries = 3
            done = False
            dbcourse = db(db.courses.course_name == course).select().first()
            while num_tries > 0 and not done:
                try:
                    db.code.insert(sid=sid,
                        acid=div_id,
                        code=code,
                        emessage=error_info,
                        timestamp=ts,
                        course_id=dbcourse,
                        language=request.vars.lang)
                    if request.vars.partner:
                        if _same_class(sid, request.vars.partner):
                            newcode = "# This code was shared by {}\n\n".format(sid) + code
                            db.code.insert(sid=request.vars.partner,
                                acid=div_id,
                                code=newcode,
                                emessage=error_info,
                                timestamp=ts,
                                course_id=dbcourse,
                                language=request.vars.lang)
                        else:
                            res = {'message': 'You must be enrolled in the same class as your partner'}
                            return json.dumps(res)
                    done = True
                except:
                    num_tries -= 1
                    logger.error("INSERT into code FAILED retrying")
            if num_tries == 0:
                raise Exception("Runlog Failed to insert into code")

    res = {'log':True}
    if setCookie:
        response.cookies['ipuser'] = sid
        response.cookies['ipuser']['expires'] = 24*3600*90
        response.cookies['ipuser']['path'] = '/'
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

    if request.vars.sid:
        sid = request.vars.sid
        course_id = db(db.auth_user.username == sid).select(db.auth_user.course_id).first().course_id
    elif auth.user:
        sid = auth.user.username
        course_id = auth.user.course_id
    else:
        sid = None
        course_id = None

    res = {}
    if sid:
        query = ((codetbl.sid == sid) & (codetbl.acid == acid) & (codetbl.course_id == course_id) & (codetbl.timestamp != None))
        res['acid'] = acid
        res['sid'] = sid
        # get the code they saved in chronological order; id order gets that for us
        r = db(query).select(orderby=codetbl.id)
        res['history'] = [row.code for row in r]
        res['timestamps'] = [row.timestamp.isoformat() for row in r]

    response.headers['content-type'] = 'application/json'
    return json.dumps(res)


def getprog():
    """
    return the program code for a particular acid
    :Parameters:
        - `acid`: id of the active code block
        - `user`: optional identifier for the owner of the code
    :Return:
        - json object containing the source text
    """
    codetbl = db.code
    acid = request.vars.acid
    sid = request.vars.sid

    if sid:
        query = ((codetbl.sid == sid) & (codetbl.acid == acid) & (codetbl.timestamp != None))
    else:
        if auth.user:
            query = ((codetbl.sid == auth.user.username) & (codetbl.acid == acid) & (codetbl.timestamp != None))
        else:
            query = None

    res = {}
    if query:
        result = db(query)
        res['acid'] = acid
        if not result.isempty():
            # get the last code they saved; id order gets that for us
            r = result.select(orderby=codetbl.id).last().code
            res['source'] = r
            if sid:
                res['sid'] = sid
        else:
            logger.debug("Did not find anything to load for %s"%sid)
    response.headers['content-type'] = 'application/json'
    return json.dumps([res])



#@auth.requires_login()
# This function is deprecated as of June 2019
# We need to keep it in place as long as we continue to serve books
# from runestone/static/  When that period is over we can eliminate
def getuser():
    response.headers['content-type'] = 'application/json'

    if auth.user:
        try:
            # return the list of courses that auth.user is registered for to keep them from
            # accidentally wandering into courses they are not registered for.
            cres = db( (db.user_courses.user_id == auth.user.id) &
                       (db.user_courses.course_id == db.courses.id)).select(db.courses.course_name)
            clist = []
            for row in cres:
                clist.append(row.course_name)
            res = {'email': auth.user.email,
                   'nick': auth.user.username,
                   'donated': auth.user.donated,
                   'isInstructor': verifyInstructorStatus(auth.user.course_name, auth.user.id),
                   'course_list': clist
                   }
            session.timezoneoffset = request.vars.timezoneoffset
            logger.debug("setting timezone offset in session %s hours" % session.timezoneoffset)
        except:
            res = dict(redirect=auth.settings.login_url)  # ?_next=....
    else:
        res = dict(redirect=auth.settings.login_url) #?_next=....
    if session.readings:
        res['readings'] = session.readings
    logger.debug("returning login info: %s" % res)
    return json.dumps([res])

def set_tz_offset():
    session.timezoneoffset = request.vars.timezoneoffset
    logger.debug("setting timezone offset in session %s hours" % session.timezoneoffset)
    return "done"


def getnumonline():
    response.headers['content-type'] = 'application/json'

    try:
        query = """select count(distinct sid) from useinfo where timestamp > current_timestamp - interval '5 minutes'  """
        rows = db.executesql(query)
    except:
        rows = [[21]]

    res = {'online':rows[0][0]}
    return json.dumps([res])


def getnumusers():
    response.headers['content-type'] = 'application/json'

    query = """select count(*) from (select distinct(sid) from useinfo) as X """
    numusers = 'more than 850,000'

    # try:
    #     numusers = cache.disk('numusers', lambda: db.executesql(query)[0][0], time_expire=21600)
    # except:
    #     # sometimes the DB query takes too long and is timed out - return something anyway
    #     numusers = 'more than 250,000'

    res = {'numusers':numusers}
    return json.dumps([res])


# I was not sure if it's okay to import it from `assignmnets.py`.
# Only questions that are marked for practice are eligible for the spaced practice.
def _get_qualified_questions(base_course, chapter_label, sub_chapter_label):
    return db((db.questions.base_course == base_course) &
              ((db.questions.topic == "{}/{}".format(chapter_label, sub_chapter_label)) |
               ((db.questions.chapter == chapter_label) &
                (db.questions.topic == None) &
                (db.questions.subchapter == sub_chapter_label))) &
              (db.questions.practice == True)).select()

#
#  Ajax Handlers to update and retrieve the last position of the user in the course
#
def updatelastpage():
    lastPageUrl = request.vars.lastPageUrl
    lastPageScrollLocation = request.vars.lastPageScrollLocation
    if lastPageUrl is None:
        return   # todo:  log request.vars, request.args and request.env.path_info
    course = request.vars.course
    completionFlag = request.vars.completionFlag
    lastPageChapter = lastPageUrl.split("/")[-2]
    lastPageSubchapter = ".".join(lastPageUrl.split("/")[-1].split(".")[:-1])
    if auth.user:
        done = False
        num_tries = 3
        while not done and num_tries > 0:
            try:
                db((db.user_state.user_id == auth.user.id) &
                        (db.user_state.course_id == course)).update(
                        last_page_url=lastPageUrl,
                        last_page_chapter=lastPageChapter,
                        last_page_subchapter=lastPageSubchapter,
                        last_page_scroll_location=lastPageScrollLocation,
                        last_page_accessed_on=datetime.datetime.utcnow())
                done = True
            except:
                num_tries -= 1
        if num_tries == 0:
            raise Exception("Failed to save the user state in update_last_page")

        done = False
        num_tries = 3
        while not done and num_tries > 0:
            try:
                db((db.user_sub_chapter_progress.user_id == auth.user.id) &
                (db.user_sub_chapter_progress.chapter_id == lastPageChapter) &
                (db.user_sub_chapter_progress.sub_chapter_id == lastPageSubchapter)).update(
                        status=completionFlag,
                        end_date=datetime.datetime.utcnow())
                done = True
            except:
                num_tries -= 1
        if num_tries == 0:
            raise Exception("Failed to save sub chapter progress in update_last_page")

        practice_settings = db(db.course_practice.course_name == auth.user.course_name)
        if (practice_settings.count() != 0 and
            practice_settings.select().first().flashcard_creation_method == 0):
            # Since each authenticated user has only one active course, we retrieve the course this way.
            course = db(db.courses.id == auth.user.course_id).select().first()

            # We only retrieve questions to be used in flashcards if they are marked for practice purpose.
            questions = _get_qualified_questions(course.base_course,
                                                 lastPageChapter,
                                                 lastPageSubchapter)
            if len(questions) > 0:
                now = datetime.datetime.utcnow()
                now_local = now - datetime.timedelta(hours=float(session.timezoneoffset) if 'timezoneoffset' in session else 0)
                existing_flashcards = db((db.user_topic_practice.user_id == auth.user.id) &
                                         (db.user_topic_practice.course_name == auth.user.course_name) &
                                         (db.user_topic_practice.chapter_label == lastPageChapter) &
                                         (db.user_topic_practice.sub_chapter_label == lastPageSubchapter) &
                                         (db.user_topic_practice.question_name == questions[0].name)
                                         )
                # There is at least one qualified question in this subchapter, so insert a flashcard for the subchapter.
                if completionFlag == '1' and existing_flashcards.isempty():
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
                        timezoneoffset=float(session.timezoneoffset) if 'timezoneoffset' in session else 0
                    )
                if completionFlag == '0' and not existing_flashcards.isempty():
                    existing_flashcards.delete()


def getCompletionStatus():
    if auth.user:
        lastPageUrl = request.vars.lastPageUrl
        lastPageChapter = lastPageUrl.split("/")[-2]
        lastPageSubchapter = ".".join(lastPageUrl.split("/")[-1].split(".")[:-1])
        result = db((db.user_sub_chapter_progress.user_id == auth.user.id) &
                    (db.user_sub_chapter_progress.chapter_id == lastPageChapter) &
                    (db.user_sub_chapter_progress.sub_chapter_id == lastPageSubchapter)).select(db.user_sub_chapter_progress.status)
        rowarray_list = []
        if result:
            for row in result:
                res = {'completionStatus': row.status}
                rowarray_list.append(res)
                #question: since the javascript in user-highlights.js is going to look only at the first row, shouldn't
                # we be returning just the *last* status? Or is there no history of status kept anyway?
            return json.dumps(rowarray_list)
        else:
            # haven't seen this Chapter/Subchapter before
            # make the insertions into the DB as necessary

            # we know the subchapter doesn't exist
            db.user_sub_chapter_progress.insert(user_id=auth.user.id,
                                                chapter_id = lastPageChapter,
                                                sub_chapter_id = lastPageSubchapter,
                                                status = -1, start_date=datetime.datetime.utcnow())
            # the chapter might exist without the subchapter
            result = db((db.user_chapter_progress.user_id == auth.user.id) & (db.user_chapter_progress.chapter_id == lastPageChapter)).select()
            if not result:
                db.user_chapter_progress.insert(user_id = auth.user.id,
                                               chapter_id = lastPageChapter,
                                               status = -1)
            return json.dumps([{'completionStatus': -1}])

def getAllCompletionStatus():
    if auth.user:
        result = db((db.user_sub_chapter_progress.user_id == auth.user.id)).select(db.user_sub_chapter_progress.chapter_id, db.user_sub_chapter_progress.sub_chapter_id, db.user_sub_chapter_progress.status, db.user_sub_chapter_progress.status, db.user_sub_chapter_progress.end_date)
        rowarray_list = []
        if result:
            for row in result:
                if row.end_date == None:
                    endDate = 0
                else:
                    endDate = row.end_date.strftime('%d %b, %Y')
                res = {'chapterName': row.chapter_id,
                       'subChapterName': row.sub_chapter_id,
                       'completionStatus': row.status,
                       'endDate': endDate}
                rowarray_list.append(res)
            return json.dumps(rowarray_list)

def getlastpage():
    course = request.vars.course
    if auth.user:
        result = db((db.user_state.user_id == auth.user.id) &
                    (db.user_state.course_id == course) &
                    (db.user_state.course_id == db.chapters.course_id) &
                    (db.user_state.last_page_chapter == db.chapters.chapter_label) &
                    (db.sub_chapters.chapter_id == db.chapters.id) &
                    (db.user_state.last_page_subchapter == db.sub_chapters.sub_chapter_label)
                    ).select(db.user_state.last_page_url, db.user_state.last_page_hash,
                             db.chapters.chapter_name,
                             db.user_state.last_page_scroll_location,
                             db.sub_chapters.sub_chapter_name)
        rowarray_list = []
        if result:
            for row in result:
                res = {'lastPageUrl': row.user_state.last_page_url,
                       'lastPageHash': row.user_state.last_page_hash,
                       'lastPageChapter': row.chapters.chapter_name,
                       'lastPageSubchapter': row.sub_chapters.sub_chapter_name,
                       'lastPageScrollLocation': row.user_state.last_page_scroll_location}
                rowarray_list.append(res)
            return json.dumps(rowarray_list)
        else:
            db.user_state.insert(user_id=auth.user.id, course_id=course)


def _getCorrectStats(miscdata,event):
    # TODO: update this to use the xxx_answer table
    # select and count grouping by the correct column
    # this version can suffer from division by zero error
    sid = None
    dbtable = EVENT_TABLE[event]  # translate event to correct table

    if auth.user:
        sid = auth.user.username
    else:
        if 'ipuser' in request.cookies:
            sid = request.cookies['ipuser'].value

    if sid:
        course = db(db.courses.course_name == miscdata['course']).select().first()
        tbl = db[dbtable]

        count_expr = tbl.correct.count()
        rows = db((tbl.sid == sid) & (tbl.timestamp > course.term_start_date)).select(tbl.correct, count_expr, groupby=tbl.correct)
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
            pctcorr = 'unavailable'
    else:
        pctcorr = 'unavailable'

    miscdata['yourpct'] = pctcorr


def _getStudentResults(question):
    """
    Internal function to collect student answers
    """
    cc = db(db.courses.id == auth.user.course_id).select().first()
    course = cc.course_name
    qst = db((db.questions.name == question) & (db.questions.base_course == cc.base_course )).select().first()
    tbl_name = EVENT_TABLE[qst.question_type]
    tbl = db[tbl_name]

    res = db( (tbl.div_id == question) &
                (tbl.course_name == cc.course_name) &
                (tbl.timestamp >= cc.term_start_date)).select(tbl.sid, tbl.answer, orderby=tbl.sid)

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
                currentAnswers.append(answer)
            else:
                currentAnswers.sort()
                resultList.append((currentSid, currentAnswers))
                currentAnswers = [answer]
                currentSid = row.sid

        currentAnswers.sort()
        resultList.append((currentSid, currentAnswers))

    return resultList


def getaggregateresults():
    course = request.vars.course
    question = request.vars.div_id
    # select act, count(*) from useinfo where div_id = 'question4_2_1' group by act;
    response.headers['content-type'] = 'application/json'

    if not auth.user:
        return json.dumps([dict(answerDict={}, misc={}, emess='You must be logged in')])

    is_instructor = verifyInstructorStatus(course,auth.user.id)
    # Yes, these two things could be done as a join.  but this **may** be better for performance
    if course == 'thinkcspy' or course == 'pythonds':
        start_date = datetime.datetime.utcnow() - datetime.timedelta(days=90)
    else:
        start_date = db(db.courses.course_name == course).select(db.courses.term_start_date).first().term_start_date
    count = db.useinfo.id.count()
    try:
        result = db((db.useinfo.div_id == question) &
                    (db.useinfo.course_id == course) &
                    (db.useinfo.timestamp >= start_date)
                    ).select(db.useinfo.act, count, groupby=db.useinfo.act)
    except:
        return json.dumps([dict(answerDict={}, misc={}, emess='Sorry, the request timed out')])

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
            l = key.split(':')
            try:
                answer = l[1]
                if 'correct' in key:
                    correct = answer
                count = int(tdata[key])
                if answer in rdata:
                    count += rdata[answer] / 100.0 * tot
                pct = round(count / tot * 100.0)

                if answer != "undefined" and answer != "":
                    rdata[answer] = pct
            except:
                logger.debug("Bad data for %s data is %s " % (question,key))

    miscdata['correct'] = correct
    miscdata['course'] = course

    _getCorrectStats(miscdata, 'mChoice')

    returnDict = dict(answerDict=rdata, misc=miscdata)

    if auth.user and is_instructor:
        resultList = _getStudentResults(question)
        returnDict['reslist'] = resultList

    return json.dumps([returnDict])


def getpollresults():
    course = request.vars.course
    div_id = request.vars.div_id

    response.headers['content-type'] = 'application/json'


    query = '''select act from useinfo
    join (select sid,  max(id) mid
        from useinfo where event='poll' and div_id = '{}' and course_id = '{}' group by sid) as T
        on id = T.mid'''.format(div_id, course)

    rows = db.executesql(query)


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
        user_res = db((db.useinfo.sid == auth.user.username) &
            (db.useinfo.course_id == course) &
            (db.useinfo.div_id == div_id)).select(db.useinfo.act, orderby=~db.useinfo.id).first()

    if user_res:
        my_vote = user_res.act
    else:
        my_vote = -1

    return json.dumps([len(result_list), opt_list, count_list, div_id, my_vote])


def gettop10Answers():
    course = request.vars.course
    question = request.vars.div_id
    response.headers['content-type'] = 'application/json'
    rows = []

    try:
        dbcourse = db(db.courses.course_name == course).select().first()
        count_expr = db.fitb_answers.answer.count()
        rows = db((db.fitb_answers.div_id == question) &
                (db.fitb_answers.course_name == course) &
                (db.fitb_answers.timestamp > dbcourse.term_start_date)).select(db.fitb_answers.answer, count_expr,
                    groupby=db.fitb_answers.answer, orderby=~count_expr, limitby=(0, 10))
        res = [{'answer':clean(row.fitb_answers.answer), 'count':row[count_expr]} for row in rows]
    except Exception as e:
        logger.debug(e)
        res = 'error in query'

    miscdata = {'course': course}
    _getCorrectStats(miscdata,'fillb')  # TODO: rewrite _getCorrectStats to use xxx_answers

    if auth.user and verifyInstructorStatus(course, auth.user.id):
        resultList = _getStudentResults(question)
        miscdata['reslist'] = resultList

    return json.dumps([res,miscdata])


def getassignmentgrade():
    response.headers['content-type'] = 'application/json'
    if not auth.user:
        return json.dumps([dict(message="not logged in")])

    divid = request.vars.div_id

    ret = {
        'grade':"Not graded yet",
        'comment': "No Comments",
        'avg': 'None',
        'count': 'None',
    }

    # check that the assignment is released
    #
    a_q = db(
        (db.assignments.released == True) &
        (db.assignments.course == auth.user.course_id) &
        (db.assignment_questions.assignment_id == db.assignments.id) &
        (db.assignment_questions.question_id == db.questions.id) &
        (db.questions.name == divid)
    ).select(db.assignments.released, db.assignments.id, db.assignment_questions.points).first()
    logger.debug(a_q)
    if not a_q:
        return json.dumps([ret])
    # try new way that we store scores and comments

    # divid is a question; find question_grades row
    result = db(
        (db.question_grades.sid == auth.user.username) &
        (db.question_grades.course_name == auth.user.course_name) &
        (db.question_grades.div_id == divid)
    ).select(db.question_grades.score, db.question_grades.comment).first()
    logger.debug(result)
    if result:
        # say that we're sending back result styles in new version, so they can be processed differently without affecting old way during transition.
        ret['version'] = 2
        ret['grade'] = result.score
        ret['max'] = a_q.assignment_questions.points
        if result.comment:
            ret['comment'] = result.comment

    return json.dumps([ret])


def getAssessResults():
    if not auth.user:
        # can't query for user's answers if we don't know who the user is, so just load from local storage
        return ""

    course = request.vars.course
    div_id = request.vars.div_id
    event = request.vars.event
    if request.vars.sid:   # retrieving results for grader
        sid = request.vars.sid
    else:
        sid = auth.user.username

    response.headers['content-type'] = 'application/json'

    # Identify the correct event and query the database so we can load it from the server
    if event == "fillb":
        rows = db((db.fitb_answers.div_id == div_id) & (db.fitb_answers.course_name == course) & (db.fitb_answers.sid == sid)).select(db.fitb_answers.answer, db.fitb_answers.timestamp, orderby=~db.fitb_answers.id).first()
        if not rows:
            return ""   # server doesn't have it so we load from local storage instead
        #
        res = {
            'answer': rows.answer,
            'timestamp': str(rows.timestamp)
        }
        do_server_feedback, feedback = is_server_feedback(div_id, course)
        if do_server_feedback:
            correct, res_update = fitb_feedback(rows.answer, feedback)
            res.update(res_update)
        return json.dumps(res)
    elif event == "mChoice":
        rows = db((db.mchoice_answers.div_id == div_id) & (db.mchoice_answers.course_name == course) & (db.mchoice_answers.sid == sid)).select(db.mchoice_answers.answer, db.mchoice_answers.timestamp, db.mchoice_answers.correct, orderby=~db.mchoice_answers.id).first()
        if not rows:
            return ""
        res = {'answer': rows.answer, 'timestamp': str(rows.timestamp), 'correct': rows.correct}
        return json.dumps(res)
    elif event == "dragNdrop":
        rows = db((db.dragndrop_answers.div_id == div_id) & (db.dragndrop_answers.course_name == course) & (db.dragndrop_answers.sid == sid)).select(db.dragndrop_answers.answer, db.dragndrop_answers.timestamp, db.dragndrop_answers.correct, db.dragndrop_answers.minHeight, orderby=~db.dragndrop_answers.id).first()
        if not rows:
            return ""
        res = {'answer': rows.answer, 'timestamp': str(rows.timestamp), 'correct': rows.correct, 'minHeight': str(rows.minHeight)}
        return json.dumps(res)
    elif event == "clickableArea":
        rows = db((db.clickablearea_answers.div_id == div_id) & (db.clickablearea_answers.course_name == course) & (db.clickablearea_answers.sid == sid)).select(db.clickablearea_answers.answer, db.clickablearea_answers.timestamp, db.clickablearea_answers.correct, orderby=~db.clickablearea_answers.id).first()
        if not rows:
            return ""
        res = {'answer': rows.answer, 'timestamp': str(rows.timestamp), 'correct': rows.correct}
        return json.dumps(res)
    elif event == "timedExam":
        rows = db((db.timed_exam.reset == None) & (db.timed_exam.div_id == div_id) & (db.timed_exam.course_name == course) & (db.timed_exam.sid == sid)).select(db.timed_exam.correct, db.timed_exam.incorrect, db.timed_exam.skipped, db.timed_exam.time_taken, db.timed_exam.timestamp, db.timed_exam.reset, orderby=~db.timed_exam.id).first()
        if not rows:
            return ""
        res = {'correct': rows.correct, 'incorrect': rows.incorrect, 'skipped': str(rows.skipped), 'timeTaken': str(rows.time_taken), 'timestamp': str(rows.timestamp), 'reset': str(rows.reset)}
        return json.dumps(res)
    elif event == "parsons":
        rows = db((db.parsons_answers.div_id == div_id) & (db.parsons_answers.course_name == course) & (db.parsons_answers.sid == sid)).select(db.parsons_answers.answer, db.parsons_answers.source, db.parsons_answers.timestamp, orderby=~db.parsons_answers.id).first()
        if not rows:
            return ""
        res = {'answer': rows.answer, 'source': rows.source, 'timestamp': str(rows.timestamp)}
        return json.dumps(res)
    elif event == "shortanswer":
        row = db((db.shortanswer_answers.sid == sid) & (db.shortanswer_answers.div_id == div_id) & (db.shortanswer_answers.course_name == course)).select().first()
        if not row:
            return ""
        res = {'answer': row.answer, 'timestamp': str(row.timestamp)}
        return json.dumps(res)
    elif event == "lp_build":
        rows = db(
            (db.lp_answers.div_id == div_id) &
            (db.lp_answers.course_name == course) &
            (db.lp_answers.sid == sid)
        ).select(db.lp_answers.answer, db.lp_answers.timestamp, db.lp_answers.correct, orderby=~db.lp_answers.id).first()
        if not rows:
            return ""   # server doesn't have it so we load from local storage instead
        answer = json.loads(rows.answer)
        correct = rows.correct
        return json.dumps({
            'answer': answer,
            'timestamp': str(rows.timestamp),
            'correct': correct
        })



def checkTimedReset():
    if auth.user:
        user = auth.user.username
    else:
        return json.dumps({"canReset":False})

    divId = request.vars.div_id
    course = request.vars.course
    rows = db((db.timed_exam.div_id == divId) & (db.timed_exam.sid == user) & (db.timed_exam.course_name == course)).select(orderby=~db.timed_exam.id).first()

    if rows:        # If there was a scored exam
        if rows.reset == True:
            return json.dumps({"canReset":True})
        else:
            return json.dumps({"canReset":False})
    else:
        return json.dumps({"canReset":True})


# The request variable ``code`` must contain JSON-encoded RST to be rendered by Runestone. Only the HTML containing the actual Runestone component will be returned.
def preview_question():
    try:
        code = json.loads(request.vars.code)
        with open("applications/{}/build/preview/_sources/index.rst".format(request.application), "w", encoding="utf-8") as ixf:
            ixf.write(code)

        # Note that ``os.environ`` isn't a dict, it's an object whose setter modifies environment variables. So, modifications of a copy/deepcopy still `modify the original environment <https://stackoverflow.com/questions/13142972/using-copy-deepcopy-on-os-environ-in-python-appears-broken>`_. Therefore, convert it to a dict, where modifications will not affect the environment.
        env = dict(os.environ)
        # Prevent any changes to the database when building a preview question.
        del env['DBURL']
        # Run a runestone build.
        popen_obj = subprocess.Popen(
            [sys.executable, '-m', 'runestone', 'build'],
            # The build must be run from the directory containing a ``conf.py`` and all the needed support files.
            cwd='applications/{}/build/preview'.format(request.application),
            # Capture the build output in case of an error.
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            # Pass the modified environment which doesn't contain ``DBURL``.
            env=env)
        stdout, stderr = popen_obj.communicate()
        # If there was an error, return stdout and stderr from the build.
        if popen_obj.returncode != 0:
            return json.dumps('Error: Runestone build failed:\n\n' +
                              stdout + '\n' + stderr)

        with open('applications/{}/build/preview/build/preview/index.html'.format(request.application), 'r', encoding='utf-8') as ixf:
            src = ixf.read()
            tree = html.fromstring(src)
            component = tree.cssselect(".runestone")
            if len(component) > 0:
                ctext = html.tostring(component[0]).decode('utf-8')
            else:
                component = tree.cssselect(".system-message")
                if len(component) > 0:
                    ctext = html.tostring(component[0]).decode('utf-8')
                    logger.debug("error - ", ctext)
                else:
                    ctext = "Error: Runestone content missing."

            return json.dumps(ctext)
    except Exception as ex:
        return json.dumps('Error: {}'.format(ex))


def save_donate():
    if auth.user:
        db(db.auth_user.id == auth.user.id).update(donated=True)


def did_donate():
    if auth.user:
        d_status = db(db.auth_user.id == auth.user.id).select(db.auth_user.donated).first()

        return json.dumps(dict(donate=d_status.donated))
    return json.dumps(dict(donate=False))


def get_datafile():
    course = request.vars.course_id
    acid = request.vars.acid
    file_contents = db((db.source_code.acid == acid) & (db.source_code.course_id == course)).select(db.source_code.main_code).first()
    if file_contents:
        file_contents = file_contents.main_code
    else:
        file_contents = None

    return json.dumps(dict(data=file_contents))


def _same_class(user1, user2):
    user1_course = db(db.auth_user.username == user1).select(db.auth_user.course_id).first()
    user2_course = db(db.auth_user.username == user2).select(db.auth_user.course_id).first()

    return user1_course == user2_course
