import datetime

def pct2pts(x):
    return "%.2f" % (100*x)

class AssignmentGrade(object):
    """Grade of one user for one assignment"""
    def __init__(self, released, score, projected, assignment_score, assignment_id, assignment_name, grade_record, row):
        self.released = released
        self.score = score
        self.projected = projected
        try:
            self.assignment_score = int(assignment_score)
        except:
            self.assignment_score = 0
        self.assignment_id = assignment_id
        self.assignment_name = assignment_name
        self.grade_record = grade_record
        self.db_row = row

    def points(self, projected = False, potential = False):
        # potential gives max points for the assignment
        # projected gives actual score if it's been released, else projected
        actual = None
        if potential:
            return self.assignment_score
        elif self.released:
            return self.score
        elif projected:
            if self.projected:
                return self.projected
            else:
                return 0
        else:
            return 0

    def csv(self, row, type_name, assignment_names):
        # add values to row dictionary and field names to lists as needed
        name = type_name + '_' + self.assignment_name
        if name not in assignment_names:
            assignment_names.append(name)
        row[name] = self.points()


class AssignmentTypeGrade(object):
    """Grade of one user for a collection of assignments,"""
    def __init__(self, assignment_type, user=None, course=None):
        self.assignments = []
        self.name = assignment_type.name
        self.grade_type = assignment_type.grade_type

        try:
            self.weight = assignment_type.weight
        except:
            self.weight = 0
        try:
            self.possible = assignment_type.points_possible
        except:
            self.possible = 0
        try:
            self.assignments_count = int(assignment_type.assignments_count)
        except:
            self.assignments_count = 0
        try:
            self.assignments_dropped = int(assignment_type.assignments_dropped)
        except:
            self.assignments_dropped = 0

        assignments = db((db.assignments.course == course.id)
                         & (db.assignments.assignment_type == assignment_type.id)
                         ).select(orderby = db.assignments.name)

        for row in assignments:
            # get or create the grade object for this user for this assignment row
            grade = db.grades((db.grades.assignment == row.id) & (db.grades.auth_user == user.id))
            if not grade:
                db.grades.insert(auth_user = user.id,
                                 assignment = row.id,
                                 score = 0,
                                 projected = 0)
            grade = db.grades((db.grades.assignment == row.id) & (db.grades.auth_user == user.id))
            # add the AssignmentGrade to t
            self.assignments.append(AssignmentGrade(row.released, grade.score, grade.projected, row.points, row.id, row.name, grade, row))

    def points(self, projected = False, potential = False):
        vals = [a.points(projected, potential) for a in self.assignments]
        vals.sort()
        # drop the self.assignments_dropped lowest values
        return sum(vals[self.assignments_dropped:])

    def csv(self, row, type_names, assignment_names):
        # add values to row dictionary and field names to lists as needed
        if self.name not in type_names:
            type_names.append(self.name)
        row[self.name] = self.points()
        for a in self.assignments:
            a.csv(row, self.name, assignment_names)


class CourseGrade(object):
    def __init__(self, user, course, assignment_types):
        self.assignment_type_grades = [AssignmentTypeGrade(t, user, course) for t in assignment_types]
        self.student = user
        self.course = course


    def points(self, projected = False, potential = False):
        return sum([t.points(projected, potential) or 0 for t in self.assignment_type_grades])

    def csv(self, type_names, assignment_names, as_of_timestamp=None):
        # pass the row dictionary and fields_names into the csv method for the components, which will accumulate extra values and field names
        row = {}
        row['Lastname']= self.student.last_name
        row['Firstname']= self.student.first_name
        row['Email']= self.student.email
        row['Total']= self.points()
        if 'NonPS Seconds' not in type_names:
            type_names.append('NonPS Seconds')
        row['NonPS Seconds'] = get_engagement_time(assignment=None,
                                                   user=self.student,
                                                   preclass=False,
                                                   all_non_problem_sets=True,
                                                   as_of_timestamp=as_of_timestamp)
        if 'PS Seconds' not in type_names:
            type_names.append('PS Seconds')
        if 'Earliness' not in type_names:
            type_names.append('Earliness')
        (row['PS Seconds'],
         row['Earliness'],
         assignment_specific_data) = get_engagement_time(assignment=None,
                                                         user=self.student,
                                                         preclass=False,
                                                         all_problem_sets=True,
                                                         as_of_timestamp=as_of_timestamp)
        for assignment, v in assignment_specific_data.items():
            if str(assignment) + '_Duration' not in type_names:
                type_names.append(str(assignment) + '_Duration')
            if str(assignment) + '_Earliness' not in type_names:
                type_names.append(str(assignment) + '_Earliness')
            row[str(assignment) + '_Duration'] = v['total_duration']
            row[str(assignment) + '_Earliness'] = v['earliness']

        for t in self.assignment_type_grades:
            t.csv(row, type_names, assignment_names)
        return row


db.define_table('assignment_types',
    Field('name', 'string'),
    Field('grade_type', 'string', default="additive", requires=IS_IN_SET(['additive', 'checkmark', 'use'])),
    Field('weight', 'double', default=1.0),
    Field('points_possible','integer', default=0),
    Field('assignments_count', default=0),
    Field('assignments_dropped', default=0),
    format='%(names)s',
    migrate='runestone_assignment_types.table',
    )


db.define_table('assignments',
    Field('course', db.courses),
    Field('assignment_type', db.assignment_types,
          requires=IS_EMPTY_OR(IS_IN_DB(db, 'assignment_types.id', '%(name)s'))), # DEPRECATED, every assignment can
                                                                                  # include reading portion and
                                                                                  # questions portion
    Field('name', 'string'),
    Field('points', 'integer'),  # max possible points on the assignment, cached sum of assignment_question points
    Field('threshold_pct', 'float'), # threshold required to qualify for maximum points on the assignment; null means use actual points
    Field('released', 'boolean'),
    Field('description', 'text'),
    Field('duedate','datetime'),
    Field('visible','boolean'),
    format='%(name)s',
    migrate='runestone_assignments.table'
    )

class score(object):
    def __init__(self, acid=None, points=0, comment="", user=None):
        self.acid = acid
        self.user = user
        self.points = points
        if type(self.points) not in [float, int]:
            # would be nice to flag error here
            self.points = 0
        self.comment = comment

    def truncated_acid(self):
        if "/" in self.acid:
            # DictionaryAccumulation/AccumulatingtheBestKey.html replaces
            # /runestone/static/f15/DictionaryAccumulation/AccumulatingtheBestKey.html
            parts = self.acid.split("/")
            return "/".join(parts[-2:])
        else:
            return self.acid

def canonicalize(div_id):
    # needs to take a parameter for which book; hardcoded for pip2 right now
    # used in calculating time spent for grading "use" assignment types
    if ".html" in div_id:
        full_url = div_id
        # return canonical url, without #anchors
        if full_url.rfind('#') > 0:
            full_url = full_url[:url.rfind('#')]
        full_url = full_url.replace('/runestone/static/pip2/', '')
        return full_url
    else:
        return div_id
class Session(object):
    def __init__(self, start, end = None, assignment = None):
        self.start = start
        self.end = end
        self.count = 1
        self.assignment = assignment

def get_deadline(assignment, user):
    section = section_users(db.auth_user.id == user.id).select(db.sections.ALL).first()
    q = db(db.deadlines.assignment == assignment.id)
    if section:
        q = q((db.deadlines.section == section.id) | (db.deadlines.section==None))
    else:
        q = q(db.deadlines.section==None)
    dl = q.select(db.deadlines.ALL, orderby=db.deadlines.section).first()
    if dl:
        return dl.deadline  #a datetime object
    else:
        return None


def get_engagement_time(assignment, user, preclass=False, all_problem_sets=False, all_non_problem_sets=False,
                        as_of_timestamp=None):
    q = db(db.useinfo.sid == user.username)
    if all_problem_sets:
        # In order to get the deadline for each assignment, we join useinfo and questions.
        q = q((db.useinfo.div_id.startswith('ps_')) &
               (db.useinfo.div_id == db.questions.name) &
               (db.assignment_questions.question_id == db.questions.id) &
               (db.assignment_questions.assignment_id == db.assignments.id))

    elif all_non_problem_sets:
        q = q(~(db.useinfo.div_id.contains('Assignments') |
                db.useinfo.div_id.startswith('ps_')))
    else:
        q = q(db.useinfo.div_id == db.problems.acid)(db.problems.assignment == assignment.id)
        if preclass:
            dl = get_deadline(assignment, user)
            if dl:
                q = q(db.useinfo.timestamp < dl)
    if as_of_timestamp:
        q = q(db.useinfo.timestamp < as_of_timestamp)

    if all_problem_sets:
        activities = q.select(db.useinfo.timestamp, db.assignments.duedate, db.assignments.name,
                              orderby=db.useinfo.timestamp)
        # We want to define a variable that measures how early each student works on their assignments. We suppose this
        # measure as the inverse of a measurement of procrastination. For this purpose, we need to find the first, last,
        # and all the timestamps that the student worked on each assignment.
        assignment_specific_data = {}
    else:
        activities = q.select(db.useinfo.timestamp, orderby=db.useinfo.timestamp)

    sessions = []
    THRESH = 300
    prev = None
    new_session_created = False
    for activity in activities:
        if all_problem_sets:
            timestamp = activity.useinfo.timestamp
        else:
            timestamp = activity.timestamp
        if not prev:
            # first activity; start a session for it
            sessions.append(Session(timestamp))
            new_session_created = True
        else:
            if all_problem_sets:
                prev_timestamp = prev.useinfo.timestamp
            else:
                prev_timestamp = prev.timestamp
            if (timestamp - prev_timestamp).total_seconds() > THRESH:
                # close previous session; set its end time be previous activity's time, plus THRESH seconds
                sessions[-1].end = prev_timestamp + datetime.timedelta(seconds=THRESH)
                # start a new session
                sessions.append(Session(timestamp))
                new_session_created = True

        if all_problem_sets:
            deadline = activity.assignments.duedate
            assignment_name = activity.assignments.name
            if timestamp <= deadline:
                # Use assignment name as key.
                if assignment_name not in assignment_specific_data:
                    assignment_specific_data[assignment_name] = {'first': timestamp,
                                                                 'last': timestamp,
                                                                 'visits': [timestamp],
                                                                 'durations': [],
                                                                 'deadline': deadline}
                else:
                    # We need to find the first, last, and all the timestamps timestamps that the student worked on
                    # each assignment.
                    assignment_specific_data[assignment_name]['visits'].append(timestamp)
                    if timestamp < assignment_specific_data[assignment_name]['first']:
                        assignment_specific_data[assignment_name]['first'] = timestamp
                    if assignment_specific_data[assignment_name]['last'] < timestamp <= deadline:
                        assignment_specific_data[assignment_name]['last'] = timestamp
                    if new_session_created:
                        assignment_specific_data[assignment_name]['durations'].append(THRESH)

        prev = activity

    if prev:
        if all_problem_sets:
            prev_timestamp = prev.useinfo.timestamp
        else:
            prev_timestamp = prev.timestamp
        # close out last session
        sessions[-1].end = prev_timestamp + datetime.timedelta(seconds=THRESH)

    total_time = sum([(s.end-s.start).total_seconds() for s in sessions])

    if all_problem_sets:
        # We define the variable earliness that measures how early each student works on their assignments. We suppose
        # this measure as the inverse of a measurement of procrastination and we calculate it as the difference between
        # the deadline and mean of all the timestamps before the deadline that they worked on the assignment.
        # Add up over all assignments; students who miss an assignment get 0 earliness for it.
        earliness = 0
        for assignment, v in assignment_specific_data.items():
            average_delta = 0
            for timestamp in v['visits']:
                if v['deadline'] > timestamp:
                    average_delta += (v['deadline'] - timestamp).total_seconds()
            average_delta /= len(v['visits'])
            assignment_specific_data[assignment]['earliness'] = average_delta/float(3600)
            earliness += average_delta

            assignment_specific_data[assignment]['total_duration'] = sum(v['durations'])/float(3600)

        # Finally, divide the earliness by the number of assignments, so that earliness does not depend on the number of
        # submitted assignments.
        if len(assignment_specific_data) != 0:
            earliness /= len(assignment_specific_data)
        return total_time, earliness/float(3600), assignment_specific_data

    return total_time


def assignment_get_use_scores(assignment, problem=None, user=None, section_id=None, preclass=True):
    scores = []
    if problem and user:
        pass
    elif problem:
        pass
    elif user:
        q =  db(db.useinfo.div_id == db.problems.acid)(db.problems.assignment == assignment.id)(db.useinfo.sid == user.username)
        if preclass:
            dl = get_deadline(assignment, user)
            if dl:
                q = q(db.useinfo.timestamp < dl)
        attempted_problems = q.select(db.problems.acid)
        for problem in db(db.problems.assignment == assignment.id).select(db.problems.acid):
#            if ".html" in problem.acid:
#                # don't include opening the page as a problems they can attempt or not;
#                # they are included as problems so that total time on session prep
#                # is calculated correctly
#                continue
            matches = [x for x in attempted_problems if x.acid == problem.acid]
            points = 0
            if len(matches) > 0:
                points = 1
            scores.append(score(
                points = points,
                acid = problem.acid,
                user = user,
                ))
    else:
        pass
    return scores

def get_all_times_and_activity_counts(course):
    ## get mapping from problem names (divids) to assignments, and count of problems per assignment
    p2a = {}
    act_per_ass = {}
    deadlines = {}
    for p in db(db.assignment_types.id == db.assignments.assignment_type)(db.assignment_types.grade_type == 'use')(db.problems.assignment == db.assignments.id).select():
        p2a[canonicalize(p.problems.acid)] = p.assignments.id
        act_per_ass[p.assignments.id] = act_per_ass.get(p.assignments.id, 0) + 1
    def times(assignment, pre_deadline=False):
        sessions = assignment['sessions']
        if pre_deadline and 'deadline' in assignment and assignment['deadline']:
            dl = assignment['deadline']
            sessions = [s for s in sessions if s.start < dl]
        return sum([(s.end-s.start).total_seconds() for s in sessions])
    def count(assignment, pre_deadline=False):
        acts = assignment['activities'].values()
        if pre_deadline and 'deadline' in assignment and assignment['deadline']:
            dl = assignment['deadline']
            acts = [a for a in acts if a < dl]
        return len(acts)
    def name(assignment_id):
        return db.assignments(assignment_id).name
    def get_deadline(assignment_id, user_id):
        section = section_users(db.auth_user.registration_id == user_id).select(db.sections.ALL).first()
        q = db(db.deadlines.assignment == assignment_id)
        if section:
            q = q((db.deadlines.section == section.id) | (db.deadlines.section==None))
        else:
            q = q(db.deadlines.section==None)
        dl = q.select(db.deadlines.ALL, orderby=db.deadlines.section).first()
        if dl:
            return dl.deadline  #a datetime object
        else:
            return None
    class User_data:
        def __init__(self, user_id):
            self.user_id = user_id
            self.assignments = {}
            ## {'assignment_id' : {'deadline': datetime, 'sessions' : [instances of Session], 'activities': {div_id: datetime}}}
        def add_session(self, s, div_id):
            a = p2a[div_id]
            if a not in self.assignments:
                self.assignments[a] = {'sessions': [], 'activities': {}, 'deadline': get_deadline(a, self.user_id)}
            self.assignments[a]['sessions'].append(s)
        def add_activity(self, div_id, timestamp):
            a = p2a[div_id]
            if a not in self.assignments:
                self.assignments[a] = {'sessions': [], 'activities': {}, 'deadline': get_deadline(a, self.user_id)}
            if div_id not in self.assignments[a]['activities']:
                self.assignments[a]['activities'][div_id] = timestamp
        def csv_dict(self):
            ret = {}
            ret['user_id'] = self.user_id
            for a in self.assignments:
                nm = name(a)
                ret[nm+"_time"] = times(self.assignments[a])
                ret[nm+"_time_pre_deadline"] = times(self.assignments[a], pre_deadline=True)
                ret[nm+"_activities"] = count(self.assignments[a])
                ret[nm+"_activities_pre_deadline"] = count(self.assignments[a], pre_deadline=True)
                ret[nm+"_max_act"] = act_per_ass[a]
            return ret

    students = db(db.auth_user.course_id == course.id).select(db.auth_user.registration_id, db.auth_user.username)
    all_user_data = {}
    for student in students:
        curr_user = User_data(student.registration_id)
        ## get all use scores and times for this user
        rows = db(db.useinfo.sid == student.username).select(orderby=db.useinfo.timestamp)
        curr_session = None
        prev_row = None
        THRESH = 600
        for row in rows:
            div_id = canonicalize(row.div_id)
            if div_id not in p2a:
                continue  # ignore activities that aren't associated with any assignment
            curr_user.add_activity(div_id, row.timestamp)
            if curr_session: # see whether to continue it or close it
                if curr_session.assignment == p2a[div_id] and (row.timestamp - prev_row.timestamp).total_seconds() < THRESH:
                    # continue current session if same assignment and not too much time has passed since last activity
                    pass
                else:
                    # close previous session
                    curr_session.end = prev_row.timestamp + datetime.timedelta(seconds=30)
                    curr_session = None
            if not curr_session:
                # start a new one and add it to sessions list for that assignment for current user
                curr_session = Session(row.timestamp, assignment = p2a[div_id])
                curr_user.add_session(curr_session, div_id)
            prev_row = row
        if curr_session and not curr_session.end:
            # close very last session
            curr_session.end = prev_row.timestamp + datetime.timedelta(seconds=30)
        all_user_data[curr_user.user_id] = curr_user.csv_dict()
    return all_user_data

def partition(L, f):
    # make a new list when f(item) changes
    cur_list = []
    prev_item = None
    Ls = [cur_list]
    for cur_item in L:
        if (not prev_item) or (f(prev_item) == f(cur_item)):
            cur_list.append(cur_item)
        else:
            cur_list = [cur_item]
            Ls.append(cur_list)
        prev_item = cur_item
    return Ls

def extract_last_grades(L, f):
    return [L[-1] for L in partition(L, f) if len(L) > 0]

def assignment_get_scores(assignment, problem=None, user=None, section_id=None, preclass=True):
    assignment_type = db(db.assignment_types.id == assignment.assignment_type).select().first()
    if assignment_type and assignment_type.grade_type == 'use':
        return assignment_get_use_scores(assignment, problem, user, section_id, preclass)
    scores = []
    if problem and user:
        pass
    elif problem:
        # get grades for this acid for all users
        grades = db(
            (db.question_grades.course_name == auth.user.course_name) &
            (db.question_grades.div_id == problem)).select(
            db.question_grades.ALL
        )
        scores = [score(
            points = g.score,
            comment = g.comment,
            acid = problem,
            user = auth.user.id
        ) for g in grades]
        # grades = db(db.code.sid == db.auth_user.username)(db.code.acid == problem).select(
        #     db.code.ALL,
        #     db.auth_user.ALL,
        #     orderby= db.code.sid | db.code.id
        #     )
        # # keep only last grade for each user (for this problem)
        # last_grades = extract_last_grades(grades, lambda g: g. auth_user.id)
        # for g in last_grades:
        #     scores.append(score(
        #         points=g.code.grade,
        #         comment= g.code.comment,
        #         acid=problem,
        #         user=g.auth_user,
        #         ))
    elif user:
        # get grades for individual components of this assignment
        grades = db(
            (db.question_grades.course_name == auth.user.course_name) &
            (db.question_grades.sid == user.username) &
            (db.question_grades.div_id == db.questions.name) &
            (db.assignment_questions.question_id == db.questions.id) &
            (db.assignment_questions.assignment_id == assignment.id)
        ).select(
            db.question_grades.score,
            db.question_grades.comment,
            db.question_grades.div_id,
            db.assignment_questions.points,
            orderby = db.assignment_questions.id
        )
        scores = [score(
            points = g.score,
            comment = g.comment,
            acid = g.div_id,
            user = auth.user.id
        ) for g in grades]
        #
        #
        # q = db(db.problems.acid == db.code.acid)
        # q = q(db.problems.assignment == assignment.id)
        # q = q(db.code.sid == user.username)
        # grades = q.select(
        #    db.code.acid,
        #    db.code.grade,
        #    db.code.comment,
        #    db.code.timestamp,
        #    orderby = db.code.acid | db.code.id
        #    )
        # # keep only last grade for each problem (for this user)
        # last_grades = extract_last_grades(grades, lambda g: g.acid)
        # for g in last_grades:
        #     scores.append(
        #         score(
        #            points=g.grade,
        #            comment=g.comment,
        #            acid=g.acid,
        #            user=user
        #         ))
    else:
        # for all users: grades for all assignments, not for individual problems
        grades = db(db.grades.assignment == assignment.id).select(db.grades.ALL)
        for g in grades:
            scores.append(score(
                points=g.score,
                user=g.auth_user,
                ))
    return scores
db.assignments.scores = Field.Method(lambda row, problem=None, user=None, section_id=None, preclass=True: assignment_get_scores(row.assignments, problem, user, section_id, preclass))
db.assignments.time = Field.Method(lambda row, user=None, preclass=True: get_engagement_time(row.assignments, user, preclass))

def assignment_set_grade(assignment, user):
    # delete the old grades; we're regrading
    db(db.grades.assignment == assignment.id)(db.grades.auth_user == user.id).delete()

    assignment_type = db(db.assignment_types.id == assignment.assignment_type).select().first()
    if not assignment_type:
        # if we don't know how to grade this assignment, don't grade the assignment.
        return 0

    points = 0.0
    if assignment_type.grade_type == 'use':
        checks = len([p for p in assignment_get_scores(assignment, user=user, preclass=True) if p.points > 0])
        time = get_engagement_time(assignment, user, preclass=True)
        if checks >= assignment.threshold or time > 20*60:
            # if enough checkmarks or enough time
            # should be getting minimum time from a field of the assignment as well: FUTURE WORK
            points = assignment.points
        else:
            points = 0
    elif assignment_type.grade_type == 'checkmark':
        checks = sum([p.points for p in assignment.scores(user=user) if p.points])
        # threshold grade
        if checks >= assignment.threshold:
            points = assignment.points
        else:
            points = 0
    else:
        # they got the points they earned
        points = sum([p.points for p in assignment.scores(user=user)])

    db.grades.insert(
        auth_user=user.id,
        assignment=assignment.id,
        score=points,
        )
    return points
db.assignments.grade = Field.Method(lambda row, user: assignment_set_grade(row.assignments, user))

def assignment_release_grades(assignment, released=True):
    # update problems
    assignment.released = True
    assignment.update_record()
    return True
db.assignments.release_grades = Field.Method(lambda row, released=True: assignment_release_grades(row.assignments, released))


# now deprecated; use the new questions table in questions.py
db.define_table('problems',
    Field('assignment', db.assignments),
    Field('acid', 'string'),
    migrate='runestones_problems.table',
    )

db.define_table('grades',
    # This table records grades on whole assignments, not individual questions
    Field('auth_user', db.auth_user),
    Field('assignment', db.assignments),
    Field('score', 'double'),
    Field('manual_total', 'boolean'),
    Field('projected', 'double'),
    Field('lis_result_sourcedid', 'string'), # guid for the student x assignment cell in the external gradebook
    Field('lis_outcome_url', 'string'), #web service endpoint where you send signed xml messages to insert into gradebook; guid above will be one parameter you send in that xml; the actual grade and comment will be others
    migrate='runestone_grades.table',
    )

db.define_table('practice_grades',
                Field('auth_user', db.auth_user),
                Field('course_name', 'string'),
                Field('score', 'double'),
                Field('lis_result_sourcedid', 'string'),
                # guid for the student x assignment cell in the external gradebook
                Field('lis_outcome_url', 'string'),
                # web service endpoint where you send signed xml messages to insert into gradebook; guid above will be one parameter you send in that xml; the actual grade and comment will be others
                migrate='runestone_practice_grades.table',
                )

# deprecated; now storing deadlines directly in assignments table, so no separate deadlines for different sections
db.define_table('deadlines',
    Field('assignment', db.assignments, requires=IS_IN_DB(db, 'assignments.id', db.assignments._format)),
    Field('section', db.sections, requires=IS_EMPTY_OR(IS_IN_DB(db, 'sections.id', '%(name)s'))),
    Field('deadline', 'datetime'),
    migrate='runestone_deadlines.table',
    )

db.define_table('question_grades',
    # This table records grades on individual gradeable items
    Field('sid', type='string', notnull=True),
    Field('course_name',type='string', notnull=True),
    Field('div_id', type = 'string', notnull=True),
    Field('useinfo_id', db.useinfo), # the particular useinfo run that was graded
    Field('deadline', 'datetime'),
    Field('score', type='double'),
    Field('comment', type ='text'),
    migrate='runestone_question_grades.table',
    )
