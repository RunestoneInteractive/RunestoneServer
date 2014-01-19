db.define_table('assignments',
	Field('name', 'string'),
	Field('points', 'integer'),
	Field('query', 'string', default="", required=False),
	Field('grade_type', 'string', default="additive"),
	Field('threshold', 'integer', default=1),
	migrate='runestone_assignments.table'
	)
db.assignments.problems = Field.Method(lambda row: [])
db.assignments.grade = Field.Method(lambda row, user: 10)