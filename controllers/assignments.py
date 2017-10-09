from os import path
import os
import shutil
import sys
import json
import logging
import datetime
from psycopg2 import IntegrityError

logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)

# controller for "Progress Page" as well as List/create assignments
def index():
    if not auth.user:
        session.flash = "Please Login"
        return redirect(URL('default','index'))
    if 'sid' not in request.vars:
        return redirect(URL('assignments','index') + '?sid=%s' % (auth.user.username))

    student = db(db.auth_user.username == request.vars.sid).select(
        db.auth_user.id,
        db.auth_user.username,
        db.auth_user.first_name,
        db.auth_user.last_name,
        db.auth_user.email,
        ).first()
    if not student:
        return redirect(URL('assignments','index'))

    if auth.user.course_name in ['thinkcspy','pythonds','JavaReview','webfundamentals','StudentCSP','apcsareview']:
        session.flash = "{} is not a graded course".format(auth.user.course_name)
        return redirect(URL('default','user'))

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

    return dict(student=student, course_id=auth.user.course_id, course_name=auth.user.course_name, user=data_analyzer.user, chapters=chapters, activity=activity, assignments=data_analyzer.grades)

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
        fields=['name','points','assignment_type'],
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
            fields=['name','points','assignment_type','released'],
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

def _score_from_pct_correct(pct_correct, points, autograde):
    # ALL_AUTOGRADE_OPTIONS = ['all_or_nothing', 'pct_correct', 'interact']
    if autograde == 'interact' or autograde == 'visited':
        return points
    elif autograde == 'pct_correct':
        # prorate credit based on percentage correct
        return int(round((pct_correct * points)/100.0))
    elif autograde == 'all_or_nothing' or autograde == 'unittest':
        # 'unittest' is legacy, now deprecated
        # have to get *all* tests to pass in order to get any credit
        if pct_correct == 100:
            return points
        else:
            return 0


def _score_one_code_run(row, points, autograde):
    # row is one row from useinfo table
    # second element of act is the percentage of tests that passed
    if autograde == 'interact':
        return _score_one_interaction(row, points, autograde)

    try:
        (ignore, pct, ignore, passed, ignore, failed) = row.act.split(':')
        pct_correct = 100 * float(passed)/(int(failed) + int(passed))
    except:
        pct_correct = 0 # can still get credit if autograde is 'interact' or 'visited'; but no autograded value
    return _score_from_pct_correct(pct_correct, points, autograde)

def _score_one_mchoice(row, points, autograde):
    # row is from mchoice_answers
    ## It appears that the mchoice_answers is only storing a binary correct_or_not
    ## If that is updated to store a pct_correct, the next few lines can change
    if row.correct:
        pct_correct = 100
    else:
        pct_correct = 0
    return _score_from_pct_correct(pct_correct, points, autograde)

def _score_one_interaction(row, points, autograde):
    # row is from useinfo
    if row:
        return points
    else:
        return 0

def _score_one_parsons(row, points, autograde):
    # row is from parsons_answers
    # Much like mchoice, parsons_answers currently stores a binary correct value
    # So much like in _score_one_mchoice, the next lines can be altered if a pct_correct value is added to parsons_answers
    if row.correct:
        pct_correct = 100
    else:
        pct_correct = 0
    return _score_from_pct_correct(pct_correct, points, autograde)

def _score_one_fitb(row, points, autograde):
    # row is from fitb_answers
    if row.correct:
        pct_correct = 100
    else:
        pct_correct = 0
    return _score_from_pct_correct(pct_correct, points, autograde)

def _score_one_clickablearea(row, points, autograde):
    # row is from clickablearea_answers
    if row.correct:
        pct_correct = 100
    else:
        pct_correct = 0
    return _score_from_pct_correct(pct_correct, points, autograde)

def _score_one_dragndrop(row, points, autograde):
    # row is from dragndrop_answers
    if row.correct:
        pct_correct = 100
    else:
        pct_correct = 0
    return _score_from_pct_correct(pct_correct, points, autograde)

def _score_one_codelens(row, points, autograde):
    # row is from codelens_answers
    if row.correct:
        pct_correct = 100
    else:
        pct_correct = 0
    return _score_from_pct_correct(pct_correct, points, autograde)


def _scorable_mchoice_answers(course_name, sid, question_name, points, deadline):
    query = ((db.mchoice_answers.course_name == course_name) & \
            (db.mchoice_answers.sid == sid) & \
            (db.mchoice_answers.div_id == question_name) \
            )
    if deadline:
        query = query & (db.mchoice_answers.timestamp < deadline)
    return db(query).select(orderby=db.mchoice_answers.timestamp)

def _scorable_useinfos(course_name, sid, div_id, points, deadline, event_filter = None, question_type=None):
    # look in useinfo, to see if visited (before deadline)
    # sid matches auth_user.username, not auth_user.id
    # if question type is page we must do better with the div_id

    query = ((db.useinfo.course_id == course_name) & \
            (db.useinfo.sid == sid))

    if question_type == 'page':
        quest = db(db.questions.name == div_id).select().first()
        div_id = u"{}/{}".format(quest.chapter, quest.subchapter)
        query = query & (db.useinfo.div_id.contains(div_id))
    else:
        query = query & (db.useinfo.div_id == div_id)

    if event_filter:
        query = query & (db.useinfo.event == event_filter)
    if deadline:
        query = query & (db.useinfo.timestamp < deadline)
    return db(query).select(orderby=db.useinfo.timestamp)

def _scorable_parsons_answers(course_name, sid, question_name, points, deadline):
    query = ((db.parsons_answers.course_name == course_name) & \
            (db.parsons_answers.sid == sid) & \
            (db.parsons_answers.div_id == question_name) \
            )
    if deadline:
        query = query & (db.parsons_answers.timestamp < deadline)
    return db(query).select(orderby=db.parsons_answers.timestamp)

def _scorable_fitb_answers(course_name, sid, question_name, points, deadline):
    query = ((db.fitb_answers.course_name == course_name) & \
            (db.fitb_answers.sid == sid) & \
            (db.fitb_answers.div_id == question_name) \
            )
    if deadline:
        query = query & (db.fitb_answers.timestamp < deadline)
    return db(query).select(orderby=db.fitb_answers.timestamp)

def _scorable_clickablearea_answers(course_name, sid, question_name, points, deadline):
    query = ((db.clickablearea_answers.course_name == course_name) & \
            (db.clickablearea_answers.sid == sid) & \
            (db.clickablearea_answers.div_id == question_name) \
            )
    if deadline:
        query = query & (db.clickablearea_answers.timestamp < deadline)
    return db(query).select(orderby=db.clickablearea_answers.timestamp)

def _scorable_dragndrop_answers(course_name, sid, question_name, points, deadline):
    query = ((db.dragndrop_answers.course_name == course_name) & \
            (db.dragndrop_answers.sid == sid) & \
            (db.dragndrop_answers.div_id == question_name) \
            )
    if deadline:
        query = query & (db.dragndrop_answers.timestamp < deadline)
    return db(query).select(orderby=db.dragndrop_answers.timestamp)

def _scorable_codelens_answers(course_name, sid, question_name, points, deadline):
    query = ((db.codelens_answers.course_name == course_name) & \
            (db.codelens_answers.sid == sid) & \
            (db.codelens_answers.div_id == question_name) \
            )
    if deadline:
        query = query & (db.codelens_answers.timestamp < deadline)

    return db(query).select(orderby=db.codelens_answers.timestamp)

def _autograde_one_q(course_name, sid, question_name, points, question_type, deadline=None, autograde=None, which_to_grade=None, save_score=True):
    logger.debug("autograding %s %s %s %s %s %s", course_name, question_name, sid, deadline, autograde, which_to_grade)


    if not autograde:
        logger.debug("autograde not set returning 0")
        return 0

    # if previously manually graded, don't overwrite
    existing = db((db.question_grades.sid == sid) \
       & (db.question_grades.course_name == course_name) \
       & (db.question_grades.div_id == question_name) \
       ).select().first()
    if existing and (existing.comment != "autograded"):
        logger.debug("skipping; previously manually graded, comment = {}".format(existing.comment))
        return 0


    # For all question types, and values of which_to_grade, we have the same basic structure:
    # 1. Query the appropriate table to get rows representing student responses
    # 2. Apply a scoring function to the first, last, or all rows
    #   2a. if scoring 'best_answer', take the max score
    #   Note that the scoring function will take the autograde parameter as an input, which might
    #      affect how the score is determined.

    # get the results from the right table, and choose the scoring function
    if question_type in ['activecode', 'actex']:
        if autograde in ['pct_correct', 'all_or_nothing', 'unittest']:
            event_filter = 'unittest'
        else:
            event_filter = None
        results = _scorable_useinfos(course_name, sid, question_name, points, deadline, event_filter)
        scoring_fn = _score_one_code_run
    elif question_type == 'mchoice':
        results = _scorable_mchoice_answers(course_name, sid, question_name, points, deadline)
        scoring_fn = _score_one_mchoice
    elif question_type == 'page':
        # question_name does not help us
        results = _scorable_useinfos(course_name, sid, question_name, points, deadline, question_type='page')
        scoring_fn = _score_one_interaction
    elif question_type == 'parsonsprob':
        results = _scorable_parsons_answers(course_name, sid, question_name, points, deadline)
        scoring_fn = _score_one_parsons
    elif question_type == 'fillintheblank':
        results = _scorable_fitb_answers(course_name, sid, question_name, points, deadline)
        scoring_fn = _score_one_fitb
    elif question_type == 'clickablearea':
        results = _scorable_clickablearea_answers(course_name, sid, question_name, points, deadline)
        scoring_fn = _score_one_clickablearea
    elif question_type == 'dragndrop':
        results = _scorable_dragndrop_answers(course_name, sid, question_name, points, deadline)
        scoring_fn = _score_one_dragndrop
    elif question_type == 'codelens':
        if autograde == 'interact':  # this is probably what we want for *most* codelens it will not be correct when it is an actual codelens question in a reading
            results = _scorable_useinfos(course_name, sid, question_name, points, deadline)
            scoring_fn = _score_one_interaction
        else:
            results = _scorable_codelens_answers(course_name, sid, question_name, points, deadline)
            scoring_fn = _score_one_codelens
    elif question_type in ['video', 'showeval']:
        # question_name does not help us
        results = _scorable_useinfos(course_name, sid, question_name, points, deadline, question_type='video')
        scoring_fn = _score_one_interaction

    else:
        logger.debug("skipping; question_type = {}".format(question_type))
        return 0

    # use query results and the scoring function
    if results:
        if which_to_grade in ['first_answer', 'last_answer', None]:
            # get single row
            if which_to_grade == 'first_answer':
                row = results.first()
            elif which_to_grade == 'last_answer':
                row = results.last()
            else:
                # default is last
                row = results.last()
            # extract its score and id
            id = row.id
            score = scoring_fn(row, points, autograde)
        elif which_to_grade == 'best_answer':
            # score all rows and take the best one
            best_row = max(results, key = lambda row: scoring_fn(row, points, autograde))
            id = best_row.id
            score = scoring_fn(best_row, points, autograde)
            logger.debug("SCORE = %s by %s", score, scoring_fn)
        else:
            logger.error("Unknown Scoring Scheme %s ", which_to_grade)
            id = 0
            score = 0
    else:
        # no results found, score is 0, not attributed to any row
        id = None
        score = 0

    # Save the score
    if save_score:
        _save_question_grade(sid, course_name, question_name, score, id)

    return score

def _save_question_grade(sid, course_name, question_name, score, id):
    try:
        db.question_grades.update_or_insert(
            ((db.question_grades.sid == sid) &
            (db.question_grades.course_name == course_name) &
            (db.question_grades.div_id == question_name)
            ),
            sid=sid,
            course_name=course_name,
            div_id=question_name,
            score = score,
            comment = "autograded",
            useinfo_id = id
        )
    except IntegrityError:
        logger.error("IntegrityError {} {} {}".format(sid, course_name, question_name))


def _compute_assignment_total(student, assignment, course_name):
    # return the computed score and the manual score if there is one; if no manual score, save computed score
    # student is a row, containing id and username
    # assignment is a row, containing name and id and points

    # Get all question_grades for this sid/assignment_id
    # Retrieve from question_grades table  with right sids and div_ids
    # sid is really a username, so look it up in auth_user
    # div_id is found in questions; questions are associated with assignments, which have assignment_id

    # print(student.id, assignment.id)

    # compute the score
    query =  (db.question_grades.sid == student.username) \
             & (db.question_grades.div_id == db.questions.name) \
             & (db.questions.id == db.assignment_questions.question_id) \
             & (db.assignment_questions.assignment_id == assignment.id) \
             & (db.question_grades.course_name == course_name )
    scores = db(query).select(db.question_grades.score)
    logger.debug("List of scores to add for %s is %s",student.username, scores)
    total = sum([row.score for row in scores if row.score])
    score = total

    grade = db(
        (db.grades.auth_user == student.id) &
        (db.grades.assignment == assignment.id)).select().first()

    if grade and grade.manual_total:
        # don't save it; return the calculated and the previous manual score
        return score, grade.score
    else:
        # Write the score to the grades table
        try:
            db.grades.update_or_insert(
                ((db.grades.auth_user == student.id) &
                 (db.grades.assignment == assignment.id)),
                auth_user = student.id,
                assignment = assignment.id,
                score=score)
        except IntegrityError:
            logger.error("IntegrityError update or insert {} {} with score {}"
                         .format(student.id, assignment.id, score))
        return score, None

def _get_students(course_id, sid = None):
    if sid:
        # sid which is passed in is a username, not a row id
        student_rows = db((db.user_courses.course_id == course_id) &
                          (db.user_courses.user_id == db.auth_user.id) &
                          (db.auth_user.username == sid)
                          ).select(db.auth_user.username, db.auth_user.id)
    else:
        # get all student usernames for this course
        student_rows = db((db.user_courses.course_id == course_id) &
                          (db.user_courses.user_id == db.auth_user.id)
                          ).select(db.auth_user.username, db.auth_user.id)
    return student_rows

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def record_assignment_score():
    score = request.vars.get('score', None)
    assignment_name = request.vars.assignment
    assignment = db((db.assignments.name == assignment_name) & (db.assignments.course == auth.user.course_id)).select().first()
    if assignment:
        assignment_id = assignment.id
    else:
        return json.dumps({'success':False, 'message':"Select an assignment before trying to calculate totals."})

    if score:
        # Write the score to the grades table
        # grades table expects row ids for auth_user and assignment
        sname = request.vars.get('sid', None)
        sid = db((db.auth_user.username == sname)).select(db.auth_user.id).first().id
        db.grades.update_or_insert(
            ((db.grades.auth_user == sid) &
            (db.grades.assignment == assignment_id)),
            auth_user = sid,
            assignment = assignment_id,
            score=score,
            manual_total=True
        )

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def calculate_totals():
    assignment_name = request.vars.assignment
    assignment = db((db.assignments.name == assignment_name) & (db.assignments.course == auth.user.course_id)).select().first()
    if assignment:
        assignment_id = assignment.id
    else:
        return json.dumps({'success':False, 'message':"Select an assignment before trying to calculate totals."})

    sid = request.vars.get('sid', None)

    student_rows = _get_students(auth.user.course_id, sid)

    results = {'success':True}
    if sid:
        computed_total, manual_score = _compute_assignment_total(student_rows[0], assignment, auth.user.course_name)
        results['message'] = "Total for {} is {}".format(sid, computed_total)
        results['computed_score'] = computed_total
        results['manual_score'] = manual_score
    else:
        # compute total score for the assignment for each sid; also saves in DB unless manual value saved
        scores = [_compute_assignment_total(student, assignment, auth.user.course_name)[0] for student in student_rows]
        results['message'] = "Calculated totals for {} students\n\tmax: {}\n\tmin: {}\n\tmean: {}".format(
            len(scores),
            max(scores),
            min(scores),
            sum(scores)/float(len(scores))
        )

    return json.dumps(results)

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
    question_name = request.vars.get('question', None)
    enforce_deadline = request.vars.get('enforceDeadline', None)
    if enforce_deadline == 'true':
        # get the deadline associated with the assignment
        deadline = assignment.duedate
    else:
        deadline = None

    if 'timezoneoffset' in session and deadline:
        deadline = deadline + datetime.timedelta(hours=int(session.timezoneoffset))
        logger.debug("ASSIGNMENT DEADLINE OFFSET %s",deadline)

    student_rows = _get_students(auth.user.course_id, sid)
    sids = [row.username for row in student_rows]

    if question_name:
        questions_query = db(
            (db.assignment_questions.assignment_id == assignment_id) &
            (db.assignment_questions.question_id == db.questions.id) &
            (db.questions.name == question_name)
            ).select()
    else:
        # get all qids and point values for this assignment
        questions_query = db((db.assignment_questions.assignment_id == assignment_id) &
                             (db.assignment_questions.question_id == db.questions.id)
                             ).select()

    readings = [(row.questions.name,
                 row.questions.chapter,
                 row.questions.subchapter,
                 row.assignment_questions.points,
                 row.assignment_questions.activities_required,
                 row.assignment_questions.autograde,
                 row.assignment_questions.which_to_grade,
                 ) for row in questions_query if row.assignment_questions.reading_assignment == True]
    logger.debug("GRADING READINGS")
    # Now for each reading, get all of the questions in that subsection
    # call _autograde_one_q using the autograde and which to grade for that section. likely interact
    #
    base_course = row = db(db.courses.id == auth.user.course_id).select(db.courses.base_course).first().base_course
    count = 0
    for (name, chapter, subchapter, points, ar, ag, wtg) in readings:
        count += 1
        for s in sids:
            score = 0
            rows = db((db.questions.chapter == chapter) &
                      (db.questions.subchapter == subchapter) &
                      (db.questions.base_course == base_course)).select()
            for row in rows:
                score += _autograde_one_q(auth.user.course_name, s, row.name, 1, row.question_type,
                                          deadline=deadline, autograde=ag, which_to_grade=wtg, save_score=False )
                logger.debug("Score is now %s for %s for %s", score, row.name, auth.user.username)
            if score >= ar:
                save_points = points
                logger.debug("full points for %s on %s", auth.user.username, name)
            else:
                save_points = 0
                logger.debug("no points for %s on %s", auth.user.username, name)

            _save_question_grade(s, auth.user.course_name, name, save_points, None)

    logger.debug("GRADING QUESTIONS")
    questions = [(row.questions.name,
                  row.assignment_questions.points,
                  row.assignment_questions.autograde,
                  row.assignment_questions.which_to_grade,
                  row.questions.question_type) for row in questions_query
                  if row.assignment_questions.reading_assignment == False or
                     row.assignment_questions.reading_assignment == None]

    logger.debug("questions to grade = %s", questions)
    for (qdiv, points, autograde, which_to_grade, question_type) in questions:
        for s in sids:
            if autograde != 'manual':
                _autograde_one_q(auth.user.course_name, s, qdiv, points, question_type,
                                 deadline=deadline, autograde = autograde, which_to_grade = which_to_grade)
                count += 1

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
        try:
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
        except IntegrityError:
            logger.error("IntegrityError {} {} {}".format(request.vars['sid'], request.vars['acid'], auth.user.course_name))
            return json.dumps({'response': 'not replaced'})
        return json.dumps({'response': 'replaced'})
    else:
        return json.dumps({'response': 'not replaced'})

# create a unique index:  question_grades_sid_course_name_div_id_idx" UNIQUE, btree (sid, course_name, div_id)

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

    # get the deadline associated with the assignment
    assignment_name = request.vars.assignment
    if assignment_name and auth.user.course_id:
        assignment = db((db.assignments.name == assignment_name) & (db.assignments.course == auth.user.course_id)).select().first()
        deadline = assignment.duedate
    else:
        deadline = None

    offset = 0
    if session.timezoneoffset and deadline:
        offset = datetime.timedelta(hours=int(session.timezoneoffset))
        logger.debug("setting offset %s %s", offset, deadline+offset)

    query =  (db.code.acid == request.vars.acid) & (db.code.sid == request.vars.sid) & (db.code.course_id == auth.user.course_id)
    if request.vars.enforceDeadline == "true" and deadline:
        query = query & (db.code.timestamp < deadline + offset)
        logger.debug("DEADLINE QUERY = %s", query)
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
            #logger.debug(res['includes'])
        if source.suffix_code:
            res['suffix_code'] = source.suffix_code
            #logger.debug(source.suffix_code)

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
            grade = 0.0
            logger.debug("failed to convert {} to float".format(request.vars.grade))
            session.flash = "Grade must be a float 0.0 is recorded"

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

    res = {
        'id':"%s-%d" % (request.vars.acid, user.id),
        'acid':request.vars.acid,
        'sid':user.id,
        'username':user.username,
        'name':"%s %s" % (user.first_name, user.last_name),
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
            #logger.debug(res['includes'])
        if source.suffix_code:
            res['suffix_code'] = source.suffix_code
            #logger.debug(source.suffix_code)

        file_divs = [x.strip() for x in source.available_files.split(',') if x != '']
        res['file_includes'] = [{'acid': acid, 'contents': get_source(acid)} for acid in file_divs]
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

def doAssignment():
    if not auth.user:
        session.flash = "Please Login"
        return redirect(URL('default','index'))

    course = db(db.courses.id == auth.user.course_id).select().first()
    assignment_id = request.vars.assignment_id
    if not assignment_id or assignment_id.isdigit() == False:
        logger.error("BAD ASSIGNMENT = %s assignment %s", course, assignment_id)
        session.flash = "Bad Assignment ID"
        return redirect(URL("assignments","chooseAssignment"))

    logger.debug("COURSE = %s assignment %s", course, assignment_id)
    assignment = db((db.assignments.id == assignment_id) & (db.assignments.course == auth.user.course_id)).select().first()

    if not assignment:
        logger.error("NO ASSIGNMENT assign_id = %s course = %s user = %s",assignment_id, course, auth.user.username)
        session.flash = "Could not find login and try again."
        return redirect(URL('default','index'))

    questions_html = db((db.assignment_questions.assignment_id == assignment.id) & \
                        (db.assignment_questions.question_id == db.questions.id) & \
                        (db.assignment_questions.reading_assignment == None or db.assignment_questions.reading_assignment != 'T')) \
                        .select(db.questions.htmlsrc, db.questions.id, db.questions.chapter, db.questions.subchapter, db.questions.name, orderby=db.assignment_questions.sorting_priority)

    readings = db((db.assignment_questions.assignment_id == assignment.id) & \
                (db.assignment_questions.question_id == db.questions.id) & \
                (db.assignment_questions.reading_assignment == 'T')) \
                .select(db.questions.base_course, db.questions.name, orderby=db.assignment_questions.sorting_priority)

    questions_scores = db((db.assignment_questions.assignment_id == assignment.id) & \
                    (db.assignment_questions.question_id == db.questions.id) & \
                    (db.assignment_questions.reading_assignment == None or db.assignment_questions.reading_assignment != 'T') & \
                    (db.question_grades.sid == auth.user.username) & \
                    (db.question_grades.div_id == db.questions.name)) \
                    .select(db.questions.id, db.question_grades.score, db.question_grades.comment, db.assignment_questions.points, orderby=db.assignment_questions.sorting_priority)

    questionslist = []
    readingsDict = {}

    # The next for loop formats the readings information into readingsDict
    # The keys of readingsDict are ids in the chapters table
    # Each value is a list of lists detailing the information about each section within the assigned chapter
    # Chapter ids are used as keys so the dictionary can be iterated in the correct order within doAssignment.html

    # Because readings do not record chapters in the questions table
    # assigned readings cannot (nicely) be grouped into chapters by a DB query yet
    # so using a dictionary is a quick short-term solution to group all the sections to each chapter
    # The chapters will appear in the order that they do in the ToC,
    # but the sections within each chapter will appear according to the sorting_priority in assignment_questions

    # Once the questions table starts recording chapters for readings, a dictionary may not be needed anymore,
    # and the labels query won't be needed at all

    for r in readings:
        logger.debug("READING = %s",r.name)
        chapterSections = r.name.split('/')

        labels = db((db.chapters.chapter_name == chapterSections[0]) & \
                    (db.chapters.course_id == auth.user.course_name) & \
                    (db.chapters.id == db.sub_chapters.chapter_id) & \
                    (db.sub_chapters.sub_chapter_name == chapterSections[1])) \
                    .select(db.sub_chapters.chapter_id, db.sub_chapters.sub_chapter_name, db.sub_chapters.sub_chapter_label, db.chapters.chapter_name, db.chapters.chapter_label, db.chapters.id).first()
        logger.debug("LABELS = %s",labels)
        logger.debug("user_id = %s labels[chapters] = %s labels[sub_chapters] = %s",auth.user.id,labels['chapters'].chapter_label,labels['sub_chapters'].sub_chapter_label)
        completion = db((db.user_sub_chapter_progress.user_id == auth.user.id) & \
            (db.user_sub_chapter_progress.chapter_id == labels['chapters'].chapter_label) & \
            (db.user_sub_chapter_progress.sub_chapter_id == labels['sub_chapters'].sub_chapter_label)).select().first()

        # Sometimes when a sub-chapter is added to the book after the user has registerd and the
        # subchapter tables have been created you need to catch that and insert.
        if not completion:
            newid = db.user_sub_chapter_progress.insert(chapter_id=labels['chapters'].chapter_label,
                                                        sub_chapter_id=labels['sub_chapters'].sub_chapter_label,
                                                        status=-1,
                                                        user_id=auth.user.id)
            completion = db(db.user_sub_chapter_progress.id == newid).select().first()

        logger.debug("COMPLETION = %s",completion)
        chapterPath = (completion.chapter_id + '/toctree.html')
        sectionPath = (completion.chapter_id + '/' + completion.sub_chapter_id + '.html')

        if labels['chapters'].id not in readingsDict:
            readingsDict[labels['chapters'].id] = []

        if completion.status == 1:
            readingsDict[labels['chapters'].id].append([chapterSections[0], chapterPath, chapterSections[1], sectionPath, 'completed'])
        elif completion.status == 0:
            readingsDict[labels['chapters'].id].append([chapterSections[0], chapterPath, chapterSections[1], sectionPath, 'started'])
        else:
            readingsDict[labels['chapters'].id].append([chapterSections[0], chapterPath, chapterSections[1], sectionPath, 'notstarted'])

    # This is to get the chapters' completion states based on the completion of sections of the readings in assignments
    # The completion of chapters in reading assignments means that all the assigned sections for that specific chapter have been completed
    # This means chapter completion states within assignments will not always match up with chapter completion states in the ToC,
    # So the DB is not queried and instead the readingsDict is iterated through after it's been built.
    # Each chapter's completion gets appended to the first list within the list of section information for each chapter in the readingsDict
    for chapter in readingsDict:
        hasStarted = False
        completionState = 'completed'
        for s in readingsDict[chapter]:
            if s[4] == 'completed':
                hasStarted = True
            if s[4] == 'started':
                hasStarted = True
                completionState = 'started'
        if hasStarted:
            readingsDict[chapter][0].append(completionState)
        else:
            readingsDict[chapter][0].append('notstarted')

    currentqScore = 0

    # This formats questionslist into a list of lists.
    # Each list within questionslist represents a question and holds the question's html string to be rendered in the view and the question's scoring information
    # If scores have not been released for the question or if there are no scores yet available, the scoring information will be recorded as empty strings
    for q in questions_html:

        # It there is no html recorded, the question can't be rendered
        if q.htmlsrc != None:

            # This replacement is to render images
            q.htmlsrc = bytes(q.htmlsrc).decode('utf8').replace('src="../_static/', 'src="../static/' + course['course_name'] + '/_static/')
            q.htmlsrc = q.htmlsrc.replace("../_images","/{}/static/{}/_images".format(request.application,course.course_name))
            try:
                if q.id == questions_scores[currentqScore]['questions'].id  and assignment['released']:
                    questioninfo = [q.htmlsrc,
                                    questions_scores[currentqScore]['question_grades'].score,
                                    questions_scores[currentqScore]['assignment_questions'].points,
                                    questions_scores[currentqScore]['question_grades'].comment,
                                    q.chapter,
                                    q.subchapter,
                                    q.name]
                    currentqScore += 1
                else:
                    questioninfo  = [q.htmlsrc, '', '','',q.chapter,q.subchapter,q.name]
            except:
                # There are still questions, but no more recorded grades
                questioninfo  = [q.htmlsrc, '', '','',q.chapter,q.subchapter,q.name]

            questionslist.append(questioninfo)

    return dict(course=course, course_name=auth.user.course_name, assignment=assignment, questioninfo=questionslist, course_id=auth.user.course_name, readings=readingsDict)

def chooseAssignment():
    if not auth.user:
        session.flash = "Please Login"
        return redirect(URL('default','index'))

    course = db(db.courses.id == auth.user.course_id).select().first()
    assignments = db(db.assignments.course == course.id).select(orderby=db.assignments.duedate)
    return(dict(assignments=assignments))
