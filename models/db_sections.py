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
    def users():
      return section_users(db.sections.id == self.sections.id).select(db.auth_user.ALL)
    return users
  def add_user(self):
    def user_func(user):
      db.section_users.insert(section=self.sections.id,auth_user=user)
      return True
    return user_func
  def clear_users(self):
    def clear():
      db(db.section_users.section == self.sections.id).delete()
      return True
    return clear
db.sections.virtualfields.append(ExtendedSection())

db.define_table('section_users',
  Field('auth_user',db.auth_user, required=True),
  Field('section',db.sections, label="Section ID", required=True),
  migrate= 'runestone_section_users.table',
  )

section_users = db((db.sections.id==db.section_users.section) & (db.auth_user.id==db.section_users.auth_user))
