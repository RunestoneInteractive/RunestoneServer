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
import json
import logging
import os
import random

# Third Party
# -----------
import altair as alt
import pandas as pd
import redis
from dateutil.parser import parse

logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)


@auth.requires(
    lambda: verifyInstructorStatus(auth.user.course_id, auth.user),
    requires_login=True,
)
def instructor():
    assignments = db(
        (db.assignments.is_peer == True)
        & (db.assignments.course == auth.user.course_id)
    ).select(orderby=~db.assignments.duedate)

    return dict(
        course_id=auth.user.course_name,
        course=get_course_row(db.courses.ALL),
        assignments=assignments,
        is_instructor=True,
    )


@auth.requires(
    lambda: verifyInstructorStatus(auth.user.course_id, auth.user),
    requires_login=True,
)
def dashboard():
    """
    We track through questions by "submitting" the form that causes us
    to go to the next question.
    """
    assignment_id = request.vars.assignment_id
    if request.vars.next == "Next":
        next = True
    elif request.vars.next == "Reset":
        next = "Reset"
    else:
        next = False
    current_question = _get_current_question(assignment_id, next)
    db.useinfo.insert(
        course_id=auth.user.course_name,
        sid=auth.user.username,
        div_id=current_question.name,
        event="peer",
        act="start_question",
        timestamp=datetime.datetime.utcnow(),
    )
    return dict(
        course_id=auth.user.course_name,
        course=get_course_row(db.courses.ALL),
        current_question=current_question,
        assignment_id=assignment_id,
    )


def _get_current_question(assignment_id, get_next):

    assignment = db(db.assignments.id == assignment_id).select().first()

    if get_next == "Reset":
        idx = 0
        db(db.assignments.id == assignment_id).update(current_index=idx)
    elif get_next is True:
        idx = assignment.current_index + 1
        db(db.assignments.id == assignment_id).update(current_index=idx)
    else:
        idx = assignment.current_index

    a_qs = db(db.assignment_questions.assignment_id == assignment_id).select(
        orderby=[db.assignment_questions.sorting_priority, db.assignment_questions.id]
    )
    logger.debug(f"idx = {idx} len of qs = {len(a_qs)}")
    if idx > len(a_qs) - 1:
        idx = len(a_qs) - 1
    current_question_id = a_qs[idx].question_id
    current_question = db(db.questions.id == current_question_id).select().first()

    return current_question


def _get_n_answers(num_answer, div_id, course_name, start_time):
    dburl = settings.database_uri.replace("postgres://", "postgresql://")

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
            AND timestamp > '{start_time}'
    )
    SELECT
        *
    FROM
        first_answer
    WHERE
        rn <= {num_answer}
    ORDER BY
        sid
    limit 4000    
    """,
        dburl,
    )
    df = df.dropna(subset=["answer"])
    logger.debug(df.head())
    # FIXME: this breaks for multiple answer mchoice!
    df = df[df.answer != ""]
    df["answer"] = df.answer.astype("int64")

    return df


@auth.requires(
    lambda: verifyInstructorStatus(auth.user.course_id, auth.user),
    requires_login=True,
)
def chartdata():
    response.headers["content-type"] = "application/json"
    div_id = request.vars.div_id
    start_time = request.vars.start_time
    num_choices = request.vars.num_answers
    course_name = auth.user.course_name
    logger.debug(f"divid = {div_id}")
    df = _get_n_answers(2, div_id, course_name, start_time)
    df["letter"] = df.answer.map(lambda x: chr(65 + x))
    x = df.groupby(["letter", "rn"])["answer"].count()
    df = x.reset_index()
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    y = pd.DataFrame(
        {
            "letter": list(alpha[:num_choices] * 2),
            "rn": [1] * num_choices + [2] * num_choices,
            "answer": [0] * num_choices * 2,
        }
    )
    df = df.merge(y, how="outer")
    c = (
        alt.Chart(df[df.rn == 1], title="First Answer")
        .mark_bar()
        .encode(x="letter", y=alt.Y("sum(answer)", title="Number of Students"))
    )
    d = (
        alt.Chart(df[df.rn == 2], title="Second Answer")
        .mark_bar()
        .encode(x="letter", y=alt.Y("sum(answer)", title="Number of Students"))
    )

    return alt.hconcat(c, d).to_json()


@auth.requires(
    lambda: verifyInstructorStatus(auth.user.course_id, auth.user),
    requires_login=True,
)
def num_answers():
    response.headers["content-type"] = "application/json"
    div_id = request.vars.div_id
    acount = db(
        (db.mchoice_answers.div_id == div_id)
        & (db.mchoice_answers.course_name == auth.user.course_name)
        & (db.mchoice_answers.timestamp > parse(request.vars.start_time))
    ).count(distinct=db.mchoice_answers.sid)

    return json.dumps({"count": acount})


#
# Student Facing pages
#
@auth.requires_login()
def student():

    if "access_token" not in request.cookies:
        # this means the user is logged in to web2py but not fastapi - this is not good
        # as the javascript in the questions assumes the new server and a token.
        logger.error(f"Missing Access Token: {auth.user.username} adding one Now")
        _create_access_token(
            {"sub": auth.user.username}, expires=datetime.timedelta(days=30)
        )

    assignments = db(
        (db.assignments.is_peer == True)
        & (db.assignments.course == auth.user.course_id)
        & (db.assignments.visible == True)
    ).select(orderby=~db.assignments.duedate)

    return dict(
        course_id=auth.user.course_name,
        course=get_course_row(db.courses.ALL),
        assignments=assignments,
    )


@auth.requires_login()
def peer_question():
    if "access_token" not in request.cookies:
        return redirect(URL("default", "accessIssue"))

    assignment_id = request.vars.assignment_id

    current_question = _get_current_question(assignment_id, False)

    return dict(
        course_id=auth.user.course_name,
        course=get_course_row(db.courses.ALL),
        current_question=current_question,
        assignment_id=assignment_id,
    )


@auth.requires(
    lambda: verifyInstructorStatus(auth.user.course_id, auth.user),
    requires_login=True,
)
def make_pairs():
    response.headers["content-type"] = "application/json"
    div_id = request.vars.div_id
    df = _get_n_answers(1, div_id, auth.user.course_name, request.vars.start_time)
    group_size = int(request.vars.get("group_size", 2))
    logger.debug(f"STARTING to make pairs for {auth.user.course_name}")
    # answers = list(df.answer.unique())
    correct = df[df.correct == "T"][["sid", "answer"]]
    # answers.remove(correct.iloc[0].answer)
    correct_list = correct.sid.to_list()
    incorrect = df[df.correct == "F"][["sid", "answer"]]
    incorrect_list = incorrect.sid.to_list()
    logger.debug(f"CL = {correct_list}")
    logger.debug(f"ICL = {incorrect_list}")
    if auth.user.username in correct_list:
        correct_list.remove(auth.user.username)
    if auth.user.username in incorrect_list:
        incorrect_list.remove(auth.user.username)
    r = redis.from_url(os.environ.get("REDIS_URI", "redis://redis:6379/0"))
    logger.debug(f"Clearing partnerdb_{auth.user.course_name}")
    r.delete(f"partnerdb_{auth.user.course_name}")

    done = False
    peeps = df.sid.to_list()
    random.shuffle(peeps)
    group_list = []
    while not done:
        group = []
        for i in range(group_size):
            try:
                group.append(peeps.pop())
            except IndexError:
                done = True
        if len(group) == 1:
            group_list[-1].append(group[0])
        else:
            group_list.append(group)

    gdict = {}
    for group in group_list:
        for p in group:
            gl = group.copy()
            gl.remove(p)
            gdict[p] = gl

    for k, v in gdict.items():
        r.hset(f"partnerdb_{auth.user.course_name}", k, json.dumps(v))

    logger.debug(f"DONE making pairs for {auth.user.course_name} {gdict}")
    _broadcast_peer_answers(correct, incorrect)
    logger.debug(f"DONE broadcasting pair information")
    return json.dumps("success")


def _broadcast_peer_answers(correct, incorrect):
    """
    The correct and incorrect lists are dataframes that containe the sid and their answer
    We want to iterate over the
    """
    df = pd.concat([correct, incorrect])
    answers = dict(zip(df.sid, df.answer))
    r = redis.from_url(os.environ.get("REDIS_URI", "redis://redis:6379/0"))
    for p1, p2 in r.hgetall(f"partnerdb_{auth.user.course_name}").items():
        p1 = p1.decode("utf8")
        partner_list = json.loads(p2)
        pdict = {}
        for p2 in partner_list:
            ans = answers.get(p2, None)
            pdict[p2] = ans
        # create a message from p1 to put into the publisher queue
        # it seems odd to not have a to field in the message...
        # but it is not necessary as the client can figure out how it is to
        # based on who it is from.
        mess = {
            "type": "control",
            "from": p1,
            "to": p1,
            "message": "enableChat",
            "broadcast": False,
            "answer": json.dumps(pdict),
            "course_name": auth.user.course_name,
        }
        r.publish("peermessages", json.dumps(mess))


def clear_pairs():
    response.headers["content-type"] = "application/json"
    r = redis.from_url(os.environ.get("REDIS_URI", "redis://redis:6379/0"))
    r.delete(f"partnerdb_{auth.user.course_name}")
    return json.dumps("success")


def publish_message():
    response.headers["content-type"] = "application/json"
    r = redis.from_url(os.environ.get("REDIS_URI", "redis://redis:6379/0"))
    data = json.dumps(request.vars)
    logger.debug(f"data = {data}")
    r.publish("peermessages", data)
    return json.dumps("success")


def log_peer_rating():
    response.headers["content-type"] = "application/json"
    current_question = request.vars.div_id
    peer_sid = request.vars.peer_id
    r = redis.from_url(os.environ.get("REDIS_URI", "redis://redis:6379/0"))
    retmess = "Error: no peer to rate"
    if peer_sid:
        db.useinfo.insert(
            course_id=auth.user.course_name,
            sid=auth.user.username,
            div_id=current_question,
            event="ratepeer",
            act=f"{peer_sid}:{request.vars.rating}",
            timestamp=datetime.datetime.utcnow(),
        )
        retmess = "success"

    return json.dumps(retmess)
