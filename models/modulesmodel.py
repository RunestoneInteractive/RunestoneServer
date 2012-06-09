
db.define_table('modules',
   Field('shortname','string'),
   Field('description','text'),
   Field('pathtofile','string'),
   migrate = 'runestone_modules.table' )
   
db.define_table('projects',
   Field('projectcode','string'),
   Field('description','string'),
   migrate = 'runestone_projects.table'  )
   