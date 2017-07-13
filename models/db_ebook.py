# Files in the model directory are loaded in alphabetical order.  This one needs to be loaded after db.py

db.define_table('useinfo',
  Field('timestamp','datetime'),
  Field('sid','string'),
  Field('event','string'),
  Field('act','string'),
  Field('div_id','string'),
  Field('course_id','string'),
  migrate='runestone_useinfo.table'
)

# stores student's saved code and, unfortunately, comments and grades, which really should be their own table linked to this
db.define_table('code',
  Field('acid','string'),
  Field('code','text'),
  Field('emessage','text'),
  Field('course_id','integer'),
  Field('grade','double'),
  Field('sid','string'),
  Field('timestamp','datetime'),
  Field('comment','text'),
  Field('language','text', default='python'),
  migrate='runestone_code.table'
)

# Stores the source code for activecodes, including prefix and suffix code, so that prefixes and suffixes can be run when grading
# Contents of this table are filled when processing activecode directives, in activecod.py
db.define_table('source_code',
  Field('acid','string', required=True),
  Field('course_id', 'string'),
  Field('includes', 'string'), # comma-separated string of acid main_codes to include when running this source_code
  Field('available_files', 'string'), # comma-separated string of file_names to make available as divs when running this source_code
  Field('main_code','text'),
  Field('suffix_code', 'text'), # hidden suffix code
  migrate='runestone_source_code.table'
)

db.define_table('acerror_log',
                Field('timestamp','datetime'),
                Field('sid','string'),
                Field('div_id','string'),
                Field('course_id','string'),
                Field('code','text'),
                Field('emessage','text'),
                migrate='runestone_acerror_log.table'
                )

##table to store highlights saved by the user
db.define_table('user_highlights',
  Field('created_on','datetime'),
  Field('user_id','integer'),
  Field('course_id','string'),
  Field('parent_class','string'), #class of the parent container
  Field('range','text'), #range JSON of the highlight
  Field('chapter_url','text'),
  Field('sub_chapter_url','text'),
  Field('method','string'), #self / Imported from friend
  Field('is_active','integer', default=1), #0 - deleted / inactive. 1 - active
  migrate='runestone_user_highlights.table'
)

##table to store the last position of the user. 1 row per user, per course
db.define_table('user_state',
  Field('user_id','integer'),
  Field('course_id','string'),
  Field('last_page_url','string'),
  Field('last_page_hash','string'),
  Field('last_page_chapter','string'),
  Field('last_page_subchapter','string'),
  Field('last_page_scroll_location','string'),
  Field('last_page_accessed_on','datetime'),
  migrate='runestone_user_state.table'
)

# Table to match instructor(s) to their course(s)
db.define_table('course_instructor',
    Field('course', db.courses ),
    Field('instructor', db.auth_user),
    migrate='runestone_course_instructor.table'
)

db.define_table('coach_hints',
    Field('category','string'),
    Field('symbol','string'),
    Field('msg_id','string'),
    Field('line','integer'),
    Field('col','integer'),
    Field('obj','string'),
    Field('msg','string'),
    Field('source',db.acerror_log),
    migrate='runestone_coach_hints.table'
    )

db.define_table('timed_exam',
    Field('timestamp','datetime'),
    Field('div_id','string'),
    Field('sid','string'),
    Field('course_name','string'),
    Field('correct','integer'),
    Field('incorrect','integer'),
    Field('skipped','integer'),
    Field('time_taken','integer'),
    Field('reset','boolean'),
    migrate='runestone_timed_exam.table'
    )

db.define_table('mchoice_answers',
    Field('timestamp','datetime'),
    Field('div_id','string'),
    Field('sid','string'),
    Field('course_name','string'),
    Field('answer','string', length=10),
    Field('correct','boolean'),
    migrate='runestone_mchoice_answers.table'
    )

db.define_table('fitb_answers',
    Field('timestamp','datetime'),
    Field('div_id','string'),
    Field('sid','string'),
    Field('course_name','string'),
    Field('answer','string'),
    Field('correct','boolean'),
    migrate='runestone_fitb_answers.table'
    )
db.define_table('dragndrop_answers',
    Field('timestamp','datetime'),
    Field('div_id','string'),
    Field('sid','string'),
    Field('course_name','string'),
    Field('answer','string'),
    Field('correct','boolean'),
    Field('minHeight','string'),
    migrate='runestone_dragndrop_answers.table'
    )
db.define_table('clickablearea_answers',
    Field('timestamp','datetime'),
    Field('div_id','string'),
    Field('sid','string'),
    Field('course_name','string'),
    Field('answer','string'),
    Field('correct','boolean'),
    migrate='runestone_clickablearea_answers.table'
    )
db.define_table('parsons_answers',
    Field('timestamp','datetime'),
    Field('div_id','string'),
    Field('sid','string'),
    Field('course_name','string'),
    Field('answer','string'),
    Field('source','string'),
    Field('correct','boolean'),
    migrate='runestone_parsons_answers.table'
    )
db.define_table('codelens_answers',
    Field('timestamp','datetime'),
    Field('div_id','string'),
    Field('sid','string'),
    Field('course_name','string'),
    Field('answer','string'),
    Field('source','string'),
    Field('correct','boolean'),
    migrate='runestone_codelens_answers.table'
    )

db.define_table('shortanswer_answers',
    Field('timestamp','datetime'),
    Field('div_id','string'),
    Field('sid','string'),
    Field('course_name','string'),
    Field('answer','string'),
    migrate='runestone_shortanswer_answers.table'
    )
