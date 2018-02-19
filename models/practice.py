db.define_table('user_topic_practice',
                Field('user_id', db.auth_user),
                Field('course_name', 'string'),
                Field('chapter_label', 'string'),
                Field('sub_chapter_label', 'string'),
                Field('question_name', 'string'),
                Field('i_interval', type='integer', notnull=True),
                Field('e_factor', type='double', notnull=True),
                Field('last_practice', type='datetime'),
                Field('last_presented', type='datetime'),
                Field('last_completed', type='datetime'),
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
                migrate='runestone_spacing_log.table')


db.define_table('user_topic_practice_Completion',
                Field('user_id', db.auth_user),
                Field('course_name', 'string'),
                Field('practice_completion_time', type='date'),
                migrate='user_topic_practice_Completion.table')


db.define_table('user_topic_practice_survey',
                Field('user_id', db.auth_user,
                      default=auth.user_id, update=auth.user_id, writable=False),
                Field('course_name', 'string'),
                Field('like_practice', requires=IS_IN_SET(['Like', 'Dislike'])),
                Field('response_time', type='datetime',
                      default=request.now, update=request.now, writable=False),
                migrate='user_topic_practice_survey.table')
