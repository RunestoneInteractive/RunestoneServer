db.define_table('sections',
  Field('name',
    type='string',
    label=T('Name')
    ),
  Field('course_id',
    db.courses,
    label=('Course ID'),
    required=True
    ),
  migrate='runestone_sections.table'
  )
class ExtendedSection(object):
  def get_users(self):
    def users(self=self):
      return []
    return users
  def add_user(self):
    def user(self=self):
      return True
    return user
  def clear_users(self):
    def clear(self=self):
      for user in db(db.auth_user.section_id == self.sections.id).select():
        user.update_record(section_id='')
    return clear
db.sections.virtualfields.append(ExtendedSection())

db.define_table('sections_to_users',
  Field('auth_user',db.auth_user, required=True),
  Field('section',db.sections, label="Section ID", required=True),
  migrate= 'runestone_sections_to_users.table',
  )