import json
import datetime
import logging
import time
import uuid
from collections import Counter
from diff_match_patch import *
import os, sys
from lxml import html

# kind of a hacky approach to import coach functions
#sys.path.insert(0,os.path.dirname(__file__))
#from coach import get_lint

logger = logging.getLogger('web2py.app.runestone')
logger.setLevel(logging.DEBUG)

response.headers['Access-Control-Allow-Origin'] = '*'

def compareAndUpdateCookieData(sid):
    if request.cookies.has_key('ipuser') and request.cookies['ipuser'].value != sid:
        db.useinfo(db.useinfo.sid == request.cookies['ipuser'].value).update(sid=sid)

def hsblog():    # Human Subjects Board Log
    setCookie = False
    if auth.user:
        sid = auth.user.username
        compareAndUpdateCookieData(sid)
        setCookie = True    # we set our own cookie anyway to eliminate many of the extraneous anonymous
                            # log entries that come from auth timing out even but the user hasn't reloaded
                            # the page.
    else:
        if request.cookies.has_key('ipuser'):
            sid = request.cookies['ipuser'].value
            setCookie = True
        else:
            sid = str(uuid.uuid1().int)+"@"+request.client
            setCookie = True
    act = request.vars.act
    div_id = request.vars.div_id
    event = request.vars.event
    course = request.vars.course
    ts = datetime.datetime.now()
    tt = request.vars.time
    if not tt:
        tt = 0

    try:
        db.useinfo.insert(sid=sid,act=act,div_id=div_id,event=event,timestamp=ts,course_id=course)
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

    if event == 'mChoice' and auth.user:
        # has user already submitted a correct answer for this question?
        if db((db.mchoice_answers.sid == sid) &
              (db.mchoice_answers.div_id == div_id) &
              (db.mchoice_answers.correct == 'T')).count() == 0:
            answer = request.vars.answer
            correct = request.vars.correct
            db.mchoice_answers.insert(sid=sid,timestamp=ts, div_id=div_id, answer=answer, correct=correct, course_name=course)
    elif event == "fillb" and auth.user:
        # Has user already submitted a correct answer for this question? If not, insert a record
        if db((db.fitb_answers.sid == sid) & (db.fitb_answers.div_id == div_id) & (db.fitb_answers.correct == 'T')).count() == 0:
            answer = request.vars.answer
            correct = request.vars.correct
            db.fitb_answers.insert(sid=sid, timestamp=ts, div_id=div_id, answer=answer, correct=correct, course_name=course)

    elif event == "dragNdrop" and auth.user:
        if db((db.dragndrop_answers.sid == sid) & (db.dragndrop_answers.div_id == div_id) & (db.dragndrop_answers.correct == 'T')).count() == 0:
            answers = request.vars.answer
            minHeight = request.vars.minHeight
            correct = request.vars.correct

            db.dragndrop_answers.insert(sid=sid, timestamp=ts, div_id=div_id, answer=answers, correct=correct, course_name=course, minHeight=minHeight)
    elif event == "clickableArea" and auth.user:
        if db((db.clickablearea_answers.sid == sid) & (db.clickablearea_answers.div_id == div_id) & (db.clickablearea_answers.correct == 'T')).count() == 0:
            correct = request.vars.correct
            db.clickablearea_answers.insert(sid=sid, timestamp=ts, div_id=div_id, answer=act, correct=correct, course_name=course)

    elif event == "parsons" and auth.user:
        if db((db.parsons_answers.sid == sid) & (db.parsons_answers.div_id == div_id) & (db.parsons_answers.correct == 'T')).count() == 0:
            correct = request.vars.correct
            answer = request.vars.answer
            source = request.vars.source
            db.parsons_answers.insert(sid=sid, timestamp=ts, div_id=div_id, answer=answer, source=source, correct=correct, course_name=course)

    elif event == "codelensq" and auth.user:
        if db((db.codelens_answers.sid == sid) & (db.codelens_answers.div_id == div_id) & (db.codelens_answers.correct == 'T')).count() == 0:
            correct = request.vars.correct
            answer = request.vars.answer
            source = request.vars.source
            db.codelens_answers.insert(sid=sid, timestamp=ts, div_id=div_id, answer=answer, source=source, correct=correct, course_name=course)

    elif event == "shortanswer" and auth.user:
        # for shortanswers just keep the latest?? -- the history will be in useinfo
        db.shortanswer_answers.update_or_insert((db.shortanswer_answers.sid == sid) & (db.shortanswer_answers.div_id == div_id) & (db.shortanswer_answers.course_name == course),
            sid=sid, answer=act, div_id=div_id, timestamp=ts, course_name=course)

    response.headers['content-type'] = 'application/json'
    res = {'log':True}
    if setCookie:
        response.cookies['ipuser'] = sid
        response.cookies['ipuser']['expires'] = 24*3600*90
        response.cookies['ipuser']['path'] = '/'
    return json.dumps(res)

def runlog():    # Log errors and runs with code
    setCookie = False
    if auth.user:
        sid = auth.user.username
        setCookie = True
    else:
        if request.cookies.has_key('ipuser'):
            sid = request.cookies['ipuser'].value
            setCookie = True
        else:
            sid = str(uuid.uuid1().int)+"@"+request.client
            setCookie = True
    div_id = request.vars.div_id
    course = request.vars.course
    code = request.vars.code if request.vars.code else ""
    ts = datetime.datetime.now()
    error_info = request.vars.errinfo
    pre = request.vars.prefix if request.vars.prefix else ""
    post = request.vars.suffix if request.vars.suffix else ""
    if error_info != 'success':
        event = 'ac_error'
        act = error_info
    else:
        act = 'run'
        if request.vars.event:
            event = request.vars.event
        else:
            event = 'activecode'
    try:
        db.useinfo.insert(sid=sid, act=act, div_id=div_id, event=event, timestamp=ts, course_id=course)
    except Exception as e:
        logger.debug("probable Too Long problem trying to insert sid={} act={} div_id={} event={} timestamp={} course_id={}".format(sid, act, div_id, event, ts, course))

    dbid = db.acerror_log.insert(sid=sid,
                                 div_id=div_id,
                                 timestamp=ts,
                                 course_id=course,
                                 code=pre+code+post,
                                 emessage=error_info)
    #lintAfterSave(dbid, code, div_id, sid)
    if auth.user:
        if 'to_save' in request.vars and (request.vars.to_save == "True" or request.vars.to_save == "true"):
            db.code.insert(sid=sid,
                acid=div_id,
                code=code,
                emessage=error_info,
                timestamp=ts,
                course_id=auth.user.course_id,
                language=request.vars.lang)

    response.headers['content-type'] = 'application/json'
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
            logging.debug("Did not find anything to load for %s"%sid)
    response.headers['content-type'] = 'application/json'
    return json.dumps([res])

def getlastanswer():
    # get's user's last answer for multiple choice question
    logging.debug("Hello from getlastanswer")
    divid = request.vars.div_id
    if  auth.user:
        sid = auth.user.username
        query = ((db.useinfo.sid == sid) & (db.useinfo.div_id == divid))
        logging.debug("finding last answer for %s %s " % (sid,divid))
    else:
        query = None
        logging.debug("No User, No Query")

    res = {}
    if query:
        result = db(query)
        if not result.isempty():
            r = result.select(orderby=~db.useinfo.timestamp).first()
            res['divid'] = divid
            res['answer'] = r.act
            res['timestamp'] = r.timestamp.isoformat()
        else:
            logging.debug("No saved answers for %s %s" %(sid,divid))
    response.headers['content-type'] = 'application/json'
    return json.dumps(res)



@auth.requires_membership('instructor')
def savegrade():
    res = db(db.code.id == request.vars.id)
    if request.vars.grade:
        res.update(grade = float(request.vars.grade))
    else:
        res.update(comment = request.vars.comment)


#@auth.requires_login()
def getuser():
    response.headers['content-type'] = 'application/json'

    if  auth.user:
        res = {'email':auth.user.email,'nick':auth.user.username,'cohortId':auth.user.cohort_id}
    else:
        res = dict(redirect=auth.settings.login_url) #?_next=....
    logging.debug("returning login info: %s",res)
    return json.dumps([res])


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

#
#  Ajax Handlers to save / delete and restore user highlights
#
def savehighlight():
    parentClass = request.vars.parentClass
    hrange = request.vars.range
    method = request.vars.method
    page = request.vars.page
    pageSection = request.vars.pageSection
    course = request.vars.course

    if auth.user:
        insert_id = db.user_highlights.insert(created_on=datetime.datetime.now(),
                       user_id=auth.user.id,
                       course_id=course,
                       parent_class=parentClass,
                       range=hrange,
                       chapter_url=page,
                       sub_chapter_url=pageSection,
                       method = method)
        return str(insert_id)


def deletehighlight():
    uniqueId = request.vars.uniqueId

    if auth.user:
        try:
            db(db.user_highlights.id == uniqueId).update(is_active=0)
        except:
            logging.debug('uniqueId is not valid: {} user {}'.format(uniqueId, auth.user.username))
            return json.dumps({'success': False, 'message':'invalid id for highlighted text'})

        return json.dumps({"success":True})


def gethighlights():
    """
    return all the highlights for a given user, on a given page
    :Parameters:
        - `page`: the page to search the highlights on
        - `course`: the course to search the highlights in
    :Return:
        - json object containing a list of matching highlights
    """
    page = request.vars.page
    course = request.vars.course
    if auth.user:
        result = db((db.user_highlights.user_id == auth.user.id) &
                    (db.user_highlights.chapter_url == page) &
                    (db.user_highlights.course_id == course) &
                    (db.user_highlights.is_active == 1)).select()
        rowarray_list = []
        for row in result:
            res = {'range': row.range, 'uniqueId': row.id,
                   'parentClass': row.parent_class,
                   'pageSection': row.sub_chapter_url, 'method': row.method}
            rowarray_list.append(res)
        return json.dumps(rowarray_list)


#
#  Ajax Handlers to update and retreive the last position of the user in the course
#
def updatelastpage():
    lastPageUrl = request.vars.lastPageUrl
    lastPageScrollLocation = request.vars.lastPageScrollLocation
    if lastPageUrl is None:
        return   # todo:  log request.vars, request.args and request.env.path_info
    course = request.vars.course
    completionFlag = request.vars.completionFlag
    lastPageChapter = lastPageUrl.split("/")[-2]
    lastPageSubchapter = lastPageUrl.split("/")[-1].split(".")[0]
    if auth.user:
        db((db.user_state.user_id == auth.user.id) &
                 (db.user_state.course_id == course)).update(
                   last_page_url = lastPageUrl,
                   last_page_chapter = lastPageChapter,
                   last_page_subchapter = lastPageSubchapter,
                   last_page_scroll_location = lastPageScrollLocation,
                   last_page_accessed_on = datetime.datetime.now())
        db.commit()
        db((db.user_sub_chapter_progress.user_id == auth.user.id) &
           (db.user_sub_chapter_progress.chapter_id == lastPageChapter) &
           (db.user_sub_chapter_progress.sub_chapter_id == lastPageSubchapter)).update(
                   status = completionFlag,
                   end_date = datetime.datetime.now())
        db.commit()

def getCompletionStatus():
    if auth.user:
        lastPageUrl = request.vars.lastPageUrl
        lastPageChapter = lastPageUrl.split("/")[-2]
        lastPageSubchapter = lastPageUrl.split("/")[-1].split(".")[0]
        result = db((db.user_sub_chapter_progress.user_id == auth.user.id) &
                    (db.user_sub_chapter_progress.chapter_id == lastPageChapter) &
                    (db.user_sub_chapter_progress.sub_chapter_id == lastPageSubchapter)).select(db.user_sub_chapter_progress.status)
        rowarray_list = []
        if result:
            for row in result:
                res = {'completionStatus': row.status}
                rowarray_list.append(res)
                #question: since the javascript in user-highlights.js is going to look only at the first row, shouldn't we be returning just the *last* status? Or is there no history of status kept anyway?
            return json.dumps(rowarray_list)
        else:
            # haven't seen this Chapter/Subchapter before
            # make the insertions into the DB as necessary

            # we know the subchapter doesn't exist
            db.user_sub_chapter_progress.insert(user_id=auth.user.id,
                                                chapter_id = lastPageChapter,
                                                sub_chapter_id = lastPageSubchapter,
                                                status = -1)
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


def getCorrectStats(miscdata,event):
    sid = None
    if auth.user:
        sid = auth.user.username
    else:
        if request.cookies.has_key('ipuser'):
            sid = request.cookies['ipuser'].value

    if sid:
        course = db(db.courses.course_name == miscdata['course']).select().first()

        correctquery = '''select
(select cast(count(*) as float) from useinfo where sid='%s'
                                               and event='%s'
                                               and DATE(timestamp) >= DATE('%s')
                                               and position('correct' in act) > 0 )
/
(select cast(count(*) as float) from useinfo where sid='%s'
                                               and event='%s'
                                               and DATE(timestamp) >= DATE('%s')
) as result;
''' % (sid, event, course.term_start_date, sid, event, course.term_start_date)

        try:
            rows = db.executesql(correctquery)
            pctcorr = round(rows[0][0]*100)
        except:
            pctcorr = 'unavailable in sqlite'
    else:
        pctcorr = 'unavailable'

    miscdata['yourpct'] = pctcorr


def getStudentResults(question):
        course = db(db.courses.id == auth.user.course_id).select(db.courses.course_name).first()

        q = db( (db.useinfo.div_id == question) &
                (db.useinfo.course_id == course.course_name) &
                (db.courses.course_name == course.course_name) &
                (db.useinfo.timestamp >= db.courses.term_start_date) )

        res = q.select(db.useinfo.sid,db.useinfo.act,orderby=db.useinfo.sid)

        resultList = []
        if len(res) > 0:
            currentSid = res[0].sid
            currentAnswers = []

            for row in res:
                if ':' not in row.act:
                    continue  # skip this row
                answer = row.act.split(':')[1]

                if row.sid == currentSid:
                    currentAnswers.append(answer)
                else:
                    currentAnswers.sort()
                    resultList.append((currentSid, currentAnswers))
                    currentAnswers = [row.act.split(':')[1]]

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
        start_date = datetime.datetime.now() - datetime.timedelta(days=90)
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
        tdata[row.useinfo.act] = row[count]
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
                logging.debug("Bad data for %s data is %s " % (question,key))

    miscdata['correct'] = correct
    miscdata['course'] = course

    getCorrectStats(miscdata, 'mChoice')

    returnDict = dict(answerDict=rdata, misc=miscdata)

    if auth.user and is_instructor:  #auth.has_membership('instructor', auth.user.id):
        resultList = getStudentResults(question)
        returnDict['reslist'] = resultList

    return json.dumps([returnDict])


def getpollresults():
    course = request.vars.course
    div_id = request.vars.div_id

    response.headers['content-type'] = 'application/json'

    query = '''select act from useinfo
               where event = 'poll' and div_id = '%s' and course_id = '%s'
               ''' % (div_id, course)
    rows = db.executesql(query)

    result_list = []
    for row in rows:
        val = row[0].split(":")[0]
        result_list.append(int(val))

    # maps option : count
    opt_counts = Counter(result_list)

    # opt_list holds the option numbers from smallest to largest
    # count_list[i] holds the count of responses that chose option i
    opt_list = sorted(opt_counts.keys())
    count_list = []
    for i in opt_list:
        count_list.append(opt_counts[i])

    return json.dumps([len(result_list), opt_list, count_list, div_id])


def gettop10Answers():
    course = request.vars.course
    question = request.vars.div_id
    # select act, count(*) from useinfo where div_id = 'question4_2_1' group by act;
    response.headers['content-type'] = 'application/json'
    rows = []

    query = '''select act, count(*) from useinfo, courses where event = 'fillb' and div_id = '%s' and useinfo.course_id = '%s' and useinfo.course_id = courses.course_name and timestamp > courses.term_start_date  group by act order by count(*) desc limit 10''' % (question,course)
    try:
        rows = db.executesql(query)
        res = [{'answer':row[0][row[0].index(':')+1:row[0].rindex(':')],
                'count':row[1]} for row in rows ]
    except:
        res = 'error in query'

    miscdata = {'course': course}
    getCorrectStats(miscdata,'fillb')

    if auth.user and auth.has_membership('instructor',auth.user.id):
        resultList = getStudentResults(question)
        miscdata['reslist'] = resultList

    return json.dumps([res,miscdata])


def getSphinxBuildStatus():
    task_name = request.vars.task_name
    course_url = request.vars.course_url

    response.headers['content-type'] = 'application/json'
    results = {'course_url': course_url}
    row = scheduler.task_status(task_name)
    if row:
        if row['status'] in ['QUEUED', 'ASSIGNED','RUNNING', 'COMPLETED']:
            results['status'] = row['status']
        else:  # task failed
            results['status'] = row['status']
            tb = db(db.scheduler_run.task_id == row.id).select().first()['traceback']
            results['traceback']=tb
    else:
        results['status'] = 'failed'
        results['info'] = 'no row'
    return json.dumps(results)

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
    print a_q
    if not a_q:
        return json.dumps([ret])
    # try new way that we store scores and comments

    # divid is a question; find question_grades row
    result = db(
        (db.question_grades.sid == auth.user.username) &
        (db.question_grades.course_name == auth.user.course_name) &
        (db.question_grades.div_id == divid)
    ).select(db.question_grades.score, db.question_grades.comment).first()
    print result
    if result:
        # say that we're sending back result styles in new version, so they can be processed differently without affecting old way during transition.
        ret['version'] = 2
        ret['grade'] = result.score
        ret['max'] = a_q.assignment_questions.points
        if result.comment:
            ret['comment'] = result.comment

    else:
        # fall back on old way; eventually will deprecate this
        result = db(
            (db.code.sid == auth.user.username) &
            (db.code.acid == db.problems.acid) &
            (db.problems.assignment == db.assignments.id) &
            (db.assignments.released == True) &
            (db.code.acid == divid)
            ).select(
                db.code.grade,
                db.code.comment,
                orderby=~db.code.timestamp
            ).first()

        if result:
            ret['grade'] = result.grade
            if result.comment:
                ret['comment'] = result.comment

            query = '''select avg(grade), count(grade)
                       from code where acid='%s';''' % (divid)

            rows = db.executesql(query)
            ret['avg'] = rows[0][0]
            ret['count'] = rows[0][1]

    return json.dumps([ret])


def diff_prettyHtml(self, diffs):
    """Convert a diff array into a pretty HTML report.

    Args:
      diffs: Array of diff tuples.

    Returns:
      HTML representation.
    """
    html = []
    ct = 1
    for (op, data) in diffs:
        text = (data.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace("\n", "<br>"))
        if op == self.DIFF_INSERT:
            html.append("<ins style=\"background:#e6ffe6;\">%s</ins>" % text)
        elif op == self.DIFF_DELETE:
            html.append("<del style=\"background:#ffe6e6;\">%s</del>" % text)
        elif op == self.DIFF_EQUAL:
            html.append("<span>%s</span>" % text)
    return "".join(html)


def getCodeDiffs():
    if auth.user:
        sid = auth.user.username
    else:
        sid = request.vars['sid']

    divid = request.vars['divid']
    rows = []
    if sid and divid and auth.user:
        q = '''select timestamp, sid, div_id, code, emessage, id
               from acerror_log
               where sid = '%s' and course_id = '%s' and div_id='%s'
               order by timestamp
        ''' % (sid, auth.user.course_name, divid)
        rows = db.executesql(q)
    if len(rows) < 1:
        return json.dumps(dict(timestamps=[0], code=[''],
                               diffs=[''],
                               mess=['No Coaching hints yet.  You need to run the example at least once and be logged in and registered for a course'],
                               chints=['']))

    differ = diff_match_patch()
    ts = []
    newcode = []
    diffcode = []
    messages = []
    coachHints = []

#    diffs = differ.diff_lineMode(rows[0][3], rows[0][3], True)
#    diffcode.append(differ.diff_prettyHtml(diffs).replace('&para;', ''))
    newcode.append(rows[0][3])
    ts.append(str(rows[0][0]))
    coachHints.append(getCoachingHints(int(rows[0][5])))
    messages.append(rows[0][4].replace("success",""))

    for i in range(1,len(rows)):
        diffs = differ.diff_lineMode(rows[i-1][3], rows[i][3],True)
        ts.append(str(rows[i][0]))
        newcode.append(rows[i][3])
        diffcode.append(diff_prettyHtml(differ,diffs).replace('&para;', ''))
        messages.append(rows[i][4].replace("success", ""))
        coachHints.append(getCoachingHints(int(rows[i][5])))
    return json.dumps(dict(timestamps=ts,code=newcode,diffs=diffcode,mess=messages,chints=coachHints))


def getCoachingHints(ecId):
    catToTitle = {"C": "Coding Conventions", "R": "Good Practice", "W": "Minor Programming Issues",
                  "E": "Serious Programming Error", "F": "Fatal Errors"}

    rows = db.executesql("select category,symbol,line,msg from coach_hints where source=%d order by category, line" % ecId)
    res = ''
    catres = {'C':'', 'R':'', 'W':'', 'E':'', 'F':''}
    for k in catres:
        catres[k] = '<h2>%s</h2>' % catToTitle[k]
    for row in rows:
            cat = row[0]
            catres[cat] += "Line: %d %s %s <br>" % (row[2], row[1], row[3])

    for ch in "FEWRC":
        res += catres[ch]
    return res


def lintAfterSave(dbid, code, div_id, sid):
    #dbid = request.args.id
    #entry = db(db.acerror_log.id == dbid).select().first()
    pylint_stdout = get_lint(code, div_id, sid)

    for line in pylint_stdout:
        g = re.match(r"^([RCWEF]):\s(.*?):\s([RCWEF]\d+):\s+(\d+),(\d+):(.*?):\s(.*)$", line)
        if g:
            db.coach_hints.insert(category=g.group(1), symbol=g.group(2), msg_id=g.group(3),
                                  line=g.group(4), col=g.group(5), obj=g.group(6),
                                  msg=g.group(7).replace("'", ""), source=dbid)

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
        rows = db((db.fitb_answers.div_id == div_id) & (db.fitb_answers.course_name == course) & (db.fitb_answers.sid == sid)).select(db.fitb_answers.answer, db.fitb_answers.timestamp, db.fitb_answers.correct, orderby=~db.fitb_answers.timestamp).first()
        if not rows:
            return ""   # server doesn't have it so we load from local storage instead
        res = {'answer': rows.answer, 'timestamp': str(rows.timestamp), 'correct': rows.correct}
        return json.dumps(res)
    elif event == "mChoice":
        rows = db((db.mchoice_answers.div_id == div_id) & (db.mchoice_answers.course_name == course) & (db.mchoice_answers.sid == sid)).select(db.mchoice_answers.answer, db.mchoice_answers.timestamp, db.mchoice_answers.correct, orderby=~db.mchoice_answers.timestamp).first()
        if not rows:
            return ""
        res = {'answer': rows.answer, 'timestamp': str(rows.timestamp), 'correct': rows.correct}
        return json.dumps(res)
    elif event == "dragNdrop":
        rows = db((db.dragndrop_answers.div_id == div_id) & (db.dragndrop_answers.course_name == course) & (db.dragndrop_answers.sid == sid)).select(db.dragndrop_answers.answer, db.dragndrop_answers.timestamp, db.dragndrop_answers.correct, db.dragndrop_answers.minHeight, orderby=~db.dragndrop_answers.timestamp).first()
        if not rows:
            return ""
        res = {'answer': rows.answer, 'timestamp': str(rows.timestamp), 'correct': rows.correct, 'minHeight': str(rows.minHeight)}
        return json.dumps(res)
    elif event == "clickableArea":
        rows = db((db.clickablearea_answers.div_id == div_id) & (db.clickablearea_answers.course_name == course) & (db.clickablearea_answers.sid == sid)).select(db.clickablearea_answers.answer, db.clickablearea_answers.timestamp, db.clickablearea_answers.correct, orderby=~db.clickablearea_answers.timestamp).first()
        if not rows:
            return ""
        res = {'answer': rows.answer, 'timestamp': str(rows.timestamp), 'correct': rows.correct}
        return json.dumps(res)
    elif event == "timedExam":
        rows = db((db.timed_exam.reset == None) & (db.timed_exam.div_id == div_id) & (db.timed_exam.course_name == course) & (db.timed_exam.sid == sid)).select(db.timed_exam.correct, db.timed_exam.incorrect, db.timed_exam.skipped, db.timed_exam.time_taken, db.timed_exam.timestamp, db.timed_exam.reset, orderby=~db.timed_exam.timestamp).first()
        if not rows:
            return ""
        res = {'correct': rows.correct, 'incorrect': rows.incorrect, 'skipped': str(rows.skipped), 'timeTaken': str(rows.time_taken), 'timestamp': str(rows.timestamp), 'reset': str(rows.reset)}
        return json.dumps(res)
    elif event == "parsons":
        rows = db((db.parsons_answers.div_id == div_id) & (db.parsons_answers.course_name == course) & (db.parsons_answers.sid == sid)).select(db.parsons_answers.answer, db.parsons_answers.source, db.parsons_answers.timestamp, orderby=~db.parsons_answers.timestamp).first()
        if not rows:
            return ""
        res = {'answer': rows.answer, 'source': rows.source, 'timestamp': str(rows.timestamp)}
        return json.dumps(res)
    elif event == "shortanswer":
        row = db((db.shortanswer_answers.sid == sid) & (db.shortanswer_answers.div_id == div_id) & (db.shortanswer_answers.course_name == course)).select().first()
        if not row or len(row) == 0:
            return ""
        res = {'answer': row.answer, 'timestamp': str(row.timestamp)}
        return json.dumps(res)

def checkTimedReset():
    if auth.user:
        user = auth.user.username
    else:
        return json.dumps({"canReset":False})

    divId = request.vars.div_id
    course = request.vars.course
    rows = db((db.timed_exam.div_id == divId) & (db.timed_exam.sid == user) & (db.timed_exam.course_name == course)).select(orderby=~db.timed_exam.timestamp).first()

    if rows:        # If there was a scored exam
        if rows.reset == True:
            return json.dumps({"canReset":True})
        else:
            return json.dumps({"canReset":False})
    else:
        return json.dumps({"canReset":True})

def preview_question():
    code = json.loads(request.vars.code)
    print(code)
    with open("applications/runestone/build/preview/_sources/index.rst", "w") as ixf:
        ixf.write(code)

    res = os.system('applications/runestone/scripts/build_preview.sh')
    if res == 0:
        with open('applications/runestone/build/preview/build/preview/index.html','r') as ixf:
            src = ixf.read()
            tree = html.fromstring(src)
            component = tree.cssselect(".runestone")
            if len(component) > 0:
                ctext = html.tostring(component[0])
            else:
                component = tree.cssselect(".system-message")
                if len(component) > 0:
                    ctext = html.tostring(component[0])
                    print "error - ", ctext
                else:
                    ctext = "Unknown error occurred"

            return json.dumps(ctext)

    return json.dumps(res)
