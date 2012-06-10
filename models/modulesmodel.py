
db.define_table('modules',
   Field('shortname','string'),
   Field('description','text'),
   Field('pathtofile','string'),
   migrate = settings.migprefix+'modules.table' )
   
db.define_table('projects',
   Field('projectcode','string'),
   Field('description','string'),
   migrate = settings.migprefix+'projects.table'  )
   