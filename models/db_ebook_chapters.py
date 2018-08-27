import datetime

# table of all book chapters
db.define_table('chapters',
  Field('chapter_name','string'), # can have spaces in it, for human consumption
  Field('course_id','string'), # references courses(course_name)
  Field('chapter_label','string'), #no spaces, actual filename path
  migrate='runestone_chapters.table'
)

# table of sub chapters
db.define_table('sub_chapters',
  Field('sub_chapter_name','string'), # can have spaces in it, for human consumption
  Field('chapter_id','reference chapters'),
  Field('sub_chapter_length','integer'),
  Field('sub_chapter_label','string'), # no spaces, actual filename path
  Field('skipreading', 'boolean'), # If true do not include this subchapter in the readings picker
  migrate='runestone_sub_chapters.table'
)

db.define_table('user_chapter_progress',
  Field('user_id'),
  Field('chapter_id','string'),
  Field('start_date','datetime', default=datetime.datetime.utcnow()),
  Field('end_date','datetime'),
  Field('status','integer'), #-1  - not started. 0 - active. 1 - completed
  migrate='runestone_user_chapter_progress.table'
)

db.define_table('user_sub_chapter_progress',
  Field('user_id', 'reference auth_user'),
  Field('chapter_id','string'),
  Field('sub_chapter_id','string'),
  Field('start_date','datetime', default=datetime.datetime.utcnow()),
  Field('end_date','datetime'),
  Field('status','integer'), #-1  - not started. 0 - active. 1 - completed
  migrate='runestone_user_sub_chapter_progress.table'
)

db.define_table('sub_chapter_taught',
  Field('course_name', 'string'),
  Field('chapter_label', 'string'),
  Field('sub_chapter_label', 'string'),
  Field('teaching_date', 'date', default=datetime.datetime.utcnow()),
  migrate='runestone_sub_chapter_taught.table'
)

#
# When a new user is registered we need to add a bunch of rows to the
# user_sub_chapter_progress table.  One for each section/subsection
# This is like a trigger, but will work across all databases.
#
def make_progress_entries(field_dict,id_of_insert):
    cname = db(db.courses.id == field_dict['course_id']).select(db.courses.course_name).first()['course_name']
    db.executesql('''
       INSERT INTO user_chapter_progress(user_id, chapter_id, status)
           SELECT %s, chapters.chapter_label, -1
           FROM chapters where chapters.course_id = '%s';
    ''' % (id_of_insert,cname))
    db.executesql('''
       INSERT INTO user_sub_chapter_progress(user_id, chapter_id,sub_chapter_id, status)
           SELECT %s, chapters.chapter_label, sub_chapters.sub_chapter_label, -1
           FROM chapters, sub_chapters where sub_chapters.chapter_id = chapters.id and chapters.course_id = '%s';
    ''' % (id_of_insert,cname))

if 'auth_user' in db:
    db.auth_user._after_insert.append(make_progress_entries)
