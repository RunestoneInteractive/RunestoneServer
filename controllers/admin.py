from os import path
import os
import shutil
import sys
from sphinx.application import Sphinx

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
    course = db(db.courses.id == auth.user.course_id).select().first()
    if sid:
        q = db((db.code.sid == sid)
             & (db.code.course_id == course.course_name)
             & (db.code.timestamp >= course.term_start_date))
    else:
        q = db((db.code.course_id == auth.user.course_id)
             & (db.code.timestamp >= course.term_start_date))
    
    rset = q.select(db.code.acid,orderby=db.code.acid,distinct=True)
    return dict(exercises=rset,course_id=course.course_name)

@auth.requires_membership('instructor')
def listassessments():
    course = db(db.courses.id == auth.user.course_id).select().first()

    query = '''select div_id,
                     (select count(*) from useinfo where div_id = oui.div_id
                     and course_id = '%(course_name)s'),
                     (select count(*) * 1.0 from useinfo where div_id = oui
                     .div_id  and course_id='%(course_name)s' and position(
                     'correct' in
                     act) > 0) /
                         (select count(*)
                          from useinfo
                          where div_id = oui.div_id and course_id = '%(course_name)s' ) as
                          pct
               from useinfo oui
               where event = 'mChoice'
                     and DATE(timestamp) >= DATE('%(start_date)s')
                     and course_id = '%(course_name)s' group by div_id order
                     by pct''' % dict(course_name=course.course_name, start_date=course.term_start_date)
    rset = db.executesql(query)
    return dict(solutions=rset)


@auth.requires_membership('instructor')
def assessdetail():
    course = db(db.courses.id == auth.user.course_id).select(db.courses.course_name).first()
    q = db( (db.useinfo.div_id == request.vars.id) & (db.useinfo.course_id == course.course_name) )
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
    course = db(db.courses.id == auth.user.course_id).select(db.courses.course_name).first()

    rset = db.executesql('''select acid, sid, grade, T.id, first_name, last_name from code as T, auth_user
        where sid = username and T.course_id = '%s' and  acid = '%s' and timestamp =
             (select max(timestamp) from code where sid=T.sid and acid=T.acid);''' %
             (auth.user.course_id,acid))
    return dict(solutions=rset,course_id=course.course_name)


@auth.requires_membership('instructor')
def showlog():
    course = db(db.courses.id == auth.user.course_id).select().first()
    grid = SQLFORM.grid(
        (db.useinfo.course_id==course.course_name) & (db.useinfo.timestamp >= course.term_start_date),
        fields=[db.useinfo.timestamp,db.useinfo.sid, db.useinfo.event,db.useinfo.act,db.useinfo.div_id],
        editable=False,
        deletable=False,
        details=False,
        orderby=~db.useinfo.timestamp,
        paginate=40,
        formstyle='divs')
    return dict(grid=grid,course_id=course.course_name)

@auth.requires_membership('instructor')
def studentactivity():
    course = db(db.courses.id == auth.user.course_id).select().first()
    count = db.useinfo.id.count()
    last = db.useinfo.timestamp.max()
    res = db((db.useinfo.course_id==course.course_name) & (db.useinfo.timestamp >= course.term_start_date))\
            .select(db.useinfo.sid,
                    count,
                    last,
                    groupby=db.useinfo.sid,
                    orderby=count)

    return dict(grid=res,course_id=course.course_name)
    
@auth.requires_membership('instructor')
def startdate():
    course = db(db.courses.id == auth.user.course_id).select().first()
    if request.vars.startdate:
        date = request.vars.startdate.split('/')
        date = datetime.date(int(date[2]), int(date[0]), int(date[1]))
        course.update_record(term_start_date=date)
        session.flash = "Course start date changed."
        redirect(URL('admin','index'))
    else:
        current_start_date = course.term_start_date.strftime("%m/%d/%Y")
        return dict(startdate=current_start_date)

@auth.requires_membership('instructor')
def rebuildcourse():
    if not request.vars.projectname:
        course = db(db.courses.course_name == auth.user.course_name).select().first()
        curr_start_date = course.term_start_date.strftime("%m/%d/%Y")
        return dict(curr_start_date=curr_start_date, confirm=True)
    else:
        # update the start date
        course = db(db.courses.id == auth.user.course_id).select().first()
        date = request.vars.startdate.split('/')
        date = datetime.date(int(date[2]), int(date[0]), int(date[1]))
        course.update_record(term_start_date=date)

        # sourcedir holds the all sources temporarily
        # confdir holds the files needed to rebuild the course
        workingdir = request.folder
        sourcedir = path.join(workingdir,request.vars.projectname)
        confdir = path.join(workingdir, 'custom_courses', request.vars.projectname)

        try:
            # copy all the sources into the temporary sourcedir
            shutil.copytree(path.join(workingdir,'source'),sourcedir)
        except OSError:
            # this is probably devcourse, thinkcspy, or other builtin course
            return dict(confirm=False, mess="You don't have permission to rebuild this course.", course_url='/'+request.application+'/static/'+request.vars.projectname+'/index.html')

        # copy the index and conf files to the sourcedir
        shutil.copy(path.join(confdir, 'conf.py'), path.join(sourcedir, 'conf.py'))
        shutil.copy(path.join(confdir, 'index.rst'), path.join(sourcedir, 'index.rst'))

        # run the Sphinx build
        coursename = request.vars.projectname
        confdir = sourcedir  # the Sphinx build actually gets the conf stuff from the temp sourcedir
        outdir = path.join(request.folder, 'static' , coursename)
        doctreedir = path.join(outdir,'doctrees')
        buildername = 'html'
        confoverrides = {}
        confoverrides['html_context.appname'] = request.application
        confoverrides['html_context.course_id'] = coursename
        confoverrides['html_context.loglevel'] = 10
        confoverrides['html_context.course_url'] = 'http://' + request.env.http_host
        if request.vars.loginreq == 'yes':
            confoverrides['html_context.login_required'] = 'true'
        else:
            confoverrides['html_context.login_required'] = 'false'
        status = sys.stdout
        warning = sys.stdout
        freshenv = True
        warningiserror = False
        tags = []

        sys.path.insert(0,path.join(request.folder,'modules'))
        app = Sphinx(sourcedir, confdir, outdir, doctreedir, buildername,
                    confoverrides, status, warning, freshenv,
                    warningiserror, tags)
        force_all = True
        filenames = []
        app.build(force_all, filenames)

        shutil.copy(path.join(outdir, '_static', 'jquery-1.10.2.min.js'),
                    path.join(outdir, '_static', 'jquery.js'))

        # clean up the temp source dir
        shutil.rmtree(sourcedir)

        return dict(mess='Your course has been rebuilt.',course_url='/'+request.application+'/static/'+coursename+'/index.html', confirm=False)

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



