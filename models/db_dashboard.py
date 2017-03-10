from collections import OrderedDict
import logging

rslogger = logging.getLogger('web2py.app.runestone')
rslogger.setLevel('DEBUG')

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
        if ':' in row.act:
            answer = row.act.split(':')
            choice = answer[1]
            correct = answer[2] == "correct"
            if choice == "":
                choice = "(empty)"

            self.aggregate_responses[choice] = self.aggregate_responses.get(choice, 0) + 1

            if row.sid in self.user_responses:
                self.user_responses[row.sid].add_response(choice, correct)

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
    def __init__(self, course_id, users):
        self.course_id = course_id
        self.problems = {}
        self.users = users

    def update_metrics(self, logs):
        for row in logs:
            if row.event == "mChoice" or row.event == "fillb":
                if not row.div_id in self.problems:
                    self.problems[row.div_id] = ProblemMetrics(self.course_id, row.div_id, self.users)

                self.problems[row.div_id].add_data_point(row)

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
        return len(self.rows)

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
        for subchapter_label, status in self.sub_chapters.iteritems():
            subchapters.append({
                "label": IdConverter.sub_chapter_label_to_text(subchapter_label),
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
            print sub_chapter
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
        self.sub_chapter_text = IdConverter.sub_chapter_label_to_text(sub_chapter.sub_chapter_label)
        self.not_started = 0
        self.started = 0
        self.completed = 0
        self.total_users = total_users

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
    def __init__(self, course_id):
        self.course_id = course_id

    def load_chapter_metrics(self, chapter):
        if not chapter:
            rslogger.debug("chapter not set, abort!")
            return

        self.db_chapter = chapter
        #go get all the course data... in the future the post processing
        #should probably be stored and only new data appended.
        self.course = db(db.courses.id == self.course_id).select().first()
        self.users = db(db.auth_user.course_id == auth.user.course_id).select(db.auth_user.username, db.auth_user.first_name,db.auth_user.last_name)
        self.logs = db((db.useinfo.course_id==self.course.course_name) & (db.useinfo.timestamp >= self.course.term_start_date)).select(db.useinfo.timestamp,db.useinfo.sid, db.useinfo.event,db.useinfo.act,db.useinfo.div_id, orderby=db.useinfo.timestamp)
        self.db_chapter_progress = db((db.user_sub_chapter_progress.user_id == db.auth_user.id) &
            (db.auth_user.course_id == auth.user.course_id) &  # todo: missing link from course_id to chapter/sub_chapter progress
            (db.user_sub_chapter_progress.chapter_id == chapter.chapter_label)).select(db.auth_user.username,db.user_sub_chapter_progress.chapter_id,db.user_sub_chapter_progress.sub_chapter_id,db.user_sub_chapter_progress.status)

        self.db_sub_chapters = db((db.sub_chapters.chapter_id == chapter.id)).select(db.sub_chapters.ALL,orderby=db.sub_chapters.id)
        #self.divs = db(db.div_ids).select(db.div_ids.div_id)
        #print self.divs
        self.problem_metrics = CourseProblemMetrics(self.course_id, self.users)
        self.problem_metrics.update_metrics(self.logs)
        self.user_activity = UserActivityMetrics(self.course_id, self.users)
        self.user_activity.update_metrics(self.logs)
        self.progress_metrics = ProgressMetrics(self.course_id, self.db_sub_chapters, self.users)
        self.progress_metrics.update_metrics(self.logs, self.db_chapter_progress)

    def load_user_metrics(self, username):
        self.username = username
        self.course = db(db.courses.id == self.course_id).select().first()
        self.chapters = db(db.chapters.course_id == auth.user.course_name).select()
        self.user = db((db.auth_user.username == username) & (db.auth_user.course_id == self.course_id)).select(db.auth_user.id, db.auth_user.first_name, db.auth_user.last_name, db.auth_user.email, db.auth_user.username).first()
        self.logs = db((db.useinfo.course_id==self.course.course_name) & (db.useinfo.sid == username) & (db.useinfo.timestamp >= self.course.term_start_date)).select(db.useinfo.timestamp,db.useinfo.sid, db.useinfo.event,db.useinfo.act,db.useinfo.div_id, orderby=~db.useinfo.timestamp)
        self.db_chapter_progress = db((db.user_sub_chapter_progress.user_id == self.user.id)).select(db.user_sub_chapter_progress.chapter_id,db.user_sub_chapter_progress.sub_chapter_id,db.user_sub_chapter_progress.status)
        print self.db_chapter_progress
        print self.logs
        print self.user
        self.formatted_activity = UserLogCategorizer(self.logs)
        self.chapter_progress = UserActivityChapterProgress(self.chapters, self.db_chapter_progress)

    def load_exercise_metrics(self, exercise):
        self.course = db(db.courses.id == self.course_id).select().first()
        self.users = db(db.auth_user.course_id == auth.user.course_id).select(db.auth_user.username, db.auth_user.first_name,db.auth_user.last_name)
        self.logs = db((db.useinfo.course_id==self.course.course_name) & (db.useinfo.timestamp >= self.course.term_start_date)).select(db.useinfo.timestamp,db.useinfo.sid, db.useinfo.event,db.useinfo.act,db.useinfo.div_id, orderby=db.useinfo.timestamp)
        self.problem_metrics = CourseProblemMetrics(self.course_id, self.users)
        self.problem_metrics.update_metrics(self.logs)

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

    sub_chapter_id_map = {
        #CSP - Ch1
        "studentBook": "This Book is for Stuents",
        "pretest": "Pretest",
        "computeNumbers": "Compute with Numbers",
        "computeWords": "Compute with Words",
        "computeTurtles": "Compute with Turtles",
        "computeImages": "Compute with Images",
        "standards": "Standards - Big Ideas",
        "ch1_summary": "Chapter 1 - Concept Summary",
        #CSP - Ch2
        "whatIsComputer": "What is a Computer?",
        "turingMachines": "Turing Machines",
        "abilities": "Computer Abilities",
        "ch2_summary": "Chapter 2 - Concept Summary",
        "exam1a2": "Exam Questions for Chapters 1 and 2",
        #CSP - Ch3
        "assignName": "Assigning a Name",
        "expression": "Expressions",
        "expressionTable": "Summary of Expression Types",
        "orderOfOperations": "How Expressions are Evaluated",
        "driving": "Driving from Chicago to Dallas",
        "ketchup": "Following the Ketchup Ooze",
        "walkAssign": "Walking through Assignment more Generally",
        "invoice": "Figuring out an Invoice",
        "ch3_summary": "Chapter 3 - Summary",
        "ch3_exercises": "Chapter 3 Exercises",
        #CSP - Ch4
        "assignNameStr":"Assign a Name to a String",
        "strObjects":"Strings are Objects",
        "immutable":"Strings are Immutable",
        "madlib":"Making a MadLib Story",
        "ch4_summary":"Chapter 4 - Summary",
        "ch4_exercises":"Chapter 4 Exercises",
        "exam3a4":"Exam Questions for Chapters 3 and 4",
        #CSP - Ch5
        "names4turtles": "Assign a Name to a Turtle",
        "FuncAndProc": "Procedures and Functions",
        "turtleFAP": "More Turtle Procedures and Functions",
        "multTurtles": "Single and Multiple Turtles",
        "ch5_summary": "Chapter 5 - Summary",
        "ch5_exercises": "Chapter 5 Exercises",
        "house": "Bob Builds a House",
        "changeProg": "Changing Turtle Programs"
#CSP - Ch6

    }
    @staticmethod
    def problem_id_to_text(problem_id):
        return IdConverter.problem_id_map.get(problem_id, problem_id)

    @staticmethod
    def sub_chapter_label_to_text(sub_chapter_label):
        return IdConverter.sub_chapter_id_map.get(sub_chapter_label, sub_chapter_label)
