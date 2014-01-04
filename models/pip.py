db.define_table('pipactex_deadline',
  Field('acid_prefix', 'string'),  # acid = actice code id
  Field('deadline', 'datetime'),
  Field('wed11deadline', 'datetime'),
  Field('wed4deadline', 'datetime'),
  Field('th3deadline', 'datetime'),
  migrate='runestone_pipactex_deadline.table')
