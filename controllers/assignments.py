from os import path
import os
import shutil
import sys
import json


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

    if not assignment:
        return redirect(URL('assignments','admin'))

    else:
        form = SQLFORM(db.assignments, assignment,
            showid = False,
            deletable=True,
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

    students = students.select(db.auth_user.ALL, orderby=db.auth_user.last_name | db.auth_user.first_name)
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

    # easy mean (for separating code)
    # will sometimes be ugly - could fix
    def get_mean(lst):
        return round(float(sum([i for i in lst if type(i) == type(2)]+ [i for i in lst if type(i) == type(2.0)]))/len(lst),2)
    # get spread measures of scores for problem set, not counting 0s
    # don't want to look at # of 0s because test users, instructors, etc, throws this off

    problem_points = [s.points for s in scores if s.points > 0]
    score_sum = float(sum(problem_points))

    try:
        mean_score = float("%.02f" % score_sum/len(problem_points))
    except:
        mean_score = 0
    # get min, max, median, count
    if len(problem_points) > 0:
        min_score = min(problem_points)
        max_score = max(problem_points)
        median_score = get_median(problem_points)
        min_score = min(problem_points)
        max_score = max(problem_points)
        avg_score = get_mean(problem_points)
    else:
        min_score = 0
        max_score = 0
        median_score = 0
        min_score,max_score = 0,0
        #real_score_count = 0 # not being used right now
        avg_score = 0
    # get number of problems with any code saved
    #num_problems_with_code = len([p.code for p in problems if p.code is not None])
    num_problems_with_code = "not calculated"

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
        avg_score = avg_score,
        min_score = min_score,
        max_score = max_score,
        real_score_count = num_problems_with_code,
        median_score = median_score,
        gradingUrl = URL('assignments', 'problem'),
        massGradingURL = URL('assignments', 'mass_grade_problem'),
        gradeRecordingUrl = URL('assignments', 'record_grade'),
        )

def _autograde_one_mchoice(course_name, sid, question, points, deadline, first_p):
    # Look in mchoice_answers table for results of first or last run before deadline

    # sid matches auth_user.username, not auth_user.id
    query = ((db.mchoice_answers.sid == sid) & \
            (db.mchoice_answers.div_id == question.name) \
             )

    if deadline:
        query = query & (db.mchoice_answers.timestamp < deadline)
    if first_p:
        #use first answer
        answer = db(query).select(orderby=db.mchoice_answers.timestamp).first()
    else:
        #use last answer
        answer = db(query).select(orderby=~db.mchoice_answers.timestamp).first()

    score = 0
    print answer
    if answer and answer.correct:
        score = points
    else:
        score = 0

    db.question_grades.update_or_insert(
        ((db.question_grades.sid == sid) &
         (db.question_grades.course_name == course_name) &
         (db.question_grades.div_id == question.name)
         ),
        sid=sid,
        course_name=course_name,
        div_id=question.name,
        score = score,
        comment = "autograded"
    )

def _autograde_one_ac(course_name, sid, question, points, deadline):
    # Look in code table for results of last run before deadline

    # sid matches auth_user.username, not auth_user.id

    query = ((db.useinfo.course_id == course_name) & \
            (db.useinfo.div_id == question.name) & \
            (db.useinfo.sid == sid) & \
            (db.useinfo.event == 'unittest'))

    if deadline:
        query = query & (db.useinfo.timestamp < deadline)

    most_recent = db(query).select(orderby=~db.useinfo.timestamp).first()

    score = 0
    id = None
    if most_recent:
        pct_correct = int(most_recent.act.split(':')[1])
        if pct_correct == 100:
            score = points
        id = most_recent.id

    db.question_grades.update_or_insert(
        ((db.question_grades.sid == sid) &
         (db.question_grades.course_name == course_name) &
         (db.question_grades.div_id == question.name)
         ),
        sid=sid,
        course_name=course_name,
        div_id=question.name,
        score = score,
        comment = "autograded",
        useinfo_id = id
    )

def _autograde_one_visited(course_name, sid, question, points, deadline):
    # look in useinfo, to see if visited (before deadline)
    # sid matches auth_user.username, not auth_user.id
    query =  (db.useinfo.div_id == question.name) & (db.useinfo.sid == sid)
    if deadline:
        query = query & (db.useinfo.timestamp < deadline)
    visit = db(query).select().first()

    if visit:
        score = points
    else:
        score = 0

    db.question_grades.update_or_insert(
        ((db.question_grades.sid == sid) &
         (db.question_grades.course_name == course_name) &
         (db.question_grades.div_id == question.name)
         ),
        sid=sid,
        course_name=course_name,
        div_id=question.name,
        score = score,
        comment = "autograded"
    )

def _autograde_one_q(course_name, assignment_id, sid, qname, points, deadline=None):
    print "autograding", assignment_id, sid, qname, deadline

    # if previously manually graded, don't overwrite
    existing = db((db.question_grades.sid == sid) \
       & (db.question_grades.course_name == course_name) \
       & (db.question_grades.div_id == qname) \
       ).select().first()
    if existing and (existing.comment != "autograded"):
        # print "skipping; previously manually graded, comment = {}".format(existing.comment)
        return

    # get the question object
    question = db(db.questions.name == qname).select().first()

    # dispatch on grading_type; if none specified, can't autograde
    if question.autograde == 'unittest':
        _autograde_one_ac(course_name, sid, question, points, deadline)
    elif question.autograde == 'first_answer':
        _autograde_one_mchoice(course_name, sid, question, points, deadline, first_p=True)
    elif question.autograde == 'last_answer':
        _autograde_one_mchoice(course_name, sid, question, points, deadline, first_p=False)
    elif question.autograde == 'visited':
        _autograde_one_visited(course_name, sid, question, points, deadline)
    else:
        # print "skipping; autograde = {}".format(question.autograde)
        pass

def _compute_assignment_total(student, assignment):
    # student is a row, containing id and username
    # assignment is a row, containing name and id and points and threshold
    # Get all question_grades for this sid/assignment_id
    # Retrieve from question_grades table  with right sids and div_ids
    # sid is really a username, so look it up in auth_user
    # div_id is found in questions; questions are associated with assignments, which have assignment_id
    print(student.id, assignment.id)
    query =  (db.question_grades.sid == student.username) \
             & (db.question_grades.div_id == db.questions.name) \
             & (db.questions.id == db.assignment_questions.question_id) \
             & (db.assignment_questions.assignment_id == assignment.id)
    scores = db(query).select(db.question_grades.score)
    # Sum them up; if threshold, compute total based on threshold
    print len(scores)
    total = sum([row.score for row in scores])
    print total
    if assignment.threshold:
        if total >= assignment.threshold:
            score = assignment.points
        else:
            score = 0
    else:
        score = total

    # Write the sum to the grades table
    # grades table expects row ids for auth_user and assignment
    db.grades.update_or_insert(
        ((db.grades.auth_user == student.id) &
         (db.grades.assignment == assignment.id)),
        auth_user = student.id,
        assignment = assignment.id,
        score=score)


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def autograde():
    ### This endpoint is hit to autograde one or all students or questions for an assignment

    assignment_name = request.vars.assignment
    assignment = db((db.assignments.name == assignment_name) & (db.assignments.course == auth.user.course_id)).select().first()
    if assignment:
        assignment_id = assignment.id
    else:
        return json.dumps({'success':False, 'message':"Select an assignment before trying to autograde."})

    sid = request.vars.get('sid', None)
    qname = request.vars.get('question', None)
    enforce_deadline = request.vars.get('enforceDeadline', None)

    if enforce_deadline:
        # get the deadline associated with the assignment
        deadline = assignment.duedate
    else:
        deadline = None
    if sid:
        # sid which is passed in is a username, not a row id
        student_rows = db((db.user_courses.course_id == auth.user.course_id) &
                          (db.user_courses.user_id == db.auth_user.id) &
                          (db.auth_user.username == sid)
                          ).select(db.auth_user.username, db.auth_user.id)
        sids = [row.username for row in student_rows]
    else:
        # get all student usernames for this course
        student_rows = db((db.user_courses.course_id == auth.user.course_id) &
                          (db.user_courses.user_id == db.auth_user.id)
                          ).select(db.auth_user.username, db.auth_user.id)
        sids = [row.username for row in student_rows]

    if qname:
        questions_query = db(
            (db.assignment_questions.assignment_id == assignment_id) &
            (db.assignment_questions.question_id == db.questions.id) &
            (db.questions.name == qname)
            ).select(db.questions.name, db.assignment_questions.points)
        questions = [(row.questions.name, row.assignment_questions.points) for row in questions_query]
    else:
        # get all qids and point values for this assignment
        questions_query = db((db.assignment_questions.assignment_id == assignment_id) & (db.assignment_questions.question_id == db.questions.id)).select(db.questions.name, db.assignment_questions.points)
        questions = [(row.questions.name, row.assignment_questions.points) for row in questions_query]

    count = 0
    for (qdiv, points) in questions:
        for s in sids:
            _autograde_one_q(auth.user.course_name, assignment_id, s, qdiv, points, deadline=deadline)
            count += 1

    if not qname:
        # compute total score for the assignment for each sid
        for student in student_rows:
            _compute_assignment_total(student, assignment)

    return json.dumps({'message': "autograded {} items".format(count)})

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def record_grade():
    if 'acid' not in request.vars or 'sid' not in request.vars:
        return json.dumps({'success':False, 'message':"Need problem and user."})

    score_str = request.vars.get('grade', 0)
    if score_str == "":
        score = 0
    else:
        score = float(score_str)
    comment = request.vars.get('comment', None)
    if score_str != "" or ('comment' in request.vars and comment != ""):
        db.question_grades.update_or_insert((\
            (db.question_grades.sid == request.vars['sid']) \
            & (db.question_grades.div_id == request.vars['acid']) \
            & (db.question_grades.course_name == auth.user.course_name) \
            ),
            sid = request.vars['sid'],
            div_id = request.vars['acid'],
            course_name = auth.user.course_name,
            score = score,
            comment = comment)
        return json.dumps({'response': 'replaced'})
    else:
        return json.dumps({'response': 'not replaced'})


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def get_problem():
    if 'acid' not in request.vars or 'sid' not in request.vars:
        return json.dumps({'success':False, 'message':"Need problem and user."})

    user = db(db.auth_user.username == request.vars.sid).select().first()
    if not user:
        return json.dumps({'success':False, 'message':"User does not exist. Sorry!"})

    res = {
        'id':"%s-%d" % (request.vars.acid, user.id),
        'acid':request.vars.acid,
        'sid':user.id,
        'username':user.username,
        'name':"%s %s" % (user.first_name, user.last_name),
        'code': ""
    }

    # get code from last timestamped record
    # null timestamps come out at the end, so the one we want could be in the middle, whether we sort in reverse order or regular; ugh
    # solution: the last one by id order should be the last timestamped one, as we only create ones without timestamp during grading, and then only if there is no existing record

    # get the deadline associated with the assignment
    query =  (db.code.acid == request.vars.acid) & (db.code.sid == request.vars.sid)
    if request.vars.enforceDeadline == "true" and deadline:
        query = query & (db.code.timestamp < deadline)
    c = db(query).select(orderby = db.code.id).last()

    if c:
        res['code'] = c.code

    # add prefixes, suffix_code and files that are available
    # retrieve the db record
    source = db.source_code(acid = request.vars.acid, course_id = auth.user.course_name)

    if source and c and c.code:
        def get_source(acid):
            r = db.source_code(acid=acid)
            if r:
                return r.main_code
            else:
                return ""
        if source.includes:
            # strip off "data-include"
            txt = source.includes[len("data-include="):]
            included_divs = [x.strip() for x in txt.split(',') if x != '']
            # join together code for each of the includes
            res['includes'] = '\n'.join([get_source(acid) for acid in included_divs])
            #print res['includes']
        if source.suffix_code:
            res['suffix_code'] = source.suffix_code
            #print source.suffix_code

        file_divs = [x.strip() for x in source.available_files.split(',') if x != '']
        res['file_includes'] = [{'acid': acid, 'contents': get_source(acid)} for acid in file_divs]
    return json.dumps(res)

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def problem():
    ### For backward compatibility with old grading interface; shouldn't be used after transition
    ### This endpoint is hit either to update (if 'grade' and 'comment' are in request.vars)
    ### Or just to get the current state of the grade for this acid (if not present)
    if 'acid' not in request.vars or 'sid' not in request.vars:
        return json.dumps({'success':False, 'message':"Need problem and user."})

    user = db(db.auth_user.username == request.vars.sid).select().first()
    if not user:
        return json.dumps({'success':False, 'message':"User does not exist. Sorry!"})

    # get last timestamped record
    # null timestamps come out at the end, so the one we want could be in the middle, whether we sort in reverse order or regular; ugh
    # solution: the last one by id order should be the last timestamped one, as we only create ones without timestamp during grading, and then only if there is no existing record
    c = db((db.code.acid == request.vars.acid) & (db.code.sid == request.vars.sid)).select(orderby = db.code.id).last()
    if 'grade' in request.vars and 'comment' in request.vars:
        # update grade
        try:
            grade = float(request.vars.grade)
        except:
            return json.dumps({'success':False, 'message':"cannot convert {} to a number".format(request.vars.grade)})

        comment = request.vars.comment
        if c:
            c.update_record(grade=grade, comment=comment)
        else:
            id = db.code.insert(
                acid = request.vars.acid,
                sid = user.username,
                grade = request.vars.grade,
                comment = request.vars.comment,
                )
            c = db.code(id)

    return get_problem()

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
