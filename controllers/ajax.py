import json
import datetime
import logging
import time
from collections import Counter
from diff_match_patch import *
import os, sys
# kind of a hacky approach to import coach functions
sys.path.insert(0,os.path.dirname(__file__))
from coach import get_lint

logger = logging.getLogger("web2py.app.eds")
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
            sid = str(int(time.time()*1000))+"@"+request.client
            setCookie = True
    act = request.vars.act
    div_id = request.vars.div_id
    event = request.vars.event
    course = request.vars.course
    ts = datetime.datetime.now()

    db.useinfo.insert(sid=sid,act=act,div_id=div_id,event=event,timestamp=ts,course_id=course)
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
            sid = str(int(time.time()*1000))+"@"+request.client
            setCookie = True
    div_id = request.vars.div_id
    course = request.vars.course
    code = request.vars.code
    ts = datetime.datetime.now()
    error_info = request.vars.errinfo
    if error_info != 'success':
        event = 'ac_error'
        act = error_info
    else:
        act = 'run'
        event = 'activecode'
    dbid = db.acerror_log.insert(sid=sid,div_id=div_id,timestamp=ts,course_id=course,code=code,emessage=error_info)
    db.useinfo.insert(sid=sid,act=act,div_id=div_id,event=event,timestamp=ts,course_id=course)
    lintAfterSave(dbid, code, div_id, sid)
    response.headers['content-type'] = 'application/json'
    res = {'log':True}
    if setCookie:
        response.cookies['ipuser'] = sid
        response.cookies['ipuser']['expires'] = 24*3600*90
        response.cookies['ipuser']['path'] = '/'
    return json.dumps(res)


#
#  Ajax Handlers for saving and restoring active code blocks
#

def saveprog():
    user = auth.user
    if not user:
        return json.dumps(["ERROR: auth.user is not defined.  Copy your code to the clipboard and reload or logout/login"])
    course = db(db.courses.id == auth.user.course_id).select().first()

    acid = request.vars.acid
    code = request.vars.code

    now = datetime.datetime.now()

    response.headers['content-type'] = 'application/json'
    def strip_suffix(id):
        idx = id.rfind('-') - 1
        return id[:idx]
    assignment = db(db.assignments.id == db.problems.assignment)(db.problems.acid == acid).select(db.assignments.ALL).first()
    
    section_users = db((db.sections.id==db.section_users.section) & (db.auth_user.id==db.section_users.auth_user))
    section = section_users(db.auth_user.id == user.id).select(db.sections.ALL).first()
        
    if assignment:
        q = db(db.deadlines.assignment == assignment.id)
        if section:
            q = q((db.deadlines.section == section.id) | (db.deadlines.section==None))
        else:
            q = q(db.deadlines.section==None)
        dl = q.select(db.deadlines.ALL, orderby=db.deadlines.section).first()
        if dl:
            if dl.deadline < now:
                return json.dumps(["ERROR: Sorry. The deadline for this assignment has passed. The deadline was %s" % (dl.deadline)])
    try:
        db.code.insert(sid=auth.user.username,
            acid=acid,code=code,
            timestamp=datetime.datetime.now(),
            course_id=auth.user.course_id)
    except Exception as e:
        if not auth.user:
            return json.dumps(["ERROR: auth.user is not defined.  Copy your code to the clipboard and reload or logout/login"])
        else:
            return json.dumps(["ERROR: " + str(e) + "Please copy this error and use the Report a Problem link"])

    return json.dumps([acid])



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
        query = ((codetbl.sid == sid) & (codetbl.acid == acid))
    else:
        if auth.user:
            query = ((codetbl.sid == auth.user.username) & (codetbl.acid == acid))
        else:
            query = None

    res = {}
    if query:
        result = db(query)
        res['acid'] = acid
        if not result.isempty():
            r = result.select(orderby=~codetbl.timestamp).first().code
            res['source'] = r
            if sid:
                res['sid'] = sid
        else:
            logging.debug("Did not find anything to load for %s"%sid)
    response.headers['content-type'] = 'application/json'
    return json.dumps([res])


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

    if uniqueId:
        db(db.user_highlights.id == uniqueId).update(is_active = 0)
    else:
        print 'uniqueId is None'

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

        db((db.user_sub_chapter_progress.user_id == auth.user.id) &
           (db.user_sub_chapter_progress.chapter_id == lastPageChapter) &
           (db.user_sub_chapter_progress.sub_chapter_id == lastPageSubchapter)).update(
                   status = completionFlag,
                   end_date = datetime.datetime.now())

def getCompletionStatus():
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
        return json.dumps(rowarray_list)

def getAllCompletionStatus():
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
                    (db.user_state.last_page_chapter == db.chapters.chapter_label) &
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

    # Yes, these two things could be done as a join.  but this **may** be better for performance
    start_date = db(db.courses.course_name == course).select(db.courses.term_start_date).first().term_start_date
    count = db.useinfo.id.count()
    result = db((db.useinfo.div_id == question) &
                (db.useinfo.course_id == course) &
                (db.useinfo.timestamp >= start_date)
                ).select(db.useinfo.act, count, groupby=db.useinfo.act)

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
                print "Bad data for %s data is %s " % (question,key)

    miscdata['correct'] = correct
    miscdata['course'] = course

    getCorrectStats(miscdata, 'mChoice')

    returnDict = dict(answerDict=rdata, misc=miscdata)

    if auth.user and verifyInstructorStatus(course,auth.user.id):  #auth.has_membership('instructor', auth.user.id):
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

    courseid = course_url.replace('/'+request.application+'/static/','')
    courseid = courseid.replace('/index.html', '')
    confdir = os.path.join(os.getcwd(), 'applications', request.application, 'custom_courses', courseid, 'done')


    row = scheduler.task_status(task_name)

    if os.path.exists(confdir):
        os.remove(confdir)
        try:
            db(db.scheduler_run.task_id == row.id).update(status='COMPLETED')
            db(db.scheduler_task.id == row.id).update(status='COMPLETED')
        except:
            pass
        return dict(status='true', course_url=course_url)

    st = row['status']

    if st == 'COMPLETED':
        status = 'true'
        return dict(status=status, course_url=course_url)
    elif st == 'RUNNING' or st == 'QUEUED' or st == 'ASSIGNED':
        status = 'false'
        return dict(status=status, course_url=course_url)
    else:  # task failed
        status = 'failed'
        tb = db(db.scheduler_run.task_id == row.id).select().first()['traceback']
        return dict(status=status, traceback=tb)

def getassignmentgrade():
    response.headers['content-type'] = 'application/json'
    if not auth.user:
        return json.dumps([dict(message="not logged in")])

    divid = request.vars.div_id

    result = db(
        (db.code.sid == auth.user.username) &
        (db.code.acid == db.problems.acid) &
        (db.problems.assignment == db.assignments.id) &
        (db.assignments.released == True) &
        (db.code.acid == divid)
        ).select(
            db.code.grade,
            db.code.comment,
        ).first()

    ret = {
        'grade':"Not graded yet",
        'comment': "No Comments",
        'avg': 'None',
        'count': 'None',
    }
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
    q = '''select timestamp, sid, div_id, code, emessage, id
           from acerror_log 
           where sid = '%s' and course_id = '%s' and div_id='%s'
           order by timestamp
    ''' % (sid, auth.user.course_name, divid)

    rows = db.executesql(q)
    if len(rows) < 1:
        return json.dumps(dict(timestamps=[0], code=[''],
                               diffs=[''],
                               mess=['No Coaching hints yet.  You need to run the example at least once.'],
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

