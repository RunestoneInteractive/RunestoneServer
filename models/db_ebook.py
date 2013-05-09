# Files in the model directory are loaded in alphabetical order.  This one needs to be loaded after db.py

db.define_table('useinfo',
  Field('timestamp','datetime'),
  Field('sid','string'),
  Field('event','string'),
  Field('act','string'),
  Field('div_id','string'),
  Field('course_id','string'),
  migrate=settings.migrate
)

db.define_table('code',
  Field('acid','string'),
  Field('code','text'),
  Field('course_id','string'),
  Field('grade','double'),
  Field('sid','string'),
  Field('timestamp','datetime'),
  migrate=settings.migrate
)

db.define_table('acerror_log',
                Field('timestamp','datetime'),
                Field('sid','string'),
                Field('div_id','string'),                                
                Field('course_id','string'),                
                Field('code','text'),
                Field('emessage','text'),
                migrate=settings.migrate
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
  migrate=settings.migrate
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
  migrate=settings.migrate
)