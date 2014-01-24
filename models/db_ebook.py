import datetime; now=datetime.datetime.today()

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

db.define_table('code',
  Field('acid','string'),
  Field('code','text'),
  Field('course_id','string'),
  Field('grade','double'),
  Field('sid','string'),
  Field('timestamp','datetime'),
  migrate='runestone_code.table'
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

# table of all book chapters
db.define_table('chapters',
  Field('chapter_name','string'),
  Field('course_id','reference courses'),
  Field('chapter_label','string'), #Approximate number of days, aggregated based on sub chapters
  migrate=settings.migrate
)

# table of sub chapters
db.define_table('sub_chapters',
  Field('sub_chapter_name','string'),
  Field('chapter_id','reference chapters'),
  Field('sub_chapter_length','integer'),
  Field('sub_chapter_label','string'), #Average Time it takes people to complete this subchapter, maybe calculated using a weekly batchjob
  migrate=settings.migrate
)

db.define_table('user_sub_chapter_progress',
  Field('user_id','reference auth_user'),
  Field('chapter_id','string'),
  Field('sub_chapter_id','string'),
  Field('start_date','datetime', default=request.now),
  Field('end_date','datetime'),
  Field('status','integer'), #-1  - not started. 0 - active. 1 - completed
  migrate=settings.migrate
)

db.executesql('CREATE TRIGGER  IF NOT EXISTS create_subchapter_entries AFTER INSERT ON auth_user BEGIN INSERT INTO user_sub_chapter_progress(user_id, chapter_id,sub_chapter_id, status) SELECT new.id, chapters.chapter_label, sub_chapters.sub_chapter_label, -1 FROM chapters, sub_chapters where sub_chapters.chapter_id = chapters.id; END;')
