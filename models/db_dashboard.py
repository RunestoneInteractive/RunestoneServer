from collections import OrderedDict
import logging
from datetime import datetime, timedelta

rslogger = logging.getLogger(settings.logger)
rslogger.setLevel(settings.log_level)

#db.define_table('dash_problem_answers',
#  Field('timestamp','datetime'),
#  Field('sid','string'),
#  Field('event','string'),
#  Field('act','string'),
#  Field('div_id','string'),
#  Field('course_id','string'),
#  migrate='runestone_useinfo.table'
#)


#db.define_table('dash_problem_user_metrics',
#  Field('timestamp','datetime'),
#  Field('sid','string'),
#  Field('event','string'),
#  Field('act','string'),
#  Field('div_id','string'),
#  Field('course_id','string'),
#  migrate='runestone_useinfo.table'
#)

# it would be good at some point to save these to a table and
# periodicly update them with new log entries instead of having
# to regenerate the entire collection of metrics everytime.
class ProblemMetrics(object):
    def __init__(self, course_id, problem_id, users):
        self.course_id = course_id
        self.problem_id = problem_id
        self.problem_text = IdConverter.problem_id_to_text(problem_id)
        #total responses by answer choice, eg. A: 5, B: 3, C: 13
        self.aggregate_responses = {}
        #responses keyed by user
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

        for sid, user_response in self.user_responses.iteritems():
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
        for username, user_response in self.user_responses.iteritems():
            attempts = len(user_response.responses)
            if attempts >= 5:
                attempts = "5+"
            histogram[attempts] = histogram.get(attempts,0) + 1
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
        self.user = '{0} {1}'.format(user.first_name, user.last_name)
        self.responses = []

    def add_response(self, response, correct):
        if not self.correct: #ignore if the person already answered it correctly.
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
        rslogger.debug("Updating CourseProblemMetrics for {}".format(self.chapter))
        rslogger.debug("doing chapter {}".format(self.chapter))
        # todo:  Join this with questions so that we can limit the questions to the selected chapter
        mcans = db((db.mchoice_answers.course_name==course_name) &
                   (db.mchoice_answers.div_id == db.questions.name) &
                   (db.questions.chapter == self.chapter.chapter_label)
                    ).select(orderby=db.mchoice_answers.timestamp)
        rslogger.debug("Found {} exercises")
        fbans = db((db.fitb_answers.course_name==course_name) &
                   (db.fitb_answers.div_id == db.questions.name) &
                   (db.questions.chapter == self.chapter.chapter_label)
                   ).select(orderby=db.fitb_answers.timestamp)
        psans = db((db.parsons_answers.course_name==course_name) &
                   (db.parsons_answers.div_id == db.questions.name) &
                   (db.questions.chapter == self.chapter.chapter_label)
                   ).select(orderby=db.parsons_answers.timestamp)

        # convert the numeric answer to letter answers to match the questions easier.
        to_letter = dict(zip("0123456789", "ABCDEFGHIJ"))

        for row in mcans:
            mc = row['mchoice_answers']
            mc.answer = to_letter.get(mc.answer, mc.answer)

        def add_problems(result_set,tbl):
            for srow in result_set:
                row = srow[tbl]
                rslogger.debug("UPDATE_METRICS {}".format(row))
                if not row.div_id in self.problems:
                    self.problems[row.div_id] = ProblemMetrics(self.course_id, row.div_id, self.users)
                self.problems[row.div_id].add_data_point(row)
        add_problems(mcans, 'mchoice_answers')
        add_problems(fbans, 'fitb_answers')
        add_problems(psans, 'parsons_answers')

    def retrieve_chapter_problems(self):
        return self

class UserActivityMetrics(object):
    def __init__(self, course_id, users):
        self.course_id = course_id
        self.user_activities = {}
        for user in users:
            self.user_activities[user.username] = UserActivity(user)

    def update_metrics(self, logs):
        for row in logs:
            if row.sid in self.user_activities:
                self.user_activities[row.sid].add_activity(row)

class UserActivity(object):
    def __init__(self, user):
        self.name = "{0} {1}".format(user.first_name,user.last_name)
        self.username = user.username
        self.rows = []
        self.page_views = []
        # self.exercise_correct  -- cannot find any refs to this unset attr.

    def add_activity(self, row):
        self.rows.append(row)

    def get_page_views(self):
        # returns page views for all time
        return len(self.rows)

    def get_recent_page_views(self):
        # returns page views for the last 7 days
        recentViewCount = 0
        current = len(self.rows) - 1
        while current >= 0 and self.rows[current]['timestamp'] >= datetime.utcnow() - timedelta(days=7):
            recentViewCount += 1
            current = current - 1
        return recentViewCount


    def get_activity_stats(self):
        return self

class UserActivityChapterProgress(object):
    def __init__(self, chapters, sub_chapter_progress):
        self.chapters = OrderedDict()
        for chapter in chapters:
            self.chapters[chapter.chapter_label] = UserActivitySubChapterProgress(chapter)
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
        subchapter_res = db(db.sub_chapters.chapter_id == self.chapter_id).select()
        sub_chapter_label_to_text = {sc.sub_chapter_label : sc.sub_chapter_name for sc in subchapter_res}
        for subchapter_label, status in self.sub_chapters.iteritems():
            subchapters.append({
                "label": sub_chapter_label_to_text.get(subchapter_label,subchapter_label),
                "status": UserActivitySubChapterProgress.completion_status_to_text(status)
                })
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
    def __init__(self, course_id, sub_chapters, users):
        self.sub_chapters = OrderedDict()
        for sub_chapter in sub_chapters:
            rslogger.debug(sub_chapter)
            self.sub_chapters[sub_chapter.sub_chapter_label] = SubChapterActivity(sub_chapter, len(users))

    def update_metrics(self, logs, chapter_progress):
        for row in chapter_progress:
            try:
                self.sub_chapters[row.user_sub_chapter_progress.sub_chapter_id].add_activity(row)
            except KeyError as  e:
                rslogger.debug("Key error for {} user is {}".format(row.user_sub_chapter_progress.sub_chapter_id, auth.user.username))



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

class UserLogCategorizer(object):
    def __init__(self, logs):
        self.activities = []
        for log in logs:
            self.activities.append({
                "time": log.timestamp,
                "event": UserLogCategorizer.format_event(log.event, log.act, log.div_id)
                })

    @staticmethod
    def format_event(event, action, div_id):
        short_div_id = div_id
        if len(div_id) > 25:
            short_div_id = "...{0}".format(div_id[-25:])
        if (event == 'page') & (action == 'view'):
            return "{0} {1}".format("Viewed", short_div_id)
        elif (event == 'timedExam') & (action =='start'):
            return "{0} {1}".format("Started Timed Exam", div_id)
        elif (event == 'timedExam') & (action =='finish'):
            return "{0} {1}".format("Finished Timed Exam", div_id)
        elif (event == 'highlight'):
            return "{0} {1}".format("Highlighted", short_div_id)
        elif (event == 'activecode') & (action == 'run'):
            return "{0} {1}".format("Ran Activecode", div_id)
        elif (event == 'parsons') & (action == 'yes'):
            return "{0} {1}".format("Solved Parsons", div_id)
        elif (event == 'parsons') & (action != 'yes'):
            return "{0} {1}".format("Attempted Parsons", div_id)
        elif (event == 'mChoice') | (event == 'fillb'):
            answer = action.split(':')
            if action.count(':') == 2 and answer[2] == 'correct':
                return "{0} {1}".format("Solved", div_id)
            return "{0} {1}".format("Attempted", div_id)
        return "{0} {1}".format(event, div_id)

class DashboardDataAnalyzer(object):
    def __init__(self, course_id, chapter=None):
        self.course_id = course_id
        if chapter:
            self.db_chapter = chapter
        else:
            self.db_chapter = None

    def load_chapter_metrics(self, chapter):
        if not chapter:
            rslogger.error("chapter not set, abort!")
            session.flash = "Error No Course Data in DB"
            return

        self.db_chapter = chapter
        #go get all the course data... in the future the post processing
        #should probably be stored and only new data appended.
        self.course = db(db.courses.id == self.course_id).select().first()
        rslogger.debug("COURSE QUERY GOT %s", self.course)
        self.users = db((db.auth_user.course_id == auth.user.course_id) & (db.auth_user.active == 'T') ).select(db.auth_user.username, db.auth_user.first_name,db.auth_user.last_name, db.auth_user.id)
        self.instructors = db((db.course_instructor.course == auth.user.course_id)).select(db.course_instructor.instructor)
        inums = [x.instructor for x in self.instructors]
        self.users.exclude(lambda x: x.id in inums)
        self.logs = db((db.useinfo.course_id==self.course.course_name) & (db.useinfo.timestamp >= self.course.term_start_date)).select(db.useinfo.timestamp,db.useinfo.sid, db.useinfo.event,db.useinfo.act,db.useinfo.div_id, orderby=db.useinfo.timestamp)
        # todo:  Yikes!  Loading all of the log data for a large or even medium class is a LOT
        self.db_chapter_progress = db((db.user_sub_chapter_progress.user_id == db.auth_user.id) &
            (db.auth_user.course_id == auth.user.course_id) &  # todo: missing link from course_id to chapter/sub_chapter progress
            (db.user_sub_chapter_progress.chapter_id == chapter.chapter_label)).select(db.auth_user.username,db.user_sub_chapter_progress.chapter_id,db.user_sub_chapter_progress.sub_chapter_id,db.user_sub_chapter_progress.status,db.auth_user.id)
        self.db_chapter_progress.exclude(lambda x: x.auth_user.id in inums)
        self.db_sub_chapters = db((db.sub_chapters.chapter_id == chapter.id)).select(db.sub_chapters.ALL,orderby=db.sub_chapters.id)
        self.problem_metrics = CourseProblemMetrics(self.course_id, self.users, chapter)
        rslogger.debug("About to call update_metrics")
        self.problem_metrics.update_metrics(self.course.course_name)
        self.user_activity = UserActivityMetrics(self.course_id, self.users)
        self.user_activity.update_metrics(self.logs)
        self.progress_metrics = ProgressMetrics(self.course_id, self.db_sub_chapters, self.users)
        self.progress_metrics.update_metrics(self.logs, self.db_chapter_progress)
        self.questions = {}
        for i in self.problem_metrics.problems.keys():
            self.questions[i] = db(db.questions.name == i).select(db.questions.chapter, db.questions.subchapter).first()

    def load_user_metrics(self, username):
        self.username = username
        self.course = db(db.courses.id == self.course_id).select().first()
        if not self.course:
            rslogger.debug("ERROR - NO COURSE course_id = {}".format(self.course_id))

        self.chapters = db(db.chapters.course_id == auth.user.course_name).select()
        self.user = db((db.auth_user.username == username) &
                       (db.auth_user.course_id == self.course_id)).select(db.auth_user.id, db.auth_user.first_name, db.auth_user.last_name, db.auth_user.email, db.auth_user.username).first()
        if not self.user:
            rslogger.debug("ERROR - NO USER username={} course_id={}".format(username, self.course_id))
            session.flash = 'Please make sure you are in the correct course'
            redirect('/runestone/default/courses')

        self.logs = db((db.useinfo.course_id==self.course.course_name) &
                       (db.useinfo.sid == username) &
                       (db.useinfo.timestamp >= self.course.term_start_date)).select(db.useinfo.timestamp,db.useinfo.sid, db.useinfo.event,db.useinfo.act,db.useinfo.div_id, orderby=~db.useinfo.timestamp)
        self.db_chapter_progress = db((db.user_sub_chapter_progress.user_id == self.user.id)).select(db.user_sub_chapter_progress.chapter_id,db.user_sub_chapter_progress.sub_chapter_id,db.user_sub_chapter_progress.status)
        self.formatted_activity = UserLogCategorizer(self.logs)
        self.chapter_progress = UserActivityChapterProgress(self.chapters, self.db_chapter_progress)

    def load_exercise_metrics(self, exercise):
        self.course = db(db.courses.id == self.course_id).select().first()
        self.users = db(db.auth_user.course_id == auth.user.course_id).select(db.auth_user.username, db.auth_user.first_name,db.auth_user.last_name)
        self.logs = db((db.useinfo.course_id==self.course.course_name) & (db.useinfo.timestamp >= self.course.term_start_date)).select(db.useinfo.timestamp,db.useinfo.sid, db.useinfo.event,db.useinfo.act,db.useinfo.div_id, orderby=db.useinfo.timestamp)
        self.problem_metrics = CourseProblemMetrics(self.course_id, self.users,self.db_chapter)
        self.problem_metrics.update_metrics(self.course.course_name)

    def load_assignment_metrics(self, username, studentView=False):
        self.assignments = []

        res = db(db.assignments.course == self.course_id)\
                .select(db.assignments.id, db.assignments.name, db.assignments.points, db.assignments.duedate, db.assignments.released)
                # ^ Get assignments from DB
        for aRow in res:
            self.assignments.append(aRow.as_dict())

        self.grades = {}
        for assign in self.assignments:
            rslogger.debug("Processing assignment %s",assign)
            row = db((db.grades.assignment == assign["id"]) & (db.grades.auth_user == db.auth_user.id))\
                    .select(db.auth_user.username, db.grades.auth_user, db.grades.score, db.grades.assignment)
                    # ^ Get grades for assignment

            if row.records:             # If the row has a result
                rl = row.as_list()      # List of dictionaries
                rslogger.debug("RL = %s", rl)
                if studentView and not assign['released']:      # N/A should be shown to students if assignment grades are not released
                    self.grades[assign["name"]] = {"score":"N/A",
                                               "class_average":"N/A",
                                               "due_date":assign["duedate"].date().strftime("%m-%d-%Y")}
                else:
                    s = 0.0
                    count = 0
                    self.grades[assign["name"]] = {}
                    for userEntry in rl:
                        rslogger.debug("GETTING USER SCORES %s",userEntry)
                        s += userEntry["grades"]["score"]   # Calculating average
                        count += 1
                        if userEntry["auth_user"]["username"] == username:      # If this is the student we are looking for
                            self.grades[assign["name"]]["score"] = userEntry["grades"]["score"]

                    if 'score' not in self.grades[assign["name"]]:
                            self.grades[assign["name"]]["score"] = "N/A"        # This is redundant as a failsafe
                    rslogger.debug("COUNT = %s", count)
                    average = s/count
                    self.grades[assign["name"]]["class_average"] = "{:.02f}".format(average)
                    self.grades[assign["name"]]["due_date"] = assign["duedate"].date().strftime("%m-%d-%Y")

            else:           # The row has no result --> the query returned empty
                self.grades[assign["name"]] = {"score":"N/A",
                                               "class_average":"N/A",
                                               "due_date":assign["duedate"].date().strftime("%m-%d-%Y")}

# This whole object is a workaround because these strings
# are not generated and stored in the db. This needs automating
# to support all books.
class IdConverter(object):
    problem_id_map = {
        "pre_1":"Pretest-1: What will be the values in x, y, and z after the following lines of code execute?",
        "pre_2":"Pretest-2: What is the output from the program below?",
        "1_3_1_BMI_Q1":"1-3-1: Imagine that you are 5 foot 7 inches and weighed 140 pounds. What is your BMI?",
        "1_4_1_String_Methods_Q1":"1-4-1: What would the following code print?",
        "1_5_1_Turtle_Q1":"1-5-1: Which direction will alex move when the code below executes?",
        "":"1-5-2: ",
        "1_6_1_Image_Q1":"1-6-1: Which way does y increase on an image?",

        "3_2_1_Mult_fill":"3-2-1: What will be printed when you click on the Run button in the code below?",
        "3_2_2_Div_fill":"3-2-2: What will be printed when you click on the Run button in the code below?",
        "3_2_3_Mod_fill":"3-2-3: What will be printed when you click on the Run button in the code below?",
        "4_1_2_noSpace":"4-1-2: What will be printed when the following executes?",
        "4_2_2_Slice2":"4-2-2: What will be printed when the following executes?",

        "4_3_1_s1":"4-3-1: Given the following code segment, what is the value of the string s1 after these are executed?",
        "4_3_2_s2":"4-3-2: What is the value of s1 after the following code executes?",
    }

    @staticmethod
    def problem_id_to_text(problem_id):
        return IdConverter.problem_id_map.get(problem_id, problem_id)
