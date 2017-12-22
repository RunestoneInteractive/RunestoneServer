db.define_table('user_topic_practice',
                Field('user_id', db.auth_user),
                Field('chapter_name','string'),
                Field('sub_chapter_label','string'),
                Field('question_name','string'),
                Field('i_interval', type='integer', notnull=True),
                Field('e_factor', type='double', notnull=True),
                Field('last_practice', type='datetime'),
                migrate='runestone_spacing.table')
