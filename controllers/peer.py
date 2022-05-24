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

peerjs = os.path.join("applications", request.application, "static", "js", "peer.js")
try:
    mtime = int(os.path.getmtime(peerjs))
except FileNotFoundError:
    mtime = random.randrange(10000)

request.peer_mtime = str(mtime)


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
    r = redis.from_url(os.environ.get("REDIS_URI", "redis://redis:6379/0"))
    r.hset(f"{auth.user.course_name}_state", "mess_count", "0")
    return dict(
        course_id=auth.user.course_name,
        course=get_course_row(db.courses.ALL),
        current_question=current_question,
        assignment_id=assignment_id,
        is_instructor=True,
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


def _get_lastn_answers(num_answer, div_id, course_name, start_time, end_time=None):
    dburl = settings.database_uri.replace("postgres://", "postgresql://")

    time_clause = f"""
        AND timestamp > '{start_time}'
        """
    if end_time:
        time_clause += f" AND timestamp < '{end_time}'"

    df = pd.read_sql_query(
        f"""
    WITH first_answer AS (
        SELECT
            *,
            ROW_NUMBER() OVER (
                PARTITION BY sid
                ORDER BY
                    id desc
            ) AS rn
        FROM
            mchoice_answers
        WHERE
            div_id = '{div_id}'
            AND course_name = '{course_name}'
            {time_clause}
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

    return df


def to_letter(astring: str):
    if astring.isnumeric():
        return chr(65 + int(astring))
    if "," in astring:
        alist = astring.split(",")
        alist = [chr(65 + int(x)) for x in alist]
        return ",".join(alist)
    return None


@auth.requires(
    lambda: verifyInstructorStatus(auth.user.course_id, auth.user),
    requires_login=True,
)
def chartdata():
    response.headers["content-type"] = "application/json"
    div_id = request.vars.div_id
    start_time = request.vars.start_time
    end_time = request.vars.start_time2  # start time of vote 2
    num_choices = request.vars.num_answers
    course_name = auth.user.course_name
    logger.debug(f"divid = {div_id}")
    df1 = _get_lastn_answers(1, div_id, course_name, start_time, end_time)
    if end_time:
        df2 = _get_lastn_answers(1, div_id, course_name, end_time)
        df2.rn = 2
        df = pd.concat([df1, df2])
    else:
        df = df1
    df["letter"] = df.answer.map(to_letter)
    x = df.groupby(["letter", "rn"])["answer"].count()
    df = x.reset_index()
    yheight = df.answer.max()
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
        .encode(
            x="letter",
            y=alt.Y(
                "sum(answer)",
                title="Number of Students",
                scale=alt.Scale(domain=(0, yheight)),
            ),
        )
    )
    d = (
        alt.Chart(df[df.rn == 2], title="Second Answer")
        .mark_bar()
        .encode(
            x="letter",
            y=alt.Y(
                "sum(answer)",
                title="Number of Students",
                scale=alt.Scale(domain=(0, yheight)),
            ),
        )
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
    r = redis.from_url(os.environ.get("REDIS_URI", "redis://redis:6379/0"))
    mess_count = int(r.hget(f"{auth.user.course_name}_state", "mess_count"))
    return json.dumps({"count": acount, "mess_count": mess_count})


#
# Student Facing pages
#
@auth.requires_login()
def student():

    if "access_token" not in request.cookies:
        # this means the user is logged in to web2py but not fastapi - this is not good
        # as the javascript in the questions assumes the new server and a token.
        logger.error(f"Missing Access Token: {auth.user.username} adding one Now")
        create_rs_token()

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


def find_good_partner(group, peeps, answer_dict):
    # try to find a partner with a different answer than the first group member
    logger.debug(f"here {group}, {peeps}, {answer_dict}")
    ans = answer_dict[group[0]]
    i = 0
    while i < len(peeps) and answer_dict[peeps[i]] == ans:
        logger.debug(f"{i} : {peeps[i]}")
        i += 1

    logger.debug("made it")
    if i < len(peeps):
        logger.debug("made it 2")
        return peeps.pop(i)
    else:
        return peeps.pop()


@auth.requires(
    lambda: verifyInstructorStatus(auth.user.course_id, auth.user),
    requires_login=True,
)
def make_pairs():
    response.headers["content-type"] = "application/json"
    div_id = request.vars.div_id
    df = _get_lastn_answers(1, div_id, auth.user.course_name, request.vars.start_time)
    group_size = int(request.vars.get("group_size", 2))
    r = redis.from_url(os.environ.get("REDIS_URI", "redis://redis:6379/0"))
    logger.debug(f"Clearing partnerdb_{auth.user.course_name}")
    r.delete(f"partnerdb_{auth.user.course_name}")

    logger.debug(f"STARTING to make pairs for {auth.user.course_name}")
    done = False
    peeps = df.sid.to_list()
    sid_ans = df.set_index("sid")["answer"].to_dict()

    if auth.user.username in peeps:
        peeps.remove(auth.user.username)
    random.shuffle(peeps)
    group_list = []
    while not done:
        group = [peeps.pop()]
        for i in range(group_size - 1):
            try:
                group.append(find_good_partner(group, peeps, sid_ans))
            except IndexError:
                logger.debug("except")
                done = True
        if len(group) == 1:
            group_list[-1].append(group[0])
        else:
            group_list.append(group)
        if len(peeps) == 0:
            done = True

    gdict = {}
    for group in group_list:
        for p in group:
            gl = group.copy()
            gl.remove(p)
            gdict[p] = gl

    for k, v in gdict.items():
        r.hset(f"partnerdb_{auth.user.course_name}", k, json.dumps(v))
    r.hset(f"{auth.user.course_name}_state", "mess_count", "0")
    logger.debug(f"DONE makeing pairs for {auth.user.course_name} {gdict}")
    _broadcast_peer_answers(sid_ans)
    logger.debug(f"DONE broadcasting pair information")
    return json.dumps("success")


def _broadcast_peer_answers(answers):
    """
    The correct and incorrect lists are dataframes that containe the sid and their answer
    We want to iterate over the
    """

    r = redis.from_url(os.environ.get("REDIS_URI", "redis://redis:6379/0"))
    for p1, p2 in r.hgetall(f"partnerdb_{auth.user.course_name}").items():
        p1 = p1.decode("utf8")
        partner_list = json.loads(p2)
        pdict = {}
        for p2 in partner_list:
            ans = to_letter(answers.get(p2, None))
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
    mess_count = int(r.hget(f"{auth.user.course_name}_state", "mess_count"))
    if not mess_count:
        mess_count = 0
    if request.vars.type == "text":
        r.hset(f"{auth.user.course_name}_state", "mess_count", str(mess_count + 1))
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
