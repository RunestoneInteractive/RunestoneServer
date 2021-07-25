# pylint: good-names=auth, settings, db

import logging
from operator import itemgetter
from collections import OrderedDict
import urllib.parse
import six
import pandas as pd
import numpy as np
from db_dashboard import DashboardDataAnalyzer
from rs_practice import _get_practice_data

logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)

admin_logger(logger)

# this is for admin links
# use auth.requires_membership('manager')
#
# create a simple index to provide a page of links
# - re build the book
# - list assignments
# - find assignments for a student
# - show totals for all students

# select acid, sid from code as T where timestamp = (select max(timestamp) from code where sid=T.sid and acid=T.acid);


def _get_dburl():
    # DAL uses "postgres:", while SQLAlchemy (and the PostgreSQL spec) uses "postgresql:". Fix.
    dburl = settings.database_uri
    remove_prefix = "postgres://"
    if dburl.startswith(remove_prefix):
        dburl = "postgresql://" + dburl[len(remove_prefix) :]
    return dburl


class ChapterGet:
    #    chapnum_map={}
    #    sub_chapters={}
    #    subchap_map={}
    #    subchapnum_map={}
    #    subchapNum_map={}
    def __init__(self, chapters):

        self.Cmap = {}
        self.Smap = {}  # dictionary organized by chapter and section labels
        self.SAmap = {}  # organized just by section label
        for chapter in chapters:
            label = chapter.chapter_label
            self.Cmap[label] = chapter
            sub_chapters = db(db.sub_chapters.chapter_id == chapter.id).select(
                db.sub_chapters.ALL
            )  # FIX: get right course_id, too
            # NOTE: sub_chapters table doesn't have a course name column in it, kind of a problem
            self.Smap[label] = {}

            for sub_chapter in sub_chapters:
                self.Smap[label][sub_chapter.sub_chapter_label] = sub_chapter
                self.SAmap[sub_chapter.sub_chapter_label] = sub_chapter

    def ChapterNumber(self, label):
        """Given the label of a chapter, return its number"""
        try:
            return self.Cmap[label].chapter_num
        except KeyError:
            return ""

    def ChapterName(self, label):
        try:
            return self.Cmap[label].chapter_name
        except KeyError:
            return label

    def SectionName(self, chapter, section):
        try:
            return self.Smap[chapter][section].sub_chapter_name
        except KeyError:
            return section

    def SectionNumber(self, chapter, section=None):
        try:
            if section is None:
                lookup = self.SAmap
                section = chapter
            else:
                lookup = self.Smap[chapter]

            return lookup[section].sub_chapter_num
        except KeyError:
            return 999


@auth.requires(
    lambda: verifyInstructorStatus(auth.user.course_name, auth.user),
    requires_login=True,
)
def index():
    selected_chapter = None
    questions = []
    sections = []

    if settings.academy_mode and not settings.docker_institution_mode:
        if auth.user.course_name in [
            "thinkcspy",
            "pythonds",
            "JavaReview",
            "JavaReview-RU",
            "StudentCSP",
            "csawesome",
            "fopp",
        ]:
            session.flash = "Student Progress page not available for {}".format(
                auth.user.course_name
            )
            return redirect(URL("admin", "admin"))

    course = db(db.courses.id == auth.user.course_id).select().first()
    assignments = db(db.assignments.course == course.id).select(
        db.assignments.ALL, orderby=db.assignments.name
    )
    chapters = db(db.chapters.course_id == course.base_course).select(
        orderby=db.chapters.chapter_num
    )

    logger.debug("getting chapters for {}".format(auth.user.course_name))
    chapget = ChapterGet(chapters)
    for chapter in chapters.find(
        lambda chapter: chapter.chapter_label == request.vars["chapter"]
    ):
        selected_chapter = chapter
    if selected_chapter is None:
        selected_chapter = chapters.first()

    logger.debug("making an analyzer")
    data_analyzer = DashboardDataAnalyzer(auth.user.course_id, selected_chapter)
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
            schtmp = data_analyzer.questions[problem_id].subchapter
            entry = {
                "id": problem_id,
                "text": metric.problem_text,
                "chapter": chtmp,
                "chapter_title": chapget.ChapterName(chtmp),
                "chapter_number": chapget.ChapterNumber(chtmp),
                "sub_chapter": schtmp,
                "sub_chapter_number": chapget.SectionNumber(chtmp, schtmp),
                "sub_chapter_title": chapget.SectionName(chtmp, schtmp),
                "correct": stats[2],
                "correct_mult_attempt": stats[3],
                "incomplete": stats[1],
                "not_attempted": stats[0],
                "attemptedBy": stats[1] + stats[2] + stats[3],
            }
        else:
            entry = {
                "id": problem_id,
                "text": metric.problem_text,
                "chapter": "unknown",
                "sub_chapter": "unknown",
                "sub_chapter_number": 0,
                "sub_chapter_title": "unknown",
                "chapter_title": "unknown",
                "correct": stats[2],
                "correct_mult_attempt": stats[3],
                "incomplete": stats[1],
                "not_attempted": stats[0],
                "attemptedBy": stats[1] + stats[2] + stats[3],
            }
        questions.append(entry)
        logger.debug("ADDING QUESTION %s ", entry["chapter"])

    logger.debug("getting questions")
    try:
        questions = sorted(questions, key=itemgetter("chapter", "sub_chapter_number"))
    except Exception as e:
        logger.error("FAILED TO SORT {} Error detail: {}".format(questions, e))
    logger.debug("starting sub_chapter loop")
    for sub_chapter, metric in six.iteritems(progress_metrics.sub_chapters):
        sections.append(
            {
                "id": metric.sub_chapter_label,
                "text": metric.sub_chapter_text,
                "name": metric.sub_chapter_name,
                "number": chapget.SectionNumber(
                    selected_chapter.chapter_label, metric.sub_chapter_label
                ),
                # FIX: Using selected_chapter here might be a kludge
                # Better if metric contained chapter numbers associated with sub_chapters
                "readPercent": metric.get_completed_percent(),
                "startedPercent": metric.get_started_percent(),
                "unreadPercent": metric.get_not_started_percent(),
            }
        )

    read_data = []
    correct_data = []
    missed_data = []
    recent_data = []
    recent_correct = []
    recent_missed = []
    daily_data = []
    daily_correct = []
    daily_missed = []
    logger.debug("getting user activity")
    user_activity = data_analyzer.user_activity

    # All of this can be replaced by a nice crosstab call
    # See UserActivityCrosstab.ipynb
    for user, activity in six.iteritems(user_activity.user_activities):
        read_data.append(
            {
                "student": activity.name,  # causes username instead of full name to show in the report, but it works  ?? how to display the name but use the username on click??
                "sid": activity.username,
                "count": activity.get_page_views(),
            }
        )
        correct_data.append(
            {
                "student": activity.name,  # causes username instead of full name to show in the report, but it works  ?? how to display the name but use the username on click??
                "sid": activity.username,
                "count": activity.get_correct_count(),
            }
        )
        missed_data.append(
            {
                "student": activity.name,  # causes username instead of full name to show in the report, but it works  ?? how to display the name but use the username on click??
                "sid": activity.username,
                "count": activity.get_missed_count(),
            }
        )

        recent_data.append(
            {
                "student": activity.name,
                "sid": activity.username,
                "count": activity.get_recent_page_views(),
            }
        )

        recent_correct.append(
            {
                "student": activity.name,
                "sid": activity.username,
                "count": activity.get_recent_correct(),
            }
        )
        recent_missed.append(
            {
                "student": activity.name,
                "sid": activity.username,
                "count": activity.get_recent_missed(),
            }
        )

        daily_data.append(
            {
                "student": activity.name,
                "sid": activity.username,
                "count": activity.get_daily_page_views(),
            }
        )

        daily_correct.append(
            {
                "student": activity.name,
                "sid": activity.username,
                "count": activity.get_daily_correct(),
            }
        )
        daily_missed.append(
            {
                "student": activity.name,
                "sid": activity.username,
                "count": activity.get_daily_missed(),
            }
        )

    logger.debug("finishing")
    # TODO -- this is not right and explains why all are the same!!
    studentactivity = [
        {"data": read_data, "name": "Sections Read"},
        {"data": correct_data, "name": "Exercises Correct"},
        {"data": missed_data, "name": "Exercises Missed"},
    ]

    recentactivity = [
        {"data": recent_data, "name": "Sections Read"},
        {"data": recent_correct, "name": "Exercises Correct"},
        {"data": recent_missed, "name": "Exercises Missed"},
    ]

    dailyactivity = [
        {"data": daily_data, "name": "Sections Read"},
        {"data": daily_correct, "name": "Exercises Correct"},
        {"data": daily_missed, "name": "Exercises Missed"},
    ]

    return dict(
        assignments=assignments,
        course=course,
        questions=questions,
        sections=sections,
        chapters=chapters,
        selected_chapter=selected_chapter,
        studentactivity=studentactivity,
        recentactivity=recentactivity,
        dailyactivity=dailyactivity,
    )


@auth.requires_login()
def studentreport():
    data_analyzer = DashboardDataAnalyzer(auth.user.course_id)
    for_dashboard = verifyInstructorStatus(auth.user.course_id, auth.user.id)
    if "id" in request.vars and for_dashboard:
        sid = request.vars.id
    else:
        sid = auth.user.username
        response.view = "assignments/index.html"

    logger.debug(f"id = {request.vars.id} is instructor = {for_dashboard} sid = {sid}")

    data_analyzer.load_user_metrics(sid)
    data_analyzer.load_assignment_metrics(sid, not for_dashboard)

    chapters = []
    for chapter_label, chapter in six.iteritems(
        data_analyzer.chapter_progress.chapters
    ):
        chapters.append(
            {
                "label": chapter.chapter_label,
                "status": chapter.status_text(),
                "subchapters": chapter.get_sub_chapter_progress(),
            }
        )
    activity = data_analyzer.formatted_activity

    logger.debug("GRADES = %s", data_analyzer.grades)

    pd_dict = dict()
    if response.view == "assignments/index.html":
        (
            pd_dict["now"],
            pd_dict["now_local"],
            pd_dict["practice_message1"],
            pd_dict["practice_message2"],
            pd_dict["practice_graded"],
            pd_dict["spacing"],
            pd_dict["interleaving"],
            pd_dict["practice_completion_count"],
            pd_dict["remaining_days"],
            pd_dict["max_days"],
            pd_dict["max_questions"],
            pd_dict["day_points"],
            pd_dict["question_points"],
            pd_dict["presentable_flashcards"],
            pd_dict["flashcard_count"],
            pd_dict["practiced_today_count"],
            pd_dict["questions_to_complete_day"],
            pd_dict["practice_today_left"],
            pd_dict["points_received"],
            pd_dict["total_possible_points"],
            pd_dict["flashcard_creation_method"],
        ) = _get_practice_data(
            auth.user,
            float(session.timezoneoffset) if "timezoneoffset" in session else 0,
            db,
        )
        pd_dict["total_today_count"] = min(
            pd_dict["practice_today_left"] + pd_dict["practiced_today_count"],
            pd_dict["questions_to_complete_day"],
        )

    dburl = _get_dburl()
    if request.vars.action == "dlcsv":
        mtbl = pd.read_sql_query(
            """
        select * from useinfo where sid = %(sid)s and course_id = %(course)s
        """,
            dburl,
            params={"sid": sid, "course": auth.user.course_name},
        )
        response.headers["Content-Type"] = "application/vnd.ms-excel"
        response.headers[
            "Content-Disposition"
        ] = "attachment; filename=data_for_{}.csv".format(sid)
        session.flash = f"Downloading to data_for_{sid}.csv"
        return mtbl.to_csv(na_rep=" ")

    if request.vars.action == "dlcode":
        mtbl = pd.read_sql_query(
            """
        select * from code where sid = %(sid)s and course_id = %(course)s
        """,
            dburl,
            params={"sid": sid, "course": auth.user.course_id},
        )
        response.headers["Content-Type"] = "application/vnd.ms-excel"
        response.headers[
            "Content-Disposition"
        ] = "attachment; filename=code_for_{}.csv".format(sid)
        session.flash = f"Downloading to code_for_{sid}.csv"
        return mtbl.to_csv(na_rep=" ")

    return dict(
        course=get_course_row(db.courses.ALL),
        user=data_analyzer.user,
        chapters=chapters,
        activity=activity,
        assignments=data_analyzer.grades,
        **pd_dict,
    )


@auth.requires_login()
def studentprogress():
    return dict(course_name=auth.user.course_name)


@auth.requires(
    lambda: verifyInstructorStatus(auth.user.course_name, auth.user),
    requires_login=True,
)
def grades():
    response.title = "Gradebook"
    course = db(db.courses.id == auth.user.course_id).select().first()

    if not course:
        session.flash = "Your course does not exist"
        redirect(URL("dashboard", "index"))

    assignments = db(db.assignments.course == course.id).select(
        db.assignments.ALL, orderby=(db.assignments.duedate, db.assignments.id)
    )

    # recalculate total points for each assignment in case the stored
    # total is out of sync.
    duedates = []
    for assign in assignments:
        assign.points = update_total_points(assign.id)
        duedates.append(date2String(assign.duedate))

    students = db(
        (db.user_courses.course_id == auth.user.course_id)
        & (db.auth_user.id == db.user_courses.user_id)
    ).select(
        db.auth_user.username,
        db.auth_user.first_name,
        db.auth_user.last_name,
        db.auth_user.id,
        db.auth_user.email,
        db.auth_user.course_name,
        orderby=(db.auth_user.last_name, db.auth_user.first_name),
    )

    query = """select score, points, assignments.id, auth_user.id, is_submit
        from auth_user join grades on (auth_user.id = grades.auth_user)
        join assignments on (grades.assignment = assignments.id)
        where points is not null and assignments.course = %s and auth_user.id in
            (select user_id from user_courses where course_id = %s)
            order by last_name, first_name, assignments.duedate, assignments.id;"""
    rows = db.executesql(query, [course["id"], course["id"]])

    studentinfo = {}
    practice_setting = (
        db(db.course_practice.course_name == auth.user.course_name).select().first()
    )
    practice_average = 0
    total_possible_points = 0
    for s in students:
        if practice_setting:
            if practice_setting.spacing == 1:
                practice_completion_count = db(
                    (db.user_topic_practice_completion.course_name == s.course_name)
                    & (db.user_topic_practice_completion.user_id == s.id)
                ).count()
                total_possible_points = (
                    practice_setting.day_points * practice_setting.max_practice_days
                )
                points_received = (
                    practice_setting.day_points * practice_completion_count
                )
            else:
                practice_completion_count = db(
                    (db.user_topic_practice_log.course_name == s.course_name)
                    & (db.user_topic_practice_log.user_id == s.id)
                    & (db.user_topic_practice_log.q != 0)
                    & (db.user_topic_practice_log.q != -1)
                ).count()
                total_possible_points = (
                    practice_setting.question_points
                    * practice_setting.max_practice_questions
                )
                points_received = (
                    practice_setting.question_points * practice_completion_count
                )
        if total_possible_points > 0:
            practice_average += 100 * points_received / total_possible_points
        studentinfo[s.id] = {
            "last_name": s.last_name,
            "first_name": s.first_name,
            "username": s.username,
            "email": s.email,
            "practice": "{0:.2f}".format(
                (100 * points_received / total_possible_points)
            )
            if total_possible_points > 0
            else "n/a",
        }
    practice_average /= len(students)
    practice_average = "{0:.2f}".format(practice_average)

    # create a matrix indexed by user.id and assignment.id
    gradebook = OrderedDict((sid.id, OrderedDict()) for sid in students)
    avgs = OrderedDict((assign.id, {"total": 0, "count": 0}) for assign in assignments)
    for k in gradebook:
        gradebook[k] = OrderedDict((assign.id, "n/a") for assign in assignments)

    for score, points, assignments_id, auth_user_id, is_submit in rows:
        if (score is not None) and (points > 0):
            percent_grade = 100 * score / points
            gradebook_entry = "{0:.2f}".format(percent_grade)
            avgs[assignments_id]["total"] += percent_grade
            avgs[assignments_id]["count"] += 1
        elif is_submit:
            gradebook_entry = is_submit
        else:
            gradebook_entry = "n/a"
        gradebook[auth_user_id][assignments_id] = gradebook_entry

    logger.debug("GRADEBOOK = {}".format(gradebook))
    # now transform the matrix into the gradetable needed by the template

    gradetable = []
    averagerow = []

    for k in gradebook:
        studentrow = []
        studentrow.append(studentinfo[k]["first_name"])
        studentrow.append(studentinfo[k]["last_name"])
        studentrow.append(urllib.parse.quote(studentinfo[k]["username"]))
        studentrow.append(studentinfo[k]["email"])
        studentrow.append(studentinfo[k]["practice"])
        for assignment in gradebook[k]:
            studentrow.append(gradebook[k][assignment])
        gradetable.append(studentrow)

    # Then build the average row for the table
    for g in avgs:
        if avgs[g]["count"] > 0:
            averagerow.append("{0:.2f}".format(avgs[g]["total"] / avgs[g]["count"]))
        else:
            averagerow.append("n/a")

    return dict(
        course=course,
        assignments=assignments,
        gradetable=gradetable,
        averagerow=averagerow,
        practice_average=practice_average,
        duedates=duedates,
    )


def date2String(date_time):
    day = str(date_time.strftime("%b")) + " " + str(date_time.day)
    time = date_time.strftime("%I:%M %p")
    displayDate = day + ", " + time
    return displayDate


# This is meant to be called from a form submission, not as a bare controller endpoint
@auth.requires(
    lambda: verifyInstructorStatus(auth.user.course_name, auth.user),
    requires_login=True,
)
def questiongrades():
    if "sid" not in request.vars or "assignment_id" not in request.vars:
        logger.error("It Appears questiongrades was called without any request vars")
        session.flash = "Cannot call questiongrades directly"
        redirect(URL("dashboard", "index"))

    course = db(db.courses.id == auth.user.course_id).select().first()

    # make sure points total is up to date
    assignment_id = request.vars.assignment_id

    if assignment_id.isnumeric():
        assignmatch = db.assignments.id == request.vars.assignment_id
    else:
        assignmatch = db.assignments.name == request.vars.assignment_id
    assignment = db(assignmatch & (db.assignments.course == course.id)).select().first()
    assignment_id = assignment.id
    update_total_points(assignment_id)

    sid = request.vars.sid
    student = db(db.auth_user.username == sid).select(
        db.auth_user.first_name, db.auth_user.last_name, db.auth_user.username
    )
    student[0].username = urllib.parse.quote(student[0].username)
    query = """select questions.name, score, points
        from questions join assignment_questions on (questions.id = assignment_questions.question_id)
        left outer join question_grades on (questions.name = question_grades.div_id
            and sid = %s and question_grades.course_name = %s)
            where assignment_id = %s ;"""
    rows = db.executesql(query, [sid, course.course_name, assignment["id"]])
    if not student or not rows:
        session.flash = "Student {} not found for course {}".format(
            sid, course.course_name
        )
        return redirect(URL("dashboard", "grades"))

    return dict(
        assignment=assignment, student=student, rows=rows, total=0, course=course
    )


def update_total_points(assignment_id):
    sum_op = db.assignment_questions.points.sum()
    total = (
        db(db.assignment_questions.assignment_id == assignment_id)
        .select(sum_op)
        .first()[sum_op]
    )
    db(db.assignments.id == assignment_id).update(points=total)
    return total


# Note this is meant to be called from a form submission not as a bare endpoint
@auth.requires(
    lambda: verifyInstructorStatus(auth.user.course_name, auth.user),
    requires_login=True,
)
def exercisemetrics():
    if "chapter" not in request.vars:
        logger.error("It Appears exercisemetrics was called without any request vars")
        session.flash = "Cannot call exercisemetrics directly"
        redirect(URL("dashboard", "index"))
    chapter = request.vars["chapter"]
    base_course = (
        db(db.courses.course_name == auth.user.course_name).select().first().base_course
    )
    chapter = (
        db(
            (
                (db.chapters.course_id == auth.user.course_name)
                | (db.chapters.course_id == base_course)
            )
            & (db.chapters.chapter_label == chapter)
        )
        .select()
        .first()
    )
    if not chapter:
        logger.error(
            "Error -- No Chapter information for {} and {}".format(
                auth.user.course_name, request.vars["chapter"]
            )
        )
        session.flash = "No Chapter information for {} and {}".format(
            auth.user.course_name, request.vars["chapter"]
        )
        redirect(URL("dashboard", "index"))

    # TODO: When all old style courses were gone this can be just a base course
    data_analyzer = DashboardDataAnalyzer(auth.user.course_id, chapter)
    data_analyzer.load_exercise_metrics(request.vars["id"])
    problem_metrics = data_analyzer.problem_metrics

    prob_id = request.vars["id"]
    answers = []
    attempt_histogram = []
    logger.debug(problem_metrics.problems)
    try:
        problem_metric = problem_metrics.problems[prob_id]
    except KeyError:
        session.flash = f"Not enough data for {prob_id}"
        redirect(request.env.http_referer)
    response_frequency = problem_metric.aggregate_responses

    for username, user_responses in six.iteritems(problem_metric.user_responses):
        responses = user_responses.responses[:4]
        responses += [""] * (4 - len(responses))
        answers.append(
            {
                "user": user_responses.user,
                "username": urllib.parse.quote(user_responses.username),
                "answers": responses,
            }
        )

    for attempts, count in six.iteritems(problem_metric.user_number_responses()):
        attempt_histogram.append({"attempts": attempts, "frequency": count})

    return dict(
        course=get_course_row(db.courses.ALL),
        answers=answers,
        response_frequency=response_frequency,
        attempt_histogram=attempt_histogram,
        exercise_label=problem_metric.problem_text,
    )


def format_cell(sid, chap, subchap, val):
    sid = urllib.parse.quote(sid)
    if np.isnan(val):
        return ""
    else:
        return f"""<a href="/runestone/dashboard/subchapdetail?chap={chap}&sub={subchap}&sid={sid}">{val}</a>"""


@auth.requires(
    lambda: verifyInstructorStatus(auth.user.course_name, auth.user),
    requires_login=True,
)
def subchapoverview():
    thecourse = db(db.courses.id == auth.user.course_id).select().first()
    course = auth.user.course_name

    is_instructor = verifyInstructorStatus(course, auth.user.id)
    if not is_instructor:
        session.flash = "Not Authorized for this page"
        return redirect(URL("default", "user"))

    dburl = _get_dburl()
    data = pd.read_sql_query(
        """
    select sid, useinfo.timestamp, div_id, chapter, subchapter from useinfo
    join questions on div_id = name and base_course = '{}' join auth_user on username = useinfo.sid
    where useinfo.course_id = '{}' and active='T' and useinfo.timestamp >= '{}'""".format(
            thecourse.base_course, course, thecourse.term_start_date
        ),
        dburl,
        parse_dates=["timestamp"],
    )
    data = data[~data.sid.str.contains(r"^\d{38,38}@")]
    tdoff = pd.Timedelta(
        hours=float(session.timezoneoffset) if "timezoneoffset" in session else 0
    )
    data["timestamp"] = data.timestamp.map(lambda x: x - tdoff)
    if "tablekind" not in request.vars:
        request.vars.tablekind = "sccount"

    values = "timestamp"
    idxlist = ["chapter", "subchapter", "div_id"]

    if request.vars.tablekind == "sccount":
        values = "div_id"
        afunc = "nunique"
        idxlist = ["chapter", "subchapter"]
    elif request.vars.tablekind == "dividmin":
        afunc = "min"
    elif request.vars.tablekind == "dividmax":
        afunc = "max"
    else:
        afunc = "count"

    pt = data.pivot_table(index=idxlist, values=values, columns="sid", aggfunc=afunc)

    # TODO: debug tests so these can be live
    if pt.empty:
        logger.error(
            "Empty Dataframe after pivot for {} ".format(auth.user.course_name)
        )
        session.flash = "Error: Not enough data"
        return redirect(URL("dashboard", "index"))

    if request.vars.tablekind == "sccount":
        x = pt.to_dict()
        for k in x:
            for j in x[k]:
                if request.vars.action != "tocsv":
                    x[k][j] = format_cell(k, j[0], j[1], x[k][j])
        pt = pd.DataFrame(x)

    cmap = pd.read_sql_query(
        """select chapter_num, sub_chapter_num, chapter_label, sub_chapter_label
        from sub_chapters join chapters on chapters.id = sub_chapters.chapter_id
        where chapters.course_id = '{}'
        order by chapter_num, sub_chapter_num;
        """.format(
            thecourse.base_course
        ),
        dburl,
    )

    act_count = pd.read_sql_query(
        """
    select chapter, subchapter, count(*) act_count
    from questions
    where base_course = '{}'
    group by chapter, subchapter order by chapter, subchapter;
    """.format(
            thecourse.base_course
        ),
        dburl,
    )

    if request.vars.tablekind != "sccount":
        pt = pt.reset_index(2)

    mtbl = pt.merge(
        cmap,
        left_index=True,
        right_on=["chapter_label", "sub_chapter_label"],
        how="outer",
    )
    mtbl = mtbl.set_index(["chapter_num", "sub_chapter_num"]).sort_index()
    mtbl = mtbl.reset_index()

    mtbl = mtbl.merge(
        act_count,
        left_on=["chapter_label", "sub_chapter_label"],
        right_on=["chapter", "subchapter"],
    )

    def to_int(x):
        try:
            res = int(x)
            return res
        except ValueError:
            return ""

    if request.vars.tablekind == "sccount":
        mtbl["chapter_label"] = mtbl.apply(
            lambda row: "{}.{} {}/{} ({})".format(
                to_int(row.chapter_num),
                to_int(row.sub_chapter_num),
                row.chapter_label,
                row.sub_chapter_label,
                row.act_count - 1,
            ),
            axis=1,
        )
    else:
        mtbl["chapter_label"] = mtbl.apply(
            lambda row: "{}.{} {}/{}".format(
                to_int(row.chapter_num),
                to_int(row.sub_chapter_num),
                row.chapter_label,
                row.sub_chapter_label,
            ),
            axis=1,
        )

    neworder = mtbl.columns.to_list()
    neworder = neworder[-5:-4] + neworder[2:-5]
    mtbl = mtbl[neworder]

    if request.vars.action == "tocsv":
        response.headers["Content-Type"] = "application/vnd.ms-excel"
        response.headers[
            "Content-Disposition"
        ] = "attachment; filename=data_for_{}.csv".format(auth.user.course_name)
        return mtbl.to_csv(na_rep=" ")
    else:
        return dict(
            course_name=auth.user.course_name,
            course_id=auth.user.course_name,
            course=thecourse,
            summary=mtbl.to_json(orient="records", date_format="iso"),
        )


@auth.requires(
    lambda: verifyInstructorStatus(auth.user.course_name, auth.user),
    requires_login=True,
)
def active():
    course = db(db.courses.id == auth.user.course_id).select().first()

    res = db.executesql(
        """select useinfo.timestamp, useinfo.sid, div_id
                           from useinfo join
                           (select sid, count(*), max(id)
                            from useinfo where course_id = %(cname)s
                                and event = 'page'
                                and timestamp > now() - interval '15 minutes' group by sid) as T
                          on useinfo.id = T.max""",
        dict(cname=course.course_name),
    )

    newres = []
    for row in res:
        div_id = row[2]
        components = div_id.rsplit("/", 2)
        div_id = "/".join(components[1:])
        time_local = row[0] - datetime.timedelta(
            hours=float(session.timezoneoffset) if "timezoneoffset" in session else 0
        )
        newres.append(dict(timestamp=time_local, sid=row[1], div_id=div_id))
    print(newres)
    logger.error(newres)
    return dict(activestudents=newres, course=course)


GRADEABLE_TYPES = {
    "mchoice": "mchoice_answers",
    "clickablearea": "clickablearea_answers",
    "fillintheblank": "fitb_answers",
    "parsonsprob": "parsons_answers",
    "dragndrop": "dragndrop_answers",
}


@auth.requires(
    lambda: verifyInstructorStatus(auth.user.course_name, auth.user),
    requires_login=True,
)
def subchapdetail():
    # 1. select the name, question_type, from questions for this chapter/subchapter/base_course
    # 2. for each question get tries to correct, min time, max time, total
    thecourse = db(db.courses.id == auth.user.course_id).select().first()
    questions = db(
        (db.questions.chapter == request.vars.chap)
        & (db.questions.subchapter == request.vars.sub)
        & (db.questions.base_course == thecourse.base_course)
        & (db.questions.question_type != "page")
    ).select(db.questions.name, db.questions.question_type)

    res = db.executesql(
        """
select name, question_type, min(useinfo.timestamp) as first, max(useinfo.timestamp) as last, count(*) as clicks
    from questions join useinfo on name = div_id and course_id = %s
    where chapter = %s and subchapter = %s
    and base_course = %s and sid = %s
    group by name, question_type""",
        (
            auth.user.course_name,
            request.vars.chap,
            request.vars.sub,
            thecourse.base_course,
            request.vars.sid,
        ),
        as_dict=True,
    )
    tdoff = datetime.timedelta(
        hours=float(session.timezoneoffset) if "timezoneoffset" in session else 0
    )

    for row in res:
        row["first"] = row["first"] - tdoff
        row["last"] = row["last"] - tdoff
        if row["question_type"] in GRADEABLE_TYPES.keys():
            tname = GRADEABLE_TYPES[row["question_type"]]
            isc = (
                db(
                    (db[tname].sid == request.vars.sid)
                    & (db[tname].correct == "T")
                    & (db[tname].div_id == row["name"])
                )
                .select()
                .first()
            )
            if isc:
                row["correct"] = "Yes"
            else:
                row["correct"] = "No"
        elif row["question_type"] == "activecode":
            isU = (
                db(
                    (db.questions.name == row["name"])
                    & (db.questions.autograde == "unittest")
                    & (db.questions.base_course == thecourse.base_course)
                )
                .select()
                .first()
            )
            if isU:
                isC = (
                    db(
                        (db.useinfo.sid == request.vars.sid)
                        & (db.useinfo.div_id == row["name"])
                        & (db.useinfo.course_id == thecourse.course_name)
                        & (db.useinfo.event == "unittest")
                        & (db.useinfo.act.like("percent:100%"))
                    )
                    .select()
                    .first()
                )
                if isC:
                    row["correct"] = "Yes"
                else:
                    row["correct"] = "No"
            else:
                row["correct"] = "NA"

        else:
            row["correct"] = "NA"

    active = set([r["name"] for r in res])
    allq = set([r.name for r in questions])
    qtype = {r.name: r.question_type for r in questions}
    missing = allq - active
    for q in missing:
        res.append(
            {
                "name": q,
                "question_type": qtype[q],
                "first": "",
                "last": "",
                "clicks": "",
                "correct": "",
            }
        )
    print(res)
    return dict(
        rows=res,
        sid=request.vars.sid,
        chapter=request.vars.chap,
        subchapter=request.vars.sub,
        course_name=auth.user.course_name,
        course_id=auth.user.course_name,
        course=thecourse,
    )
