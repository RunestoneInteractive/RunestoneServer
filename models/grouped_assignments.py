db.define_table('assignments',
	Field('course',db.courses),
	Field('name', 'string'),
	Field('points', 'integer'),
	Field('query', 'string', default="", required=False),
	Field('grade_type', 'string', default="additive", requires=IS_IN_SET(['additive','checkmark'])),
	Field('threshold', 'integer', default=1),
	format='%(name)s',
	migrate='runestone_assignments.table'
	)

def assignment_get_problems(assignment, user):
	return db(db.code.acid.like(assignment.query+"%"))(db.code.sid==user.username).select(
		db.code.ALL,
		orderby=db.code.acid|~db.code.timestamp,
		distinct=db.code.acid,
		)
db.assignments.problems = Field.Method(lambda row, user: assignment_get_problems(row.assignments, user))
def assignment_set_grade(assignment, user):
	# delete the old grades; we're regrading
	db(db.grades.assignment == assignment.id)(db.grades.auth_user == user.id).delete()
	
	points = 0.0
	for prob in assignment.problems(user):
		if not prob.grade:
			continue
		points = points + prob.grade

	if assignment.grade_type == 'checkmark':
		#threshold grade
		if points >= assignment.threshold:
			points = assignment.points
		else:
			points = 0
	else:
		# they got the points they earned
		pass

	db.grades.insert(
		auth_user = user.id,
		assignment = assignment.id,
		score = points,
		)
	return points
db.assignments.grade = Field.Method(lambda row, user: assignment_set_grade(row.assignments, user))

db.define_table('grades',
	Field('auth_user', db.auth_user),
	Field('assignment', db.assignments),
	Field('score', 'double'),
	migrate='runestone_grades.table',
	)

db.define_table('deadlines',
	Field('assignment', db.assignments, requires=IS_IN_DB(db,'assignments.id',db.assignments._format)),
	Field('section', db.sections, requires=IS_EMPTY_OR(IS_IN_DB(db,'sections.id','%(name)s'))),
	Field('deadline','datetime'),
	migrate='runestone_deadlines.table',
	)