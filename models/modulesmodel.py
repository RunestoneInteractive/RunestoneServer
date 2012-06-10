
db.define_table('modules',
   Field('shortname','string'),
   Field('description','text'),
   Field('pathtofile','string'),
   migrate = settings.migrate 
)
   
db.define_table('projects',
   Field('projectcode','string'),
   Field('description','string'),
   migrate = settings.migrate
)
   