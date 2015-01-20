from os import path
import os
import shutil
import sys


# controller for "Progress Page" as well as List/create assignments
def index():
    if not auth.user:
        session.flash = "Please Login"
        return redirect(URL('default','index'))
    if 'sid' not in request.vars and verifyInstructorStatus(auth.user.course_name, auth.user):
        return redirect(URL('assignments','admin'))
    if 'sid' not in request.vars:
        return redirect(URL('assignments','index') + '?sid=%d' % (auth.user.id))
    if str(auth.user.id) != request.vars.sid and not verifyInstructorStatus(auth.user.course_name, auth.user):
        return redirect(URL('assignments','index'))
    student = db(db.auth_user.id == request.vars.sid).select(
        db.auth_user.id,
        db.auth_user.username,
        db.auth_user.first_name,
        db.auth_user.last_name,
        db.auth_user.email,
        ).first()
    if not student:
        return redirect(URL('assignments','index'))

    course = db(db.courses.id == auth.user.course_id).select().first()
    assignments = db(db.assignments.id == db.grades.assignment)
    assignments = assignments(db.assignments.course == course.id)
    assignments = assignments(db.grades.auth_user == student.id)
    assignments = assignments(db.assignments.released == True)
    assignments = assignments.select(
        db.assignments.ALL,
        db.grades.ALL,
        orderby = db.assignments.name,
        )

    assignment_types = db(db.assignment_types).select(db.assignment_types.ALL, orderby=db.assignment_types.name)
    grade = CourseGrade(user = student, course=course, assignment_types = assignment_types)
    last_action = db(db.useinfo.sid == student.username)(db.useinfo.course_id == course.course_name).select(orderby=~db.useinfo.timestamp).first()

    # add forms for all of the individual grades that are student-projected, because not yet released or no grade row at all yet
    # use http://web2py.com/books/default/chapter/29/07/forms-and-validators, see section on multiple forms on one page

    for t in grade.assignment_type_grades:
        for a in t.assignments:
            if (not a.released) or (not a.score):
                a.form = SQLFORM(db.grades, 
                                 record=a.grade_record, 
                                 submit_button = 'change my projected grade',
                                 fields = ['projected'],
                                 showid = False
                                 )
                # still need to figure out how to get the right values for inserting; perhaps we should do the insertion on fetching, if the record didn't exist.
                if a.form.process(formname=a.assignment_name + str(a.assignment_id)).accepted:
                    print request.vars
                    a.projected = float(request.vars.projected)
                    response.flash = 'projected grade updated'
            
        
    return dict(
#        types = assignment_types,
        student = student,
        grade = grade,
        last_action = last_action,
        )

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def admin():
    course = db(db.courses.id == auth.user.course_id).select().first()
    assignments = db(db.assignments.course == course.id).select(db.assignments.ALL, orderby=db.assignments.name)
    sections = db(db.sections.course_id == course.id).select()
    students = db((db.auth_user.course_id == course.id) &
                            (db.auth_user.active==True))
    section_id = None
    try:
        section_id = int(request.get_vars.section_id)
        current_section = [x for x in sections if x.id == section_id][0]
        students = students((db.sections.id==db.section_users.section) &
                            (db.auth_user.id==db.section_users.auth_user))
        students = students(db.sections.id == current_section.id)
    except:
        pass
    students = students.select(db.auth_user.ALL, orderby=db.auth_user.last_name)
    return dict(
        assignments = assignments,
        students = students,
        sections = sections,
        section_id = section_id,
        )

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def create():
    course = db(db.courses.id == auth.user.course_id).select().first()
    assignment = db(db.assignments.id == request.get_vars.id).select().first()
    form = SQLFORM(db.assignments, assignment,
        showid = False,
        fields=['name','points','assignment_type','threshold'],
        keepvalues = True,
        formstyle='table3cols',
        )
    form.vars.course = course.id
    if form.process().accepted:
        session.flash = 'form accepted'
        return redirect(URL('assignments','update')+'?id=%d' % (form.vars.id))
    elif form.errors:
        response.flash = 'form has errors'
    return dict(
        form = form,
        )

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def update():
    course = db(db.courses.id == auth.user.course_id).select().first()
    assignment = db(db.assignments.id == request.get_vars.id).select().first()

    form = SQLFORM(db.assignments, assignment,
        showid = False,
        fields=['name','points','assignment_type','threshold','released'],
        keepvalues = True,
        formstyle='table3cols',
        )

    form.vars.course = course.id
    if form.process().accepted:
        session.flash = 'form accepted'
        return redirect(URL('assignments','update')+'?id=%d' % (form.vars.id))
    elif form.errors:
        response.flash = 'form has errors'

    db.deadlines.section.requires = IS_IN_DB(db(db.sections.course_id == course),'sections.id','%(name)s')
    new_deadline_form = SQLFORM(db.deadlines,
        showid = False,
        fields=['section','deadline'],
        keepvalues = True,
        formstyle='table3cols',
        )
    new_deadline_form.vars.assignment = assignment
    if new_deadline_form.process().accepted:
        session.flash = 'added new deadline'
    elif new_deadline_form.errors:
        response.flash = 'error adding deadline'

    deadlines = db(db.deadlines.assignment == assignment.id).select()
    delete_deadline_form = FORM()
    for deadline in deadlines:
        deadline_label = "On %s" % (deadline.deadline)
        if deadline.section:
            section = db(db.sections.id == deadline.section).select().first()
            deadline_label = deadline_label + " for %s" % (section.name)
        delete_deadline_form.append(
            DIV(
                LABEL(
                INPUT(_type="checkbox", _name=deadline.id, _value="delete"),
                deadline_label,
                ),
                _class="checkbox"
            ))
    delete_deadline_form.append(
        INPUT(
            _type="submit",
            _value="Delete Deadlines",
            _class="btn btn-default"
            ))

    if delete_deadline_form.accepts(request,session, formname="delete_deadline_form"):
        for var in delete_deadline_form.vars:
            if delete_deadline_form.vars[var] == "delete":
                db(db.deadlines.id == var).delete()
        session.flash = 'Deleted deadline(s)'
        return redirect(URL('assignments','update')+'?id=%d' % (assignment.id))

    problems_delete_form = FORM(
        _method="post",
        _action=URL('assignments','update')+'?id=%d' % (assignment.id)
        )
    for problem in db(db.problems.assignment == assignment.id).select(
        db.problems.id,
        db.problems.acid,
        orderby=db.problems.acid):
        problems_delete_form.append(
        DIV(
            LABEL(
            INPUT(_type="checkbox", _name=problem.id, _value="delete"),
            problem.acid,
            ),
            _class="checkbox"
        ))
    problems_delete_form.append(
        INPUT(
            _type="submit",
            _value="Remove Problems",
            _class="btn btn-default"
            ))
    if problems_delete_form.accepts(request, session, formname="problems_delete_form"):
        count = 0
        for var in problems_delete_form.vars:
            if problems_delete_form.vars[var] == "delete":
                db(db.problems.id == var).delete()
                count += 1
        if count > 0:
            session.flash = "Removed %d Problems" % (count)
        else:
            session.flash = "Didn't remove any problems"
        return redirect(URL('assignments','update')+'?id=%d' % (assignment.id))


    problem_query_form = FORM(
        _method="post",
        _action=URL('assignments','update')+'?id=%d' % (assignment.id)
        )
    problem_query_form.append(
        INPUT(
            _type="text",
            _name="acid"
            ))
    problem_query_form.append(
        INPUT(
            _type="submit",
            _value="Search"
            ))
    if problem_query_form.accepts(request,session,formname="problem_query_form"):
        if 'acid' in problem_query_form.vars:
            count = 0
            for acid in problem_query_form.vars['acid'].split(','):
                acid = acid.replace(' ','')
                if db(db.problems.acid == acid)(db.problems.assignment == assignment.id).select().first() == None:
                    count += 1
                    db.problems.insert(
                        assignment = assignment.id,
                        acid = acid,
                        )
            session.flash = "Added %d problems" % (count)
        else:
            session.flash = "Didn't add any problems."
        return redirect(URL('assignments','update')+'?id=%d' % (assignment.id))

    return dict(
        assignment = assignment,
        form = form,
        new_deadline_form = new_deadline_form,
        delete_deadline_form = delete_deadline_form,
        problem_query_form = problem_query_form,
        problems_delete_form = problems_delete_form,
        )

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def grade():
    course = db(db.courses.id == auth.user.course_id).select().first()
    assignment = db(db.assignments.id == request.get_vars.id).select().first()

    count_graded = 0
    for row in db(db.auth_user.course_id == course.id).select():
        assignment.grade(row)
        count_graded += 1
    session.flash = "Graded %d Assignments" % (count_graded)
    if request.env.HTTP_REFERER:
        return redirect(request.env.HTTP_REFERER)
    return redirect("%s?id=%d" % (URL('assignments','detail'), assignment.id))

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def release_grades():
    course = db(db.courses.id == auth.user.course_id).select().first()
    assignment = db(db.assignments.id == request.get_vars.id).select().first()

    if assignment.release_grades():
        session.flash = "Grades Relased"
    if request.env.HTTP_REFERER:
        return redirect(request.env.HTTP_REFERER)
    return redirect("%s?id=%d" % (URL('assignments','detail'), assignment.id))

def fill_empty_scores(scores=[], students=[], student=None, problems=[], acid=None):
    for student in students:
        found = False
        for sc in scores:
            if sc.user.id == student.id:
                found = True
        if not found:
            scores.append(score(
                user = student,
                acid = acid,
                ))
    for p in problems:
        found = False
        for sc in scores:
            if sc.acid == p.acid:
                found = True
        if not found:
            scores.append(score(
                user = student,
                acid = p.acid,
                ))

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def detail():
    course = db(db.courses.id == auth.user.course_id).select().first()
    assignment = db(db.assignments.id == request.vars.id)(db.assignments.course == course.id).select().first()
    if not assignment:
        return redirect(URL("assignments","index"))

    sections = db(db.sections.course_id == course.id).select(db.sections.ALL)
    students = db(( db.auth_user.course_id == course.id) &
                            (db.auth_user.active==True))

    section_id = None
    try:
        section_id = int(request.get_vars.section_id)
        current_section = [x for x in sections if x.id == section_id][0]
        students = students((db.sections.id==db.section_users.section) & (db.auth_user.id==db.section_users.auth_user))
        students = students(db.sections.id == current_section.id)
    except:
        pass

    students = students.select(db.auth_user.ALL, orderby=db.auth_user.last_name)
    problems = db(db.problems.assignment == assignment.id).select(db.problems.ALL)

    # getting scores
    student = None
    if 'sid' in request.vars:
        student_id = request.vars.sid
        student = db(db.auth_user.id == student_id).select().first()
        acid = None
    acid = None
    if "acid" in request.vars:
        acid = request.vars.acid

    scores = assignment.scores(problem = acid, user=student, section_id=section_id)

    if acid and not student:
        fill_empty_scores(scores = scores, students = students, acid=acid)
    if student and not acid:
        fill_empty_scores(scores = scores, problems = problems, student=student)


    # easy median
    def get_median(lst):
        sorts = sorted(lst)
        length = len(sorts)
        if not length % 2:
            return (sorts[length/2] + sorts[length/2 - 1]) / 2.0
        return sorts[length/2]

    # get average of scores for problem set, not counting 0s
    problem_points = [s.points for s in scores if s.points > 0]
    score_sum = float(sum(problem_points))
    try:
        mean_score = score_sum/len(problem_points)
    except:
        mean_score = 0
    # get min, max, median, count
    min_score = min(problem_points)
    max_score = max(problem_points)
    if len(problem_points) > 0:
        median_score = get_median(problem_points)
        real_score_count = len(problem_points)
    else:
        median_score = 0
        real_score_count = 0


    # Used as a convinence function for navigating within the page template
    def page_args(id=assignment.id, section_id=section_id, student=student, acid=acid):
        arg_str = "?id=%d" % (id)
        if section_id:
            arg_str += "&section_id=%d" % section_id
        if student:
            arg_str += "&sid=%d" % student.id
        if acid:
            arg_str += "&acid=%s" % acid
        return arg_str

    return dict(
        assignment = assignment,
        problems = problems,
        students = students,
        sections = sections,
        section_id = section_id,
        selected_student = student,
        scores = scores,
        page_args = page_args,
        selected_acid = acid,
        course_id = auth.user.course_name,
        avg_score = mean_score,
        min_score = min_score,
        max_score = max_score,
        real_score_count = real_score_count,
        median_score = median_score,
        gradingUrl = URL('assignments', 'problem'),
        massGradingURL = URL('assignments', 'mass_grade_problem'),
        )

import json
@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def problem():
    if 'acid' not in request.vars or 'sid' not in request.vars:
        return json.dumps({'success':False, 'message':"Need problem and user."})

    user = db(db.auth_user.username == request.vars.sid).select().first()
    if not user:
        return json.dumps({'success':False, 'message':"User does not exit. Sorry!"})

    # update grade - if you dare!
    if 'grade' in request.vars and 'comment' in request.vars:
        grade = float(request.vars.grade)
        comment = request.vars.comment
        q = db(db.code.acid == request.vars.acid)(db.code.sid == request.vars.sid).select().first()
        if not q:
            db.code.insert(
                acid = request.vars.acid,
                sid = user.username,
                grade = request.vars.grade,
                comment = request.vars.comment,
                )
        else:
            db((db.code.acid == request.vars.acid) &
                (db.code.sid == request.vars.sid)
                ).update(
                grade = grade,
                comment = comment,
                )

    res = {
        'id':"%s-%d" % (request.vars.acid, user.id),
        'acid':request.vars.acid,
        'sid':user.id,
        'username':user.username,
        'name':"%s %s" % (user.first_name, user.last_name),
        'code':"",
        'grade':0.0,
        'comment':"",
        }

    q = db(db.code.sid == db.auth_user.username)
    q = q(db.code.acid == request.vars.acid)
    q = q(db.auth_user.username == request.vars.sid)
    q = q.select(
        db.auth_user.ALL,
        db.code.ALL,
        orderby = db.code.acid|db.code.timestamp,
        distinct = db.code.acid,
        ).first()
    if q:
        res = {
            'id':"%s-%d" % (q.code.acid, q.auth_user.id),
            'acid':q.code.acid,
            'sid':int(q.auth_user.id),
            'username':q.auth_user.username,
            'name':"%s %s" % (q.auth_user.first_name, q.auth_user.last_name),
            'code':q.code.code,
            'grade':q.code.grade,
            'comment':q.code.comment,
            'lang':q.code.language
            }
    return json.dumps(res)

def mass_grade_problem():
    if 'csv' not in request.vars or 'acid' not in request.vars:
        return json.dumps({"success":False})
    scores = []
    for row in request.vars.csv.split("\n"):
        cells = row.split(",")
        if len(cells) < 2:
            continue
        
        email = cells[0]
        if cells[1]=="":
            cells[1]=0
        grade = float(cells[1])
        if len(cells) == 2:
            comment = ""
        else: # should only ever be 2 or 3
            comment = cells[-1] # comment should be the last element
        user = db(db.auth_user.email == email).select().first()
        if user == None:
            continue
        q = db(db.code.acid == request.vars.acid)(db.code.sid == user.username).select().first()
        if not q:
            db.code.insert(
                acid = request.vars.acid,
                sid = user.username,
                grade = request.vars.grade,
                comment = request.vars.comment,
                )
        else:
            db((db.code.acid == request.vars.acid) &
                (db.code.sid == user.username)
                ).update(
                grade = grade,
                comment = comment,
                )
        scores.append({
            'acid':request.vars.acid,
            'username':user.username,
            'grade':grade,
            'comment':comment,
            })
    return json.dumps({
        "success":True,
        "scores":scores,
        })

def migrate_to_scores():
    """ Temp command to migrate db.code grades to db.score table """

    accumulated_scores = {}
    code_rows = db(db.code.grade != None).select(
        db.code.ALL,
        orderby = db.code.acid|db.code.timestamp,
        distinct = db.code.acid,
        )
    for row in code_rows:
        if row.sid not in accumulated_scores:
            accumulated_scores[row.sid] = {}
        if row.acid not in accumulated_scores[row.sid]:
            accumulated_scores[row.sid][row.acid] = {
                'score':row.grade,
                'comment':row.comment,
                }
    acid_count = 0
    user_count = 0
    for sid in accumulated_scores:
        user = db(db.auth_user.username == sid).select().first()
        if not user:
            continue
        user_count += 1
        for acid in accumulated_scores[sid]:
            db.scores.update_or_insert(
                ((db.scores.acid == acid) & (db.scores.auth_user == user.id)),
                acid = acid,
                auth_user = user.id,
                score = accumulated_scores[sid][acid]['score'],
                comment = accumulated_scores[sid][acid]['comment'],
                )
            acid_count += 1
    session.flash = "Set %d scores for %d users" % (acid_count, user_count)
    return redirect(URL("assignments","index"))

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def download():
    course = db(db.courses.id == auth.user.course_id).select().first()
    students = db(db.auth_user.course_id == course.id).select()
    assignments = db(db.assignments.course == course.id)(db.assignments.assignment_type==db.assignment_types.id).select(orderby=db.assignments.assignment_type)
    grades = db(db.grades).select()

    field_names = ['Lastname','Firstname','Email','Total']
    type_names = []
    assignment_names = []
    
    assignment_types = db(db.assignment_types).select(db.assignment_types.ALL, orderby=db.assignment_types.name)
    rows = [CourseGrade(user = student, course=course, assignment_types = assignment_types).csv(type_names, assignment_names) for student in students]
    response.view='generic.csv'
    return dict(filename='grades_download.csv', csvdata=rows,field_names=field_names+type_names+assignment_names)


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def newtype():
    form = SQLFORM(db.assignment_types,
                   fields=['name', 'grade_type', 'weight', 'points_possible','assignments_dropped'],)

    course = db(db.courses.id == auth.user.course_id).select().first()
    form.vars.course = course.id

    if form.process().accepted:
        session.flash = 'assignment type added'
        return redirect(URL('admin', 'index'))

    return dict(form=form)

