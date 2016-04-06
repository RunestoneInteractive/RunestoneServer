
db.define_table('dash_problem_answers',
  Field('timestamp','datetime'),
  Field('sid','string'),
  Field('event','string'),
  Field('act','string'),
  Field('div_id','string'),
  Field('course_id','string'),
  migrate='runestone_useinfo.table'
)


db.define_table('dash_problem_user_metrics',
  Field('timestamp','datetime'),
  Field('sid','string'),
  Field('event','string'),
  Field('act','string'),
  Field('div_id','string'),
  Field('course_id','string'),
  migrate='runestone_useinfo.table'
)

# it would be good at some point to save these to a table and
# periodicly update them with new log entries instead of having
# to regenerate the entire collection of metrics everytime.
class ProblemMetrics(object):
    def __init__(self, course_id, problem_id, users):
        self.course_id = course_id
        self.problem_id = problem_id
        #total responses by answer choice, eg. A: 5, B: 3, C: 13
        self.aggregate_responses = {}
        #responses keyed by user
        self.user_responses = {}

        for user in users:
        	self.user_responses[user.username] = UserResponse()

    def add_data_point(self, row):
    	answer = row.act.split(':')
    	choice = answer[1]
    	correct = answer[2] == "correct"
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
    		histogram[attempts] = histogram.get(attempts,0) + 1
    	return histogram
class UserResponse(object):
	NOT_ATTEMPTED = 0
	INCOMPLETE = 1
	CORRECT = 2
	CORRECT_AFTER_MULTIPLE_ATTEMPTS = 3

	def __init__(self):
		self.status = UserResponse.NOT_ATTEMPTED
		self.correct = False
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
			self.user_activities[user.username] = UserActivity()

	def update_metrics(self, logs):
		for row in logs:
			if row.sid in self.user_activities:
				self.user_activities[row.sid].add_activity(row)

class UserActivity(object):
	def __init__(self):
		self.rows = []

	def add_activity(self, row):
		self.rows.append(row)

class DashboardDataAnalyzer(object):
	def __init__(self, course_id):
		self.course_id = course_id

		#go get all the course data... in the future the post processing
		#should probably be stored and only new data appended.
		self.course = db(db.courses.id == self.course_id).select().first()
		self.users = db(db.auth_user.course_id == auth.user.course_id).select(db.auth_user.username, db.auth_user.first_name,db.auth_user.last_name)
		self.logs = db((db.useinfo.course_id==self.course.course_name) & (db.useinfo.timestamp >= self.course.term_start_date)).select(db.useinfo.timestamp,db.useinfo.sid, db.useinfo.event,db.useinfo.act,db.useinfo.div_id, orderby=db.useinfo.timestamp)
		self.chapter_progress = db((db.user_sub_chapter_progress.user_id == db.auth_user.id) &
			(db.auth_user.course_id == auth.user.course_id)).select(db.auth_user.username,db.user_sub_chapter_progress.sub_chapter_id)
		print self.chapter_progress
		self.problem_metrics = CourseProblemMetrics(course_id, self.users)
		self.problem_metrics.update_metrics(self.logs)
		self.user_activity = UserActivityMetrics(course_id, self.users)
		self.user_activity.update_metrics(self.logs)


		#if row.event == "mChoice" or row.event == "fillb":
		#if row.event == "page":
			


