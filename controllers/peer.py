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


# Third Party
# -----------
import pandas as pd
import altair as alt


def dashboard():

    current_question = db(db.questions.name == "question1_2_3").select().first()
    return dict(
        course_id=auth.user.course_name,
        course=get_course_row(db.courses.ALL),
        current_question=current_question,
    )


def chartdata():
    response.headers["content-type"] = "application/json"
    div_id = request.vars.div_id
    qnum = request.vars.answer_num
