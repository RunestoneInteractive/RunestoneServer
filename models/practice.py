db.define_table('course_practice',
                Field('auth_user_id', 'reference auth_user', label=T('Instructor Name'), required=True, default=1),
                Field('course_name', 'string'),
                Field('start_date', type='date'),
                Field('end_date', type='date'),
                Field('max_practice_days', type='integer'),
                Field('max_practice_questions', type='integer'),
                Field('day_points', type='double'),
                Field('question_points', type='double'),
                Field('questions_to_complete_day', type='integer'),
                Field('graded', type='integer'),
                Field('spacing', type='integer'),
                Field('interleaving', type='integer'),
                # A value of 0 indicates self-paced (when student marks a page complete).
                # A value of 1 indicates whenever a page is assigned in any reading assignment and the reading
                #   assignment deadline passes.
                # A value of 2 indicates manually by the instructor, as it is implemented currently.
                Field('flashcard_creation_method', type='integer', default=0),
                migrate='course_practice.table')


db.define_table('user_topic_practice',
                Field('user_id', db.auth_user),
                Field('course_name', 'string'),
                Field('chapter_label', 'string'),
                Field('sub_chapter_label', 'string'),
                Field('question_name', 'string'),
                Field('i_interval', type='integer', notnull=True),
                Field('e_factor', type='double', notnull=True),
                Field('q', type='integer', notnull=True, default=0),
                Field('last_presented', type='datetime'),
                Field('last_completed', type='datetime'),
                Field('next_eligible_date', type='date'),
                Field('creation_time', type='datetime'),
                Field('timezoneoffset', type='integer', default=0),
                migrate='runestone_spacing.table')


db.define_table('user_topic_practice_log',
                Field('user_id', db.auth_user),
                Field('course_name', 'string'),
                Field('chapter_label', 'string'),
                Field('sub_chapter_label', 'string'),
                Field('question_name', 'string'),
                Field('i_interval', type='integer', notnull=True),
                Field('e_factor', type='double', notnull=True),
                Field('q', type='integer', notnull=True, default=-1),
                Field('trials_num', type='integer', notnull=True),
                Field('available_flashcards', type='integer', notnull=True, default=-1),
                Field('start_practice', type='datetime'),
                Field('end_practice', type='datetime'),
                Field('timezoneoffset', type='integer', default=0),
                Field('next_eligible_date', type='date'),
                migrate='runestone_spacing_log.table')


db.define_table('user_topic_practice_Completion',
                Field('user_id', db.auth_user),
                Field('course_name', 'string'),
                Field('practice_completion_date', type='date'),
                migrate='user_topic_practice_Completion.table')


db.define_table('user_topic_practice_survey',
                Field('user_id', db.auth_user,
                      default=auth.user_id, update=auth.user_id, writable=False),
                Field('course_name', 'string'),
                Field('like_practice', requires=IS_IN_SET(['Like', 'Dislike'])),
                Field('response_time', type='datetime',
                      default=request.now, update=request.now, writable=False),
                Field('timezoneoffset', type='integer', default=0),
                migrate='user_topic_practice_survey.table')


db.define_table('user_topic_practice_feedback',
                Field('user_id', db.auth_user,
                      default=auth.user_id, update=auth.user_id, writable=False),
                Field('course_name', 'string'),
                Field('feedback', 'string'),
                Field('response_time', type='datetime',
                      default=request.now, update=request.now, writable=False),
                Field('timezoneoffset', type='integer', default=0),
                migrate='user_topic_practice_feedback.table')
