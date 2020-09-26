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
    )
    # should be id 1
    BASE_COURSES = [
        "ac1",
        "cppds",
        "cppforpython",
        "csawesome",
        "csjava",
        "fopp",
        "httlads",
        "java4python",
        "JS4Python",
        "learnwebgl2",
        "MasteringDatabases",
        "overview",
        "py4e-int",
        "pythonds",
        "pythonds3",
        "StudentCSP",
        "TeacherCSP",
        "thinkcpp",
        "thinkcspy",
        "webfundamentals",
    ]

    for c in BASE_COURSES:
        db.courses.insert(
            course_name=c, base_course=c, term_start_date=datetime.date(2000, 1, 1),
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
        """alter table grades ADD CONSTRAINT user_assign_unique UNIQUE (auth_user, assignment);""",
        """alter table assignments add constraint unique_assign_names unique (name, course)""",
        """alter table course_attributes add constraint course_attr_unique UNIQUE(course_id, attr);""",
        ## Indexes; alphabetically by index
        """CREATE INDEX "course_id_index" on useinfo using btree (course_id);""",
        """CREATE INDEX "course_name_index" on user_topic_practice_log using btree (course_name);""",
        """CREATE INDEX "div_id_index" on useinfo using btree (div_id);""",
        """CREATE INDEX "event_index" on useinfo using btree (event);""",
        """CREATE INDEX "q_index" on user_topic_practice_log using btree (q);""",
        """CREATE INDEX "sid_index" on useinfo using btree (sid);""",
        """CREATE INDEX "timestamp_idx" on useinfo using btree ("timestamp");""",
        """CREATE INDEX "user_id_index" on user_topic_practice_log using btree (user_id);""",
        """CREATE INDEX assign_course_idx ON assignments USING btree (course)""",  # New
        """CREATE INDEX c_i_idx ON course_instructor USING btree (course, instructor)""",  # New
        """CREATE INDEX chap_label_idx on sub_chapters using btree(sub_chapter_label);""",
        """CREATE INDEX chap_subchap_idx ON questions USING btree (chapter, subchapter)""",  # New
        """CREATE INDEX chapters_course_id_idx ON chapters USING btree (course_id);""",
        """CREATE INDEX code_acid_idx on code using btree(acid)""",
        """CREATE INDEX code_course_id_idx on code using btree(course_id)""",
        """CREATE INDEX code_sid_idx on code using btree(sid)""",
        """CREATE INDEX code_timestamp_idx on code using btree(timestamp)""",
        """CREATE INDEX course_attr_idx ON course_attributes USING btree(course_id, attr);""",
        """CREATE INDEX mchoice_answers_course_name_idx ON mchoice_answers USING btree (course_name);""",
        """CREATE INDEX mchoice_answers_div_id_idx ON mchoice_answers USING btree (div_id);""",
        """CREATE INDEX mchoice_answers_sid_idx ON mchoice_answers USING btree (sid);""",
        """CREATE INDEX mult_scd_idx on mchoice_answers (div_id, course_name, sid)""",
        """CREATE INDEX parsons_answers_course_name_idx ON parsons_answers USING btree (course_name)""",  # New
        """CREATE INDEX parsons_answers_div_id_idx ON parsons_answers USING btree (div_id)""",  # New
        """CREATE INDEX parsons_answers_sid_idx ON parsons_answers USING btree (sid)""",  # New
        """CREATE INDEX parsons_scd_idx ON parsons_answers USING btree (div_id, course_name, sid)""",  # New
        """CREATE INDEX q_bc_idx ON questions USING btree (base_course) """,  # New
        """CREATE INDEX question_grades_key on question_grades (div_id, course_name, sid)""",
        """CREATE INDEX questions_chapter_idx ON questions USING btree (chapter);""",
        """CREATE INDEX questions_name_idx ON questions USING btree (name);""",
        """CREATE INDEX sid_divid_idx ON useinfo USING btree(sid, div_id)""",
        """CREATE INDEX source_code_acid_idx ON source_code USING btree (acid)""",  # New
        """CREATE INDEX source_code_course_id_idx ON source_code USING btree (course_id)""",  # New
        """CREATE INDEX sub_chapters_chapter_id_idx ON sub_chapters USING btree (chapter_id);""",
        """CREATE INDEX subchap_idx ON questions USING btree (subchapter)""",  # New
        """CREATE INDEX unittest_answers_course_name_idx ON unittest_answers USING btree (course_name);""",
        """CREATE INDEX unittest_answers_div_id_idx ON unittest_answers USING btree (div_id);""",
        """CREATE INDEX unittest_answers_sid_idx ON unittest_answers USING btree (sid);""",
        """CREATE INDEX us_cid_idx ON public.user_state USING btree (course_id)""",  # New
        """CREATE INDEX us_sid_idx ON public.user_state USING btree (user_id)""",  # New
        """CREATE INDEX user_sub_chapter_progress_chapter_id_idx ON user_sub_chapter_progress USING btree (chapter_id);""",
        """CREATE INDEX user_sub_chapter_progress_user_id_idx ON user_sub_chapter_progress USING btree (user_id)""",  # New
        """CREATE INDEX user_sub_chapter_progress_course_name_idx ON user_sub_chapter_progress USING btree (course_name)""",
        """CREATE UNIQUE INDEX courses_course_name_idx ON courses USING btree (course_name)""",  # New
        """CREATE UNIQUE INDEX q_comp_unique ON competency USING btree (question, competency)""",
        """CREATE UNIQUE INDEX selector_sid_unique ON selected_questions USING btree (selector_id, sid)""",
        """CREATE UNIQUE INDEX tags_tag_name_idx ON tags USING btree (tag_name)""",  # New
        """CREATE UNIQUE INDEX unique_user ON auth_user USING btree (username)""",  # New
        """CREATE UNIQUE INDEX user_assign_unique_idx ON grades USING btree (auth_user, assignment)""",  # New
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
