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
    """ Get data about one exam
    using a very cool query.

    """

    assignment_name = request.vars.assignment
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

    clx = pd.read_sql_query(query, settings.database_uri)
    logging.debug(clx)
    glx = (
        clx[clx.is_primary == "T"]
        .groupby(["competency", "sid"])
        .agg(avg_score=("score", "mean"), num_qs=("score", "count"))
    )
    glx = glx.reset_index()
    c = alt.Chart(glx).mark_rect().encode(x="sid:O", y="competency", color="avg_score")
    pcdata = c.to_json()

    glx = (
        clx[clx.is_primary == "F"]
        .groupby(["competency", "sid"])
        .agg(avg_score=("score", "mean"), num_qs=("score", "count"))
    )
    glx = glx.reset_index()
    c = alt.Chart(glx).mark_rect().encode(x="sid:O", y="competency", color="avg_score")
    scdata = c.to_json()

    return dict(
        course_id=auth.user.course_name,
        course=get_course_row(db.courses.ALL),
        pcdata=pcdata,
        scdata=scdata,
    )
