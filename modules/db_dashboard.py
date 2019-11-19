from collections import OrderedDict
import logging
import datetime
import six
from gluon import current, URL, redirect

rslogger = logging.getLogger(current.settings.logger)
rslogger.setLevel(current.settings.log_level)

UNGRADED_EVENTS = [
    "activecode",
    "codelens",
    "showeval",
    "shortanswer",
    "parsonsMove",
    "timedExam",
    "livecode",
    "video",
    "poll",
    "Audio",
    "tie",
    "coach",
    "page",
]


class ProblemMetrics(object):
    """
    Used to display the donut charts.

    for all users create a UserReponse
    """

    def __init__(self, course_id, problem_id, users):
        self.course_id = course_id
        self.problem_id = problem_id
        self.problem_text = problem_id
        # total responses by answer choice, eg. A: 5, B: 3, C: 13
        self.aggregate_responses = {}
        # responses keyed by user
        self.user_responses = {}

        for user in users:
            self.user_responses[user.username] = UserResponse(user)

    def add_data_point(self, row):
        correct = row.correct
        choice = row.answer
        if choice == "":
            choice = "(empty)"

        self.aggregate_responses[choice] = self.aggregate_responses.get(choice, 0) + 1

        if row.sid in self.user_responses:
            self.user_responses[row.sid].add_response(choice, correct)

    # this is where the donut chart data is created
    def user_response_stats(self):
        correct = 0
        correct_mult_attempts = 0
        not_attempted = 0
        incomplete = 0

        for sid, user_response in six.iteritems(self.user_responses):
            if user_response.status == UserResponse.NOT_ATTEMPTED:
                not_attempted = not_attempted + 1
            if user_response.status == UserResponse.INCOMPLETE:
                incomplete = incomplete + 1
            if user_response.status == UserResponse.CORRECT:
                correct = correct + 1
            if user_response.status == UserResponse.CORRECT_AFTER_MULTIPLE_ATTEMPTS:
                correct_mult_attempts = correct_mult_attempts + 1

        return [not_attempted, incomplete, correct, correct_mult_attempts]

    def user_number_responses(self):
        histogram = {}
        for username, user_response in six.iteritems(self.user_responses):
            attempts = len(user_response.responses)
            if attempts >= 5:
                attempts = "5+"
            histogram[attempts] = histogram.get(attempts, 0) + 1
        return histogram


class UserResponse(object):
    NOT_ATTEMPTED = 0
    INCOMPLETE = 1
    CORRECT = 2
    CORRECT_AFTER_MULTIPLE_ATTEMPTS = 3

    def __init__(self, user):
        self.status = UserResponse.NOT_ATTEMPTED
        self.correct = False
        self.username = user.username
        self.user = "{0} {1}".format(user.first_name, user.last_name)
        self.responses = []

    def add_response(self, response, correct):
        if not self.correct:  # ignore if the person already answered it correctly.
            self.responses.append(response)

            if correct:
                if len(self.responses) == 1:
                    self.status = UserResponse.CORRECT
                else:
                    self.status = UserResponse.CORRECT_AFTER_MULTIPLE_ATTEMPTS
                self.correct = True
            else:
                self.status = UserResponse.INCOMPLETE


class CourseProblemMetrics(object):
    def __init__(self, course_id, users, chapter):
        self.course_id = course_id
        self.problems = {}
        self.users = users
        self.chapter = chapter

    def update_metrics(self, course_name):
        rslogger.debug(
            "Updating CourseProblemMetrics for {} of {}".format(
                self.chapter, course_name
            )
        )
        rslogger.debug("doing chapter {}".format(self.chapter))

        res = {}
        tbl_list = [
            "mchoice_answers",
            "fitb_answers",
            "parsons_answers",
            "clickablearea_answers",
            "dragndrop_answers",
            "codelens_answers",
        ]
        for tbl in tbl_list:
            res[tbl] = current.db(
                (current.db[tbl].course_name == course_name)
                & (current.db[tbl].div_id == current.db.questions.name)
                & (current.db.questions.chapter == self.chapter.chapter_label)
            ).select(orderby=current.db[tbl].timestamp)

        # convert the numeric answer to letter answers to match the questions easier.
        to_letter = dict(zip("0123456789", "ABCDEFGHIJ"))

        for row in res["mchoice_answers"]:
            mc = row["mchoice_answers"]
            mc.answer = to_letter.get(mc.answer, mc.answer)

        def add_problems(result_set, tbl):
            for srow in result_set:
                row = srow[tbl]
                rslogger.debug("UPDATE_METRICS {}".format(row))
                if not row.div_id in self.problems:
                    self.problems[row.div_id] = ProblemMetrics(
                        self.course_id, row.div_id, self.users
                    )
                self.problems[row.div_id].add_data_point(row)

        for tbl in tbl_list:
            add_problems(res[tbl], tbl)

    def retrieve_chapter_problems(self):
        return self


class UserActivityMetrics(object):
    def __init__(self, course_name, users):
        self.course_id = course_name
        self.user_activities = {}
        for user in users:
            self.user_activities[user.username] = UserActivity(user)

        # Get summary of logs
        self.logs = current.db.executesql(
            """select sid, event, count(*)
        from useinfo where course_id = '{}'
        group by sid, event
        order by sid, event""".format(
                self.course_id
            ),
            as_dict=True,
        )

        self.recent_logs = current.db.executesql(
            """select sid, event, count(*)
        from useinfo where course_id = '{}'
        and timestamp > now() - interval '7 days'
        group by sid, event
        order by sid, event""".format(
                self.course_id
            ),
            as_dict=True,
        )
        # read logs here

    def update_metrics(self):

        for row in self.logs:
            if row["sid"] in self.user_activities:
                self.user_activities[row["sid"]].add_activity(row)

        for row in self.recent_logs:
            if row["sid"] in self.user_activities:
                self.user_activities[row["sid"]].add_recent_activity(row)


class UserActivity(object):
    def __init__(self, user):
        self.name = "{0} {1}".format(user.first_name, user.last_name)
        self.username = user.username
        self.rows = []
        self.page_views = 0
        self.correct_count = 0
        self.missed_count = 0
        self.recent_page_views = 0
        self.recent_correct = 0
        self.recent_missed = 0

    def add_activity(self, row):
        # row is a row from useinfo
        if row["event"] == "page":
            self.page_views += row["count"]
        elif row["event"] == "activecode":
            self.rows.append(row)
            self.correct_count += row["count"]
        else:
            self.missed_count += row["count"]

    def add_recent_activity(self, row):
        # row is a row from useinfo
        if row["event"] == "page":
            self.recent_page_views += row["count"]
        elif row["event"] == "activecode":
            self.recent_correct += row["count"]
        else:
            self.recent_missed += row["count"]

    def get_page_views(self):
        # returns page views for all time
        return self.page_views

    def get_recent_page_views(self):
        return self.recent_page_views

    def get_activity_stats(self):
        return self

    def get_correct_count(self):
        return self.correct_count

    def get_missed_count(self):
        return self.missed_count

    def get_recent_correct(self):
        return self.recent_correct

    def get_recent_missed(self):
        return self.recent_missed


class UserActivityChapterProgress(object):
    def __init__(self, chapters, sub_chapter_progress):
        self.chapters = OrderedDict()
        for chapter in chapters:
            self.chapters[chapter.chapter_label] = UserActivitySubChapterProgress(
                chapter
            )
        for sub_chapter in sub_chapter_progress:
            try:
                self.chapters[sub_chapter.chapter_id].add_progress(sub_chapter)
            except KeyError:
                rslogger.debug("Key Error for {}".format(sub_chapter.chapter_id))


class UserActivitySubChapterProgress(object):
    def __init__(self, chapter):
        self.chapter_label = chapter.chapter_name
        self.chapter_id = chapter.id
        self.sub_chapters = OrderedDict()
        self.highest_status = -1
        self.lowest_status = 1

    def add_progress(self, progress):
        self.sub_chapters[progress.sub_chapter_id] = progress.status
        if self.lowest_status > progress.status:
            self.lowest_status = progress.status
        if self.highest_status < progress.status:
            self.highest_status = progress.status

    def get_sub_chapter_progress(self):
        subchapters = []
        subchapter_res = current.db(
            current.db.sub_chapters.chapter_id == self.chapter_id
        ).select()
        sub_chapter_label_to_text = {
            sc.sub_chapter_label: sc.sub_chapter_name for sc in subchapter_res
        }
        for subchapter_label, status in six.iteritems(self.sub_chapters):
            subchapters.append(
                {
                    "label": sub_chapter_label_to_text.get(
                        subchapter_label, subchapter_label
                    ),
                    "status": UserActivitySubChapterProgress.completion_status_to_text(
                        status
                    ),
                }
            )
        return subchapters

    def status_text(self):
        status = None
        if self.highest_status == -1:
            status = -1
        elif self.lowest_status == 1:
            status = 1
        else:
            status = 0
        return UserActivitySubChapterProgress.completion_status_to_text(status)

    @staticmethod
    def completion_status_to_text(status):
        if status == 1:
            return "completed"
        elif status == 0:
            return "started"
        elif status == -1:
            return "notstarted"
        return status


class ProgressMetrics(object):
    """
    Build the progress information for Chapter/Subchapter

    * number of starts
    * number of completions
    * number of non-starts

    Used on the index page of the dashboard for a particular chapter
    TODO: Replace most of this with a single aggregation query:
    select user_sub_chapter_progress.sub_chapter_id, status, count(status)
    from auth_user join user_sub_chapter_progress ON user_sub_chapter_progress.user_id = http://auth_user.id
    where chapter_id = 'SimplePythonData' and course_name = 'ac_summit_2019'
    group by user_sub_chapter_progress.sub_chapter_id, status
    order by user_sub_chapter_progress.sub_chapter_id;

    """

    def __init__(self, course_id, sub_chapters, users):
        self.sub_chapters = OrderedDict()
        for sub_chapter in sub_chapters:
            rslogger.debug(sub_chapter)
            self.sub_chapters[sub_chapter.sub_chapter_label] = SubChapterActivity(
                sub_chapter, len(users)
            )

    def update_metrics(self, chapter_progress):
        for row in chapter_progress:
            try:
                self.sub_chapters[
                    row.user_sub_chapter_progress.sub_chapter_id
                ].add_activity(row)
            except KeyError as e:
                rslogger.debug(
                    "Key error for {} user is {}".format(
                        row.user_sub_chapter_progress.sub_chapter_id,
                        current.auth.user.username,
                    )
                )


class SubChapterActivity(object):
    def __init__(self, sub_chapter, total_users):
        self.sub_chapter_label = sub_chapter.sub_chapter_label
        rslogger.debug(sub_chapter.sub_chapter_name)
        self.sub_chapter_text = sub_chapter.sub_chapter_label
        self.sub_chapter_name = sub_chapter.sub_chapter_name
        self.not_started = 0
        self.started = 0
        self.completed = 0
        self.total_users = total_users if total_users > 0 else 1

    def add_activity(self, row):
        if row.user_sub_chapter_progress.status == -1:
            self.not_started += 1
        if row.user_sub_chapter_progress.status == 0:
            self.started += 1
        if row.user_sub_chapter_progress.status == 1:
            self.completed += 1

    def get_started_percent(self):
        return "{0:.2f}%".format(float(self.started) / self.total_users * 100)

    def get_not_started_percent(self):
        return "{0:.2f}%".format(float(self.not_started) / self.total_users * 100)

    def get_completed_percent(self):
        return "{0:.2f}%".format(float(self.completed) / self.total_users * 100)


class DashboardDataAnalyzer(object):
    def __init__(self, course_id, chapter=None):
        self.course_id = course_id
        if chapter:
            self.db_chapter = chapter
        else:
            self.db_chapter = None

        self.course = (
            current.db(current.db.courses.id == self.course_id).select().first()
        )

        self.users = current.db(
            (current.db.auth_user.course_id == current.auth.user.course_id)
            & (current.db.auth_user.active == "T")
        ).select(
            current.db.auth_user.username,
            current.db.auth_user.first_name,
            current.db.auth_user.last_name,
            current.db.auth_user.id,
        )
        self.instructors = current.db(
            (current.db.course_instructor.course == current.auth.user.course_id)
        ).select(current.db.course_instructor.instructor)
        self.inums = [x.instructor for x in self.instructors]
        self.users.exclude(lambda x: x.id in self.inums)

    def load_chapter_metrics(self, chapter):
        if not chapter:
            rslogger.error("chapter not set, abort!")
            current.session.flash = "Error No Course Data in DB"
            return

        self.db_chapter = chapter
        # go get all the course data... in the future the post processing
        # should probably be stored and only new data appended.
        rslogger.debug("COURSE QUERY GOT %s", self.course)
        # todo:  Yikes!  Loading all of the log data for a large or even medium class is a LOT
        self.db_chapter_progress = current.db(
            (current.db.user_sub_chapter_progress.user_id == current.db.auth_user.id)
            & (current.db.auth_user.course_id == current.auth.user.course_id)
            & (  # todo: missing link from course_id to chapter/sub_chapter progress
                current.db.user_sub_chapter_progress.chapter_id == chapter.chapter_label
            )
        ).select(
            current.db.auth_user.username,
            current.db.user_sub_chapter_progress.chapter_id,
            current.db.user_sub_chapter_progress.sub_chapter_id,
            current.db.user_sub_chapter_progress.status,
            current.db.auth_user.id,
        )
        self.db_chapter_progress.exclude(lambda x: x.auth_user.id in self.inums)
        self.db_sub_chapters = current.db(
            (current.db.sub_chapters.chapter_id == chapter.id)
        ).select(current.db.sub_chapters.ALL, orderby=current.db.sub_chapters.id)
        self.problem_metrics = CourseProblemMetrics(self.course_id, self.users, chapter)
        rslogger.debug("About to call update_metrics")
        self.problem_metrics.update_metrics(self.course.course_name)

        self.user_activity = UserActivityMetrics(self.course.course_name, self.users)
        self.user_activity.update_metrics()

        self.progress_metrics = ProgressMetrics(
            self.course_id, self.db_sub_chapters, self.users
        )
        self.progress_metrics.update_metrics(self.db_chapter_progress)

        self.questions = {}
        for i in self.problem_metrics.problems.keys():
            self.questions[i] = (
                current.db(
                    (current.db.questions.name == i)
                    & (current.db.questions.base_course == self.course.base_course)
                )
                .select(current.db.questions.chapter, current.db.questions.subchapter)
                .first()
            )

    def load_user_metrics(self, username):
        self.username = username

        if not self.course:
            rslogger.debug("ERROR - NO COURSE course_id = {}".format(self.course_id))

        base_course = self.course.base_course

        self.chapters = current.db(
            current.db.chapters.course_id == base_course
        ).select()

        self.user = (
            current.db(
                (current.db.auth_user.username == username)
                & (current.db.auth_user.course_id == self.course_id)
            )
            .select(
                current.db.auth_user.id,
                current.db.auth_user.first_name,
                current.db.auth_user.last_name,
                current.db.auth_user.email,
                current.db.auth_user.username,
            )
            .first()
        )
        if not self.user:
            rslogger.debug(
                "ERROR - NO USER username={} course_id={}".format(
                    username, self.course_id
                )
            )
            current.session.flash = "Please make sure you are in the correct course"
            redirect(URL("default", "courses"))
            # TODO: calling redirect here is kind of a hacky way to handle this.

        self.db_chapter_progress = current.db(
            (current.db.user_sub_chapter_progress.user_id == self.user.id)
        ).select(
            current.db.user_sub_chapter_progress.chapter_id,
            current.db.user_sub_chapter_progress.sub_chapter_id,
            current.db.user_sub_chapter_progress.status,
        )
        self.formatted_activity = self.load_recent_activity()
        self.chapter_progress = UserActivityChapterProgress(
            self.chapters, self.db_chapter_progress
        )

    def load_recent_activity(self):
        week_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)
        res = current.db(
            (current.db.useinfo.sid == self.user.username)
            & (current.db.useinfo.course_id == self.course.course_name)
            & (current.db.useinfo.timestamp > week_ago)
        ).select(orderby=~current.db.useinfo.timestamp)

        return res

    def load_exercise_metrics(self, exercise):
        self.problem_metrics = CourseProblemMetrics(
            self.course_id, self.users, self.db_chapter
        )
        self.problem_metrics.update_metrics(self.course.course_name)

    def load_assignment_metrics(self, username, studentView=False):
        self.assignments = []

        res = current.db(current.db.assignments.course == self.course_id).select(
            current.db.assignments.id,
            current.db.assignments.name,
            current.db.assignments.points,
            current.db.assignments.duedate,
            current.db.assignments.released,
        )
        # ^ Get assignments from DB
        for aRow in res:
            self.assignments.append(aRow.as_dict())

        self.grades = {}
        for assign in self.assignments:
            rslogger.debug("Processing assignment %s", assign)
            row = current.db(
                (current.db.grades.assignment == assign["id"])
                & (current.db.grades.auth_user == current.db.auth_user.id)
            ).select(
                current.db.auth_user.username,
                current.db.grades.auth_user,
                current.db.grades.score,
                current.db.grades.assignment,
            )
            # ^ Get grades for assignment

            if row.records:  # If the row has a result
                rl = row.as_list()  # List of dictionaries
                rslogger.debug("RL = %s", rl)
                if (
                    studentView and not assign["released"]
                ):  # N/A should be shown to students if assignment grades are not released
                    self.grades[assign["name"]] = {
                        "score": "N/A",
                        "class_average": "N/A",
                        "due_date": assign["duedate"].date().strftime("%m-%d-%Y"),
                    }
                else:
                    s = 0.0
                    count = 0
                    self.grades[assign["name"]] = {}
                    for userEntry in rl:
                        rslogger.debug("GETTING USER SCORES %s", userEntry)
                        this_score = userEntry["grades"]["score"]
                        if this_score != None:
                            s += this_score  # Calculating average
                            count += 1
                            if (
                                userEntry["auth_user"]["username"] == username
                            ):  # If this is the student we are looking for
                                self.grades[assign["name"]]["score"] = this_score

                    if "score" not in self.grades[assign["name"]]:
                        self.grades[assign["name"]][
                            "score"
                        ] = "N/A"  # This is redundant as a failsafe
                    rslogger.debug("COUNT = %s", count)
                    try:
                        average = s / count
                    except:
                        average = 0
                    self.grades[assign["name"]]["class_average"] = "{:.02f}".format(
                        average
                    )
                    self.grades[assign["name"]]["due_date"] = (
                        assign["duedate"].date().strftime("%m-%d-%Y")
                    )

            else:  # The row has no result --> the query returned empty
                self.grades[assign["name"]] = {
                    "score": "N/A",
                    "class_average": "N/A",
                    "due_date": assign["duedate"].date().strftime("%m-%d-%Y"),
                }
