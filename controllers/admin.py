# this is for admin links
# use auth.requires_membership('manager')
#
# create a simple index to provide a page of links
# - re build the book
# - list assignments
# - find assignments for a student
# - show totals for all students

# select acid, sid from code as T where timestamp = (select max(timestamp) from code where sid=T.sid and acid=T.acid);

@auth.requires_login()
def index():
    return dict()

@auth.requires_membership('instructor')
def listassignments():
    sid = request.vars.student
    course = db(db.courses.id == auth.user.course_id).select(db.courses.course_id).first()
    if sid:
        q = db(db.code.sid == sid & db.code.course_id == course.course_id)
    else:
        q = db(db.code.course_id == auth.user.course_id)
    
    rset = q.select(db.code.acid,orderby=db.code.acid,distinct=True)
    return dict(exercises=rset,course_id=course.course_id)

@auth.requires_membership('instructor')
def listassessments():
    course = db(db.courses.id == auth.user.course_id).select(db.courses.course_id).first()
    query = '''select div_id,
                     (select count(*) from useinfo where div_id = oui.div_id and course_id = '%s'),
                     count(*) * 1.0 /
                         (select count(*)
                          from useinfo
                          where div_id = oui.div_id and course_id = '%s' ) as pct
               from useinfo oui
               where event = 'mChoice' and act like '%%:correct'
                     and course_id = '%s' group by div_id order by pct;''' % (course.course_id,course.course_id,course.course_id)
    rset = db.executesql(query)
    return dict(solutions=rset)

@auth.requires_membership('instructor')
def assessdetail():
    course = db(db.courses.id == auth.user.course_id).select(db.courses.course_id).first()
    q = db( (db.useinfo.div_id == request.vars.id) & (db.useinfo.course_id == course.course_id) )
    res = q.select(db.useinfo.sid,db.useinfo.act,orderby=db.useinfo.sid)
    
    currentSid = res[0].sid
    currentAnswers = []
    answerDict = {}
    totalAnswers = 0
    resultList = []
    correct = ''
    for row in res:
        answer = row.act.split(':')[1]
        answerDict[answer] = answerDict.get(answer,0) + 1
        totalAnswers += 1
        
        if row.sid == currentSid:
            currentAnswers.append(answer)
            if row.act.split(':')[2] == 'correct':
                correct = answer
        else:
            currentAnswers.sort()
            resultList.append((currentSid,currentAnswers))
            currentAnswers = [row.act.split(':')[1]]
            
            currentSid = row.sid

    
    
    currentAnswers.sort()
    resultList.append((currentSid,currentAnswers))
    
    return dict(reslist=resultList, answerDict=answerDict, correct=correct)



@auth.requires_membership('instructor')
def gradeassignment():
    sid = request.vars.student
    acid = request.vars.id
    course = db(db.courses.id == auth.user.course_id).select(db.courses.course_id).first()
    if sid:
        q = db(db.code.sid == sid & db.code.course_id == course.course_id)
    else:
        q = db(db.code.course_id == auth.user.course_id)
    
    rset = db.executesql('''select acid, sid, grade, T.id, first_name, last_name from code as T, auth_user
        where sid = username and T.course_id = '%s' and  acid = '%s' and timestamp =
             (select max(timestamp) from code where sid=T.sid and acid=T.acid);''' %
             (auth.user.course_id,acid))
    return dict(solutions=rset,course_id=course.course_id)


@auth.requires_membership('instructor')
def showlog():
    course = db(db.courses.id == auth.user.course_id).select(db.courses.course_id).first()
    grid = SQLFORM.grid(db.useinfo.course_id==course.course_id,
        fields=[db.useinfo.timestamp,db.useinfo.sid, db.useinfo.event,db.useinfo.act,db.useinfo.div_id],
        editable=False,
        deletable=False,
        details=False,
        orderby=~db.useinfo.timestamp,
        paginate=40,
        formstyle='divs')
    return dict(grid=grid,course_id=course.course_id)

@auth.requires_membership('instructor')
def studentactivity():
    course = db(db.courses.id == auth.user.course_id).select(db.courses.course_id).first()
    count = db.useinfo.id.count()
    last = db.useinfo.timestamp.max()
    res = db(db.useinfo.course_id==course.course_id).select(
        db.useinfo.sid, count, last, groupby=db.useinfo.sid, orderby=count)

    return dict(grid=res,course_id=course.course_id)
    


#@auth.requires_membership('instructor')
def buildmodulelist():
    import os.path
    import re
    db.modules.truncate()
    
    def procrst(arg, dirname, names):
        rstfiles = [x for x in names if '.rst' in x]
        
        for rf in rstfiles:
            found = 0
            openrf = open(os.path.abspath(os.path.join(dirname,rf)))
            for line in openrf:
                if 'shortname::' in line:
                    first,shortname = line.split('::')
                    found += 1
                if 'description::' in line:
                    first,description = line.split('::')
                    found += 1
                if found > 1:
                    break
            if found > 1:
                dirs = dirname.split('/')
                db.modules.insert(shortname=shortname.strip(),
                                  description=description.strip(),
                                  pathtofile=os.path.join(dirs[-1],rf))


    
    
    os.path.walk(os.path.join(request.folder,'source'),procrst,None)
    
    session.flash = 'Module Database Rebuild Finished'
    redirect('/%s/admin'%request.application)



