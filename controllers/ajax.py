import json
import datetime
import logging
import time

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
    '''
    return the program code for a particular acid
    :Parameters:
        - `acid`: id of the active code block
        - `user`: optional identifier for the owner of the code
    :Return:
        - json object containing the source text
    '''
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
        if not result.isempty():
            res['acid'] = acid
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
    range = request.vars.range
    method = request.vars.method
    page = request.vars.page
    pageSection = request.vars.pageSection
    course = request.vars.course

    print 'inserting new highlight'
    insert_id = db.user_highlights.insert(created_on=datetime.datetime.now(),
                   user_id=auth.user.id,
                   course_id=course,
                   parent_class=parentClass,
                   range=range,
                   chapter_url=page,
                   sub_chapter_url=pageSection,
                   method = method)
    return str(insert_id)

def deletehighlight():
    uniqueId = request.vars.uniqueId

    print 'deleting highlight'
    db(db.user_highlights.id == uniqueId).update(is_active = 0)

def gethighlights():
    '''
    return all the highlights for a given user, on a given page 
    :Parameters:
        - `page`: the page to search the highlights on
        - `course`: the course to search the highlights in
    :Return:
        - json object containing a list of matching highlights
    '''
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
            res = {}
            res['lastPageUrl'] = row.last_page_url
            res['lastPageHash'] = row.last_page_hash
            res['lastPageChapter'] = row.last_page_chapter
            res['lastPageSubchapter'] = row.last_page_subchapter
            res['lastPageScrollLocation'] = row.last_page_scroll_location
            rowarray_list.append(res)
        return json.dumps(rowarray_list)
    else:
        db.user_state.insert(user_id=auth.user.id, course_id=course)