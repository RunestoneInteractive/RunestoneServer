import json
import datetime
import logging
import time
from collections import Counter

logger = logging.getLogger("web2py.app.eds")
logger.setLevel(logging.DEBUG)

response.headers['Access-Control-Allow-Origin'] = '*'

def hsblog():    # Human Subjects Board Log
    setCookie = False
    if auth.user:
        sid = auth.user.username
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
    db.acerror_log.insert(sid=sid,div_id=div_id,timestamp=ts,course_id=course,code=code,emessage=error_info)
    db.useinfo.insert(sid=sid,act=act,div_id=div_id,event=event,timestamp=ts,course_id=course)
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
    acid = request.vars.acid
    code = request.vars.code

    response.headers['content-type'] = 'application/json'

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
    res.update(grade = int(request.vars.grade))


#@auth.requires_login()
def getuser():
    response.headers['content-type'] = 'application/json'

    if  auth.user:
        res = {'email':auth.user.email,'nick':auth.user.username}
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
    rows = db.executesql(query)

    res = {'numusers':rows[0][0]}
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

    print 'inserting new highlight'
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

    print 'deleting highlight'
    db(db.user_highlights.id == uniqueId).update(is_active = 0)


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

    result = db((db.user_highlights.user_id == auth.user.id) & (db.user_highlights.chapter_url == page) & (db.user_highlights.course_id == course) & (db.user_highlights.is_active == 1)).select()
    rowarray_list = []
    for row in result:
        res = {}
        res['range'] = row.range
        res['uniqueId'] = row.id
        res['parentClass'] = row.parent_class
        res['pageSection'] = row.sub_chapter_url
        res['method'] = row.method
        rowarray_list.append(res)
    return json.dumps(rowarray_list)


#
#  Ajax Handlers to update and retreive the last position of the user in the course
#
def updatelastpage():
    lastPageUrl = request.vars.lastPageUrl
    lastPageHash = request.vars.lastPageHash
    lastPageChapter = request.vars.lastPageChapter
    lastPageSubchapter = request.vars.lastPageSubchapter
    lastPageScrollLocation = request.vars.lastPageScrollLocation
    course = request.vars.course

    res = db((db.user_state.user_id == auth.user.id) & (db.user_state.course_id == course))
    res.update(last_page_url = lastPageUrl, last_page_hash = lastPageHash, last_page_chapter = lastPageChapter, last_page_subchapter = lastPageSubchapter, last_page_scroll_location = lastPageScrollLocation, last_page_accessed_on = datetime.datetime.now())


def getlastpage():
    course = request.vars.course

    result = db((db.user_state.user_id == auth.user.id) & (db.user_state.course_id == course)).select(db.user_state.last_page_url, db.user_state.last_page_hash, db.user_state.last_page_chapter, db.user_state.last_page_scroll_location, db.user_state.last_page_subchapter)
    rowarray_list = []
    if result:
        for row in result:
            res = {'lastPageUrl': row.last_page_url,
                   'lastPageHash': row.last_page_hash,
                   'lastPageChapter': row.last_page_chapter,
                   'lastPageSubchapter': row.last_page_subchapter,
                   'lastPageScrollLocation': row.last_page_scroll_location}
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


def verifyInstructorStatus(course, instructor):
    """
    Make sure that the instructor specified is actually an instructor for the
    given course.
    """
    if type(course) == str:
        course = db(db.courses.course_name == course).select(db.courses.id).first()

    return db((db.course_instructor.course == course) &
             (db.course_instructor.instructor == instructor)
            ).count() > 0


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

    count = db.useinfo.id.count()
    result = db((db.useinfo.div_id == question) &
                (db.useinfo.course_id == course) &
                (db.courses.course_name == course) &
                (db.useinfo.timestamp >= db.courses.term_start_date)
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
            answer = l[1]
            if 'correct' in key:
                correct = answer
            count = int(tdata[key])
            if answer in rdata:
                count += rdata[answer] / 100.0 * tot
            pct = round(count / tot * 100.0)

            if answer != "undefined" and answer != "":
                rdata[answer] = pct

    miscdata['correct'] = correct
    miscdata['course'] = course

    getCorrectStats(miscdata, 'mChoice')

    returnDict = dict(answerDict=rdata, misc=miscdata)

    if auth.user and auth.has_membership('instructor', auth.user.id):
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

    st = scheduler.task_status(task_name)['status']

    if st == 'COMPLETED':
        status = 'true'
        return dict(status=status, course_url=course_url)
    elif st == 'RUNNING' or st == 'QUEUED' or st == 'ASSIGNED':
        status = 'false'
        return dict(status=status, course_url=course_url)
    else: # task failed
        status = 'failed'
        return dict(status=status)

