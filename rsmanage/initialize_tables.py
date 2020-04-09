import click
import sys
from os import environ
import datetime

# this script is meant to be run from the initdb subcommand of rsmange, which
# simply spawns python web2py.py -S runestone -M applications/runestone/initialize_tables.py
#


if db(db.courses.id > 0).isempty():
    click.echo(
        message="Definining initial Courses",
        file=None,
        nl=True,
        err=False,
        color="green",
    )
    db.courses.insert(
        course_name="boguscourse", term_start_date=datetime.date(2000, 1, 1)
    )  # should be id 1
    db.courses.insert(
        course_name="thinkcspy",
        base_course="thinkcspy",
        term_start_date=datetime.date(2000, 1, 1),
    )
    db.courses.insert(
        course_name="pythonds",
        base_course="pythonds",
        term_start_date=datetime.date(2000, 1, 1),
    )
    db.courses.insert(
        course_name="overview",
        base_course="overview",
        term_start_date=datetime.date(2000, 1, 1),
    )
    db.courses.insert(
        course_name="pip2",
        base_course="pip2",
        term_start_date=datetime.date(2000, 1, 1),
    )
    db.courses.insert(
        course_name="apcsareview",
        base_course="apcsareview",
        term_start_date=datetime.date(2000, 1, 1),
    )
    db.courses.insert(
        course_name="StudentCSP",
        base_course="StudentCSP",
        term_start_date=datetime.date(2000, 1, 1),
    )
    db.courses.insert(
        course_name="TeacherCSP",
        base_course="TeacherCSP",
        term_start_date=datetime.date(2000, 1, 1),
    )
    db.courses.insert(
        course_name="JavaReview",
        base_course="apcsareview",
        term_start_date=datetime.date(2000, 1, 1),
    )
    db.courses.insert(
        course_name="publicpy3",
        base_course="pip2",
        term_start_date=datetime.date(2000, 1, 1),
    )
    db.courses.insert(
        course_name="fopp",
        base_course="fopp",
        term_start_date=datetime.date(2000, 1, 1),
    )
    db.courses.insert(
        course_name="cppds",
        base_course="cppds",
        term_start_date=datetime.date(2000, 1, 1),
    )
    db.courses.insert(
        course_name="webfundamentals",
        base_course="webfundamentals",
        term_start_date=datetime.date(2000, 1, 1),
    )
else:
    click.echo(message="Your database already has Courses")


# create the instructor and editor groups if needed
if not db(db.auth_group.role == "instructor").select().first():
    db.auth_group.insert(role="instructor")

if not db(db.auth_group.role == "editor").select().first():
    db.auth_group.insert(role="editor")


def try_running(sql_command):
    try:
        db.executesql(sql_command)
        click.echo(f"success: {sql_command}")
        db.commit()
    except Exception as e:
        click.echo(f"FAILED: {sql_command}", color="red")
        click.echo("Details: {}".format(e))
        db.rollback()


if environ.get("WEB2PY_MIGRATE", "") != "fake":
    click.echo(
        message="Adding Constraints and Indices",
        file=None,
        nl=True,
        err=False,
        color="red",
    )

    sql_commands = [
        ## constraints
        """alter table questions add constraint name_bc_unique UNIQUE(name, base_course)""",
        """alter table auth_user add constraint unique_user UNIQUE(username)""",
        """alter table auth_user add constraint unique_user UNIQUE(username)""",
        """alter table grades ADD CONSTRAINT user_assign_unique UNIQUE (auth_user, assignment);""",
        """alter table assignments add constraint unique_assign_names unique (name, course)""",
        ## Indexes; alphabetically by table name
        """CREATE INDEX assign_course_idx ON assignments USING btree (course)""",  # New
        """CREATE UNIQUE INDEX unique_user ON auth_user USING btree (username)""",  # New
        """CREATE INDEX chapters_course_id_idx ON chapters USING btree (course_id);""",
        """create index code_sid_idx on code using btree(sid)""",
        """create index code_acid_idx on code using btree(acid)""",
        """create index code_course_id_idx on code using btree(course_id)""",
        """create index code_timestamp_idx on code using btree(timestamp)""",
        """CREATE INDEX c_i_idx ON course_instructor USING btree (course, instructor)""",  # New
        """CREATE UNIQUE INDEX courses_course_name_key ON courses USING btree (course_name)""",  # New
        """CREATE UNIQUE INDEX user_assign_unique ON grades USING btree (auth_user, assignment)""",  # New
        """CREATE INDEX mchoice_answers_course_name_idx ON mchoice_answers USING btree (course_name);""",
        """CREATE INDEX mchoice_answers_div_id_idx ON mchoice_answers USING btree (div_id);""",
        """CREATE INDEX mchoice_answers_sid_idx ON mchoice_answers USING btree (sid);""",
        """create index mult_scd_idx on mchoice_answers (div_id, course_name, sid)""",
        """CREATE INDEX parsons_answers_course_name_idx ON parsons_answers USING btree (course_name)""",  # New
        """CREATE INDEX parsons_answers_div_id_idx ON parsons_answers USING btree (div_id)""",  # New
        """CREATE INDEX parsons_answers_sid_idx ON parsons_answers USING btree (sid)""",  # New
        """CREATE INDEX parsons_scd_idx ON parsons_answers USING btree (div_id, course_name, sid)""",  # New
        """create index question_grades_key on question_grades (div_id, course_name, sid)""",
        """CREATE INDEX chap_subchap_idx ON questions USING btree (chapter, subchapter)""",  # New
        """CREATE UNIQUE INDEX name_bc_unique ON questions USING btree (name, base_course)""",  # New
        """CREATE INDEX q_bc_idx ON questions USING btree (base_course) """,  # New
        """CREATE INDEX questions_chapter_idx ON questions USING btree (chapter);""",
        """CREATE INDEX questions_name_idx ON questions USING btree (name);""",
        """CREATE INDEX subchap_idx ON questions USING btree (subchapter)""",  # New
        """CREATE UNIQUE INDEX scheduler_task_uuid_key ON scheduler_task USING btree (uuid)""",  # New
        """CREATE UNIQUE INDEX scheduler_worker_worker_name_key ON scheduler_worker USING btree (worker_name)""",  # New
        """CREATE INDEX source_code_acid_idx ON source_code USING btree (acid)""",  # New
        """CREATE INDEX source_code_course_id_idx ON source_code USING btree (course_id)""",  # New
        """CREATE INDEX sub_chapters_chapter_id_idx ON sub_chapters USING btree (chapter_id);""",
        """CREATE UNIQUE INDEX tags_tag_name_key ON tags USING btree (tag_name)""",  # New
        """create index "course_id_index" on useinfo using btree (course_id);""",
        """create index "div_id_index" on useinfo using btree (div_id);""",
        """create index "event_index" on useinfo using btree (event);""",
        """create index "sid_index" on useinfo using btree (sid);""",
        """create index "timestamp_idx" on useinfo using btree ("timestamp");""",
        """CREATE INDEX us_cid_idx ON public.user_state USING btree (course_id)""",  # New
        """CREATE INDEX us_sid_idx ON public.user_state USING btree (user_id)""",  # New
        """CREATE INDEX user_sub_chapter_progress_chapter_id_idx ON user_sub_chapter_progress USING btree (chapter_id);""",
        """CREATE INDEX user_sub_chapter_progress_user_id_idx ON user_sub_chapter_progress USING btree (user_id)""",  # New
    ]

    for cmd in sql_commands:
        try_running(cmd)

if "--list_tables" in sys.argv:
    res = db.executesql(
        """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema='public' AND table_type='BASE TABLE'"""
    )

    click.echo("The following tables are defined")
    for row in res:
        click.echo(row[0])
