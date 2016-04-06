
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
    def __init__(self, course_id, problem_id):
        self.course_id = course_id
        self.problem_id = problem_id
        #total responses by answer choice, eg. A: 5, B: 3, C: 13
        self.aggregate_responses = {}
        #responses keyed by user
        self.user_responses = {}

    def add_data_point(self, row):
    	answer = row.act.split(':')
    	choice = answer[1]
    	correct = answer[2] == "correct"
    	self.aggregate_responses[choice] = self.aggregate_responses.get(choice, 0) + 1
    	
    	if not row.sid in self.user_responses:
    		self.user_responses[row.sid] = UserResponse()

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
	def __init__(self, course_id):
		self.course_id = course_id
		self.problems = {}
		self.update_metrics()

	def update_metrics(self):
		course = db(db.courses.id == self.course_id).select().first()
		rows = db((db.useinfo.course_id==course.course_name) & (db.useinfo.timestamp >= course.term_start_date)).select(db.useinfo.timestamp,db.useinfo.sid, db.useinfo.event,db.useinfo.act,db.useinfo.div_id,
        orderby=~db.useinfo.timestamp)
		print rows
		for row in rows:
			if row.event == "mChoice" or row.event == "fillb":
				if not row.div_id in self.problems:
					self.problems[row.div_id] = ProblemMetrics(self.course_id, row.div_id)

				self.problems[row.div_id].add_data_point(row)
		print self.problems





