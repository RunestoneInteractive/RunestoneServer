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
import logging

# Third Party
# -----------
import altair as alt
import pandas as pd


logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)


@auth.requires(
    lambda: verifyInstructorStatus(auth.user.course_id, auth.user),
    requires_login=True,
)
def instructor():
    assignments = db(db.assignments.is_peer == True).select(
        orderby=~db.assignments.duedate
    )

    return dict(
        course_id=auth.user.course_name,
        course=get_course_row(db.courses.ALL),
        assignments=assignments,
    )


@auth.requires(
    lambda: verifyInstructorStatus(auth.user.course_id, auth.user),
    requires_login=True,
)
def dashboard():

    assignment_id = request.vars.assignment_id
    if request.vars.next == "Next":
        next = True
    else:
        next = False
    current_question = _get_current_question(assignment_id, next)

    return dict(
        course_id=auth.user.course_name,
        course=get_course_row(db.courses.ALL),
        current_question=current_question,
        assignment_id=assignment_id,
    )


def _get_current_question(assignment_id, get_next):

    assignment = db(db.assignments.id == assignment_id).select().first()
    idx = 0
    if get_next:
        idx = assignment.current_index + 1
    a_qs = db(db.assignment_questions.assignment_id == assignment_id).select(
        orderby=db.assignment_questions.sorting_priority
    )
    logger.debug(f"{idx=} {len(a_qs)=}")
    if idx > len(a_qs) - 1:
        idx = len(a_qs) - 1
    current_question_id = a_qs[idx].question_id
    current_question = db(db.questions.id == current_question_id).select().first()

    return current_question


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


#
# Student Facing pages
#
@auth.requires_login()
def student():
    assignments = db(db.assignments.is_peer == True).select(
        orderby=~db.assignments.duedate
    )

    return dict(
        course_id=auth.user.course_name,
        course=get_course_row(db.courses.ALL),
        assignments=assignments,
    )


@auth.requires_login()
def peer_question():
    assignment_id = request.vars.assignment_id

    current_question = _get_current_question(assignment_id, False)

    return dict(
        course_id=auth.user.course_name,
        course=get_course_row(db.courses.ALL),
        current_question=current_question,
        assignment_id=assignment_id,
    )


@auth.requires_login()
def home():
    return dict()
