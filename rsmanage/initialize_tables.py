import click
import sys
from os import environ

# this script is meant to be run from the initdb subcommand of rsmange, which
# simply spawns python web2py.py -S runestone -M applications/runestone/initialize_tables.py
#


if db(db.courses.id > 0).isempty():
    click.echo(message="Definining initial Courses", file=None, nl=True, err=False, color='green')
    db.courses.insert(course_name='boguscourse', term_start_date=datetime.date(2000, 1, 1)) # should be id 1
    db.courses.insert(course_name='thinkcspy', base_course = 'thinkcspy', term_start_date=datetime.date(2000, 1, 1))
    db.courses.insert(course_name='pythonds', base_course = 'pythonds', term_start_date=datetime.date(2000, 1, 1))
    db.courses.insert(course_name='overview', term_start_date=datetime.date(2000, 1, 1))
    db.courses.insert(course_name='pip2', base_course='pip2', term_start_date=datetime.date(2000, 1, 1))
    db.courses.insert(course_name='apcsareview', base_course='apcsareview', term_start_date=datetime.date(2000, 1, 1))
    db.courses.insert(course_name='StudentCSP', base_course='StudentCSP', term_start_date=datetime.date(2000, 1, 1))
    db.courses.insert(course_name='TeacherCSP', base_course='TeacherCSP', term_start_date=datetime.date(2000, 1, 1))
    db.courses.insert(course_name='JavaReview', base_course='apcsareview', term_start_date=datetime.date(2000, 1, 1))
    db.courses.insert(course_name='publicpy3', base_course='pip2', term_start_date=datetime.date(2000, 1, 1))
    db.courses.insert(course_name='fopp', base_course='fopp', term_start_date=datetime.date(2000, 1, 1))    
    db.courses.insert(course_name='cppds', base_course='cppds', term_start_date=datetime.date(2000, 1, 1))        
    db.courses.insert(course_name='webfundamentals', base_course='webfundamentals', term_start_date=datetime.date(2000, 1, 1))            
else:
    click.echo(message="Your database already has Courses")


# create the instructor group if it doesn't already exist
if not db(db.auth_group.role == 'instructor').select().first():
    db.auth_group.insert(role='instructor')

## DEPRECATED
if db(db.cohort_master.id > 0).isempty():
    db.cohort_master.insert(cohort_name='Default Group', is_active = 1)

# In SQL we can manually add the constraint
# alter table questions add constraint name_bc_unique UNIQUE(name, base_course);

if environ.get('WEB2PY_MIGRATE', "") != 'fake':
    click.echo(message="Adding Constraints and Indices", file=None, nl=True, err=False, color='red')
    try:
        db.executesql('''alter table questions add constraint name_bc_unique UNIQUE(name, base_course)''')
        db.executesql('''alter table grades ADD CONSTRAINT user_assign_unique UNIQUE (auth_user, assignment);''')
        db.executesql('''create index "course_id_index" on useinfo using btree (course_id);''')
        db.executesql('''create index "div_id_index" on useinfo using btree (div_id);''')
        db.executesql('''create index "event_index" on useinfo using btree (event);''')
        db.executesql('''create index "sid_index" on useinfo using btree (sid);''')
        db.executesql('''create index "timestamp_idx" on useinfo using btree ("timestamp");''')
        db.executesql('''CREATE INDEX chapters_course_id_idx ON chapters USING btree (course_id);''')
        db.executesql('''CREATE INDEX mchoice_answers_course_name_idx ON mchoice_answers USING btree (course_name);''')
        db.executesql('''CREATE INDEX mchoice_answers_div_id_idx ON mchoice_answers USING btree (div_id);''')
        db.executesql('''CREATE INDEX mchoice_answers_sid_idx ON mchoice_answers USING btree (sid);''')
        db.executesql('''CREATE INDEX questions_chapter_idx ON questions USING btree (chapter);''')
        db.executesql('''CREATE INDEX questions_name_idx ON questions USING btree (name);''')
        db.executesql('''CREATE INDEX sub_chapters_chapter_id_idx ON sub_chapters USING btree (chapter_id);''')
        db.executesql('''CREATE INDEX user_sub_chapter_progress_chapter_id_idx ON user_sub_chapter_progress USING btree (chapter_id);''')
    except:
        click.echo(message="The creation of one or more indices/constraints failed", file=None, nl=True, err=False, color='red')

if "--list_tables" in sys.argv:
    res = db.executesql("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema='public' AND table_type='BASE TABLE'""")

    click.echo("The following tables are defined")
    for row in res:
        click.echo(row[0])
