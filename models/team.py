# -*- coding: utf-8 -*-
#
# *************************************
# |docname| - various report generators
# *************************************
# This module provides supports for collecting team evaluations and generating reports from those evaluations. It also contains a report generator for assignments.
#
# Imports
# =======
# These are listed in the order prescribed by `PEP 8
# <http://www.python.org/dev/peps/pep-0008/#imports>`_.
#
# Standard library
# ----------------
from collections import namedtuple, defaultdict, OrderedDict
import csv
try:
    from pathlib import Path
except:
    from pathlib2 import Path
import json
from datetime import datetime, timedelta

# Third-party imports
# -------------------
import six

# Local application imports
# -------------------------
# None.


# Functions
# =========
# Given a CSV file containing a list of teams and the desired course, create two data structures to store team information for the given course only and return these.
def _load_teams(course_name):
    # Type: Dict[user_id: str, team_name: str]
    # This only supports one team per user_id and course_name.
    team_member = dict()
    # Type: Dict[team_name: str, OrderedDict[user_id: str, name: str]]
    team = defaultdict(OrderedDict)
    open_args = 'r' if six.PY3 else 'rb'
    with open(str(Path(request.folder, 'books', get_course_row().base_course, course_name + '.csv')), open_args) as csv_file:
        is_first_row = True
        for row in csv.reader(csv_file):
            assert len(row) == 3, 'Incorrect number of rows in "{}".'.format(','.join(row))
            user_id, user_name, team_name = row
            if not is_first_row and user_id == '' and user_name == '' and team_name == '':
                continue
            if is_first_row:
                is_first_row = False
                assert user_id == 'user id', 'Expected the first column of the first row to be "user id" instead of  "{}".'.format(user_id)
                assert user_name == 'user name', 'Expected the second column of the first row to be "user name" instead of "{}".'.format(user_name)
                assert team_name == 'team name', 'Expected the third column of the first row to be "team name" instead of "{}".'.format(team_name)
            else:
                # Add this user to the team.
                assert user_id not in team_member, 'Duplicate user ID {}.'.format(user_id)
                team_member[user_id] = team_name
                assert user_id not in team[team_name], 'Duplicate user ID {} in team {}.'.format(user_id, team_name)
                team[team_name][user_id] = user_name

    return team, team_member


# This returnes the team name for the given ``user_id`` and a list of team members/user IDs of the given ``user_id``.
def _get_team_members(user_id, team, team_member, is_list_of_names=True):
    # Identify the team of the given user.
    assert user_id in team_member, 'User ID {} not in list of team members.'.format(user_id)
    team_name = team_member[user_id]
    assert team_name in team, 'Team {} of user ID {} not in list of teams.'.format(team_name, user_id)
    this_team = team[team_name]

    # Extract only teammates of this user.
    teammate_member_list = [
        team_member_name if is_list_of_names else team_member_user_id
        for team_member_user_id, team_member_name in six.iteritems(this_team)
        if team_member_user_id != user_id
    ]

    return team_name, teammate_member_list


# Convert any exceptions into an error message, so the view can complete.
def get_team_members(user_id, course_name):
    try:
        team, team_member_list = _load_teams(course_name)
        return _get_team_members(user_id, team, team_member_list)
    except Exception as e:
        return 'Error: {}'.format(e), ["Error"]


# Grades query
# ============
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
## create index useinfo_course_id on useinfo (course_id);
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
    # Get information about each user_id.
    for row in db(
        (db.courses.course_name == course_name) &
        (db.courses.id == db.user_courses.course_id) &
        (db.user_courses.user_id == db.auth_user.id)
    ).select(
        db.auth_user.username,
        db.auth_user.first_name, db.auth_user.last_name,
        db.auth_user.email,
        orderby=db.auth_user.last_name | db.auth_user.first_name
    ):

        user_id = row.username
        grades[user_id] = dict()
        grades[user_id][None] = _UserInfo._make([row.first_name, row.last_name, row.email])

    # **body data query**
    #--------------------
    # Get information about each user_id/div_id combination.
    query = (
        # Choose seleted questions.
        query_questions &
        # Join them to ``useinfo``.
        (db.questions.name == db.useinfo.div_id) &
        # Select only this class.
        (db.useinfo.course_id == course_name)
    )

    # Define a query to select the newest (maximum) useinfo row for each unique set of (sid, div_id).
    timestamp_max = db.useinfo.timestamp.max()
    useinfo_max_query = (db.useinfo.course_id == course_name)
    # Include the due date in the query if it's provided.
    if due_date:
        useinfo_max_query &= (db.useinfo.timestamp <= due_date)
        query &= (db.useinfo.timestamp <= due_date)
    # Produce SQL for this query.
    useinfo_max_sql = db(useinfo_max_query)._select(
        db.useinfo.sid, db.useinfo.div_id, timestamp_max,
        # This selects the newest (max) ``useinfo.timestamp`` **for each record**. Note that any selected field must appear in the group by clause -- see https://blog.jooq.org/2016/12/09/a-beginners-guide-to-the-true-order-of-sql-operations/.
        groupby=db.useinfo.sid | db.useinfo.div_id
    )
    # Now, query this for the id of these useinfo records. This is required, since SQL can't select any fields outside of the groupby fields, and adding additional fields causes the max not to work.
    newest_useinfo_ids = (
        'select useinfo.id from useinfo, (' +
        # Omit the closing semicolon from the previous query to use it as a subquery.
        useinfo_max_sql[:-1] +
        ') u where '
            'u.sid=useinfo.sid and '
            'u.div_id=useinfo.div_id;'
    )
    # Use this id to limit the query.
    for row in db(query & (db.useinfo.id.belongs(newest_useinfo_ids))).select(
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
    for row in db(query).select(
        db.useinfo.sid, db.useinfo.div_id, attempts,
        groupby=db.useinfo.sid | db.useinfo.div_id,
    ):
        grades[row.useinfo.sid][row.useinfo.div_id].append(row[attempts])

    return grades


# Team reports
# ============
# Transform data from a team evaluation into a report.
#
# Globals
# -------
NO_DATA = 'No data'


# EvalData
# --------
# A class to hold data about each evaluation. Attributes containing tuples are indexed by ``teammate_netids``. TODO: these are actually teammate e-mail addresses. Update this!
#
# - name: str
# - teammate_netids: (netid0, ...)
class EvalData:
    def __init__(self, name, teammate_netids):
        self.name = name
        self.teammate_netids = teammate_netids

    def __repr__(self):
        return '<team.EvalData instance, name={}, teammate_netids={}'.format(repr(self.name), repr(self.teammate_netids))


# TeamData
# --------
# A class to collect data about each team. Tuples are indexed by team_netids.
class TeamData:
    def __init__(self, grades, eval_data_dict, team_netids):
        self.grades = grades
        self.eval_data_dict = eval_data_dict
        self.team_netids = team_netids
        self.collected_response = set()

    def __repr__(self):
        return '<team.TeamData instance, team_netids={}>'.format(repr(self.team_netids))

    # Given a key and one or move div_ids, store data in ``eval_data_dict`` using that key.
    def collect_responses(self, key, *args, **kwargs):
        average = kwargs.get('average', False)

        # If we've already done the work, simply return the key from last time.
        if args not in self.collected_response:
            self.collected_response.add(args)

            # Walk through all grades with these div_ids and put them in eval_data.
            for user_id, div_id_dict in six.iteritems(self.grades):
                # Ignore info about each user.
                if user_id is None:
                    continue
                responses = []
                for arg in args:
                    # Get this user's response (index 2) for the provided div_id.
                    response = div_id_dict.get(arg, [None]*3)[2]
                    # Fill-in-the-blank questions return a list; others don't. Convert non-lists into a single-element list, then add all list elements. This supports multi-blank fitb questions.
                    responses.extend(
                        response if isinstance(response, list) else [response]
                    )
                # Transform the user_id into an e-mail, which is how eval_data_dict is addressed.
                email = self.grades[user_id][None].email
                # Discard responses for undefined team members
                responses = responses[:len(self.eval_data_dict[email].teammate_netids)]
                # Normalize data to be averaged.
                if average:
                    responses = normalize_grades(responses)
                setattr(self.eval_data_dict[email], key, responses)

        return key

    # Produce a list of the eval_data.key for all team members.
    def list_(self, *args):
        key = self.collect_responses(*args)
        names = [getattr(self.eval_data_dict[x], key, NO_DATA) for x in self.team_netids]
        names_li = ''.join(['  <li>{}</li>\n'.format(name) for name in names])
        return XML('<ul>\n{}</ul>\n\n'.format(names_li))

    # Produce a table of eval_data.name, eval_data.key for all team members.
    def table(self, *args):
        key = self.collect_responses(*args)
        html_table = HtmlTableMaker()
        for x in self.team_netids:
            html_table.add_data(
                self.eval_data_dict[x].name,
                *getattr(self.eval_data_dict[x], key, [NO_DATA])
            )
        return html_table.to_html()

    # Produce a table of eval_data.key for each member about each team member.
    def grid(self, *args, **kwargs):
        average = kwargs.get('average', False)
        key = self.collect_responses(*args, **kwargs)
        html_table = HtmlTableMaker()
        # Print a title of names of each team member
        html_table.add_header(
            u'Evaluator→<br>↓Evaluatee↓',
            *(
                [self.eval_data_dict[x].name for x in self.team_netids] +
                (['Average', 'Delta'] if average else [])
            )
        )

        # Produce each row of the table.
        for x in self.team_netids:
            # Look up the values that team member x reported about team member y.
            vals = [self.teammate(y, x, key) for y in self.team_netids]
            if average:
                good_vals = [_ for _ in vals if isinstance(_, float)]
                if not good_vals:
                    # If no other team members provided an evaluation, and this is the average evalution for the one person on the team who provided data, provide a value of 100% as a placeholder.
                    vals.append(100.0)
                else:
                    vals.append(sum(good_vals) / (len(good_vals)))
                # Save the average for this user.
                setattr(self.eval_data_dict[x], key + '_average', vals[-1])
                # Save this normalized delta. This is :math:`\frac{actual - expected}{expected} \cdot 100 = \left( \frac{actual}{expected} - 1 \right) \cdot 100`, where ``actual = vals[-1]``, :math:`expected = \frac{1}{\# teammates - 1} \cdot 100`, and ``#teammates = len(self.teammates)``.
                delta = (vals[-1]/(1.0/(len(self.team_netids) - 1.0)*100.0) - 1.0)*100.0
                setattr(self.eval_data_dict[x], key + '_delta', delta)
                vals.append(delta)
                # Format nicely.
                vals = ['{:.1f}%'.format(_) if isinstance(_, float) else _ for _ in vals]
            html_table.add_data(self.eval_data_dict[x].name, *vals)
        return html_table.to_html()


    # Look up the value in key that netid reported about teammate_netid.
    def teammate(self, netid, teammate_netid, key):
        # There are no self-evaluations.
        if netid == teammate_netid:
            return ''
        # If students don't submit an evaluation, return NO_DATA.
        eval_data = self.eval_data_dict[netid]
        try:
            index = eval_data.teammate_netids.index(teammate_netid)
            return getattr(eval_data, key)[index]
        except (ValueError, IndexError, AttributeError):
            return NO_DATA


def grades_table(team_data_dict, *args):
    html_table = HtmlTableMaker()
    eval_data_attr_list = ['name']
    for arg in args:
        eval_data_attr_list += [arg + '_average', arg + '_delta']
    html_table.add_header('e-mail', 'team', *eval_data_attr_list)
    # Sort this by team, then by last name, first name. Easy -- this is the order that team_data_dict is already in!
    for team_name, team_data in six.iteritems(team_data_dict):
        eval_data_dict = team_data.eval_data_dict
        for email in team_data.team_netids:
            html_table.add_data(
                email, team_name,
                *[getattr(eval_data_dict[email], eval_data_attr, NO_DATA)
                  for eval_data_attr in eval_data_attr_list]
            )
    return html_table.to_html()


# A class to generate simple HTML tables.
class HtmlTableMaker(object):
    def __init__(self):
        self.l = [u'<table class="table" style="white-space: pre-wrap;">\n']
        self.has_body_tag = False

    # This optional method must be called only once, before ``add_data``.
    def add_header(self, *args):
        self.l.append((
            u'  <thead>\n' +
            '    <tr>\n' +
            ('      <th>{}</th>\n' * (len(args))) +
            '    </tr>\n'
            '  </thead>\n'
            '  <tbody>\n'
        ).format(*args))
        self.has_body_tag = True

    def add_data(self, *args):
        if not self.has_body_tag:
            self.has_body_tag = True
            self.l.append(u'  <tbody>\n')
        self.l.append((
            u'    <tr>\n' +
            ('      <td>{}</td>\n' * (len(args))) +
            '    </tr>\n'
        ).format(*args))

    def to_html(self):
        self.l.append(u'  </tbody>\n</table>')
        return XML(u''.join(self.l))


# team_report
# -----------
# Build the data structures needed to produce a team report.
def team_report(
    # The subchapter name containing the evaluation. Simply remove ``.rst`` from the filename -- ``team_evaluation_1.rst`` has a subchapter_name of ``team_evaluation_1``.
    subchapter_name,
    # The course name.
    course_name
):

    team, team_member = _load_teams(course_name)
    grades = _query_questions(
        course_name,
        (db.questions.chapter == request.args[-2]) &
        # TODO: Use something like request.args[-1][:-5] (this takes the ``.html`` extension off the subchapter name), but renamed for the eval document, not this document. Or include the report at the bottom of the eval?)
        (db.questions.subchapter == subchapter_name) &
        (db.questions.base_course == get_course_row().base_course)
    )

    # Type: Dict[net_id: str, eval_data: EvalData].
    eval_data_dict = {
        user_id: EvalData(team[team_name][user_id], _get_team_members(user_id, team, team_member, False)[1])
        for user_id, team_name in six.iteritems(team_member)
    }
    # Type: OrderedDict[team_name: str, team_data: TeamData].
    # The dict is sorted by team name.
    team_data_dict = OrderedDict()
    for team_name in sorted(six.iterkeys(team)):
        # Create the struct [[netid, first_name, last_name], ...]
        ##                     [0]      [1]         [2]
        team_struct = [[userid] + name.split()
                       for userid, name in six.iteritems(team[team_name])]
        team_data_dict[team_name] = TeamData(
            grades, eval_data_dict,
            # Sort it by last name then first name.
            [x[0] for x in sorted(team_struct, key=lambda x: (x[2], x[1]) if len(x) >=3 else x[1])]
        )

    return eval_data_dict, team_data_dict, grades


# Utilities
# =========
def to_float(_str):
    try:
        return float(_str)
    except:
        return 0


# Normalize student grades.
def normalize_grades(grades_str):
    grades = [to_float(x) for x in grades_str]
    grades_sum = sum(grades)
    if grades_sum != 0:
        return [grade/grades_sum*100 for grade in grades]
    else:
        return [NO_DATA for grade in grades]


# Make a list of sequentially numbered strings. For example, ``str_array('foo', 3)`` produces ``['foo0', 'foo1', 'foo2']``.
def str_array(
    # The string prefix for the array.
    prefix_str,
    # These parameters are passed to `range <https://docs.python.org/3/library/stdtypes.html#range>`_, and each resulting value appended to the ``prefix_str``.
    *range_args
):
    return [prefix_str + str(index) for index in range(*range_args)]
