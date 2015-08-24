from os import path
import os
import pygal
from datetime import date, timedelta
from paver.easy import sh


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
    row = db(db.courses.id == auth.user.course_id).select(db.courses.course_name, db.courses.base_course).first()
    # get current build info
    # read build info from application/custom_courses/course/build_info
    if row.course_name not in ['thinkcspy','pythonds','webfundamentals','apcsareview', 'pip2']:
        if not verifyInstructorStatus(auth.user.course_name, auth.user):
            session.flash = "You must be an instructor to access this page"
            redirect(URL(c="default"))
    cwd = os.getcwd()
    try:
        os.chdir(path.join('applications',request.application,'books',row.base_course))
        master_build = sh("git describe --long", capture=True)[:-1]
        with open('build_info','w') as bc:
            bc.write(master_build)
            bc.write("\n")
    except:
        master_build = ""
    finally:
        os.chdir(cwd)

    try:
        mbf_path = path.join('applications',request.application,'custom_courses',row.course_name,'build_info')
        mbf = open(mbf_path,'r')
        last_build = os.path.getmtime(mbf_path)
        my_build = mbf.read()[:-1]
        mbf.close()
    except:
        my_build = ""
        last_build = 0

    my_vers = 0
    mst_vers = 0
    rebuild_notice = path.join('applications',request.application,'REBUILD')
    if os.path.exists(rebuild_notice):
        rebuild_post = os.path.getmtime(rebuild_notice)
        if rebuild_post > last_build:
            response.flash = "Bug Fixes Available \n Rebuild is Recommended"
    elif master_build and my_build:
        mst_vers,mst_bld,mst_hsh = master_build.split('-')
        my_vers,my_bld,my_hsh = my_build.split('-')
        if my_vers != mst_vers:
            response.flash = "Updates available, consider rebuilding"

    # Now build the activity bar chart
    bar_chart = pygal.Bar(disable_xml_declaration=True, explicit_size=True,
                          show_legend=False, height=400, width=400,
                          style=pygal.style.TurquoiseStyle)
    bar_chart.title = 'Class Activities'
    bar_chart.x_labels = []
    counts = []

    d = date.today() - timedelta(days=10)
    query = '''select date(timestamp) xday, count(*)  ycount from useinfo where timestamp > '%s' and course_id = '%s' group by date(timestamp) order by xday''' % (d, row.course_name)
    rows = db.executesql(query)
    for row in rows:
        bar_chart.x_labels.append(str(row[0]))
        counts.append(row[1])

    bar_chart.add('Class', counts)
    chart = bar_chart.render()


    return dict(build_info=my_build, master_build=master_build, my_vers=my_vers,
                mst_vers=mst_vers, bchart=chart, course_name=auth.user.course_name)

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
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
    prefixes = {}
    for row in q.select(db.code.acid,orderby=db.code.acid,distinct=True):
        acid = row.acid
        acid_prefix = acid.split('_')[0]
        if acid_prefix not in prefixes.keys():
            prefixes[acid_prefix] = []
        prefixes[acid_prefix].append(acid)
    return dict(sections=prefixes,course_id=course.course_name)

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def listassessments():
    course = db(db.courses.id == auth.user.course_id).select().first()

    # get all the useinfos for this course
    results = db((db.useinfo.course_id == course.course_name) & (db.useinfo.timestamp > course.term_start_date) & (db.useinfo.event == 'mChoice')).select(orderby=db.useinfo.div_id)
    # by div_id, calculate percent correct and popularity of answers, taking only the first answer for each user
    divs = {}
    for row in results:
        if row.div_id not in divs:
            divs[row.div_id] = dict(sids = {}, answers = {}, correct = 0)
        thisdiv = divs[row.div_id]
        if row.sid not in thisdiv['sids']:
            thisdiv['sids'][row.sid] = True
            ignore, answer, grade = row.act.split(":")
            thisdiv['answers'][answer] = 1 + thisdiv['answers'].get(answer, 0)
            if grade == 'correct':
                thisdiv['correct'] +=1
    for div in divs.values():
        div['pct'] = int(100 * float(div['correct']) / len(div['sids']))
        counts = {}
        pop_answers = sorted(div['answers'].keys(), key = lambda k: div['answers'][k], reverse = True)
        try:
            div['first'] = (pop_answers[0], div['answers'][pop_answers[0]])
        except:
            div['first'] = ""
        try:
            div['second'] = (pop_answers[1], div['answers'][pop_answers[1]])
        except:
            div['second'] = ""
        try:
            div['third'] = (pop_answers[2], div['answers'][pop_answers[2]])
        except:
            div['third'] = ""

    # group and order by chapter;  using Brad's div_ids table
    results = db(db.div_ids.course_name == course.course_name).select()
    by_chapter = {}
    chapter_ordering = {}
    for row in results:
        if row.chapter not in by_chapter:
            by_chapter[row.chapter] = []
            chapter_ordering[row.chapter] = row.id
        if row.div_id in divs:
            div = divs[row.div_id]
            div['subchapter'] = row.subchapter
            div['ordering'] = row.id
            div['div_id'] = row.div_id   #stick div_id into the div for lookup in templated
            by_chapter[row.chapter].append(div)
    for L in by_chapter.values():
        L.sort(key = lambda div: div['ordering'], reverse = True)
    # a little hack: sort the chapters by their appearance in div_ids table, which is generated by going through all the divs in a chapter before moving on to next chapter
    chap_list = sorted(by_chapter.items(), key = lambda (chap, divs): chapter_ordering[chap])

    return dict(solutions=chap_list)

#@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
#def assessdetail():
#    course = db(db.courses.id == auth.user.course_id).select(db.courses.course_name).first()
#    q = db( (db.useinfo.div_id == request.vars.id) & (db.useinfo.course_id == course.course_name) )
#    res = q.select(db.useinfo.sid,db.useinfo.act,orderby=db.useinfo.sid)
#    
#    currentSid = res[0].sid
#    currentAnswers = []
#    answerDict = {}
#    totalAnswers = 0
#    resultList = []
#    correct = ''
#    for row in res:
#        answer = row.act.split(':')[1]
#        answerDict[answer] = answerDict.get(answer,0) + 1
#        totalAnswers += 1
#        
#        if row.sid == currentSid:
#            currentAnswers.append(answer)
#            if row.act.split(':')[2] == 'correct':
#                correct = answer
#        else:
#            currentAnswers.sort()
#            resultList.append((currentSid,currentAnswers))
#            currentAnswers = [row.act.split(':')[1]]
#            
#            currentSid = row.sid
#
#    
#    
#    currentAnswers.sort()
#    resultList.append((currentSid,currentAnswers))
#    
#    return dict(reslist=resultList, answerDict=answerDict, correct=correct)



@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def gradeassignment():
    sid = request.vars.student
    acid = request.vars.id
    course = db(db.courses.id == auth.user.course_id).select(db.courses.course_name).first()

    section_form=FORM(
        INPUT(_type="hidden", _name="id", _value=acid),
        _class="form-inline",
        _method="GET",
        )
    section_form.append(LABEL(
            INPUT(_name="section_id", _type="radio", _value=""),
            "All Students",
            _class="radio-inline",
            ))
    for section in db(db.sections.course_id == auth.user.course_id).select():
        section_form.append(LABEL(
            INPUT(_name="section_id", _type="radio", _value=section.id),
            section.name,
            _class="radio-inline",
            ))

    section_form.append(INPUT(_type="submit", _value="Filter Students", _class="btn btn-default"))

    joined = db((db.code.sid == db.auth_user.username) & (db.section_users.auth_user == db.auth_user.id))
    q = joined((db.code.course_id == auth.user.course_id) & (db.code.acid == acid))

    if section_form.accepts(request.vars, session, keepvalues=True) and section_form.vars.section_id != "":
        q = q(db.section_users.section == section_form.vars.section_id)

    rset = q.select(
        db.code.acid,
        db.code.sid,
        db.code.grade,
        db.code.id,
        db.code.language,
        db.auth_user.first_name,
        db.auth_user.last_name,
        db.code.comment,
        distinct = db.code.sid,
        orderby = db.code.sid|db.code.timestamp,
        )
    return dict(
        acid = acid,
        sid = sid,
        section_form = section_form,
        solutions=rset,
        course_id=course.course_name
        )


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
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

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
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
    
@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
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

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def rebuildcourse():
    if not request.vars.projectname or not request.vars.startdate:
        course = db(db.courses.course_name == auth.user.course_name).select().first()
        curr_start_date = course.term_start_date.strftime("%m/%d/%Y")
        return dict(curr_start_date=curr_start_date, confirm=True)
    else:
        # update the start date
        course = db(db.courses.id == auth.user.course_id).select().first()
        date = request.vars.startdate.split('/')
        date = datetime.date(int(date[2]), int(date[0]), int(date[1]))
        course.update_record(term_start_date=date)
        
        # run_sphinx in defined in models/scheduler.py
        row = scheduler.queue_task(run_sphinx, timeout=120, pvars=dict(folder=request.folder,
                                                                       rvars=request.vars,
                                                                       base_course=course.base_course,
                                                                       application=request.application,
                                                                       http_host=request.env.http_host))
        uuid = row['uuid']


        course_url=path.join('/',request.application,'static', request.vars.projectname, 'index.html')

        return dict(confirm=False,
                    task_name=uuid,
                    course_url=course_url)

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


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def sections_list():
    course = db(db.courses.id == auth.user.course_id).select().first()
    sections = db(db.sections.course_id == course.id).select()
    # get all sections - for course, list number of users in each section
    return dict(
        course = course,
        sections = sections
        )

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def sections_create():
    course = db(db.courses.id == auth.user.course_id).select().first()
    form = FORM(
        DIV(
            LABEL("Section Name", _for="section_name"),
            INPUT(_id="section_name" ,_name="name", requires=IS_NOT_EMPTY(),_class="form-control"),
            _class="form-group"
            ),
        INPUT(_type="Submit", _value="Create Section", _class="btn"),
        )
    if form.accepts(request,session):
        section = db.sections.update_or_insert(name=form.vars.name, course_id=course.id)
        session.flash = "Section Created"
        return redirect('/%s/admin/sections_create' % (request.application))
    return dict(
        form = form,
        )

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def sections_delete():
    course = db(db.courses.id == auth.user.course_id).select().first()
    section = db(db.sections.id == request.vars.id).select().first()
    if not section or section.course_id != course.id:
        return redirect(URL('admin','sections_list'))
    section.clear_users()
    session.flash = "Deleted Section: %s" % (section.name)
    db(db.sections.id == section.id).delete()
    return redirect(URL('admin','sections_list'))

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def sections_update():
    course = db(db.courses.id == auth.user.course_id).select().first()
    section = db(db.sections.id == request.vars.id).select().first()
    if not section or section.course_id != course.id:
        redirect(URL('admin','sections_list'))
    bulk_email_form = FORM(
        DIV(
            TEXTAREA(_name="emails_csv",
                requires=IS_NOT_EMPTY(),
                _class="form-control",
                ),
            _class="form-group",
            ),
        LABEL(
            INPUT(_name="overwrite", _type="Checkbox"),
            "Overwrite Users In Section",
            _class="checkbox",
            ),
        INPUT(_type='Submit', _class="btn", _value="Update Section"),
        )
    if bulk_email_form.accepts(request,session):
        if bulk_email_form.vars.overwrite:
            section.clear_users()
        users_added_count = 0
        for email_address in bulk_email_form.vars.emails_csv.split(','):
            user = db(db.auth_user.email == email_address.lower()).select().first()
            if user:
                if section.add_user(user):
                    users_added_count += 1
        session.flash = "%d Emails Added" % (users_added_count)
        return redirect('/%s/admin/sections_update?id=%d' % (request.application, section.id))
    elif bulk_email_form.errors:
        response.flash = "Error Processing Request"
    return dict(
        section = section,
        users = section.get_users(),
        bulk_email_form = bulk_email_form,
        )

def diffviewer():
    sid = ""
    div_id = request.vars.divid
    course_name = "thinkcspy"
    if auth.user:
        sid = auth.user.username
        course_name = auth.user.course_name
    return dict(course_id=course_name, sid=sid, divid=div_id)



@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def cohortprogress():
    course = db(db.courses.id == auth.user.course_id).select().first()
    cohort = db(db.cohort_master.course_name == course.course_name).select(db.cohort_master.cohort_name)
    cohort_plan = db( (db.cohort_plan.cohort_id == db.cohort_master.id) &
                      (db.cohort_plan.chapter_id == db.chapters.id)).select(db.cohort_master.cohort_name,
                                                                             db.chapters.chapter_name,
                                                                             db.cohort_plan.start_date,
                                                                             db.cohort_plan.end_date,
                                                                             db.cohort_plan.actual_end_date,
                                                                             db.cohort_plan.status,
                                                                             orderby=db.cohort_master.cohort_name|db.cohort_plan.start_date)

    return dict(grid=cohort_plan, course_id=course.course_name)


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def editcustom():
    course_name = auth.user.course_name
    custom_file = request.args[0]
    try:
        assignfile = open(path.join('applications', request.application,
                                'custom_courses', course_name, custom_file+'.rst'), 'r')
    except IOError as e:
        session.flash = "Sorry, " + custom_file + " does not exist for this course."
        redirect(URL('index'))

    form = FORM(TEXTAREA(_id='text', _name='text', value=assignfile.read()),
                INPUT(_type='submit', _value='submit'))

    assignfile.close()

    if form.process().accepted:
        session.flash = 'File Updated'
        assignfile = open(path.join('applications', request.application,
                                    'custom_courses', course_name, custom_file+'.rst'), 'w')
        assignfile.write(request.vars.text)
        assignfile.close()
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Assignments has errors'


    return dict(form=form,cfile=custom_file.capitalize())


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def chapterprogress():
    import numpy as np
    from matplotlib import use, colors
    use('Agg')
    import matplotlib.pyplot as plt
    from collections import OrderedDict

    subcquery = '''
    select chapter_label, sub_chapter_label, sub_chapter_name
    from chapters join sub_chapters on chapters.id = sub_chapters.chapter_id
    WHERE course_id = '{}' order by chapters.id
    '''.format(auth.user.course_name)

    subs = db.executesql(subcquery)

    idxdict = {}
    xlabs = []
    i = 0
    for row in subs:
        idxdict[row[0]+row[1]] = i
        xlabs.append(row[2])
        i += 1

    subs = None

    spquery = '''
    select username, chapter_id, sub_chapter_id, status, start_date, end_date
from user_sub_chapter_progress join auth_user on auth_user.id = user_sub_chapter_progress.user_id join courses on courses.course_name = auth_user.course_name
where auth_user.course_name = '{}' and sub_chapter_id in
    (select sub_chapter_label from chapters join sub_chapters on chapters.id = sub_chapters.chapter_id and course_id = 'webfundamentals' order by chapters.id)
order by username;
    '''.format(auth.user.course_name)

    spres = db.executesql(spquery)

    snames = OrderedDict()
    for row in spres:
            snames[row[0]] = None

    statmat = [[2 for j in range(len(idxdict))] for i in range(len(snames))]
    print len(idxdict), len(snames)
    rowix = -1
    prev = ""
    for row in spres:
        #        statmat[row][idxdict[i[1].subchap]] = i[1].status
        scidx = row[1]+row[2]
        if row[0] != prev:
            rowix += 1
        if row[3]< 0:
            status = 2
        else:
            status = row[3]
        statmat[rowix][idxdict[scidx]] = status
        prev = row[0]

    final = np.matrix(statmat)

    fig,ax = plt.subplots(figsize=(20,20))
    cmap = colors.ListedColormap(['orange', 'green', 'white'])

    #labels = [item.get_text() for item in ax.get_xticklabels()]
    labels = list(snames.keys())
    ax.set_yticks(list(range(len(snames))))
    ax.set_yticklabels(labels)

    ax.set_xticks(list(range(len(xlabs))))
    ax.set_xticklabels(xlabs)


    for i in ax.xaxis.get_major_ticks():
        i.label.set_rotation(90)
    ax.imshow(final,interpolation='nearest', cmap=cmap)
    saveName = path.join('applications',request.application,'static', auth.user.course_name,'_static','progress.png')
    fig.savefig(saveName)

    return dict(coursename=auth.user.course_name)