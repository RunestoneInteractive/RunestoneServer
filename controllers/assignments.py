from os import path
import os
import shutil
import sys
import json
import logging
import datetime
from collections import OrderedDict
from psycopg2 import IntegrityError
from rs_grading import do_autograde, do_calculate_totals, do_check_answer

logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)


# controller for "Progress Page" as well as List/create assignments
def index():
    if not auth.user:
        session.flash = "Please Login"
        return redirect(URL('default', 'index'))
    if 'sid' not in request.vars:
        return redirect(URL('assignments', 'index') + '?sid=%s' % (auth.user.username))

    student = db(db.auth_user.username == request.vars.sid).select(
        db.auth_user.id,
        db.auth_user.username,
        db.auth_user.first_name,
        db.auth_user.last_name,
        db.auth_user.email,
    ).first()
    if not student:
        return redirect(URL('assignments', 'index'))

    if auth.user.course_name in ['thinkcspy', 'pythonds', 'JavaReview', 'webfundamentals', 'StudentCSP', 'apcsareview']:
        session.flash = "{} is not a graded course".format(auth.user.course_name)
        return redirect(URL('default', 'user'))

    data_analyzer = DashboardDataAnalyzer(auth.user.course_id)
    data_analyzer.load_user_metrics(request.get_vars["sid"])
    data_analyzer.load_assignment_metrics(request.get_vars["sid"], studentView=True)

    chapters = []
    for chapter_label, chapter in data_analyzer.chapter_progress.chapters.iteritems():
        chapters.append({
            "label": chapter.chapter_label,
            "status": chapter.status_text(),
            "subchapters": chapter.get_sub_chapter_progress()
        })
    activity = data_analyzer.formatted_activity.activities

    return dict(student=student, course_id=auth.user.course_id, course_name=auth.user.course_name,
                user=data_analyzer.user, chapters=chapters, activity=activity, assignments=data_analyzer.grades)


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def admin():
    course = db(db.courses.id == auth.user.course_id).select().first()
    assignments = db(db.assignments.course == course.id).select(db.assignments.ALL, orderby=db.assignments.name)
    sections = db(db.sections.course_id == course.id).select()
    students = db((db.auth_user.course_id == course.id) &
                  (db.auth_user.active == True))
    section_id = None
    try:
        section_id = int(request.get_vars.section_id)
        current_section = [x for x in sections if x.id == section_id][0]
        students = students((db.sections.id == db.section_users.section) &
                            (db.auth_user.id == db.section_users.auth_user))
        students = students(db.sections.id == current_section.id)
    except:
        pass
    students = students.select(db.auth_user.ALL, orderby=db.auth_user.last_name)
    return dict(
        assignments=assignments,
        students=students,
        sections=sections,
        section_id=section_id,
    )


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def create():
    course = db(db.courses.id == auth.user.course_id).select().first()
    assignment = db(db.assignments.id == request.get_vars.id).select().first()
    form = SQLFORM(db.assignments, assignment,
                   showid=False,
                   fields=['name', 'points', 'assignment_type'],
                   keepvalues=True,
                   formstyle='table3cols',
                   )
    form.vars.course = course.id
    if form.process().accepted:
        session.flash = 'form accepted'
        return redirect(URL('assignments', 'update') + '?id=%d' % (form.vars.id))
    elif form.errors:
        response.flash = 'form has errors'
    return dict(
        form=form,
    )


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def update():
    course = db(db.courses.id == auth.user.course_id).select().first()
    assignment = db(db.assignments.id == request.get_vars.id).select().first()

    if not assignment:
        return redirect(URL('assignments', 'admin'))

    else:
        form = SQLFORM(db.assignments, assignment,
                       showid=False,
                       deletable=True,
                       fields=['name', 'points', 'assignment_type', 'released'],
                       keepvalues=True,
                       formstyle='table3cols',
                       )

        form.vars.course = course.id
        if form.process().accepted:
            session.flash = 'form accepted'
            return redirect(URL('assignments', 'update') + '?id=%d' % (form.vars.id))
        elif form.errors:
            response.flash = 'form has errors'

        db.deadlines.section.requires = IS_IN_DB(db(db.sections.course_id == course), 'sections.id', '%(name)s')
        new_deadline_form = SQLFORM(db.deadlines,
                                    showid=False,
                                    fields=['section', 'deadline'],
                                    keepvalues=True,
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

        if delete_deadline_form.accepts(request, session, formname="delete_deadline_form"):
            for var in delete_deadline_form.vars:
                if delete_deadline_form.vars[var] == "delete":
                    db(db.deadlines.id == var).delete()
            session.flash = 'Deleted deadline(s)'
            return redirect(URL('assignments', 'update') + '?id=%d' % (assignment.id))

        problems_delete_form = FORM(
            _method="post",
            _action=URL('assignments', 'update') + '?id=%d' % (assignment.id)
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
            return redirect(URL('assignments', 'update') + '?id=%d' % (assignment.id))

        problem_query_form = FORM(
            _method="post",
            _action=URL('assignments', 'update') + '?id=%d' % (assignment.id)
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
        if problem_query_form.accepts(request, session, formname="problem_query_form"):
            if 'acid' in problem_query_form.vars:
                count = 0
                for acid in problem_query_form.vars['acid'].split(','):
                    acid = acid.replace(' ', '')
                    if db(db.problems.acid == acid)(db.problems.assignment == assignment.id).select().first() == None:
                        count += 1
                        db.problems.insert(
                            assignment=assignment.id,
                            acid=acid,
                        )
                session.flash = "Added %d problems" % (count)
            else:
                session.flash = "Didn't add any problems."
            return redirect(URL('assignments', 'update') + '?id=%d' % (assignment.id))

        return dict(
            assignment=assignment,
            form=form,
            new_deadline_form=new_deadline_form,
            delete_deadline_form=delete_deadline_form,
            problem_query_form=problem_query_form,
            problems_delete_form=problems_delete_form,
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
    return redirect("%s?id=%d" % (URL('assignments', 'detail'), assignment.id))


## deprecated; now using admin/releasegrades
@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def release_grades():
    course = db(db.courses.id == auth.user.course_id).select().first()
    assignment = db(db.assignments.id == request.get_vars.id).select().first()

    if assignment.release_grades():
        session.flash = "Grades Released"
    if request.env.HTTP_REFERER:
        return redirect(request.env.HTTP_REFERER)
    return redirect("%s?id=%d" % (URL('assignments', 'detail'), assignment.id))


def fill_empty_scores(scores=[], students=[], student=None, problems=[], acid=None):
    for student in students:
        found = False
        for sc in scores:
            if sc.user.id == student.id:
                found = True
        if not found:
            scores.append(score(
                user=student,
                acid=acid,
            ))
    for p in problems:
        found = False
        for sc in scores:
            if sc.acid == p.acid:
                found = True
        if not found:
            scores.append(score(
                user=student,
                acid=p.acid,
            ))


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def detail():
    course = db(db.courses.id == auth.user.course_id).select().first()
    assignment = db(db.assignments.id == request.vars.id)(db.assignments.course == course.id).select().first()
    if not assignment:
        return redirect(URL("assignments", "index"))

    sections = db(db.sections.course_id == course.id).select(db.sections.ALL)
    students = db((db.auth_user.course_id == course.id) &
                  (db.auth_user.active == True))

    section_id = None
    try:
        section_id = int(request.get_vars.section_id)
        current_section = [x for x in sections if x.id == section_id][0]
        students = students(
            (db.sections.id == db.section_users.section) & (db.auth_user.id == db.section_users.auth_user))
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

    scores = assignment.scores(problem=acid, user=student, section_id=section_id)

    if acid and not student:
        fill_empty_scores(scores=scores, students=students, acid=acid)
    if student and not acid:
        fill_empty_scores(scores=scores, problems=problems, student=student)

    # easy median
    def get_median(lst):
        sorts = sorted(lst)
        length = len(sorts)
        if not length % 2:
            return (sorts[length / 2] + sorts[length / 2 - 1]) / 2.0
        return sorts[length / 2]

    # easy mean (for separating code)
    # will sometimes be ugly - could fix
    def get_mean(lst):
        return round(
            float(sum([i for i in lst if type(i) == type(2)] + [i for i in lst if type(i) == type(2.0)])) / len(lst), 2)

    # get spread measures of scores for problem set, not counting 0s
    # don't want to look at # of 0s because test users, instructors, etc, throws this off

    problem_points = [s.points for s in scores if s.points > 0]
    score_sum = float(sum(problem_points))

    try:
        mean_score = float("%.02f" % score_sum / len(problem_points))
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
        min_score, max_score = 0, 0
        # real_score_count = 0 # not being used right now
        avg_score = 0
    # get number of problems with any code saved
    # num_problems_with_code = len([p.code for p in problems if p.code is not None])
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
        assignment=assignment,
        problems=problems,
        students=students,
        sections=sections,
        section_id=section_id,
        selected_student=student,
        scores=scores,
        page_args=page_args,
        selected_acid=acid,
        course_id=auth.user.course_name,
        avg_score=avg_score,
        min_score=min_score,
        max_score=max_score,
        real_score_count=num_problems_with_code,
        median_score=median_score,
        gradingUrl=URL('assignments', 'problem'),
        massGradingURL=URL('assignments', 'mass_grade_problem'),
        gradeRecordingUrl=URL('assignments', 'record_grade'),
    )


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def record_assignment_score():
    score = request.vars.get('score', None)
    assignment_name = request.vars.assignment
    assignment = db(
        (db.assignments.name == assignment_name) & (db.assignments.course == auth.user.course_id)).select().first()
    if assignment:
        assignment_id = assignment.id
    else:
        return json.dumps({'success': False, 'message': "Select an assignment before trying to calculate totals."})

    if score:
        # Write the score to the grades table
        # grades table expects row ids for auth_user and assignment
        sname = request.vars.get('sid', None)
        sid = db((db.auth_user.username == sname)).select(db.auth_user.id).first().id
        db.grades.update_or_insert(
            ((db.grades.auth_user == sid) &
             (db.grades.assignment == assignment_id)),
            auth_user=sid,
            assignment=assignment_id,
            score=score,
            manual_total=True
        )


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def calculate_totals():
    assignment_name = request.vars.assignment
    sid = request.vars.get('sid', None)
    assignment = db(
        (db.assignments.name == assignment_name) & (db.assignments.course == auth.user.course_id)).select().first()
    if assignment:
        return json.dumps(
            do_calculate_totals(assignment, auth.user.course_id, auth.user.course_name, sid, db, settings))
    else:
        return json.dumps({'success': False, 'message': "Select an assignment before trying to calculate totals."})


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def autograde():
    ### This endpoint is hit to autograde one or all students or questions for an assignment

    sid = request.vars.get('sid', None)
    question_name = request.vars.get('question', None)
    enforce_deadline = request.vars.get('enforceDeadline', None)
    assignment_name = request.vars.assignment
    timezoneoffset = session.timezoneoffset if 'timezoneoffset' in session else None

    assignment = db(
        (db.assignments.name == assignment_name) & (db.assignments.course == auth.user.course_id)).select().first()
    if assignment:
        count = do_autograde(assignment, auth.user.course_id, auth.user.course_name, sid, question_name,
                             enforce_deadline, timezoneoffset, db, settings)
        return json.dumps({'message': "autograded {} items".format(count)})
    else:
        return json.dumps({'success': False, 'message': "Select an assignment before trying to autograde."})


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def record_grade():
    if 'acid' not in request.vars or 'sid' not in request.vars:
        return json.dumps({'success': False, 'message': "Need problem and user."})

    score_str = request.vars.get('grade', 0)
    if score_str == "":
        score = 0
    else:
        score = float(score_str)
    comment = request.vars.get('comment', None)
    if score_str != "" or ('comment' in request.vars and comment != ""):
        try:
            db.question_grades.update_or_insert(( \
                        (db.question_grades.sid == request.vars['sid']) \
                        & (db.question_grades.div_id == request.vars['acid']) \
                        & (db.question_grades.course_name == auth.user.course_name) \
                ),
                sid=request.vars['sid'],
                div_id=request.vars['acid'],
                course_name=auth.user.course_name,
                score=score,
                comment=comment)
        except IntegrityError:
            logger.error(
                "IntegrityError {} {} {}".format(request.vars['sid'], request.vars['acid'], auth.user.course_name))
            return json.dumps({'response': 'not replaced'})
        return json.dumps({'response': 'replaced'})
    else:
        return json.dumps({'response': 'not replaced'})


# create a unique index:  question_grades_sid_course_name_div_id_idx" UNIQUE, btree (sid, course_name, div_id)

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def get_problem():
    if 'acid' not in request.vars or 'sid' not in request.vars:
        return json.dumps({'success': False, 'message': "Need problem and user."})

    user = db(db.auth_user.username == request.vars.sid).select().first()
    if not user:
        return json.dumps({'success': False, 'message': "User does not exist. Sorry!"})

    res = {
        'id': "%s-%d" % (request.vars.acid, user.id),
        'acid': request.vars.acid,
        'sid': user.id,
        'username': user.username,
        'name': "%s %s" % (user.first_name, user.last_name),
        'code': ""
    }

    # get the deadline associated with the assignment
    assignment_name = request.vars.assignment
    if assignment_name and auth.user.course_id:
        assignment = db(
            (db.assignments.name == assignment_name) & (db.assignments.course == auth.user.course_id)).select().first()
        deadline = assignment.duedate
    else:
        deadline = None

    offset = 0
    if session.timezoneoffset and deadline:
        offset = datetime.timedelta(hours=int(session.timezoneoffset))
        logger.debug("setting offset %s %s", offset, deadline + offset)

    query = (db.code.acid == request.vars.acid) & (db.code.sid == request.vars.sid) & (
            db.code.course_id == auth.user.course_id)
    if request.vars.enforceDeadline == "true" and deadline:
        query = query & (db.code.timestamp < deadline + offset)
        logger.debug("DEADLINE QUERY = %s", query)
    c = db(query).select(orderby=db.code.id).last()

    if c:
        res['code'] = c.code

    # add prefixes, suffix_code and files that are available
    # retrieve the db record
    source = db.source_code(acid=request.vars.acid, course_id=auth.user.course_name)

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
            # logger.debug(res['includes'])
        if source.suffix_code:
            res['suffix_code'] = source.suffix_code
            # logger.debug(source.suffix_code)

        file_divs = [x.strip() for x in source.available_files.split(',') if x != '']
        res['file_includes'] = [{'acid': acid, 'contents': get_source(acid)} for acid in file_divs]
    return json.dumps(res)


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def problem():
    ### For backward compatibility with old grading interface; shouldn't be used after transition
    ### This endpoint is hit either to update (if 'grade' and 'comment' are in request.vars)
    ### Or just to get the current state of the grade for this acid (if not present)
    if 'acid' not in request.vars or 'sid' not in request.vars:
        return json.dumps({'success': False, 'message': "Need problem and user."})

    user = db(db.auth_user.username == request.vars.sid).select().first()
    if not user:
        return json.dumps({'success': False, 'message': "User does not exist. Sorry!"})

    # get last timestamped record
    # null timestamps come out at the end, so the one we want could be in the middle, whether we sort in reverse order or regular; ugh
    # solution: the last one by id order should be the last timestamped one, as we only create ones without timestamp during grading, and then only if there is no existing record
    c = db((db.code.acid == request.vars.acid) & (db.code.sid == request.vars.sid)).select(orderby=db.code.id).last()
    if 'grade' in request.vars and 'comment' in request.vars:
        # update grade
        try:
            grade = float(request.vars.grade)
        except:
            grade = 0.0
            logger.debug("failed to convert {} to float".format(request.vars.grade))
            session.flash = "Grade must be a float 0.0 is recorded"

        comment = request.vars.comment
        if c:
            c.update_record(grade=grade, comment=comment)
        else:
            id = db.code.insert(
                acid=request.vars.acid,
                sid=user.username,
                grade=request.vars.grade,
                comment=request.vars.comment,
            )
            c = db.code(id)

    res = {
        'id': "%s-%d" % (request.vars.acid, user.id),
        'acid': request.vars.acid,
        'sid': user.id,
        'username': user.username,
        'name': "%s %s" % (user.first_name, user.last_name),
    }

    if c:
        # return the existing code, grade, and comment
        res['code'] = c.code
        res['grade'] = c.grade
        res['comment'] = c.comment
        res['lang'] = c.language
    else:
        # default: return grade of 0.0 if nothing exists
        res['code'] = ""
        res['grade'] = 0.0
        res['comment'] = ""

    # add prefixes, suffix_code and files that are available
    # retrieve the db record
    source = db.source_code(acid=request.vars.acid, course_id=auth.user.course_name)

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
            # logger.debug(res['includes'])
        if source.suffix_code:
            res['suffix_code'] = source.suffix_code
            # logger.debug(source.suffix_code)

        file_divs = [x.strip() for x in source.available_files.split(',') if x != '']
        res['file_includes'] = [{'acid': acid, 'contents': get_source(acid)} for acid in file_divs]
    return json.dumps(res)


def mass_grade_problem():
    if 'csv' not in request.vars or 'acid' not in request.vars:
        return json.dumps({"success": False})
    scores = []
    for row in request.vars.csv.split("\n"):
        cells = row.split(",")
        if len(cells) < 2:
            continue

        email = cells[0]
        if cells[1] == "":
            cells[1] = 0
        grade = float(cells[1])
        if len(cells) == 2:
            comment = ""
        else:  # should only ever be 2 or 3
            comment = cells[-1]  # comment should be the last element
        user = db(db.auth_user.email == email).select().first()
        if user == None:
            continue
        q = db(db.code.acid == request.vars.acid)(db.code.sid == user.username).select().first()
        if not q:
            db.code.insert(
                acid=request.vars.acid,
                sid=user.username,
                grade=request.vars.grade,
                comment=request.vars.comment,
            )
        else:
            db((db.code.acid == request.vars.acid) &
               (db.code.sid == user.username)
               ).update(
                grade=grade,
                comment=comment,
            )
        scores.append({
            'acid': request.vars.acid,
            'username': user.username,
            'grade': grade,
            'comment': comment,
        })
    return json.dumps({
        "success": True,
        "scores": scores,
    })


def migrate_to_scores():
    """ Temp command to migrate db.code grades to db.score table """

    accumulated_scores = {}
    code_rows = db(db.code.grade != None).select(
        db.code.ALL,
        orderby=db.code.acid | db.code.timestamp,
        distinct=db.code.acid,
    )
    for row in code_rows:
        if row.sid not in accumulated_scores:
            accumulated_scores[row.sid] = {}
        if row.acid not in accumulated_scores[row.sid]:
            accumulated_scores[row.sid][row.acid] = {
                'score': row.grade,
                'comment': row.comment,
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
                acid=acid,
                auth_user=user.id,
                score=accumulated_scores[sid][acid]['score'],
                comment=accumulated_scores[sid][acid]['comment'],
            )
            acid_count += 1
    session.flash = "Set %d scores for %d users" % (acid_count, user_count)
    return redirect(URL("assignments", "index"))


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def download():
    course = db(db.courses.id == auth.user.course_id).select().first()
    students = db(db.auth_user.course_id == course.id).select()
    assignments = db(db.assignments.course == course.id)(
        db.assignments.assignment_type == db.assignment_types.id).select(orderby=db.assignments.assignment_type)
    grades = db(db.grades).select()

    field_names = ['Lastname', 'Firstname', 'Email', 'Total']
    type_names = []
    assignment_names = []

    assignment_types = db(db.assignment_types).select(db.assignment_types.ALL, orderby=db.assignment_types.name)
    rows = [
        CourseGrade(user=student, course=course, assignment_types=assignment_types).csv(type_names, assignment_names)
        for student in students]
    response.view = 'generic.csv'
    return dict(filename='grades_download.csv', csvdata=rows, field_names=field_names + type_names + assignment_names)


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def newtype():
    form = SQLFORM(db.assignment_types,
                   fields=['name', 'grade_type', 'weight', 'points_possible', 'assignments_dropped'], )

    course = db(db.courses.id == auth.user.course_id).select().first()
    form.vars.course = course.id

    if form.process().accepted:
        session.flash = 'assignment type added'
        return redirect(URL('admin', 'index'))

    return dict(form=form)


def doAssignment():
    if not auth.user:
        session.flash = "Please Login"
        return redirect(URL('default', 'index'))

    course = db(db.courses.id == auth.user.course_id).select().first()
    assignment_id = request.vars.assignment_id
    if not assignment_id or assignment_id.isdigit() == False:
        logger.error("BAD ASSIGNMENT = %s assignment %s", course, assignment_id)
        session.flash = "Bad Assignment ID"
        return redirect(URL("assignments", "chooseAssignment"))

    logger.debug("COURSE = %s assignment %s", course, assignment_id)
    assignment = db(
        (db.assignments.id == assignment_id) & (db.assignments.course == auth.user.course_id)).select().first()

    if not assignment:
        logger.error("NO ASSIGNMENT assign_id = %s course = %s user = %s", assignment_id, course, auth.user.username)
        session.flash = "Could not find login and try again."
        return redirect(URL('default', 'index'))

    if assignment.visible == 'F' or assignment.visible == None:
        if verifyInstructorStatus(auth.user.course_name, auth.user) == False:
            session.flash = "That assignment is no longer available"
            return redirect(URL('assignments', 'chooseAssignment'))

    questions = db((db.assignment_questions.assignment_id == assignment.id) & \
                   (db.assignment_questions.question_id == db.questions.id)) \
        .select(db.questions.name,
                db.questions.htmlsrc,
                db.questions.id,
                db.questions.chapter,
                db.questions.subchapter,
                db.assignment_questions.points,
                db.assignment_questions.activities_required,
                db.assignment_questions.reading_assignment,
                orderby=db.assignment_questions.sorting_priority)

    questionslist = []
    questions_score = 0
    readings = OrderedDict()
    readings_score = 0

    # For each question, accumulate information, and add it to either the readings or questions data structure
    # If scores have not been released for the question or if there are no scores yet available, the scoring information will be recorded as empty strings

    for q in questions:
        if q.questions.htmlsrc:
            # This replacement is to render images
            htmlsrc = bytes(q.questions.htmlsrc).decode('utf8').replace('src="../_static/', 'src="../static/' + course[
                'course_name'] + '/_static/')
            htmlsrc = htmlsrc.replace("../_images",
                                      "/{}/static/{}/_images".format(request.application, course.course_name))
        else:
            htmlsrc = None
        if assignment['released']:
            # get score and comment
            grade = db((db.question_grades.sid == auth.user.username) &
                       (db.question_grades.div_id == q.questions.name)).select().first()
            if grade:
                score, comment = grade.score, grade.comment
            else:
                score, comment = 0, 'ungraded'
        else:
            score, comment = 0, 'ungraded'

        info = dict(
            htmlsrc=htmlsrc,
            score=score,
            points=q.assignment_questions.points,
            comment=comment,
            chapter=q.questions.chapter,
            subchapter=q.questions.subchapter,
            name=q.questions.name,
            activities_required=q.assignment_questions.activities_required
        )
        if q.assignment_questions.reading_assignment:
            # add to readings
            if q.questions.chapter not in readings:
                # add chapter info
                completion = db((db.user_chapter_progress.user_id == auth.user.id) & \
                                (db.user_chapter_progress.chapter_id == q.questions.chapter)).select().first()
                if not completion:
                    status = 'notstarted'
                elif completion.status == 1:
                    status = 'completed'
                elif completion.status == 0:
                    status = 'started'
                else:
                    status = 'notstarted'
                readings[q.questions.chapter] = dict(status=status, subchapters=[])

            # add subchapter info
            # add completion status to info
            subch_completion = db((db.user_sub_chapter_progress.user_id == auth.user.id) & \
                                  (
                                          db.user_sub_chapter_progress.sub_chapter_id == q.questions.subchapter)).select().first()
            if not subch_completion:
                status = 'notstarted'
            elif subch_completion.status == 1:
                status = 'completed'
            elif subch_completion.status == 0:
                status = 'started'
            else:
                status = 'notstarted'
            info['status'] = status

            readings[q.questions.chapter]['subchapters'].append(info)
            readings_score += info['score']
        else:
            # add to questions
            questionslist.append(info)
            questions_score += info['score']

    return dict(course=course,
                course_name=auth.user.course_name,
                assignment=assignment,
                questioninfo=questionslist,
                course_id=auth.user.course_name,
                readings=readings,
                questions_score=questions_score,
                readings_score=readings_score)


def chooseAssignment():
    if not auth.user:
        session.flash = "Please Login"
        return redirect(URL('default', 'index'))

    course = db(db.courses.id == auth.user.course_id).select().first()
    assignments = db((db.assignments.course == course.id) & (db.assignments.visible == 'T')).select(
        orderby=db.assignments.duedate)
    return (dict(assignments=assignments))


# The rest of the file is about the the spaced practice:


# Called when user clicks "I'm done" button.
def checkanswer():
    if not auth.user:
        session.flash = "Please Login"
        return redirect(URL('default', 'index'))

    sid = auth.user.id
    course_name = auth.user.course_name
    # Retrieve the question id from the request object.
    qid = request.vars.get('QID', None)
    username = auth.user.username
    # Retrieve the q (quality of answer) from the request object.
    q = request.vars.get('q', None)

    # If the question id exists:
    if request.vars.QID:
        now = datetime.datetime.utcnow() - datetime.timedelta(hours=int(session.timezoneoffset))
        # Use the autograding function to update the flashcard's e-factor and i-interval.
        do_check_answer(sid, course_name, qid, username, q, db, settings, now)
        # Since the user wants to continue practicing, continue with the practice action.
        redirect(URL('practice'))
    session.flash = "Sorry, your score was not saved. Please try submitting your answer again."
    redirect(URL('practice'))


# Only questions that are marked for practice are eligible for the spaced practice.
def _get_qualified_questions(base_course, chapter_label, sub_chapter_label):
    return db((db.questions.base_course == base_course) & \
              (db.questions.topic == "{}/{}".format(chapter_label, sub_chapter_label)) & \
              (db.questions.practice == True)).select()

# Gets invoked from lti to set timezone and then redirect to practice()
def settz_then_practice():
    return dict(course_name=request.vars.get('course_name', 'UMSI106'))

# Gets invoked when the student requests practicing topics.
def practice():
    if not auth.user:
        session.flash = "Please Login"
        return redirect(URL('default', 'index'))

    now = datetime.datetime.utcnow() - datetime.timedelta(hours=int(session.timezoneoffset))

    # Calculates the remaining days to the end of the semester. If your semester ends at any time other than April 19,
    # 2018, please replace it.
    remaining_days = (datetime.date(2018, 4, 19) - now.date()).days

    # Since each authenticated user has only one active course, we retrieve the course this way.
    course = db(db.courses.id == auth.user.course_id).select().first()

    # Retrieve the existing flashcards in the current course for this user.
    existing_flashcards = db((db.user_topic_practice.course_name == auth.user.course_name) & \
                             (db.user_topic_practice.user_id == auth.user.id))

    # If the user already has flashcards for the current course.
    if existing_flashcards.isempty():
        # new student; create flashcards
        # We only create flashcards for those sections that are marked by the instructor as taught.
        subchaptersTaught = db((db.sub_chapter_taught.course_name == auth.user.course_name) & \
                               (db.sub_chapter_taught.chapter_name == db.chapters.chapter_name) & \
                               (db.sub_chapter_taught.sub_chapter_name == db.sub_chapters.sub_chapter_name) & \
                               (db.chapters.course_id == auth.user.course_name) & \
                               (db.sub_chapters.chapter_id == db.chapters.id)) \
            .select(db.chapters.chapter_label, db.chapters.chapter_name, db.sub_chapters.sub_chapter_label,
                    orderby=db.chapters.id | db.sub_chapters.id)
        for subchapterTaught in subchaptersTaught:
            # We only retrive questions to be used in flashcards if they are marked for practice purpose.
            questions = _get_qualified_questions(course.base_course,
                                                 subchapterTaught.chapters.chapter_label,
                                                 subchapterTaught.sub_chapters.sub_chapter_label)
            if len(questions) > 0:
                # There is at least one qualified question in this subchapter, so insert a flashcard for the subchapter.
                db.user_topic_practice.insert(
                    user_id=auth.user.id,
                    course_name=auth.user.course_name,
                    chapter_label=subchapterTaught.chapters.chapter_label,
                    sub_chapter_label=subchapterTaught.sub_chapters.sub_chapter_label,
                    question_name=questions[0].name,
                    # Treat it as if the first eligible question is the last one asked.
                    i_interval=0,
                    e_factor=2.5,
                    # add as if yesterday, so can practice right away
                    last_presented=now.date() - datetime.timedelta(1),
                    last_completed=now.date() - datetime.timedelta(1),
                )

    # How many times has this user submitted their practice from the beginning of today (12:00 am) till now?
    practiced_today_count = db((db.user_topic_practice_log.course_name == auth.user.course_name) & \
                               (db.user_topic_practice_log.user_id == auth.user.id) & \
                               (db.user_topic_practice_log.q != 0) & \
                               (db.user_topic_practice_log.end_practice >= datetime.datetime(now.year,
                                                                                             now.month,
                                                                                             now.day,
                                                                                             0, 0, 0, 0))).count()
    # Retrieve all the falshcards created for this user in the current course and order them by their order of creation.
    flashcards = db((db.user_topic_practice.course_name == auth.user.course_name) & \
                    (db.user_topic_practice.user_id == auth.user.id)).select(orderby=db.user_topic_practice.id)
    # Select only those where enough time has passed since last presentation.
    presentable_flashcards = [f for f in flashcards if
                              (now.date() - f.last_completed.date()).days >= f.i_interval]

    all_flashcards = db((db.user_topic_practice.course_name == auth.user.course_name) & \
                        (db.user_topic_practice.user_id == auth.user.id) & \
                        (db.user_topic_practice.chapter_label == db.chapters.chapter_label) & \
                        (db.user_topic_practice.sub_chapter_label == db.sub_chapters.sub_chapter_label) & \
                        (db.chapters.course_id == auth.user.course_name) & \
                        (db.sub_chapters.chapter_id == db.chapters.id)) \
            .select(db.chapters.chapter_name, db.sub_chapters.sub_chapter_name, db.user_topic_practice.i_interval,
                db.user_topic_practice.last_completed, orderby=db.user_topic_practice.id)
    for f_card in all_flashcards:
        f_card["remaining_days"] = max(0, f_card.user_topic_practice.i_interval -
                                       (now.date() - f_card.user_topic_practice.last_completed.date()).days)
        f_card["mastery_percent"] = int(100 * f_card["remaining_days"] // 55)
        f_card["mastery_color"] = "danger"
        if f_card["mastery_percent"] >= 75:
            f_card["mastery_color"] = "success"
        elif f_card["mastery_percent"] >= 50:
            f_card["mastery_color"] = "info"
        elif f_card["mastery_percent"] >= 25:
            f_card["mastery_color"] = "warning"

    # Define how many topics you expect your students practice every day.
    practice_times_to_pass_today = 10

    # If the student has any flashcards to practice and has not practiced enough to get their points for today or they
    # have intrinsic motivation to practice beyond what they are expected to do.
    if len(presentable_flashcards) > 0 and (practiced_today_count != practice_times_to_pass_today or
                                            request.vars.willing_to_continue):
        # Ppresent the first one.
        flashcard = presentable_flashcards[0]
        # Get eligible questions.
        questions = _get_qualified_questions(course.base_course,
                                             flashcard.chapter_label,
                                             flashcard.sub_chapter_label)
        # Find index of the last question asked.
        question_names = [q.name for q in questions]
        qIndex = question_names.index(flashcard.question_name)
        # present the next one in the list after the last one that was asked
        question = questions[(qIndex + 1) % len(questions)]

        # This replacement is to render images
        question.htmlsrc = bytes(question.htmlsrc).decode('utf8').replace('src="../_static/',
                                                                          'src="../static/' + course[
                                                                              'course_name'] + '/_static/')
        question.htmlsrc = question.htmlsrc.replace("../_images",
                                                    "/{}/static/{}/_images".format(request.application,
                                                                                   course.course_name))

        autogradable = 1
        # If it is possible to autograde it:
        if ((question.autograde is not None) or
                (question.question_type is not None and question.question_type in
                 ['mchoice', 'parsonsprob', 'fillintheblank', 'clickablearea', 'dragndrop'])):
            autogradable = 2

        questioninfo = [question.htmlsrc, question.name, question.id, autogradable]

        # This is required to check the same question in do_check_answer().
        flashcard.question_name = question.name
        # This is required to only check answers after this timestamp in do_check_answer().
        flashcard.last_presented = now
        flashcard.update_record()

    else:
        questioninfo = None

        # Add a practice completion record for today, if there isn't one already.
        practice_completion_today = db((db.user_topic_practice_Completion.course_name == auth.user.course_name) & \
                                       (db.user_topic_practice_Completion.user_id == auth.user.id) & \
                                       (db.user_topic_practice_Completion.practice_completion_time == now.date()))
        if practice_completion_today.isempty():
            db.user_topic_practice_Completion.insert(
                user_id=auth.user.id,
                course_name=auth.user.course_name,
                practice_completion_time=now.date()
            )

    # The number of days the student has completed their practice.
    practice_completion_count = db((db.user_topic_practice_Completion.course_name == auth.user.course_name) & \
                                   (db.user_topic_practice_Completion.user_id == auth.user.id)).count()

    # Calculate the number of times left for the student to practice today to get the completion point.
    practice_today_left = min(len(presentable_flashcards), max(0, practice_times_to_pass_today - practiced_today_count))

    return dict(course=course, course_name=auth.user.course_name,
                course_id=auth.user.course_name,
                q=questioninfo, all_flashcards=all_flashcards,
                flashcard_count=len(presentable_flashcards),
                # The number of days the student has completed their practice.
                practice_completion_count=practice_completion_count,
                remaining_days=remaining_days, max_days=45,
                # The number of times remaining to practice today to get the completion point.
                practice_today_left=practice_today_left,
                # The number of times this user has submitted their practice from the beginning of today (12:00 am) till now.
                practiced_today_count=practiced_today_count)


# Called when user clicks like or dislike icons.
def like_dislike():
    if not auth.user:
        session.flash = "Please Login"
        return redirect(URL('default', 'index'))

    sid = auth.user.id
    course_name = auth.user.course_name
    likeVal = request.vars.get('likeVal', None)

    if likeVal:
        db.user_topic_practice_survey.insert(
            user_id=sid,
            course_name=course_name,
            like_practice=likeVal,
            response_time=datetime.datetime.now(),
        )
        return json.dumps(dict(complete=True))
    session.flash = "Sorry, your request was not saved. Please login and try again."
    redirect(URL('practice'))
