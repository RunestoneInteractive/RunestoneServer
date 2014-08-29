from os import path
import os
import shutil
import sys
from sphinx.application import Sphinx


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

    grade = CourseGrade()
    assignment_types = db(db.assignment_types).select(db.assignment_types.ALL, orderby=db.assignment_types.name)
    for t in assignment_types:
        t.grade = student_grade(user = student, course = course, assignment_type=t)
        grade.points += t.grade.current()
        grade.projected_pts += t.grade.projected()
        grade.max_pts += t.grade.max()
    last_action = db(db.useinfo.sid == student.username)(db.useinfo.course_id == course.course_name).select(orderby=~db.useinfo.timestamp).first()

    return dict(
        types = assignment_types,
        assignments = assignments,
        student = student,
        grade = grade,
        last_action = last_action,
        )

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def admin():
    course = db(db.courses.id == auth.user.course_id).select().first()
    assignments = db(db.assignments.course == course.id).select(db.assignments.ALL, orderby=db.assignments.name)
    sections = db(db.sections.course_id == course.id).select()
    students = db(db.auth_user.course_id == course.id)
    section_id = None
    try:
        section_id = int(request.get_vars.section_id)
        current_section = [x for x in sections if x.id == section_id][0]
        students = students((db.sections.id==db.section_users.section) & (db.auth_user.id==db.section_users.auth_user))
        students = students(db.sections.id == current_section.id)
    except:
        pass
    students = students.select(db.auth_user.ALL)
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
    students = db(db.auth_user.course_id == course.id)

    section_id = None
    try:
        section_id = int(request.get_vars.section_id)
        current_section = [x for x in sections if x.id == section_id][0]
        students = students((db.sections.id==db.section_users.section) & (db.auth_user.id==db.section_users.auth_user))
        students = students(db.sections.id == current_section.id)
    except:
        pass

    students = students.select(db.auth_user.ALL)
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
        grade = float(cells[1])
        comment = ""
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

    field_names = ['Name','Email']
    regular_assignments = [a for a in assignments if a.assignment_types.grade_type != 'use']
    use_assignments = [a for a in assignments if a.assignment_types.grade_type == 'use']
    def sort_key(assignment_name):
        try:
            return int(assignment_name.split()[-1])
        except:
            return assignment_name
    for ass in regular_assignments:
        field_names.append(ass.assignments.name)
    for postfix in ["_time", "_time_pre_deadline", "_activities", "_activities_pre_deadline", "_max_act"]:
        for nm in sorted([ass.assignments.name for ass in use_assignments], key = sort_key):
            field_names.append(nm + postfix)

    student_data = []
    use_data = get_all_times_and_activity_counts(course)
    for student in students:
        row = {}
        row['Name']=student.first_name+" "+student.last_name
        row['Email']=student.email
        for ass in assignments:
            grade = [x for x in grades if x.auth_user==student.id and x.assignment==ass.assignments.id]
            if len(grade) > 0:
                row[ass.assignments.name] = grade[0].score
            else:
                row[ass.assignments.name] = 0
        usage = use_data[student.registration_id]
        for k in usage:
            row[k]= usage[k]

        student_data.append(row)
    response.view='generic.csv'
    return dict(filename='grades_download.csv', csvdata=student_data,field_names=field_names)


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def newtype():
    form = SQLFORM(db.assignment_types)

    return dict(form=form)

