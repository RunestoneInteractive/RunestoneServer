# *******************************
# |docname| - route to a textbook
# *******************************
# This controller provides routes to admin functions
#
# Imports
# =======
# These are listed in the order prescribed by `PEP 8
# <http://www.python.org/dev/peps/pep-0008/#imports>`_.
#
# Standard library
# ----------------
import os
import logging

# Third Party
# -----------
import pandas as pd
import altair as alt

logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)


def dashboard():

    current_question = db(db.questions.name == "question1_1").select().first()
    return dict(
        course_id=auth.user.course_name,
        course=get_course_row(db.courses.ALL),
        current_question=current_question,
    )


@auth.requires(
    lambda: verifyInstructorStatus(auth.user.course_id, auth.user),
    requires_login=True,
)
def chartdata():
    response.headers["content-type"] = "application/json"
    div_id = request.vars.div_id
    qnum = request.vars.answer_num
    course_name = auth.user.course_name
    dburl = settings.database_uri.replace("postgres://", "postgresql://")
    logger.debug(f"divid = {div_id}")
    df = pd.read_sql_query(
        f"""
    WITH first_answer AS (
        SELECT
            *,
            ROW_NUMBER() OVER (
                PARTITION BY sid
                ORDER BY
                    id
            ) AS rn
        FROM
            mchoice_answers
        WHERE
            div_id = '{div_id}'
            AND course_name = '{course_name}'
    )
    SELECT
        *
    FROM
        first_answer
    WHERE
        rn <= 2
    ORDER BY
        sid
    limit 4000    
    """,
        dburl,
    )

    df = df.dropna(subset=["answer"])
    logger.debug(df.head())
    df["answer"] = df.answer.astype("int64")
    df["letter"] = df.answer.map(lambda x: chr(65 + x))
    c = alt.Chart(df[df.rn == 1]).mark_bar().encode(x="letter", y="count()")
    d = alt.Chart(df[df.rn == 2]).mark_bar().encode(x="letter", y="count()")

    return alt.vconcat(c, d).to_json()
