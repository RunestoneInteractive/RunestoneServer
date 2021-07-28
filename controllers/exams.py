# *********************************************
# |docname| - Endpoints relating to assignments
# *********************************************
#
# Imports
# =======
# These are listed in the order prescribed by `PEP 8
# <http://www.python.org/dev/peps/pep-0008/#imports>`_.
#
# Standard library
# ----------------
import json
import logging
import datetime
from collections import OrderedDict
import traceback
import logging

# Third-party imports
# -------------------
from psycopg2 import IntegrityError
import pandas as pd
import altair as alt

# Local application imports
# -------------------------

logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)


@auth.requires(
    lambda: verifyInstructorStatus(auth.user.course_name, auth.user),
    requires_login=True,
)
def one_exam_competency():
    """Get data about one exam
    using a very cool query.

    """

    assignment_name = request.vars.assignment

    if not assignment_name:
        session.flash = "You must provide an assignment ID"
        return redirect(redirect(URL("admin", "admin")))

    course_id = auth.user.course_id

    logger.debug(f"COMP REPORT for {assignment_name} , {course_id}")
    query = f"""
    SELECT course, assignments.name,  question_grades.sid, div_id, score, selected_questions.points, selected_id, competency.competency, is_primary
    FROM assignments JOIN assignment_questions ON assignment_id = assignments.id
        JOIN questions ON question_id = questions.id
        JOIN question_grades ON questions.name = div_id
        JOIN selected_questions ON selector_id = div_id AND question_grades.sid = selected_questions.sid
        JOIN competency ON selected_id = question_name
    WHERE assignments.name='{assignment_name}' AND course={course_id};
    """

    clx = pd.read_sql_query(
        query, settings.database_uri.replace("postgres://", "postgresql://")
    )
    clx["pct"] = clx.score / clx.points
    clx["correct"] = clx.pct.map(lambda x: 1 if x > 0.9 else 0)

    logging.debug(clx)
    glx = (
        clx[clx.is_primary == "T"]
        .groupby(["competency", "sid"])
        .agg(num_correct=("correct", "sum"), num_answers=("correct", "count"))
    )
    glx = glx.reset_index()
    glx["pct_correct"] = glx.num_correct / glx.num_answers
    c = (
        alt.Chart(glx, title="Primary Competencies")
        .mark_rect()
        .encode(
            x="sid:O",
            y="competency",
            color=alt.Color("pct_correct", scale=alt.Scale(scheme="blues")),
            tooltip="num_answers",
        )
    )
    pcdata = c.to_json()
    # Supporting
    glx = (
        clx[clx.is_primary == "F"]
        .groupby(["competency", "sid"])
        .agg(num_correct=("correct", "sum"), num_answers=("correct", "count"))
    )
    glx = glx.reset_index()
    glx["pct_correct"] = glx.num_correct / glx.num_answers
    c = (
        alt.Chart(glx, title="Supplemental Competencies")
        .mark_rect()
        .encode(
            x="sid:O",
            y="competency",
            color=alt.Color("pct_correct", scale=alt.Scale(scheme="reds")),
            tooltip="num_answers",
        )
    )

    scdata = c.to_json()

    return dict(
        course_id=auth.user.course_name,
        course=get_course_row(db.courses.ALL),
        pcdata=pcdata,
        scdata=scdata,
    )
