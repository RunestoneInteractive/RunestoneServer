# pylint: good-names=auth, settings, db

import logging
from operator import itemgetter
from collections import OrderedDict
import six
import pandas as pd
from db_dashboard import DashboardDataAnalyzer


logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)


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
    selected_chapter = None
    questions = []
    sections = []

    if settings.academy_mode and not settings.docker_institution_mode:
        if auth.user.course_name in ['thinkcspy','pythonds','JavaReview','JavaReview-RU', 'StudentCSP']:
            session.flash = "Student Progress page not available for {}".format(auth.user.course_name)
            return redirect(URL('admin','admin'))

    course = db(db.courses.id == auth.user.course_id).select().first()
    assignments = db(db.assignments.course == course.id).select(db.assignments.ALL, orderby=db.assignments.name)
    logger.debug("getting chapters for {}".format(auth.user.course_name))
    chapters = db(db.chapters.course_id == course.base_course).select()
    chap_map = {}
    for chapter in chapters:
        chap_map[chapter.chapter_label] = chapter.chapter_name
    for chapter in chapters.find(lambda chapter: chapter.chapter_label==request.vars['chapter']):
        selected_chapter = chapter
    if selected_chapter is None:
        selected_chapter = chapters.first()

    logger.debug("making an analyzer")
    data_analyzer = DashboardDataAnalyzer(auth.user.course_id,selected_chapter)
    logger.debug("loading chapter metrics for course {}".format(auth.user.course_name))
    data_analyzer.load_chapter_metrics(selected_chapter)
    logger.debug("loading problem metrics")
    problem_metrics = data_analyzer.problem_metrics
    logger.debug("loading progress_metrics metrics")
    progress_metrics = data_analyzer.progress_metrics

    logger.debug("starting problem_id, metric loop")
    for problem_id, metric in six.iteritems(problem_metrics.problems):
        stats = metric.user_response_stats()

        if data_analyzer.questions[problem_id]:
            chtmp = data_analyzer.questions[problem_id].chapter
            entry = {
                "id": problem_id,
                "text": metric.problem_text,
                "chapter": chtmp,
                "chapter_title": chap_map.get(chtmp,chtmp),
                "sub_chapter": data_analyzer.questions[problem_id].subchapter,
                "correct": stats[2],
                "correct_mult_attempt": stats[3],
                "incomplete": stats[1],
                "not_attempted": stats[0],
                "attemptedBy": stats[1] + stats[2] + stats[3]
                }
        else:
            entry = {
                "id": problem_id,
                "text": metric.problem_text,
                "chapter": "unknown",
                "sub_chapter": "unknown",
                "chapter_title": "unknown",
                "correct": stats[2],
                "correct_mult_attempt": stats[3],
                "incomplete": stats[1],
                "not_attempted": stats[0],
                "attemptedBy": stats[1] + stats[2] + stats[3]
                }
        questions.append(entry)
        logger.debug("ADDING QUESTION %s ", entry["chapter"])

    logger.debug("getting questsions")
    questions = sorted(questions, key=itemgetter("chapter"))
    logger.debug("starting sub_chapter loop")
    for sub_chapter, metric in six.iteritems(progress_metrics.sub_chapters):
        sections.append({
            "id": metric.sub_chapter_label,
            "text": metric.sub_chapter_text,
            "name": metric.sub_chapter_name,
            "readPercent": metric.get_completed_percent(),
            "startedPercent": metric.get_started_percent(),
            "unreadPercent": metric.get_not_started_percent()
            })

    read_data = []
    recent_data = []
    logger.debug("getting user activity")
    user_activity = data_analyzer.user_activity

    for user, activity in six.iteritems(user_activity.user_activities):
        read_data.append({
            "student":activity.name,  # causes username instead of full name to show in the report, but it works  ?? how to display the name but use the username on click??
            "sid":activity.username,
            "count":activity.get_page_views()
            })

        recent_data.append({
            "student":activity.name,
            "sid":activity.username,
            "count":activity.get_recent_page_views()
            })

    logger.debug("finishing")
    studentactivity = [{
    "data":read_data,
    "name":"Sections Read"
    },{
    "data":read_data,
    "name":"Exercises Correct"
    },{
    "data":read_data,
    "name":"Exercises Missed"
    }]

    recentactivity = [{
    "data":recent_data,
    "name":"Sections Read"
    },{
    "data":recent_data,
    "name":"Exercises Correct"
    },{
    "data":recent_data,
    "name":"Exercises Missed"
    }]

    return dict(assignments=assignments, course=course, questions=questions, sections=sections, chapters=chapters, selected_chapter=selected_chapter, studentactivity=studentactivity, recentactivity=recentactivity)

@auth.requires_login()
def studentreport():
    data_analyzer = DashboardDataAnalyzer(auth.user.course_id)
    #todo: Test to see if vars.id is there -- if its not then load_user_metrics will crash
    #todo: This seems redundant with assignments/index  -- should use this one... id should be text sid
    data_analyzer.load_user_metrics(request.vars.id)
    data_analyzer.load_assignment_metrics(request.vars.id)

    chapters = []
    for chapter_label, chapter in six.iteritems(data_analyzer.chapter_progress.chapters):
        chapters.append({
            "label": chapter.chapter_label,
            "status": chapter.status_text(),
            "subchapters": chapter.get_sub_chapter_progress()
            })
    activity = data_analyzer.formatted_activity.activities

    logger.debug("GRADES = %s",data_analyzer.grades)
    return dict(course=get_course_row(db.courses.ALL), user=data_analyzer.user, chapters=chapters, activity=activity, assignments=data_analyzer.grades)

@auth.requires_login()
def studentprogress():
    return dict(course_name=auth.user.course_name)

@auth.requires_login()
def grades():
    course = db(db.courses.id == auth.user.course_id).select().first()

    assignments = db(db.assignments.course == course.id).select(db.assignments.ALL,
                    orderby=(db.assignments.duedate, db.assignments.id))

    students = db(
        (db.user_courses.course_id == auth.user.course_id) &
        (db.auth_user.id == db.user_courses.user_id)
    ).select(db.auth_user.username, db.auth_user.first_name, db.auth_user.last_name,
             db.auth_user.id, db.auth_user.email, db.auth_user.course_name,
             orderby=(db.auth_user.last_name, db.auth_user.first_name))


    query = """select score, points, assignments.id, auth_user.id
        from auth_user join grades on (auth_user.id = grades.auth_user)
        join assignments on (grades.assignment = assignments.id)
        where points is not null and assignments.course = %s and auth_user.id in
            (select user_id from user_courses where course_id = %s)
            order by last_name, first_name, assignments.duedate, assignments.id;"""
    rows = db.executesql(query, [course['id'], course['id']])

    studentinfo = {}
    practice_setting = db(db.course_practice.course_name == auth.user.course_name).select().first()
    practice_average = 0
    total_possible_points = 0
    for s in students:
        practice_grade = 0
        if practice_setting:
            if practice_setting.spacing == 1:
                practice_completion_count = db((db.user_topic_practice_Completion.course_name == s.course_name) &
                                            (db.user_topic_practice_Completion.user_id == s.id)).count()
                total_possible_points = practice_setting.day_points * practice_setting.max_practice_days
                points_received = practice_setting.day_points * practice_completion_count
            else:
                practice_completion_count = db((db.user_topic_practice_log.course_name == s.course_name) &
                                            (db.user_topic_practice_log.user_id == s.id) &
                                            (db.user_topic_practice_log.q != 0) &
                                            (db.user_topic_practice_log.q != -1)).count()
                total_possible_points = practice_setting.question_points * practice_setting.max_practice_questions
                points_received = practice_setting.question_points * practice_completion_count
        if total_possible_points > 0:
            practice_average += 100 * points_received / total_possible_points
        studentinfo[s.id] = {'last_name': s.last_name,
                             'first_name': s.first_name,
                             'username': s.username,
                             'email': s.email,
                             'practice': '{0:.2f}'.format((100 * points_received/total_possible_points)
                                                          ) if total_possible_points > 0 else 'n/a'}
    practice_average /= len(students)
    practice_average = '{0:.2f}'.format(practice_average)

    # create a matrix indexed by user.id and assignment.id
    gradebook = OrderedDict((sid.id, OrderedDict()) for sid in students)
    avgs = OrderedDict((assign.id, {'total':0, 'count':0}) for assign in assignments)
    for k in gradebook:
        gradebook[k] = OrderedDict((assign.id,'n/a') for assign in assignments)

    for row in rows:
        gradebook[row[3]][row[2]] = '{0:.2f}'.format((100 * row[0]/row[1])) if row[1] > 0 else 'n/a'
        avgs[row[2]]['total'] += (100 * row[0]/row[1]) if row[1] > 0 else 0
        avgs[row[2]]['count'] += 1 if row[0] >= 0 else 0

    logger.debug("GRADEBOOK = {}".format(gradebook))
    # now transform the matrix into the gradetable needed by the template

    gradetable = []
    averagerow = []

    for k in gradebook:
        studentrow = []
        studentrow.append(studentinfo[k]['first_name'])
        studentrow.append(studentinfo[k]['last_name'])
        studentrow.append(studentinfo[k]['username'])
        studentrow.append(studentinfo[k]['email'])
        studentrow.append(studentinfo[k]['practice'])
        for assignment in gradebook[k]:
            studentrow.append(gradebook[k][assignment])
        gradetable.append(studentrow)

    #Then build the average row for the table
    for g in avgs:
        if avgs[g]['count'] > 0:
            averagerow.append('{0:.2f}'.format(avgs[g]['total']/avgs[g]['count']))
        else:
            averagerow.append('n/a')


    return dict(course=course,
                assignments=assignments, students=students, gradetable=gradetable,
                averagerow=averagerow, practice_average=practice_average)

# This is meant to be called from a form submission, not as a bare controller endpoint
@auth.requires_login()
def questiongrades():
    if 'sid' not in request.vars:
        logger.error("It Appears questiongrades was called without any request vars")
        session.flash = "Cannot call questiongrades directly"
        redirect(URL('dashboard','index'))

    course = db(db.courses.id == auth.user.course_id).select().first()
    assignment = db((db.assignments.id == request.vars.assignment_id) & (db.assignments.course == course.id)).select().first()
    sid = request.vars.sid
    student = db(db.auth_user.username == sid).select(db.auth_user.first_name, db.auth_user.last_name)

    query = ("""select questions.name, score, points
        from questions join assignment_questions on (questions.id = assignment_questions.question_id)
             join question_grades on (questions.name = question_grades.div_id)
             where assignment_id = %s and sid = %s and question_grades.course_name = %s;""")
    rows = db.executesql(query, [assignment['id'], sid, course.course_name])
    if not student or not rows:
        session.flash = "Student {} not found for course {}".format(sid, course.course_name)
        return redirect(URL('dashboard','grades'))

    return dict(assignment=assignment, student=student, rows=rows, total=0, course=course)

# Note this is meant to be called from a form submission not as a bare endpoint
@auth.requires_login()
def exercisemetrics():
    if 'chapter' not in request.vars:
        logger.error("It Appears exercisemetrics was called without any request vars")
        session.flash = "Cannot call exercisemetrics directly"
        redirect(URL('dashboard','index'))
    chapter = request.vars['chapter']
    base_course = db(db.courses.course_name == auth.user.course_name).select().first().base_course
    chapter = db(((db.chapters.course_id == auth.user.course_name) | (db.chapters.course_id == base_course))  &
        (db.chapters.chapter_label == chapter)).select().first()
    if not chapter:
        logger.error("Error -- No Chapter information for {} and {}".format(auth.user.course_name, request.vars['chapter']))
        session.flash = "No Chapter information for {} and {}".format(auth.user.course_name, request.vars['chapter'])
        redirect(URL('dashboard','index'))

    # TODO: When all old style courses were gone this can be just a base course
    data_analyzer = DashboardDataAnalyzer(auth.user.course_id,chapter)
    data_analyzer.load_exercise_metrics(request.vars["id"])
    problem_metrics = data_analyzer.problem_metrics

    prob_id = request.vars["id"]
    answers = []
    attempt_histogram = []
    logger.debug(problem_metrics.problems)
    problem_metric = problem_metrics.problems[prob_id]
    response_frequency = problem_metric.aggregate_responses

    for username, user_responses in six.iteritems(problem_metric.user_responses):
        responses = user_responses.responses[:4]
        responses += [''] * (4 - len(responses))
        answers.append({
            "user":user_responses.user,
            "username": user_responses.username,
            "answers":responses
            })

    for attempts, count in six.iteritems(problem_metric.user_number_responses()):
        attempt_histogram.append({
            "attempts": attempts,
            "frequency": count
            })

    return dict(course=get_course_row(db.courses.ALL), answers=answers, response_frequency=response_frequency, attempt_histogram=attempt_histogram, exercise_label=problem_metric.problem_text)


@auth.requires_login()
def subchapoverview():
    thecourse = db(db.courses.id == auth.user.course_id).select().first()
    course = auth.user.course_name

    is_instructor = verifyInstructorStatus(course, auth.user.id)
    if not is_instructor:
        session.flash = "Not Authorized for this page"
        return redirect(URL('default','user'))

    data = pd.read_sql_query("""
    select sid, useinfo.timestamp, div_id, chapter, subchapter from useinfo
    join questions on div_id = name
    where course_id = '{}'""".format(course), settings.database_uri)
    data = data[~data.sid.str.contains('@')]
    if 'tablekind' not in request.vars:
        request.vars.tablekind = 'sccount'

    values = "timestamp"
    idxlist = ['chapter', 'subchapter', 'div_id']

    if request.vars.tablekind == "sccount":
        values = "div_id"
        afunc = "nunique"
        idxlist = ['chapter', 'subchapter']
    elif request.vars.tablekind == "dividmin":
        afunc = "min"
    elif request.vars.tablekind == "dividmax":
        afunc = "max"
    else:
        afunc = "count"

    pt = data.pivot_table(index=idxlist, values=values, columns='sid', aggfunc=afunc)

    cmap = pd.read_sql_query("""select chapter_num, sub_chapter_num, chapter_label, sub_chapter_label
        from sub_chapters join chapters on chapters.id = sub_chapters.chapter_id
        where chapters.course_id = '{}'
        order by chapter_num, sub_chapter_num;
        """.format(course), settings.database_uri )

    if request.vars.tablekind != "sccount":
        pt = pt.reset_index(2)

    l = pt.merge(cmap, left_index=True, right_on=['chapter_label', 'sub_chapter_label'], how='outer')
    l = l.set_index(['chapter_num','sub_chapter_num']).sort_index()


    if request.vars.action == "tocsv":
        response.headers['Content-Type']='application/vnd.ms-excel'
        response.headers['Content-Disposition']= 'attachment; filename=data_for_{}.csv'.format(auth.user.course_name)
        return l.to_csv(na_rep=" ")
    else:
        return dict(course_name=auth.user.course_name, course_id=auth.user.course_name, course=thecourse,
            summary=l.to_html(classes="table table-striped table-bordered table-lg", na_rep=" ", table_id="scsummary").replace("NaT",""))
