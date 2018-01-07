db.define_table('questions',
                Field('base_course', type='string', notnull=True),
                Field('name', type='string', notnull=True),
                Field('chapter', type='string'),  # matches chapter_label, not name
                Field('subchapter', type='string'), # matches sub_chapter_label, not name
                Field('author', type='string'),
                Field('difficulty', type='integer'),
                Field('question', type='text'),
                Field('timestamp',type='datetime'),
                Field('question_type',type='string'),
                Field('is_private', type='boolean'),
                Field('htmlsrc', type='text'),
                Field('practice', type='boolean'),
                Field('autograde', type='string'),
                Field('practice', type='boolean'),
                migrate='runestone_questions.table')


db.define_table('tags',
                Field('tag_name', type='string', unique=True),
                migrate='runestone_tags.table')

db.define_table('question_tags',
                Field('question_id', db.questions),
                Field('tag_id', db.tags),
                migrate='runestone_question_tags.table')

## assignment <--> questions is a many-to-many relation. This table associates them
## points and how it's autograded are properties of a particular use of a question in an assignment,
## so that different instructors (assignments) can have a different way of doing it.
db.define_table('assignment_questions',
                Field('assignment_id', db.assignments),
                Field('question_id', db.questions),
                Field('points', type='integer'),
                Field('timed', type='boolean'), #deprecated; should be a property of the assignment
                Field('autograde', type='string'), # oneof: null, all_or_nothing, pct_correct
                Field('which_to_grade', type='string'), # oneof: first_answer, last_answer, last_answer_before_deadline, or best_answer
                Field('reading_assignment', type='boolean'), # so we can differentiate reading part of an assignment from the questions to be embedded on the assignment page
                                                             # Also use this when it's an mchoice or parsons that's within a subchapter, not to be embeddedon the assignment page
                Field('sorting_priority', type='integer'), #determines sort order of questions when displaying
                Field('activities_required', type='integer'), # specifies how many activities in a sub chapter a student must perform in order to receive credit
                migrate='runestone_assignment_questions.table')
