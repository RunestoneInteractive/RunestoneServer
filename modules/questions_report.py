# -*- coding: utf-8 -*-
#
# ****************************************
# |docname| - question queries and reports
# ****************************************
# This module provides tools for querying and reporting on students' answers to questions and related info.
#
# Imports
# =======
# These are listed in the order prescribed by `PEP 8
# <http://www.python.org/dev/peps/pep-0008/#imports>`_.
#
# Standard library
# ----------------
from collections import namedtuple, OrderedDict
try:
    from pathlib import Path
except:
    from pathlib2 import Path
import json
import itertools
from pprint import pformat
from datetime import timedelta

# Third-party imports
# -------------------
import six
from gluon import current
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell

# Local application imports
# -------------------------
# None.


# Questions query
# ===============
# Provide a convenient container for storing some results of the query.
_UserInfo = namedtuple('_UserInfo', 'first_name, last_name, email')
_QuestionInfo = namedtuple('_QuestionInfo', 'points, chapter, subchapter, htmlsrc')


# Given an query which defines the div_ids of interest, return the struct ``grades[user_id][div_id]``:
#
# .. code-block:: Python
#   :number-lines:
#
#   grades = ordered dict {
#       str(user_id): {                 # Will be an ordered dict if user_id == None.
#           str(div_id):
#               namedtuple(int(max points), str(chapter), str(subchapter), str(htmlsrc))    if user_id == None.
#               namedtuple(str(first_name), str(last_name), str(email))                     if div_id == None
#               [datetime(timestamp), float(score), answer, correct]                        otherwise
#       }
#   }
#
# This is like a spreadsheet:
#
# grades[row][column] contains:
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
def _query_questions(
    # The name of the course.
    course_name,
    # A query defining the questions of interest.
    query_questions,
    # True to sort the ``div_ids`` by ``db.assignment_questions.sorting_priority``.
    orderby_sorting_priority=True,
    # An optional due date.
    due_date=None,
):

    # **div_id headings query**
    #--------------------------
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
        db.questions.name, db.assignment_questions.points,
        db.questions.chapter, db.questions.subchapter, db.questions.htmlsrc,
        # Eliminate duplicates.
        groupby=db.questions.name | db.assignment_questions.points |
            db.questions.chapter | db.questions.subchapter |
            db.questions.htmlsrc | db.assignment_questions.sorting_priority,
        **kwargs
    ):

        # Store the max points for this ``div_id``.
        grades[None][row.questions.name] = _QuestionInfo._make([
            row.assignment_questions.points, row.questions.chapter,
            row.questions.subchapter, row.questions.htmlsrc
        ])

    # **user_id headings query**
    #---------------------------
    # Get information about each user_id/div_id combination.
    query = (
        # Choose seleted questions.
        query_questions &
        # Join them to ``useinfo``.
        (db.questions.name == db.useinfo.div_id)
    )
    # Include the course in some queries.
    query_course = query & (db.useinfo.course_id == course_name)

    # Get information about each user_id.
    select_args = [
        db.auth_user.username,
        db.auth_user.first_name, db.auth_user.last_name,
        db.auth_user.email
    ]
    select_kwargs = dict(
        orderby=db.auth_user.last_name | db.auth_user.first_name
    )
    for row in itertools.chain(
        # Note: writing these as one query combined with an OR produces a VERY slow query. Better might be a UNION, but the DAL doesn't support this.
        #
        # First, find all students enrolled in the course. This may include students who answered no questions, hence this part of the query.
        db (
            (db.courses.course_name == course_name) &
            (db.courses.id == db.user_courses.course_id) &
            (db.user_courses.user_id == db.auth_user.id)
        ).select(*select_args, **select_kwargs),
        # Second, find all students who answered a question in this course. Students can later remove themselves from a course, but their answers will still be in the course, hence this part of the query.
        db(
            query_course &
            (db.useinfo.sid == db.auth_user.username)
        # Ask for distinct entries, since a given students will answer many questions.
        ).select(*select_args, distinct=True, **select_kwargs)
    ):

        user_id = row.username
        # Skip duplicates from the two queries.
        if user_id not in grades:
            grades[user_id] = dict()
            grades[user_id][None] = _UserInfo._make([row.first_name, row.last_name, row.email])

    # **body data query**
    #--------------------
    # Select only this class.
    useinfo_max_query = (db.useinfo.course_id == course_name)
    # Include the due date in the query if it's provided.
    if due_date:
        useinfo_max_query &= (db.useinfo.timestamp <= due_date)
    # Define a query to select the newest (maximum) useinfo row for each unique set of (sid, div_id).
    useinfo_max_sql = db(useinfo_max_query)._select(
        db.useinfo.sid, db.useinfo.div_id, db.useinfo.timestamp.max(),
        # This selects the newest (max) ``useinfo.timestamp`` **for each record**. Note that any selected field must appear in the group by clause -- see https://blog.jooq.org/2016/12/09/a-beginners-guide-to-the-true-order-of-sql-operations/.
        groupby=db.useinfo.sid | db.useinfo.div_id
    )
    # Now, make this an SQL clause. This is required, since SQL can't select any fields outside of the groupby fields, and adding additional fields causes the max not to work.
    newest_useinfo_expr = (
        '(useinfo.sid, useinfo.div_id, useinfo.timestamp) IN (' +
        # Omit the closing semicolon from the previous query to use it as a subquery.
        useinfo_max_sql[:-1] +
        ')'
    )
    # Use this id to limit the query.
    for row in db(query & newest_useinfo_expr).select(
        db.useinfo.sid, db.useinfo.div_id, db.useinfo.event,
        db.useinfo.timestamp,
        db.question_grades.score,
        db.mchoice_answers.answer, db.mchoice_answers.correct,
        db.fitb_answers.answer, db.fitb_answers.correct,
        db.lp_answers.answer, db.lp_answers.correct,
        db.shortanswer_answers.answer,
        # Get to the answer/correct fields for various problems, if they exist -- hence the left join.
        left=(
            # Include a question grade, if one exists.
            db.question_grades.on(
                # Join a question grade to the question that was graded. Note that ``questions.name`` is the ``div_id`` of that question.
                (db.question_grades.div_id == db.useinfo.div_id) &
                # Join to ``auth_user`` to get information about each user.
                (db.question_grades.sid == db.useinfo.sid) &
                (db.question_grades.course_name == course_name)
            ), db.mchoice_answers.on(
                (db.useinfo.timestamp == db.mchoice_answers.timestamp) &
                (db.useinfo.sid == db.mchoice_answers.sid) &
                (db.useinfo.div_id == db.mchoice_answers.div_id) &
                (db.mchoice_answers.course_name == course_name)
            ), db.fitb_answers.on(
                (db.useinfo.timestamp == db.fitb_answers.timestamp) &
                (db.useinfo.sid == db.fitb_answers.sid) &
                (db.useinfo.div_id == db.fitb_answers.div_id) &
                (db.fitb_answers.course_name == course_name)
            ), db.lp_answers.on(
                (db.useinfo.timestamp == db.lp_answers.timestamp) &
                (db.useinfo.sid == db.lp_answers.sid) &
                (db.useinfo.div_id == db.lp_answers.div_id) &
                (db.lp_answers.course_name == course_name)
            ), db.shortanswer_answers.on(
                (db.useinfo.timestamp == db.shortanswer_answers.timestamp) &
                (db.useinfo.sid == db.shortanswer_answers.sid) &
                (db.useinfo.div_id == db.shortanswer_answers.div_id) &
                (db.shortanswer_answers.course_name == course_name)
            ),
        ),
    ):

        # Get the answer and correct info based on the type of question.
        event = row.useinfo.event
        if event == 'mChoice':
            answer = row.mchoice_answers.answer
            correct = row.mchoice_answers.correct
        elif event == 'fillb':
            answer = row.fitb_answers.answer
            try:
                # Guess this is JSON-encoded or empty.
                answer = '' if not answer else json.loads(answer)
            except:
                # Handle non-JSON encoded fitb answers.
                answer = ','.split(answer)
            correct = row.fitb_answers.correct
        elif event == 'lp_build':
            answer = row.lp_answers.answer
            answer = {} if not answer else json.loads(answer)
            correct = row.lp_answers.correct
        elif event == 'shortanswer':
            answer = row.shortanswer_answers.answer
            try:
                # Try to JSON decode this, for old data.
                answer = '' if not answer else json.loads(answer)
                # Make sure we decoded a string, not something bizarre.
                assert isinstance(answer, six.string_types)
            except:
                # The newer format is to store the answer as a pure string. So, ``answer`` already has the correct value.
                pass
            correct = ''
        else:
            answer = ''
            correct = ''

        # Place the query into its appropriate matrix location.
        grades[row.useinfo.sid][row.useinfo.div_id] = [
            row.useinfo.timestamp,
            row.question_grades.score,
            answer,
            correct
        ]

    # For SQL performance analysis.
    ##with open('/home/www-data/web2py/applications/runestone/q.txt', 'w') as f:
        ##f.write(db._lastsql[0])

    # Attempts are collected in a separate query, since the previous query only selects the newest timestamps.
    attempts = db.useinfo.id.count()
    for row in db(query_course).select(
        db.useinfo.sid, db.useinfo.div_id, attempts,
        groupby=db.useinfo.sid | db.useinfo.div_id,
    ):
        grades[row.useinfo.sid][row.useinfo.div_id].append(row[attempts])

    return grades


# Assignment report
# =================
# Execute ``_query_questions`` , selecting all div_ids in a given assignment.
def _query_assignment(
    # The name of the course.
    course_name,
    # The name of the assignment.
    assignment_name=None,
    # The due date, as an instance of ``datetime``: the last avaiable answer and correct fields before or on this date will be reported. If falsey, the due date for the assignment will be used.
    due_date=None,
):

    # Verify the course and assignment are valid.
    db = current.db
    assert db(db.courses.course_name == course_name).select(db.courses.id).first(), 'Unknown course name {}'.format(course_name)
    assert db(db.assignments.name == assignment_name).select(db.assignments.id).first(), 'Unknown assignment {}'.format(assignment_name)

    # Get the due date if it wasn't specified.
    if not due_date:
        due_date = db (
            # Select the desired assignment.
            (db.assignments.name == assignment_name) &
            # Join to ``course`` so we can restrict the query to a specific course.
            (db.assignments.course == db.courses.id) &
            # Select the desired course.
            (db.courses.course_name == course_name)
        ).select(db.assignments.duedate).first().duedate
    # Correct for the time zone, since the due date is specified in local time. YUCK!!!
    time_zone_delta = timedelta(hours=float(current.session.get('timezoneoffset', 0)))
    due_date += time_zone_delta

    # Define the questions of interest, given an assignment and course.
    query_questions = (
        # Select the desired assignment.
        (db.assignments.name == assignment_name) &
        # Join to ``assignment_questions`` and from there to ``questions``.
        (db.assignments.id == db.assignment_questions.assignment_id) &
        (db.assignment_questions.question_id == db.questions.id)
    )

    return _query_questions(course_name, query_questions, due_date), time_zone_delta


# The XlsxWriter library returns 0 on success for many functions.
def _assert_0(value, string=''):
    assert value == 0, string


# Transform the ``grades`` struct into an Excel spreadsheet.
def _grades_to_xlsx(
    # The ``grades`` data structure returned from ``query_assignment``.
    grades,
    # The time zone delta to use to translate date to the local time.
    time_zone_delta,
    # The output file must end in ``.xlsx``, or Excel won't like it.
    output_file
):

    assert grades[None], 'No supported question types in this assignment.'

    # Save the grades as a worksheet.
    with xlsxwriter.Workbook(output_file, {
        # Student data (such as some answers) might look like a formula or URL, but it's not.
        'strings_to_formulas': False,
        'strings_to_urls': False
    }) as workbook:
        timestamp_sheet = workbook.add_worksheet('timestamps')
        score_sheet = workbook.add_worksheet('scores')
        answer_sheet = workbook.add_worksheet('answers')
        correct_sheet = workbook.add_worksheet('correct')
        attempts_sheet = workbook.add_worksheet('attempts')
        # Create formats for use in the export.
        date_format = workbook.add_format({'num_format': 'm/d/yy h:mm AM/PM'})
        percent_format = workbook.add_format({'num_format': '0%'})
        # Increase the column width of the timestamp sheet so the timestamps display.
        _assert_0(timestamp_sheet.set_column(4, 3 + len(grades[None]), 17))

        # Offsets to leave room for row and column headings.
        row_offset = 5
        col_offset = 5
        div_id_index_dict = {}
        # Add in titles for everything
        for sheet in workbook.worksheets():
            _assert_0(sheet.write(row_offset, 0, 'Last name'))
            _assert_0(sheet.write(row_offset, 1, 'First name'))
            _assert_0(sheet.write(row_offset, 2, 'E-mail'))
            _assert_0(sheet.write(row_offset, 3, 'User ID'))
            _assert_0(sheet.write(0, col_offset - 1, 'div_id'))
            _assert_0(sheet.write(1, col_offset - 1, 'chapter'))
            _assert_0(sheet.write(2, col_offset - 1, 'subchapter'))
            _assert_0(sheet.write(3, col_offset - 1, 'htmlsrc'))

            # Write out div_ids and create an index for it.
            for index, (div_id, question_info) in enumerate(six.iteritems(grades[None])):
                _assert_0(sheet.write(0, col_offset + index, div_id if six.PY3 else div_id.decode('utf-8')))
                _assert_0(sheet.write(1, col_offset + index, question_info.chapter if six.PY3 else question_info.chapter.decode('utf-8')))
                _assert_0(sheet.write(2, col_offset + index, question_info.subchapter if six.PY3 else question_info.subchapter.decode('utf-8')))
                _assert_0(sheet.write(3, col_offset + index, question_info.htmlsrc if six.PY3 else question_info.htmlsrc.decode('utf-8')))
                if sheet == score_sheet:
                    # This form of avergae counts blank cells as 0.
                    _assert_0(sheet.write_formula(4, col_offset + index, '{{=average(0 + {}:{})/{}}}'.format(xl_rowcol_to_cell(6, col_offset + index), xl_rowcol_to_cell(len(grades) + 4, col_offset + index), xl_rowcol_to_cell(5, col_offset + index)), percent_format))
                    # Record the index of this div_id.
                    div_id_index_dict[div_id] = col_offset + index
                    _assert_0(sheet.write(5, col_offset + index, question_info.points))
                if sheet == attempts_sheet:
                    _assert_0(sheet.write_formula(4, col_offset + index, '=average({}:{})'.format(xl_rowcol_to_cell(6, col_offset + index), xl_rowcol_to_cell(len(grades) + 4, col_offset + index))))

            # TODO: Compute the grade for each student on the score sheet.

            # Write out user info
            for index, (sid, div_id_dict) in enumerate(six.iteritems(grades)):
                if sid is None:
                    continue
                user_info = div_id_dict[None]
                _assert_0(sheet.write_string(row_offset + index, 0, user_info.last_name if six.PY3 else user_info.last_name.decode('utf-8')))
                _assert_0(sheet.write_string(row_offset + index, 1, user_info.first_name if six.PY3 else user_info.first_name.decode('utf-8')))
                _assert_0(sheet.write_string(row_offset + index, 2, user_info.email if six.PY3 else user_info.email.decode('utf-8')))
                _assert_0(sheet.write_string(row_offset + index, 3, sid if six.PY3 else sid.decode('utf-8')))

        _assert_0(score_sheet.write_string(4, col_offset - 1, 'Percent correct'))
        _assert_0(score_sheet.write_string(5, col_offset - 1, 'Max points'))
        _assert_0(attempts_sheet.write_string(4, col_offset - 1, 'Average attempts'))

        for sid_index, (sid, div_id_dict) in enumerate(six.iteritems(grades)):
            for div_id, grade_info in six.iteritems(div_id_dict):
                # Skip header info.
                if sid is None or div_id is None:
                    continue
                # It's safe to unpack the grade info after skipping headers (``None`` entries).
                timestamp, score, answer, correct, attempts = grade_info
                div_id_index = div_id_index_dict[div_id]
                # Make answers printable as necessary.
                if not isinstance(answer, six.string_types):
                    # Pretty print the answers, where newlines render as newlines, not ``\n``. See https://stackoverflow.com/a/42381643.
                    answer = pformat(answer).replace('\\n', '\n')
                # Provide local time in timestamps.
                if timestamp:
                    timestamp -= time_zone_delta
                row = row_offset + sid_index
                _assert_0(timestamp_sheet.write(row, div_id_index, timestamp, date_format))
                _assert_0(score_sheet.write(row, div_id_index, score))
                _assert_0(answer_sheet.write(row, div_id_index, answer))
                _assert_0(correct_sheet.write(row, div_id_index, correct))
                _assert_0(attempts_sheet.write(row, div_id_index, attempts))
