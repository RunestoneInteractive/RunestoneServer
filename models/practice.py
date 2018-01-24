db.define_table('user_topic_practice',
                Field('user_id', db.auth_user),
                Field('course_name', 'string'),
                Field('chapter_label', 'string'),
                Field('sub_chapter_label', 'string'),
                Field('question_name', 'string'),
                Field('i_interval', type='integer', notnull=True),
                Field('e_factor', type='double', notnull=True),
                Field('last_practice', type='datetime'),
                migrate='runestone_spacing.table')


db.define_table('user_topic_practice_log',
                Field('user_id', db.auth_user),
                Field('course_name', 'string'),
                Field('chapter_label', 'string'),
                Field('sub_chapter_label', 'string'),
                Field('question_name', 'string'),
                Field('i_interval', type='integer', notnull=True),
                Field('e_factor', type='double', notnull=True),
                Field('trials_num', type='integer', notnull=True),
                Field('start_practice', type='datetime'),
                Field('end_practice', type='datetime'),
                migrate='runestone_spacing_log.table')


db.define_table('user_topic_practice_Completion',
                Field('user_id', db.auth_user),
                Field('course_name', 'string'),
                Field('practice_completion_time', type='date'),
                migrate='user_topic_practice_Completion.table')
