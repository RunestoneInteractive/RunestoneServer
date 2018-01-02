import click
import sys
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
else:
    click.echo(message="Your database already has Courses")


# create the instructor group if it doesn't already exist
if not db(db.auth_group.role == 'instructor').select().first():
    db.auth_group.insert(role='instructor')

## DEPRECATED
if db(db.cohort_master.id > 0).isempty():
    db.cohort_master.insert(cohort_name='Default Group', is_active = 1)


res = db.executesql("""
SELECT table_name
FROM information_schema.tables
WHERE table_schema='public' AND table_type='BASE TABLE'""")

if "--list_tables" in sys.argv:
    click.echo("The following tables are defined")
    for row in res:
        click.echo(row[0])
