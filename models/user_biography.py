db.define_table('user_biography',
  Field('user_id', 'reference auth_user'),
  Field('prefered_name', 'text'),
  # Field('pronounced_name', 'string'),
  Field('interesting_fact', 'text'),
  Field('programming_experience', 'text'),
  Field('laptop_type', requires=IS_IN_SET(['Windows', 'Mac', 'Chromebook', 'Unix/Linux', 'Other'])),
  Field('image', 'upload'),
  migrate='runestone_user_biography.table')
