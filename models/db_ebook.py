# **********************************
# |docname| - Runestone eBook Tables
# **********************************
# This module contains the database table definitions
#
# Files in the model directory are loaded in alphabetical order.  This one needs to be loaded after db.py
#
# web2py does not allow you to specify indices programmatically.  The indexes for each table **should** be
# documented here, but may not be.  The command ``rsmanage init`` contains index creation statements for
# all performance critical tables.

# useinfo
# -------
# The largest and busiest table in the whole database!
# This tracks click stream information on every student
# Having indices on this table is critical, here is what we have:
# ``create index "course_id_index" on useinfo using btree (course_id);``
# ``create index "div_id_index" on useinfo using btree (div_id);``
# ``create index "event_index" on useinfo using btree (event);``
# ``create index "sid_index" on useinfo using btree (sid);``
# ``create index "timestamp_idx" on useinfo using btree ("timestamp");``
db.define_table(
    "useinfo",
    Field("timestamp", "datetime"),
    Field("sid", "string"),
    Field("event", "string"),
    Field("act", "string"),
    Field("div_id", "string"),
    Field("course_id", "string"),
    migrate=table_migrate_prefix + "useinfo.table",
)

# stores student's saved code and, unfortunately, comments and grades, which really should be their own table linked to this
# code
# ----
db.define_table(
    "code",
    Field("acid", "string"),
    Field("code", "text"),
    Field("emessage", "text"),
    Field("course_id", "integer"),
    Field("grade", "double"),
    Field("sid", "string"),
    Field("timestamp", "datetime"),
    Field("comment", "text"),
    Field("language", "text", default="python"),
    migrate=table_migrate_prefix + "code.table",
)

# Stores the source code for activecodes, including prefix and suffix code, so that prefixes and suffixes can be run when grading
# Contents of this table are filled when processing activecode directives, in activecod.py
# source_code
# -----------
db.define_table(
    "source_code",
    Field("acid", "string", required=True),
    Field("course_id", "string"),
    Field(
        "includes", "string"
    ),  # comma-separated string of acid main_codes to include when running this source_code
    Field(
        "available_files", "string"
    ),  # comma-separated string of file_names to make available as divs when running this source_code
    Field("main_code", "text"),
    Field("suffix_code", "text"),  # hidden suffix code
    migrate=table_migrate_prefix + "source_code.table",
)

# acerror_log
# ----------
# TODO: remove this definition after safely backing up and removing the table from academy
db.define_table(
    "acerror_log",
    Field("timestamp", "datetime"),
    Field("sid", "string"),
    Field("div_id", "string"),
    Field("course_id", "string"),
    Field("code", "text"),
    Field("emessage", "text"),
    migrate=table_migrate_prefix + "acerror_log.table",
)

##table to store the last position of the user. 1 row per user, per course
# user_state
# ----------
db.define_table(
    "user_state",
    Field("user_id", "integer"),
    Field("course_name", "string"),
    Field("last_page_url", "string"),
    Field("last_page_hash", "string"),
    Field("last_page_chapter", "string"),
    Field("last_page_subchapter", "string"),
    Field("last_page_scroll_location", "string"),
    Field("last_page_accessed_on", "datetime"),
    migrate=table_migrate_prefix + "user_state.table",
)

# Table to match instructor(s) to their course(s)
# course_instructor
# -----------------
db.define_table(
    "course_instructor",
    Field("course", db.courses),
    Field("instructor", db.auth_user),
    Field(
        "verified", "boolean"
    ),  # some features we want to take the extra step of verifying an instructor - such as instructor guide
    Field("paid", "boolean"),  # in the future some instructor features will be paid
    migrate=table_migrate_prefix + "course_instructor.table",
)

# timed_exam
# ----------
db.define_table(
    "timed_exam",
    Field("timestamp", "datetime"),
    Field("div_id", "string"),
    Field("sid", "string"),
    Field("course_name", "string"),
    Field("correct", "integer"),
    Field("incorrect", "integer"),
    Field("skipped", "integer"),
    Field("time_taken", "integer"),
    Field("reset", "boolean"),
    migrate=table_migrate_prefix + "timed_exam.table",
)

# mchoice_answers
# ---------------
# define the following indices
#    CREATE INDEX mchoice_answers_course_name_idx ON mchoice_answers USING btree (course_name);
#    CREATE INDEX mchoice_answers_div_id_idx ON mchoice_answers USING btree (div_id);
#    CREATE INDEX mchoice_answers_sid_idx ON mchoice_answers USING btree (sid);

db.define_table(
    "mchoice_answers",
    Field("timestamp", "datetime"),
    Field("div_id", "string"),
    Field("sid", "string"),
    Field("course_name", "string"),
    Field("answer", "string", length=50),
    Field("correct", "boolean"),
    Field("percent", "double"),
    migrate=table_migrate_prefix + "mchoice_answers.table",
)

# fitb_answers
# ------------
db.define_table(
    "fitb_answers",
    Field("timestamp", "datetime"),
    Field("div_id", "string"),
    Field("sid", "string"),
    Field("course_name", "string"),
    Field("answer", "string"),
    Field("correct", "boolean"),
    Field("percent", "double"),
    migrate=table_migrate_prefix + "fitb_answers.table",
)
# dragndrop_answers
# -----------------
db.define_table(
    "dragndrop_answers",
    Field("timestamp", "datetime"),
    Field("div_id", "string"),
    Field("sid", "string"),
    Field("course_name", "string"),
    Field("answer", "string"),
    Field("correct", "boolean"),
    Field("min_height", "string"),
    Field("percent", "double"),
    migrate=table_migrate_prefix + "dragndrop_answers.table",
)
# clickablearea_answers
# ---------------------
db.define_table(
    "clickablearea_answers",
    Field("timestamp", "datetime"),
    Field("div_id", "string"),
    Field("sid", "string"),
    Field("course_name", "string"),
    Field("answer", "string"),
    Field("correct", "boolean"),
    Field("percent", "double"),
    migrate=table_migrate_prefix + "clickablearea_answers.table",
)

# parsons_answers
# ---------------
db.define_table(
    "parsons_answers",
    Field("timestamp", "datetime"),
    Field("div_id", "string"),
    Field("sid", "string"),
    Field("course_name", "string"),
    Field("answer", "string"),
    Field("source", "string"),
    Field("correct", "boolean"),
    Field("percent", "double"),
    migrate=table_migrate_prefix + "parsons_answers.table",
)

# codelens_answers
# ----------------
db.define_table(
    "codelens_answers",
    Field("timestamp", "datetime"),
    Field("div_id", "string"),
    Field("sid", "string"),
    Field("course_name", "string"),
    Field("answer", "string"),
    Field("source", "string"),
    Field("correct", "boolean"),
    Field("percent", "double"),
    migrate=table_migrate_prefix + "codelens_answers.table",
)

# shortanswer_answers
# -------------------
db.define_table(
    "shortanswer_answers",
    Field("timestamp", "datetime"),
    Field("div_id", "string"),
    Field("sid", "string"),
    Field("course_name", "string"),
    Field("answer", "text"),
    migrate=table_migrate_prefix + "shortanswer_answers.table",
)

# unittest_answers
# ----------------
# define the following indices
#    CREATE INDEX unittest_answers_course_name_idx ON unittest_answers USING btree (course_name);
#    CREATE INDEX unittest_answers_div_id_idx ON unittest_answers USING btree (div_id);
#    CREATE INDEX unittest_answers_sid_idx ON unittest_answers USING btree (sid);
db.define_table(
    "unittest_answers",
    Field("timestamp", "datetime"),
    Field("div_id", "string"),
    Field("sid", "string"),
    Field("course_name", "string"),
    Field("answer", "string"),
    Field("passed", "integer"),
    Field("failed", "integer"),
    Field("correct", "boolean"),
    Field("percent", "double"),
    migrate=table_migrate_prefix + "unittest_answers.table",
)

# payments
# --------
db.define_table(
    "payments",
    Field("user_courses_id", db.user_courses, required=True),
    # A `Stripe charge ID <https://stripe.com/docs/api/charges/object#charge_object-id>`_. Per the `Stripe docs <https://stripe.com/docs/upgrades>`_, this is always 255 characters or less.
    Field("charge_id", "string", length=255, required=True),
    migrate=table_migrate_prefix + "payments.table",
)

# lp_answers
# ----------
db.define_table(
    "lp_answers",
    Field("timestamp", "datetime"),
    Field("div_id", "string"),
    Field("sid", "string"),
    Field("course_name", "string"),
    Field("answer", "text"),
    Field("correct", "double"),
    migrate=table_migrate_prefix + "lp_answers.table",
)

# invoice_request
# ---------------
db.define_table(
    "invoice_request",
    Field("timestamp", "datetime"),
    Field("sid", "string"),
    Field("course_name", "string"),
    Field("email", "string"),
    Field("processed", "boolean"),
    migrate=table_migrate_prefix + "invoice_request.table",
)

# editor_basecourse
# -----------------
# This table tracks the userid of a person who has editing authority over a
# particular book.
db.define_table(
    "editor_basecourse",
    Field("editor", db.auth_user),
    Field("base_course", "string"),
    migrate=table_migrate_prefix + "editor_basecourse.table",
)

# course_attributes
# -----------------
#
# The course attribute table allows us to add parameters to each course without having
# to add columns to the courses table every time we have something new to store.
# for example we could have a "source" key value pair to indicate if a course is built
# with runestone or pretext, or to store the latex macros for a pretext course
# TODO: migrate allow_pairs, download_enabled, and others from courses to this table.
db.define_table(
    "course_attributes",
    Field("course_id", db.courses),
    Field("attr", "string"),
    Field("value", "text"),
    migrate=table_migrate_prefix + "course_attributes.table",
)

# selected_questions
# ------------------
# We define a table to keep track of the questions that were randomly selected for
# each student in a generated exam.
# The following index is important for fast performance to lookup the question selected for
# a strudent, but will also keep us from having duplicate entries and causing confusion!
# ``CREATE UNIQUE INDEX selector_sid_unique ON selected_questions USING btree (selector_id, sid)``
db.define_table(
    "selected_questions",
    Field("selector_id", "string"),
    Field("sid", "string"),
    Field("selected_id", "string"),
    Field("points", "integer"),
    Field("competency", "string"),
    migrate=table_migrate_prefix + "selected_questions.table",
)

db.define_table(
    "user_experiment",
    Field("experiment_id", "string"),
    Field("sid", "string"),
    Field("exp_group", "integer"),
    migrate=table_migrate_prefix + "experiment_user.table",
)


def getCourseAttribute(course_id: int, attr_name: str):
    res = (
        db(
            (db.course_attributes.course_id == course_id)
            & (db.course_attributes.attr == attr_name)
        )
        .select(db.course_attributes.value, **SELECT_CACHE)
        .first()
    )
    if res:
        return res.value
    else:
        return None


# this check has to be here to ensure that the course_attributes table is defined.

# if auth.user:
#     if getCourseAttribute(auth.user.course_id, "lti_interface"):
#         settings.lti_interface = True
