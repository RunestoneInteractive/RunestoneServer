db.define_table('questions',
                Field('base_course', type='string', notnull=True),
                Field('name', type='string', notnull=True),
                Field('chapter', type='string'),
                Field('subchapter', type='string'),
                Field('author', type='string'),
                Field('difficulty', type='integer'),
                Field('question', type='text'),
                Field('timestamp',type='datetime'),
                Field('question_type',type='string'),
                Field('is_private', type='boolean'),
                Field('htmlsrc', type='text'),
                Field('gradeable_div', type='string'),
                Field('grading_type', type='string'),
                migrate='runestone_questions.table')

# In SQL we can manually add the constraint
# alter table questions add constraint name_bc_unique UNIQUE(name, base_course);
try:
    db.executesql('''alter table questions add constraint name_bc_unique UNIQUE(name, base_course)''')
except:
    pass

db.define_table('question_grades',
    # This table records grades on individual gradeable items
    Field('sid', type='string', notnull=True),
    Field('course_name',type='string', notnull=True),
    Field('div_id', type = 'string', notnull=True),
    Field('useinfo_id', db.useinfo), # the particular useinfo run that was graded
    Field('score', type='double'),
    Field('comment', type = 'text'),
    migrate='runestone_question_grades.table',
    )


db.define_table('tags',
                Field('tag_name', type='string', unique=True),
                migrate='runestone_tags.table')

db.define_table('question_tags',
                Field('question_id', db.questions),
                Field('tag_id', db.tags),
                migrate='runestone_question_tags.table')

db.define_table('assignment_questions',
                Field('assignment_id', db.assignments),
                Field('question_id', db.questions),
                Field('points', type='integer'),
                Field('timed', type='boolean'),
                Field('assessment_type', db.assignment_types,
                      requires=IS_EMPTY_OR(IS_IN_DB(db, 'assignment_types.id', '%(name)s'))),
                migrate='runestone_assignment_questions.table')
