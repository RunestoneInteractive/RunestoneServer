# ****************************************
# |docname| - question queries and reports
# ****************************************
# This module provides tools for querying and reporting on students' answers to questions and related info. This is used by the `assignments/grades_report endpoint`.
#
# Imports
# =======
# These are listed in the order prescribed by `PEP 8
# <http://www.python.org/dev/peps/pep-0008/#imports>`_.
#
# Standard library
# ----------------
from collections import namedtuple, OrderedDict
import datetime
from itertools import islice
import json
import logging

# Third-party imports
# -------------------
from gluon import current

# Local application imports
# -------------------------
# None.

logger = logging.getLogger(current.settings.logger)
logger.setLevel(current.settings.log_level)


# Questions query
# ===============
# Provide a convenient container for storing some results of the query.
_UserInfo = namedtuple("_UserInfo", "first_name, last_name, email")
_QuestionInfo = namedtuple(
    "_QuestionInfo", "type_, points, chapter, subchapter, number"
)


# Given an query which defines the questions of interest, return the struct ``grades[user_id][div_id]``:
#
# .. code-block:: Python
#   :linenos:
#
#   grades = ordered dict {
#       str(user_id): {                 # Will be an ordered dict if user_id == None.
#           str(div_id):
#               namedtuple(str(question type_), int(max points), str(chapter),      if user_id == None
#                   str(subchapter), str(question number))
#               namedtuple(str(first_name), str(last_name), str(email))             if div_id == None
#               [datetime(timestamp), float(score), answer, correct]                otherwise
#       }
#   }
#
# This is like a spreadsheet:
#
# grades[user_id][div_id] contains:
#
## None      div_id1   div_id2  ... div_idn   <-- From the div_id headings query
## user_id1  data 1,1  data 1,2     data 1,n  \
## user_id2  data 2,1  data 2,2     data 2,n   \
## ...                                          > From the body data query
## user_idm  data m,1  data m,2     data m,n   /
##  ^---- From the user_id headings query
#
# Note: informal testing shows that proper indices are critical to making these query run fast enough. They are:
#
## create index lp_answers_mkey on lp_answers (div_id, sid, course_name, timestamp);
## create index mchoice_answers_mkey on mchoice_answers (div_id, sid, course_name, timestamp);
## create index fitb_answers_mkey on fitb_answers (div_id, sid, course_name, timestamp);
## create index shortanswer_answers_mkey on shortanswer_answers (div_id, sid, course_name, timestamp);
#
# Use the `Postgres EXPLAIN visualizer <http://tatiyants.com/pev>`_ to imporve queries.
def questions_to_grades(
    # The name of the course.
    course_name,
    # A query defining the questions of interest.
    query_questions,
):
    # Build grades struct and populate with row/col headers.
    grades, query = _headers_query(course_name, query_questions, False)

    # **body data query**
    ## ------------------
    # Select only this class.
    db = current.db
    useinfo_max_query = db.useinfo.course_id == course_name
    # Include the due date in the query if it's provided.
    # Define a query to select the newest (maximum) useinfo row for each unique set of (sid, div_id).
    useinfo_max_sql = db(useinfo_max_query)._select(
        db.useinfo.sid,
        db.useinfo.div_id,
        db.useinfo.timestamp.max(),
        # This selects the newest (max) ``useinfo.timestamp`` **for each record**. Note that any selected field must appear in the group by clause -- see https://blog.jooq.org/2016/12/09/a-beginners-guide-to-the-true-order-of-sql-operations/.
        groupby=db.useinfo.sid | db.useinfo.div_id,
    )
    # Now, make this an SQL clause. This is required, since SQL can't select any fields outside of the groupby fields, and adding additional fields causes the max not to work.
    newest_useinfo_expr = (
        "(useinfo.sid, useinfo.div_id, useinfo.timestamp) IN ("
        +
        # Omit the closing semicolon from the previous query to use it as a subquery.
        useinfo_max_sql[:-1]
        + ")"
    )
    # Use this id to limit the query.
    for row in db(query & newest_useinfo_expr).select(
        db.useinfo.sid,
        db.useinfo.div_id,
        db.useinfo.timestamp,
        db.useinfo.course_id,
        db.useinfo.act,
        # Left join fields...
        db.question_grades.score,
        db.clickablearea_answers.answer,
        db.clickablearea_answers.correct,
        db.code.code,
        db.codelens_answers.answer,
        db.codelens_answers.correct,
        db.dragndrop_answers.answer,
        db.dragndrop_answers.correct,
        db.fitb_answers.answer,
        db.fitb_answers.correct,
        db.lp_answers.answer,
        db.lp_answers.correct,
        db.mchoice_answers.answer,
        db.mchoice_answers.correct,
        db.parsons_answers.answer,
        db.parsons_answers.correct,
        db.shortanswer_answers.answer,
        # Get to the answer/correct fields for various problems, if they exist -- hence the left join.
        left=(
            # Include a `question grade <question_grades table>`, if one exists.
            db.question_grades.on(
                # Join a question grade to the question that was graded.
                (db.question_grades.div_id == db.useinfo.div_id)
                &
                # Join to ``auth_user`` to get information about each user.
                (db.question_grades.sid == db.useinfo.sid)
                & (db.question_grades.course_name == course_name)
            ),
            # Include answer and correct fields for each question type.
            db.clickablearea_answers.on(
                (db.useinfo.timestamp == db.clickablearea_answers.timestamp)
                & (db.useinfo.sid == db.clickablearea_answers.sid)
                & (db.useinfo.div_id == db.clickablearea_answers.div_id)
                & (db.clickablearea_answers.course_name == course_name)
            ),
            db.code.on(
                (db.useinfo.timestamp == db.code.timestamp)
                & (db.useinfo.sid == db.code.sid)
                & (db.useinfo.div_id == db.code.acid)
                & (db.useinfo.course_id == db.code.course_id)
            ),
            db.codelens_answers.on(
                (db.useinfo.timestamp == db.codelens_answers.timestamp)
                & (db.useinfo.sid == db.codelens_answers.sid)
                & (db.useinfo.div_id == db.codelens_answers.div_id)
                & (db.codelens_answers.course_name == course_name)
            ),
            db.dragndrop_answers.on(
                (db.useinfo.timestamp == db.dragndrop_answers.timestamp)
                & (db.useinfo.sid == db.dragndrop_answers.sid)
                & (db.useinfo.div_id == db.dragndrop_answers.div_id)
                & (db.dragndrop_answers.course_name == course_name)
            ),
            db.fitb_answers.on(
                (db.useinfo.timestamp == db.fitb_answers.timestamp)
                & (db.useinfo.sid == db.fitb_answers.sid)
                & (db.useinfo.div_id == db.fitb_answers.div_id)
                & (db.fitb_answers.course_name == course_name)
            ),
            db.lp_answers.on(
                (db.useinfo.timestamp == db.lp_answers.timestamp)
                & (db.useinfo.sid == db.lp_answers.sid)
                & (db.useinfo.div_id == db.lp_answers.div_id)
                & (db.lp_answers.course_name == course_name)
            ),
            db.mchoice_answers.on(
                (db.useinfo.timestamp == db.mchoice_answers.timestamp)
                & (db.useinfo.sid == db.mchoice_answers.sid)
                & (db.useinfo.div_id == db.mchoice_answers.div_id)
                & (db.mchoice_answers.course_name == course_name)
            ),
            db.parsons_answers.on(
                (db.useinfo.timestamp == db.parsons_answers.timestamp)
                & (db.useinfo.sid == db.parsons_answers.sid)
                & (db.useinfo.div_id == db.parsons_answers.div_id)
                & (db.parsons_answers.course_name == course_name)
            ),
            db.shortanswer_answers.on(
                (db.useinfo.timestamp == db.shortanswer_answers.timestamp)
                & (db.useinfo.sid == db.shortanswer_answers.sid)
                & (db.useinfo.div_id == db.shortanswer_answers.div_id)
                & (db.shortanswer_answers.course_name == course_name)
            ),
        ),
    ):

        # Get the answer and correct info based on the type of question.
        question_type = grades[None][row.useinfo.div_id].type_
        answer, correct, timestamp = _row_decode(row, question_type)

        # Place the query into its appropriate matrix location.
        grades[row.useinfo.sid][row.useinfo.div_id] = [
            timestamp,
            row.question_grades.score,
            answer,
            correct,
            # This is a _`placeholder` for the number of attempts.
            None,
        ]

    # For SQL performance analysis.
    ##with open('/home/www-data/web2py/applications/runestone/q.txt', 'w') as f:
    ##f.write(db._lastsql[0])

    _attempts_query(query, grades)

    return grades


def _headers_query(
    # The name of the course.
    course_name,
    # A query defining the questions of interest.
    query_questions,
    # True to sort the ``div_ids`` by ``db.assignment_questions.sorting_priority``.
    orderby_sorting_priority,
):
    # **div_id headings query**
    ## --------------------------
    db = current.db
    # Get information about each div_id.
    grades = OrderedDict()
    grades[None] = OrderedDict()
    # Produce the ``div_id`` entries in the order specified by the assignment if requested.
    kwargs = (
        dict(orderby=db.assignment_questions.sorting_priority)
        if orderby_sorting_priority
        else {}
    )
    for row in db(query_questions).select(
        db.questions.name,
        db.assignment_questions.points,
        db.questions.question_type,
        db.questions.chapter,
        db.questions.subchapter,
        db.questions.qnumber,
        # Eliminate duplicates.
        groupby=db.questions.name
        | db.assignment_questions.points
        | db.questions.question_type
        | db.questions.chapter
        | db.questions.subchapter
        | db.questions.qnumber
        | db.assignment_questions.sorting_priority,
        **kwargs
    ):

        # Store the max points for this ``div_id``.
        grades[None][row.questions.name] = _QuestionInfo._make(
            [
                row.questions.question_type,
                row.assignment_questions.points,
                row.questions.chapter,
                row.questions.subchapter,
                row.questions.qnumber,
            ]
        )

    # **user_id headings query**
    ## ---------------------------
    # The base query for this entire function. It's used to get information about each user_id/div_id combination.
    query = (
        # Choose seleted questions.
        query_questions
        # Join them to ``useinfo``.
        & (db.questions.name == db.useinfo.div_id)
        # Select only questions in the provided course.
        & (db.useinfo.course_id == course_name)
    )
    # Get information about each user_id.
    select_args = [db.auth_user.first_name, db.auth_user.last_name, db.auth_user.email]
    select_kwargs = dict(orderby=db.auth_user.last_name | db.auth_user.first_name)
    # A query to specify all students in a given course.
    enrolled_students = (
        (db.courses.course_name == course_name)
        & (db.courses.id == db.user_courses.course_id)
        & (db.user_courses.user_id == db.auth_user.id)
    )
    # First, find all students enrolled in the course. This may include students who answered no questions, hence this part of the query.
    for row in db(enrolled_students).select(
        db.auth_user.username, *select_args, **select_kwargs
    ):

        user_id = row.username
        grades[user_id] = dict()
        grades[user_id][None] = _UserInfo._make(
            [row.first_name, row.last_name, row.email]
        )

    # Second, find all students who answered a question in this course. Students can later remove themselves from a course, but their answers will still be in the course, hence this part of the query. Likewise, students who aren't logged in but did answer questions aren't enrolled in the course, but should also be included.
    for row in db(
        query
        # Remove any students produced by the previous query.
        & ~db.useinfo.sid.belongs(db(enrolled_students)._select(db.auth_user.username))
    ).select(
        db.useinfo.sid,
        *select_args,
        # Get the associated ``auth_user`` record if possible.
        left=(db.auth_user.on(db.useinfo.sid == db.auth_user.username),),
        # Ask for distinct entries, since a given student will answer many questions.
        distinct=True,
        **select_kwargs
    ):

        user_id = row.useinfo.sid
        assert user_id not in grades
        grades[user_id] = dict()
        grades[user_id][None] = _UserInfo._make(
            [row.auth_user.first_name, row.auth_user.last_name, row.auth_user.email]
        )

    return grades, query


def _row_decode(row, question_type):
    timestamp = row.useinfo.timestamp

    # Use a specific table's timestamp field if at all possible; otherwise, use the useinfo timestamp.
    def ts_get(table):
        # Some queries don't select the timestamp field. In other cases, it may be present but None, while the ``useinfo`` timestamp is valid. So:
        return table.get("timestamp", timestamp) or timestamp

    if question_type == "clickablearea":
        return (
            row.clickablearea_answers.answer,
            row.clickablearea_answers.correct,
            ts_get(row.clickablearea_answers),
        )
    elif question_type in ("activecode", "actex"):
        ts = row.code.get("timestamp", timestamp) or timestamp
        # The format of ``useinfo.act`` for code problems with a unit test looks like ``percent:66.6666666667:passed:2:failed:1``. The code isn't as useful to display. The grade is None in the ``code`` table, so don't bother showing it.
        try:
            (
                percent_label,
                percent,
                passed_label,
                passed,
                failed_label,
                failed,
            ) = row.useinfo.act.split(":")
        except:
            # Code problems without a unit test won't be parsed.
            return "", None, ts
        return row.useinfo.act, float(percent) >= 100, ts
    elif question_type == "codelens":
        return (
            row.codelens_answers.answer,
            row.codelens_answers.correct,
            ts_get(row.codelens_answers),
        )
    elif question_type == "dragndrop":
        return (
            row.dragndrop_answers.answer,
            row.dragndrop_answers.correct,
            ts_get(row.dragndrop_answers),
        )
    elif question_type == "fillintheblank":
        answer = row.fitb_answers.answer
        try:
            # Guess this is JSON-encoded or empty.
            answer = answer and json.loads(answer)
        except:
            # Handle non-JSON encoded fitb answers.
            answer = answer.split(",")
        return (
            answer,
            row.fitb_answers.correct,
            ts_get(row.fitb_answers),
        )
    elif question_type == "lp_build":
        answer = row.lp_answers.answer
        return (
            {} if not answer else json.loads(answer),
            row.lp_answers.correct,
            ts_get(row.lp_answers),
        )
    elif question_type == "mchoice":
        # Multiple choice questions store their answer as a comma-separated string. Turn this into an array of ints.
        answer = row.mchoice_answers.answer
        answer = answer and [int(ans) for ans in answer.split(",")]
        return (
            answer,
            row.mchoice_answers.correct,
            ts_get(row.mchoice_answers),
        )
    elif question_type == "parsonsprob":
        return (
            row.parsons_answers.answer,
            row.parsons_answers.correct,
            ts_get(row.parsons_answers),
        )
    elif question_type == "shortanswer":
        # Prefer data from the shortanswer table if we have it; otherwise, we can use useinfo's act.
        answer, ts = (
            (
                row.shortanswer_answers.answer,
                ts_get(row.shortanswer_answers),
            )
            if "shortanswer_answers" in row
            else (row.useinfo.act, timestamp)
        )
        try:
            # Try to JSON decode this, for old data.
            answer = json.loads(answer)
        except:
            # The newer format is to store the answer as a pure string. So, ``answer`` already has the correct value.
            pass
        return (
            answer,
            None,
            ts,
        )
    elif question_type in [
        "page",
        "poll",
        "showeval",
        "video",
        "vimeo",
        "youtube",
    ]:
        return row.useinfo.act, None, timestamp
    else:
        # Unknown question! Panic!
        return "unknown question type", None, None


# Update the grades structure with the number of attempts for each student.
def _attempts_query(query, grades):
    # Attempts are collected in a separate query, since the body data query only selects specific timestamps (newest/those graded/etc).
    db = current.db
    attempts = db.useinfo.id.count()
    for row in db(query).select(
        db.useinfo.sid,
        db.useinfo.div_id,
        attempts,
        groupby=db.useinfo.sid | db.useinfo.div_id,
    ):
        # Create an entry for the grade if we don't have one already.
        g = grades[row.useinfo.sid].setdefault(row.useinfo.div_id, [None] * 5)
        # Fill in the placeholder_.
        g[-1] = row[attempts]


# Assignment report
# =================
# Produces ``grades`` for the given course/assignment.
def query_assignment(
    # The name of the course.
    course_name,
    # The name of the assignment.
    assignment_name,
):

    # Verify the course and assignment are valid.
    db = current.db
    course_id = db(db.courses.course_name == course_name).select(db.courses.id).first()
    assert course_id, "Unknown course name {}".format(course_name)
    assert (
        db(db.assignments.name == assignment_name).select(db.assignments.id).first()
    ), "Unknown assignment {}".format(assignment_name)

    # Define the questions of interest, given an assignment and course.
    query_questions = (
        # Select the desired assignment.
        (db.assignments.name == assignment_name)
        &
        # Restrict the query to a specific course.
        (db.assignments.course == course_id)
        &
        # Join to ``assignment_questions`` and from there to ``questions``.
        (db.assignments.id == db.assignment_questions.assignment_id)
        & (db.assignment_questions.question_id == db.questions.id)
    )

    # Build grades struct and populate with row/col headers.
    grades, query = _headers_query(course_name, query_questions, True)

    # **body data query**
    ## ------------------
    # Use this id to limit the query.
    for row in db(
        query_questions
        & (db.question_grades.div_id == db.questions.name)
        & (db.question_grades.course_name == course_name)
    ).select(
        db.question_grades.sid,
        db.question_grades.div_id,
        db.question_grades.score,
        db.clickablearea_answers.answer,
        db.clickablearea_answers.correct,
        db.clickablearea_answers.timestamp,
        db.code.code,
        db.code.timestamp,
        db.codelens_answers.answer,
        db.codelens_answers.correct,
        db.codelens_answers.timestamp,
        db.dragndrop_answers.answer,
        db.dragndrop_answers.correct,
        db.dragndrop_answers.timestamp,
        db.fitb_answers.answer,
        db.fitb_answers.correct,
        db.fitb_answers.timestamp,
        db.lp_answers.answer,
        db.lp_answers.correct,
        db.lp_answers.timestamp,
        db.mchoice_answers.answer,
        db.mchoice_answers.correct,
        db.mchoice_answers.timestamp,
        db.parsons_answers.answer,
        db.parsons_answers.correct,
        db.parsons_answers.timestamp,
        ##db.shortanswer_answers.answer,
        ##db.shortanswer_answers.timestamp,
        db.useinfo.timestamp,
        db.useinfo.act,
        # Get to the answer/correct fields for various problems, if they exist -- hence the left join.
        left=(
            # Include answer and correct fields for each question type.
            db.clickablearea_answers.on(
                (db.questions.question_type == "clickablearea")
                & (db.question_grades.answer_id == db.clickablearea_answers.id)
            ),
            db.code.on(
                (db.questions.question_type in ("activecode", "actex"))
                & (db.question_grades.answer_id == db.code.id)
            ),
            db.codelens_answers.on(
                (db.questions.question_type == "codelens")
                & (db.question_grades.answer_id == db.codelens_answers.id)
            ),
            db.dragndrop_answers.on(
                (db.questions.question_type == "dragndrop")
                & (db.question_grades.answer_id == db.dragndrop_answers.id)
            ),
            db.fitb_answers.on(
                (db.questions.question_type == "fillintheblank")
                & (db.question_grades.answer_id == db.fitb_answers.id)
            ),
            db.lp_answers.on(
                (db.questions.question_type == "lp_build")
                & (db.question_grades.answer_id == db.lp_answers.id)
            ),
            db.mchoice_answers.on(
                (db.questions.question_type == "mchoice")
                & (db.question_grades.answer_id == db.mchoice_answers.id)
            ),
            db.parsons_answers.on(
                (db.questions.question_type == "parsonsprob")
                & (db.question_grades.answer_id == db.parsons_answers.id)
            ),
            ## TODO: currently, the autograder stores the ID of the associated useinfo entry, so this code is wrong. If the autograder is updated, then can be used.
            ##db.shortanswer_answers.on(
            ##    (db.questions.question_type == "shortanswer")
            ##    & (db.question_grades.answer_id == db.shortanswer_answers.id)
            ##),
            # The autograder for interaction-only questions stores a useinfo ID. Get info from there for these questions.
            db.useinfo.on(
                (
                    db.questions.question_type
                    in (
                        "page",
                        "poll",
                        "shortanswer",
                        "showeval",
                        "vimeo",
                        "video",
                        "youtube",
                    )
                )
                & (db.question_grades.answer_id == db.useinfo.id)
            ),
        ),
    ):

        # If a student answers no questions, then is autograded, then is removed from the course, the headings query doesn't contain this student. Add them in.
        username = row.question_grades.sid
        if username not in grades:
            au_row = (
                db(db.auth_user.username == username)
                .select(
                    db.auth_user.first_name, db.auth_user.last_name, db.auth_user.email
                )
                .first()
            )
            grades[username] = dict()
            grades[username][None] = _UserInfo._make(
                [au_row.first_name, au_row.last_name, au_row.email]
            )

        # Get the answer and correct info based on the type of question.
        question_type = grades[None][row.question_grades.div_id].type_
        answer, correct, timestamp = _row_decode(row, question_type)

        # Place the query into its appropriate matrix location.
        grades[username][row.question_grades.div_id] = [
            timestamp,
            row.question_grades.score,
            answer,
            correct,
            # This is a placeholder for the number of attempts.
            None,
        ]

    _attempts_query(query, grades)

    return grades


# Send the ``grades`` to the web client by transforming it to dict of data for use with `Handsontable <http://handsontable.com>`_.
def grades_to_hot(
    # The ``grades`` data structure returned from ``query_assignment``.
    grades,
):

    div_id_dict = grades[None]
    assert div_id_dict, "No supported question types in this assignment."

    # Convert the iterator returned by a dict to a list. Otherwise, the iterator will be used up after producing the first row of data.
    question_info_values = list(div_id_dict.values())

    # Return a student's score, or 0 if no score was reported.
    def get_score(grade_info):
        if grade_info:
            score = grade_info[1]
            if score:
                assert isinstance(score, float)
        return grade_info[1] or 0 if grade_info else 0

    # Return a "" if a divide by zero occurs.
    def blank_divide_by_0(num, dem):
        try:
            return num / dem
        except ZeroDivisionError:
            return ""

    # Collect the points for each question.
    points = [_question_info.points for _question_info in question_info_values]
    max_points = sum(points)

    data = [
        # Index 0
        ["div_id", "", "", "", ""] + [div_id for div_id in div_id_dict.keys()],
        # Index 1
        ["location", "", "", "", ""]
        + [
            _question_info.chapter + " - " + _question_info.subchapter
            for _question_info in question_info_values
        ],
        # Index 2
        ["type", "", "", "", ""]
        + [_question_info.type_ for _question_info in question_info_values],
        # Index 3
        ["points", "", "", "", ""] + points,
        # Index 4
        ["avg grade (%)", "", "", "", ""],
        # Index 5
        ["avg attempts", "", "", "", ""],
    ] + [
        # Index 6 and following: rows of grades data.
        [
            # Index 0
            user_id,
            # Index 1
            grades[user_id][None].last_name,
            # Index 2
            grades[user_id][None].first_name,
            # Index 3
            grades[user_id][None].email,
            # Index 4 -- each student's grade. Skip the _UserInfo obtained from ``grades[user_id][None]``.
            blank_divide_by_0(
                sum(
                    [
                        get_score(grade_info)
                        for div_id, grade_info in grades[user_id].items()
                        if div_id
                    ]
                ),
                max_points,
            ),
        ]
        # Get grades[None].keys()[1:], but using iterator syntax.
        for user_id in islice(grades.keys(), 1, None)
    ]
    orig_data = [
        [grades[user_id].get(div_id) for div_id in div_id_dict.keys()]
        for user_id in islice(grades.keys(), 1, None)
    ]

    # Compute the average score and average attempts for each question.
    def get_attempts(grade_info):
        return grade_info[4] or 0 if grade_info else 0

    # Merge cells when the location is identical.
    mergeCells = []
    # Start at the beginning of real data -- indices 0-4 is userid, first name, last name, e-mail, avg grade.
    index = 5
    # End one index before the actual end, since this must compare index to index+1.
    end_index = len(data[1]) - 1
    while index < end_index:
        colspan = 1
        colspan_start = index
        # Loop if locations are identical to count the colspan size.
        while (index < end_index) and (data[1][index] == data[1][index + 1]):
            colspan += 1
            index += 1
        if colspan > 1:
            mergeCells.append(
                dict(row=1, col=colspan_start, rowspan=1, colspan=colspan)
            )
        index += 1

    # Gather the results into a single object to send to the client.
    res = dict(
        ## Index:      0           1              2            3          4
        colHeaders=["userid", "Family name", "Given name", "e-mail", "avg grade (%)"]
        + [_question_info.number for _question_info in question_info_values],
        data=data,
        orig_data=orig_data,
        mergeCells=mergeCells,
    )

    # Provide a function that knows how to JSON encode a datetime. This should be passed to the ``default`` parameter in ``json.dumps``.
    def datetime_json_default(o):
        if isinstance(o, datetime.datetime):
            # All times are in UTC, even though the datetime object doesn't know that.
            return o.isoformat() + "Z"
        raise TypeError

    # from pprint import pprint; pprint(grades)
    return json.dumps(res, default=datetime_json_default)
