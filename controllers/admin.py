from os import path
import os
import pygal
from datetime import date, timedelta
from paver.easy import sh
import json
from runestone import cmap

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
    if not row:
        session.flash = "You must be registered for a course to access this page"
        redirect(URL(c="default"))

    if row.course_name not in ['thinkcspy','pythonds','webfundamentals','apcsareview', 'JavaReview', 'pip2', 'StudentCSP']:
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
             & (db.code.course_id == course.id)
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
        orderby = db.code.sid|~db.code.timestamp,
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
        row = scheduler.queue_task(run_sphinx, timeout=300, pvars=dict(folder=request.folder,
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
    from math import ceil
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
where auth_user.course_name = '{}' and auth_user.active = 'T' and sub_chapter_id in
    (select sub_chapter_label from chapters join sub_chapters on chapters.id = sub_chapters.chapter_id and course_id = '{}' order by chapters.id)
order by username;
    '''.format(auth.user.course_name, auth.user.course_name)

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
        if scidx in idxdict:
            statmat[rowix][idxdict[scidx]] = status
        prev = row[0]

    final = np.matrix(statmat)
    ht = int(ceil(len(snames)/4.0)+1)
    wt = int(ceil(len(xlabs)/4.0)+1)
    fig,ax = plt.subplots(figsize=(wt,ht))
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


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def assignments():
    sidQuery = db(db.courses.course_name == auth.user.course_name).select() #Querying to find the course_id
    courseid = sidQuery[0].id


    cur_assignments = db(db.assignments.course == auth.user.course_id).select()
    assigndict = {}
    for row in cur_assignments:
        assigndict[row.id] = row.name

    tags = []
    tag_query = db(db.tags).select()
    for tag in tag_query:
        tags.append(tag.tag_name)

    course_url = path.join('/',request.application, 'static', auth.user.course_name, 'index.html')

    print("ready")
    row = db(db.courses.id == auth.user.course_id).select(db.courses.course_name, db.courses.base_course).first()
    base_course = row.base_course
    chapter_labels = []
    chapters_query = db(db.chapters.course_id == base_course).select(db.chapters.chapter_label)
    for row in chapters_query:
        chapter_labels.append(row.chapter_label)
    return dict(coursename=auth.user.course_name,confirm=False,
                    course_url=course_url, assignments=assigndict, tags=tags, chapters=chapter_labels)


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def admin():
    sidQuery = db(db.courses.course_name == auth.user.course_name).select() #Querying to find the course_id
    courseid = sidQuery[0].id
    sectionsQuery = db(db.sections.course_id == courseid).select() #Querying to find all sections for that given course_id found above
    sectionsList = []
    for row in sectionsQuery:
        sectionsList.append(row.name)
    #Now get the start date
    dateQuery = db(db.courses.course_name == auth.user.course_name).select()
    date = dateQuery[0].term_start_date
    date = date.strftime("%m/%d/%Y")



    cur_instructors = db(db.course_instructor.course == auth.user.course_id).select(db.course_instructor.instructor)
    instructordict = {}
    for row in cur_instructors:
        name = db(db.auth_user.id == row.instructor).select(db.auth_user.first_name, db.auth_user.last_name)
        for person in name:
            instructordict[str(row.instructor)] = person.first_name + " " + person.last_name

    cur_students = db(db.user_courses.course_id == auth.user.course_id).select(db.user_courses.user_id)
    studentdict = {}
    for row in cur_students:
        person = db(db.auth_user.id == row.user_id).select(db.auth_user.username, db.auth_user.first_name, db.auth_user.last_name)
        for identity in person:
            name = identity.first_name + " " + identity.last_name
            if row.user_id not in instructordict:
                studentdict[row.user_id]= name

    #Not rebuilding
    if not request.vars.projectname or not request.vars.startdate:
        course = db(db.courses.course_name == auth.user.course_name).select().first()
        curr_start_date = course.term_start_date.strftime("%m/%d/%Y")
        return dict(sectionInfo=sectionsList,startDate=date,coursename=auth.user.course_name,instructors=instructordict, students=studentdict, curr_start_date=curr_start_date, confirm=True)

    #Rebuilding now
    else:
        # update the start date
        course = db(db.courses.id == auth.user.course_id).select().first()
        due = request.vars.startdate
        format_str = "%m/%d/%Y"
        date = datetime.datetime.strptime(due, format_str).date()
        course.update_record(term_start_date=date)

        # run_sphinx in defined in models/scheduler.py
        row = scheduler.queue_task(run_sphinx, timeout=180, pvars=dict(folder=request.folder,
                                                                       rvars=request.vars,
                                                                       base_course=course.base_course,
                                                                       application=request.application,
                                                                       http_host=request.env.http_host))
        uuid = row['uuid']


        course_url=path.join('/',request.application,'static', request.vars.projectname, 'index.html')


    return dict(sectionInfo=sectionsList, startDate=date.isoformat(), coursename=auth.user.course_name,
                instructors=instructordict, students=studentdict, confirm=False,
                task_name=uuid, course_url=course_url)

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def course_students():
    cur_students = db(
        (db.user_courses.course_id == auth.user.course_id) &
        (db.auth_user.id == db.user_courses.user_id)
    ).select(db.auth_user.username, db.auth_user.first_name,db.auth_user.last_name)
    searchdict = {}
    for row in cur_students:
        name = row.first_name + " " + row.last_name
        username = row.username
        searchdict[str(username)] = name
    return json.dumps(searchdict)

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def grading():

    assignments = {}
    assignments_query = db(db.assignments.course == auth.user.course_id).select()
    summative_qid = db(db.assignment_types.name == 'summative').select(db.assignment_types.id).first().id

    assignmentids = {}

    for row in assignments_query:
        assignmentids[row.name] = int(row.id)
        assignment_questions = db((db.assignment_questions.assignment_id == int(row.id)) & (db.assignment_questions.assessment_type == summative_qid)).select()
        questions = []
        for q in assignment_questions:
            question_name = db(db.questions.id == q.question_id).select(db.questions.name).first().name
            questions.append(question_name)
        assignments[row.name] = questions

    cur_students = db(db.user_courses.course_id == auth.user.course_id).select(db.user_courses.user_id)
    searchdict = {}
    for row in cur_students:
        isinstructor = db((db.course_instructor.course == auth.user.course_id) & (db.course_instructor.instructor == row.user_id)).select()
        instructorlist = []
        for line in isinstructor:
            instructorlist.append(line.instructor)
        if row.user_id not in instructorlist:
            person = db(db.auth_user.id == row.user_id).select(db.auth_user.username, db.auth_user.first_name,
                                                               db.auth_user.last_name)
            for identity in person:
                name = identity.first_name + " " + identity.last_name
                username = db(db.auth_user.id == int(row.user_id)).select(db.auth_user.username).first().username
                searchdict[str(username)] = name


    row = db(db.courses.id == auth.user.course_id).select(db.courses.course_name, db.courses.base_course).first()
    base_course = row.base_course
    chapter_labels = {}
    chapters_query = db(db.chapters.course_id == base_course).select()
    for row in chapters_query:
        q_list = []
        chapter_questions = db((db.questions.chapter == row.chapter_label) & (db.questions.base_course == base_course) & (db.questions.question_type == 'question')).select()
        for chapter_q in chapter_questions:
            q_list.append(chapter_q.name)
        chapter_labels[row.chapter_label] = q_list
    return dict(assignmentinfo=assignments, students=searchdict, chapters=chapter_labels, gradingUrl = URL('assignments', 'get_problem'), autogradingUrl = URL('assignments', 'autograde'),gradeRecordingUrl = URL('assignments', 'record_grade'), calcTotalsURL = URL('assignments', 'calculate_totals'), setTotalURL=URL('assignments', 'record_assignment_score'), getCourseStudentsURL = URL('admin', 'course_students'), course_id = auth.user.course_name, assignmentids = assignmentids
)

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def getChangeLog():
    bookQuery = db(db.courses.course_name == auth.user.course_name).select()
    base_course = bookQuery[0].base_course
    #The stuff below looks messy but it's necessary because the ChangeLog.rst will not be located in the same directory as this Python file
    #so we have to move up to find the correct log file
    try:
        file = open(os.path.join(os.path.split(os.path.dirname(__file__))[0], 'books/' + base_course + '/ChangeLog.rst'))
        logFile = file.read()
        return str(logFile)
    except:
        return "No ChangeLog for this book\n\n\n"

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def backup():
    #Begin the process of zipping up a backup file
    #This function will put the backup book in runestone/static/bookname/backup.zip
    import zipfile
    bookQuery = db(db.courses.course_name == auth.user.course_name).select()
    base_course = bookQuery[0].base_course
    toBeZippedPath = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'static/' + base_course + '/backup')
    tobeZippedDirectory = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'books/'+base_course)

    zip = zipfile.ZipFile("%s.zip" % (toBeZippedPath), "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(tobeZippedDirectory)
    for dirname, subdirs, files in os.walk(tobeZippedDirectory):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            zip.write(absname, arcname)
    zip.close()
    directoryPath = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'static/' + base_course + '/backup.zip')
    return response.stream(directoryPath, attachment=True)




@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def removeinstructor():
    removed = []
    if request.args[0] != str(auth.user.id):
        db((db.course_instructor.instructor == request.args[0]) & (db.course_instructor.course == auth.user.course_id)).delete()
        removed.append(True)
        return json.dumps(removed)
    else:
        session.flash = T("You cannot remove yourself as an instructor.")
        removed.append(False)
        return json.dumps(removed)

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def addinstructor():
    db.executesql('''
        INSERT INTO course_instructor(course, instructor)
        SELECT %s, %s
        ''' % (auth.user.course_id, request.args[0]))


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def deletecourse():
    course_name = auth.user.course_name
    cset = db(db.courses.course_name == course_name)
    if not cset.isempty():
        courseid = cset.select(db.courses.id).first()
        qset = db((db.course_instructor.course == courseid) & (db.course_instructor.instructor == auth.user.id))
        if not qset.isempty():
            qset.delete()
            students = db(db.auth_user.course_id == courseid)
            students.update(course_id=1)
            uset=db(db.user_courses.course_id == courseid.id)
            uset.delete()
            db(db.courses.id == courseid).delete()
            try:
                shutil.rmtree(path.join('applications', request.application, 'static', course_name))
                shutil.rmtree(path.join('applications', request.application, 'custom_courses', course_name))
                session.clear()
            except:
                response.flash = 'Error, %s does not appear to exist' % course_name
        else:
            response.flash = 'You are not the instructor of %s' % course_name
    else:
        response.flash = 'course, %s, not found' % course_name

    redirect(URL('default','index'))


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def removeassign():
    db(db.assignments.id == request.args[0]).delete()

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def createAssignment():
    try:
        d_str = request.vars['due']
        format_str = "%Y/%m/%d %H:%M"
        due = datetime.datetime.strptime(d_str, format_str)
        print(due)
        newassignID = db.assignments.insert(course=auth.user.course_id, name=request.vars['name'], duedate=due, description=request.vars['description'])
        returndict = {request.vars['name']: newassignID}
        return json.dumps(returndict)

    except Exception as ex:
        print(ex)
        return json.dumps('ERROR')


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def assignmentInfo():
    assignment_id = request.vars['assignmentid']
    assignment_points = db(db.assignments.id == assignment_id).select(db.assignments.points).first().points
    assignment_questions = db(db.assignment_questions.assignment_id == assignment_id).select()
    allquestion_info = {}
    allquestion_info['assignment_points'] = assignment_points
    date = db(db.assignments.id == assignment_id).select(db.assignments.duedate).first().duedate
    try:
        due = date.strftime("%Y/%m/%d %H:%M")
    except Exception as ex:
        print(ex)
        due = 'No due date set for this assignment'
    allquestion_info['due_date'] = due
    description = db(db.assignments.id == assignment_id).select(db.assignments.description).first().description
    if description == None:
        allquestion_info['description'] = 'No description available for this assignment'
    else:
        allquestion_info['description'] = description


    try:
        for row in assignment_questions:
            timed = row.timed
            try:
                question_points = int(row.points)
            except:
                question_points = 0
            question_info_query = db(db.questions.id == int(row.question_id)).select()
            for row in question_info_query:
                question_dict = {}
                #question_dict['base course'] = row.base_course
                #question_dict['chapter'] = row.chapter
                #question_dict['author'] = row.author
                #question_dict['difficulty'] = int(row.difficulty)
                #question_dict['question'] = row.question
                question_id = int(row.id)
                question_dict['name'] = row.name
                question_dict['timed'] = timed
                question_dict['points'] = question_points
                type_id = db((db.assignment_questions.question_id == question_id) & (db.assignment_questions.assignment_id == assignment_id)).select(db.assignment_questions.assessment_type).first().assessment_type
                type = db(db.assignment_types.id == type_id).select(db.assignment_types.name).first().name
                question_dict['type'] = type
                allquestion_info[int(row.id)] = question_dict
    except Exception as ex:
        print(ex)

    return json.dumps(allquestion_info)

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def getQuestions():
    assignment_id = request.vars['assignmentid']
    assignment_questions = db(db.assignment_questions.assignment_id == assignment_id).select()
    questions = []
    for row in assignment_questions:
        question_info_query = db(db.questions.id == int(row.question_id)).select()
        for q in question_info_query:
            questions.append(q.name)
    return json.dumps(questions)



@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def removeQuestion():
    question_name = request.vars['name']
    assignment_id = request.vars['assignment_id']
    question_id = db(db.questions.name == question_name).select(db.questions.id).first().id
    question_points = db((db.assignment_questions.assignment_id == int(assignment_id)) & (db.assignment_questions.question_id == int(question_id))).select(db.assignment_questions.points).first().points

    assignment = db(db.assignments.id == int(assignment_id)).select().first()
    assignment_points = db(db.assignments.id == int(assignment_id)).select(db.assignments.points).first().points
    new_points = int(assignment_points) - int(question_points)
    assignment.update_record(points=new_points)
    db((db.assignment_questions.assignment_id == int(assignment_id)) & (db.assignment_questions.question_id == int(question_id))).delete()
    return json.dumps(new_points)

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def questionBank():
    row = db(db.courses.id == auth.user.course_id).select(db.courses.course_name, db.courses.base_course).first()
    base_course = row.base_course

    tags = False
    if request.vars['tags'] != "null":
        tags = True
    term = False
    if request.vars['term'] != "":
        term = True
    chapterQ = None
    if request.vars['chapter'] != "":
        chapter_label = db(db.chapters.chapter_label == request.vars['chapter']).select(db.chapters.chapter_label).first().chapter_label
        chapterQ =  db.questions.chapter == chapter_label
    difficulty = False
    if request.vars['difficulty'] != "null":
        difficulty = True
    authorQ = None
    if request.vars['author'] != "":
        authorQ = db.questions.author == request.vars['author']
    rows = []
    questions = []

    base_courseQ = db.questions.base_course == base_course
    try:

        if chapterQ != None and authorQ != None:

            questions_query = db(chapterQ & authorQ & base_courseQ).select()

        elif chapterQ == None and authorQ != None:

            questions_query = db(authorQ & base_courseQ).select()

        elif chapterQ != None and authorQ == None:

            questions_query = db(chapterQ & base_courseQ).select()

        else:

            questions_query = db(base_courseQ).select()

        for question in questions_query: #Initially add all questions that we can to the list, and then remove the rows that don't match search criteria
            rows.append(question)
        for row in questions_query:
            removed_row = False
            if term:
                if request.vars['term'] not in row.name and request.vars['term'] not in row.question:
                    try:
                        rows.remove(row)
                        removed_row = True
                    except Exception as err:
                        ex = err

            if removed_row == False:
                if difficulty:
                    if int(request.vars['difficulty']) != row.difficulty:
                        try:
                            rows.remove(row)
                            removed_row = True
                        except Exception as err:
                            ex = err

            if removed_row == False:
                if tags:
                    tags_query = db(db.question_tags.question_id == row.id).select()
                    tag_list = []
                    for q_tag in tags_query:
                        tag_names = db(db.tags.id == q_tag.tag_id).select()
                        for tag_name in tag_names:
                            tag_list.append(tag_name.tag_name)
                    needsRemoved = False
                    for search_tag in request.vars['tags'].split(','):
                        if search_tag not in tag_list:
                            needsRemoved = True
                    if needsRemoved:
                        try:
                            rows.remove(row)
                        except Exception as err:
                            print(err)
        for q_row in rows:
            questions.append(q_row.name)

    except Exception as ex:
        print(ex)
        return 'Error'
    return json.dumps(questions)



@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def addToAssignment():
    assignment_id = int(request.vars['assignment'])
    question_name = request.vars['question']
    qtype = request.vars['type']
    question_id = db((db.questions.name == question_name)).select(db.questions.id).first().id

    timed = request.vars['timed']
    try:
        points = int(request.vars['points'])
    except:
        points = 0

    try:
        type_id = db(db.assignment_types.name == qtype).select(db.assignment_types.id).first().id
    except Exception as ex:
        print(ex)

    try:
        db.assignment_questions.insert(assignment_id=assignment_id, question_id=question_id, points=points, timed=timed, assessment_type=type_id)
        assignment = db(db.assignments.id == assignment_id).select().first()
        assignment_points = db(db.assignments.id == assignment_id).select(db.assignments.points).first().points
        if assignment_points == None:
            new_points = points
        else:
            new_points = int(assignment_points) + points

        assignment.update_record(points=new_points)
        return json.dumps([new_points,qtype])
    except Exception as ex:
        print(ex)



@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def getQuestionInfo():
    assignment_id = int(request.vars['assignment'])
    question_name = request.vars['question']
    try:
        question_code = db((db.questions.name == question_name)).select(db.questions.question).first().question
        question_author = db((db.questions.name == question_name)).select(db.questions.author).first().author
        question_difficulty = db((db.questions.name == question_name)).select(db.questions.difficulty).first().difficulty
        question_id = db((db.questions.name == question_name)).select(db.questions.id).first().id
        tags = []
        question_tags = db((db.question_tags.question_id == question_id)).select()
        for row in question_tags:
            tag_id = row.tag_id
            tag_name = db((db.tags.id == tag_id)).select(db.tags.tag_name).first().tag_name
            tags.append(" " + str(tag_name))
        if question_difficulty != None:
            returnDict = {'code':question_code, 'author':question_author, 'difficulty':int(question_difficulty), 'tags': tags}
        else:
            returnDict = {'code':question_code, 'author':question_author, 'difficulty':None, 'tags': tags}

        return json.dumps(returnDict)

    except Exception as ex:
        print(ex)



@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def edit_question():
    vars = request.vars
    old_qname = vars['question']
    new_qname = vars['name']
    try:
        difficulty = int(vars['difficulty'])
    except:
        difficulty = 0
    tags = vars['tags']
    old_question = db(db.questions.name == old_qname).select().first()
    author = auth.user.first_name + " " + auth.user.last_name
    base_course = old_question.base_course
    timestamp = datetime.datetime.now()
    chapter = old_question.chapter
    question_type = old_question.question_type
    subchapter = old_question.subchapter

    question = vars['questiontext']

    try:
        if new_qname != "" and new_qname != old_qname:
            new_qid = db.questions.insert(difficulty=difficulty, question=question, name=new_qname, author=author, base_course=base_course, timestamp=timestamp,
            chapter=chapter, subchapter=subchapter, question_type=question_type)
            if tags != 'null':
                tags = tags.split(',')
                for tag in tags:
                    tag_id = db(db.tags.tag_name == tag).select(db.tags.id).first().id
                    db.question_tags.insert(question_id = new_qid, tag_id=tag_id)
            return "Success"

    except Exception as ex:
        print(ex)


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def question_text():
    qname = request.vars['question_name']
    q_text = db(db.questions.name == qname).select(db.questions.question).first().question
    return q_text


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def searchstudents():
    if request.args[0] == "_":
        #seperate the students from instructors in a hopefully more efficient way
        cur_students = db(db.user_courses.course_id == auth.user.course_id).select(db.user_courses.user_id)
        searchdict = {}
        for row in cur_students:
            isinstructor = db((db.course_instructor.course == auth.user.course_id) & (db.course_instructor.instructor == row.user_id)).select()
            instructorlist = []
            for line in isinstructor:
                instructorlist.append(line.instructor)
            if row.user_id not in instructorlist:
                person = db(db.auth_user.id == row.user_id).select(db.auth_user.username, db.auth_user.first_name,
                                                               db.auth_user.last_name)
                for identity in person:
                    name = identity.first_name + " " + identity.last_name
                    searchdict[row.user_id] = name

    else:
        cur_students = db(db.user_courses.course_id == auth.user.course_id).select(db.user_courses.user_id)
        searchdict = {}
        for row in cur_students:
            isinstructor = db((db.course_instructor.course == auth.user.course_id) & (
            db.course_instructor.instructor == row.user_id)).select()
            instructorlist = []
            for line in isinstructor:
                instructorlist.append(line.instructor)
            if row.user_id not in instructorlist:
                person = db(db.auth_user.id == row.user_id).select(db.auth_user.username, db.auth_user.first_name, db.auth_user.last_name)
                for identity in person:
                    if request.args[0] in identity.first_name or request.args[0] in identity.last_name:
                        name = identity.first_name + " " + identity.last_name
                        searchdict[row.user_id] = name

    return json.dumps(searchdict)


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def gettemplate():
    template = request.args[0]
    returndict = {}
    base = ''

    returndict['template'] = base + cmap.get(template,'').__doc__

    chapters = []
    chaptersrow = db(db.chapters.course_id == auth.user.course_name).select(db.chapters.chapter_name)
    for row in chaptersrow:
        chapters.append(row['chapter_name'])
    print(chapters)
    returndict['chapters'] = chapters

    return json.dumps(returndict)


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def createquestion():
    row = db(db.courses.id == auth.user.course_id).select(db.courses.course_name, db.courses.base_course).first()
    base_course = row.base_course
    tab = request.vars['tab']
    typeid = db(db.assignment_types.name == tab).select(db.assignment_types.id).first().id
    assignmentid = int(request.vars['assignmentid'])
    points = int(request.vars['points'])
    timed = request.vars['timed']

    try:
        newqID = db.questions.insert(base_course=base_course, name=request.vars['name'], chapter=request.vars['chapter'],
                 author=auth.user.first_name + " " + auth.user.last_name, difficulty=request.vars['difficulty'],
                 question=request.vars['question'], timestamp=datetime.datetime.now(), question_type=request.vars['template'], is_private=request.vars['isprivate'])

        assignment_question = db.assignment_questions.insert(assignment_id=assignmentid, question_id=newqID, timed=timed, points=points, assessment_type=typeid)

        returndict = {request.vars['name']: newqID, 'timed':timed, 'points': points}

        return json.dumps(returndict)
    except Exception as ex:
        print(ex)
        return json.dumps('ERROR')

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def questions2rst():
    assignmentId = request.args[0]

    custom_dir = os.path.join('applications', request.application, 'custom_courses', auth.user.course_name)
    assignment_folder = os.path.join(custom_dir,'assignments')
    if not os.path.exists(assignment_folder):
        os.mkdir(assignment_folder)

    assignment_file = os.path.join(assignment_folder,'assignment_{}.rst'.format(assignmentId))

    questions = db(db.assignment_questions.assignment_id == assignmentId).select(db.assignment_questions.id,db.questions.question, join=db.questions.on(db.assignment_questions.question_id == db.questions.id) )

    assignment = db(db.assignments.id == assignmentId).select().first()
    points = assignment.points if assignment.points else 0
    due = assignment.duedate if assignment.duedate else "None given"
    description = assignment.description if assignment.description else "No Description"

    with open(assignment_file,'w') as af:
        af.write(assignment.name+'\n')
        af.write("="*len(assignment.name)+'\n\n')
        af.write("**Points**: {}\n\n".format(points))
        af.write("**Due**: {}\n\n".format(due))
        af.write(description+"\n\n")
        for q in questions:
            af.write(q.questions.question)
            af.write("\n\n")

    assign_list = db(db.assignments.course == auth.user.course_id).select(orderby=db.assignments.duedate)

    with open(os.path.join(custom_dir,'assignments.rst'),'w') as af:
        af.write("Assignments\n===========\n\n")
        af.write(".. toctree::\n\n")
        for a in assign_list:
            af.write("   assignments/assignment_{}.rst\n".format(a.id))




@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def htmlsrc():
    acid = request.vars['acid']
    htmlsrc = db(
        (db.questions.name == acid) &
        (db.questions.base_course == db.courses.base_course) &
        (db.courses.course_name == auth.user.course_name)
         ).select(db.questions.htmlsrc).first().htmlsrc
    return json.dumps(htmlsrc)


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def changeDate():
    try:
        newdate = request.vars['newdate']
        format_str = "%Y/%m/%d %H:%M"
        due = datetime.datetime.strptime(newdate, format_str)
        assignmentid = int(request.vars['assignmentid'])
        assignment = db(db.assignments.id == assignmentid).select().first()
        assignment.update_record(duedate=due)
        return 'success'
    except:
        return 'error'


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def changeDescription():
    try:
        newdescription = request.vars['newdescription']
        assignmentid = int(request.vars['assignmentid'])
        assignment = db(db.assignments.id == assignmentid).select().first()
        assignment.update_record(description=newdescription)
        return 'success'
    except:
        return 'error'


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def getStudentCode():
    try:
        acid = request.vars['acid']
        sid = request.vars['sid']
        c = db((db.code.acid == acid) & (db.code.sid == sid)).select(orderby = db.code.id).last()
        return json.dumps(c.code)
    except Exception as ex:
        print(ex)


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def getGradeComments():

    acid = request.vars['acid']
    sid = request.vars['sid']

    c =  db((db.question_grades.sid == sid) \
             & (db.question_grades.div_id == acid) \
             & (db.question_grades.course_name == auth.user.course_name)\
            ).select().first()
    if c != None:
        return json.dumps({'grade':c.score, 'comments':c.comment})
    else:
        return json.dumps("Error")



@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def coursename():
    row = db(db.courses.id == auth.user.course_id).select(db.courses.course_name, db.courses.base_course).first()
    return json.dumps(row.course_name)


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def indexrst():
    try:
        row = db(db.courses.id == auth.user.course_id).select(db.courses.course_name, db.courses.base_course).first()
        course_name = row.course_name
        file = open(os.path.join(os.path.split(os.path.dirname(__file__))[0], 'custom_courses/' + course_name + '/index.rst'))
        filetxt = file.read()
    except Exception as ex:
        print(ex)
        filetxt = "Sorry, no index.rst file could be found"
    return json.dumps(filetxt)

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def editindexrst():
    try:
        row = db(db.courses.id == auth.user.course_id).select(db.courses.course_name, db.courses.base_course).first()
        course_name = row.course_name
        newtext = request.vars['newtext']
        file = open(os.path.join(os.path.split(os.path.dirname(__file__))[0], 'custom_courses/' + course_name + '/index.rst'),'w')
        file.write(newtext)
        file.close()
        return 'ok'
    except Exception as ex:
        print(ex)


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def releasegrades():
    try:
        assignmentid = request.vars['assignmentid']
        assignment = db(db.assignments.id == assignmentid).select().first()
        assignment.update_record(released=True)
        return "Success"
    except Exception as ex:
        print(ex)


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def checkQType():
    acid = request.vars['acid']
    sid = request.vars['sid']
    answer = None
    useinfoquery = db((db.useinfo.div_id == acid) & (db.useinfo.sid == sid)).select(db.useinfo.event, db.useinfo.act).first()
    if useinfoquery != None:
        if useinfoquery.event == 'shortanswer':
            answer = useinfoquery.act

    return json.dumps(answer)
