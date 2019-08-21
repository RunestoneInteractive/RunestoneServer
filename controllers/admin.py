import signal
from os import path
import os
import datetime
from random import randint
from collections import OrderedDict
from paver.easy import sh
import json
from runestone import cmap
from rs_grading import send_lti_grades
from dateutil.parser import parse
import pandas as pd

import logging

logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)


ALL_AUTOGRADE_OPTIONS = ['manual', 'all_or_nothing', 'pct_correct', 'interact']
AUTOGRADE_POSSIBLE_VALUES = dict(
    clickablearea=['manual', 'all_or_nothing', 'interact'],
    external=[],
    fillintheblank=ALL_AUTOGRADE_OPTIONS,
    activecode=ALL_AUTOGRADE_OPTIONS,
    actex=ALL_AUTOGRADE_OPTIONS,
    dragndrop=['manual', 'all_or_nothing', 'interact'],
    shortanswer=ALL_AUTOGRADE_OPTIONS,
    mchoice=ALL_AUTOGRADE_OPTIONS,
    codelens=ALL_AUTOGRADE_OPTIONS,
    parsonsprob=ALL_AUTOGRADE_OPTIONS,
    video=['interact'],
    youtube=['interact'],
    poll=['interact'],
    page=['interact'],
    showeval=['interact'],
    lp_build=ALL_AUTOGRADE_OPTIONS,
    reveal = []
)

ALL_WHICH_OPTIONS = ['first_answer', 'last_answer', 'best_answer']
WHICH_TO_GRADE_POSSIBLE_VALUES = dict(
    clickablearea=ALL_WHICH_OPTIONS,
    external=[],
    fillintheblank=ALL_WHICH_OPTIONS,
    activecode=ALL_WHICH_OPTIONS,
    actex=ALL_WHICH_OPTIONS,
    dragndrop=ALL_WHICH_OPTIONS,
    shortanswer=ALL_WHICH_OPTIONS,
    mchoice=ALL_WHICH_OPTIONS,
    codelens=ALL_WHICH_OPTIONS,
    parsonsprob=ALL_WHICH_OPTIONS,
    video=[],
    youtube=[],
    poll=[],
    reveal=[],
    showeval=ALL_WHICH_OPTIONS,
    page=ALL_WHICH_OPTIONS,
    lp_build=ALL_WHICH_OPTIONS,
)

# create a simple index to provide a page of links
# - re build the book
# - list assignments
# - find assignments for a student
# - show totals for all students

# select acid, sid from code as T where timestamp = (select max(timestamp) from code where sid=T.sid and acid=T.acid);


@auth.requires_login()
def index():
    redirect(URL("admin","admin"))

@auth.requires_login()
def doc():
    response.title = "Documentation"
    return dict(course_id=auth.user.course_name, course=get_course_row(db.courses.ALL))

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def sections_list():
    course = db(db.courses.id == auth.user.course_id).select().first()
    sections = db(db.sections.course_id == course.id).select()
    # get all sections - for course, list number of users in each section
    return dict(
        course = course,
        sections = sections
        )

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def sections_create():
    course = db(db.courses.id == auth.user.course_id).select().first()
    form = FORM(
        DIV(
            LABEL("Section Name", _for="section_name"),
            INPUT(_id="section_name" ,_name="name", requires=IS_NOT_EMPTY(),_class="form-control"),
            _class="form-group"
            ),
        INPUT(_type="Submit", _value="Create Section", _class="btn"),
        )
    if form.accepts(request,session):
        section = db.sections.update_or_insert(name=form.vars.name, course_id=course.id)
        session.flash = "Section Created"
        return redirect('/%s/admin/admin' % (request.application))
    return dict(
        form = form,
        )

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def sections_delete():
    course = db(db.courses.id == auth.user.course_id).select().first()
    section = db(db.sections.id == request.vars.id).select().first()
    if not section or section.course_id != course.id:
        return redirect(URL('admin','sections_list'))
    section.clear_users()
    session.flash = "Deleted Section: %s" % (section.name)
    db(db.sections.id == section.id).delete()
    return redirect(URL('admin','sections_list'))

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def sections_update():
    course = db(db.courses.id == auth.user.course_id).select().first()
    section = db(db.sections.id == request.vars.id).select().first()
    if not section or section.course_id != course.id:
        redirect(URL('admin','sections_list'))
    bulk_email_form = FORM(
        DIV(
            TEXTAREA(_name="emails_csv",
                requires=IS_NOT_EMPTY(),
                _class="form-control",
                ),
            _class="form-group",
            ),
        LABEL(
            INPUT(_name="overwrite", _type="Checkbox"),
            "Overwrite Users In Section",
            _class="checkbox",
            ),
        INPUT(_type='Submit', _class="btn", _value="Update Section"),
        )
    if bulk_email_form.accepts(request,session):
        if bulk_email_form.vars.overwrite:
            section.clear_users()
        users_added_count = 0
        for email_address in bulk_email_form.vars.emails_csv.split(','):
            user = db(db.auth_user.email == email_address.lower()).select().first()
            if user:
                if section.add_user(user):
                    users_added_count += 1
        session.flash = "%d Emails Added" % (users_added_count)
        return redirect('/%s/admin/sections_update?id=%d' % (request.application, section.id))
    elif bulk_email_form.errors:
        response.flash = "Error Processing Request"
    return dict(
        section = section,
        users = section.get_users(),
        bulk_email_form = bulk_email_form,
        )


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def assignments():
    """
    This is called for the assignments tab on the instructor interface
    """
    response.title = "Assignments"
    cur_assignments = db(db.assignments.course == auth.user.course_id).select(orderby=db.assignments.duedate)
    assigndict = OrderedDict()
    for row in cur_assignments:
        assigndict[row.id] = row.name

    tags = []
    tag_query = db(db.tags).select()
    for tag in tag_query:
        tags.append(tag.tag_name)

    course_url = path.join('/',request.application, 'static', auth.user.course_name, 'index.html')

    course = get_course_row(db.courses.ALL)
    base_course = course.base_course
    chapter_labels = []
    chapters_query = db(db.chapters.course_id == base_course).select(db.chapters.chapter_label)
    for row in chapters_query:
        chapter_labels.append(row.chapter_label)
    return dict(coursename=auth.user.course_name,
                confirm=False,
                course_id=auth.user.course_name,
                course_url=course_url,
                assignments=assigndict,
                tags=tags,
                chapters=chapter_labels,
                toc=_get_toc_and_questions(),   # <-- This Gets the readings and questions
                course=course,
                )


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def practice():
    response.title = "Practice"
    course = db(db.courses.id == auth.user.course_id).select().first()
    course_start_date = course.term_start_date

    start_date = course_start_date + datetime.timedelta(days=13)
    end_date = ""
    max_practice_days = 50
    max_practice_questions = 500
    day_points = 2
    question_points = 0.2
    questions_to_complete_day = 10
    flashcard_creation_method = 0
    graded = 1
    spacing = 0
    interleaving = 0
    error_start_date = 0
    error_end_date = 0
    error_max_practice_days = 0
    error_max_practice_questions = 0
    error_day_points = 0
    error_question_points = 0
    error_questions_to_complete_day = 0
    error_flashcard_creation_method = 0
    error_graded = 0

    already_exists = 0
    any_practice_settings = db(db.course_practice.auth_user_id == auth.user.id)
    practice_settings = any_practice_settings(db.course_practice.course_name == course.course_name)
    # If the instructor has created practice for other courses, don't randomize spacing and interleaving for the new
    # course.
    if not any_practice_settings.isempty():
        any_practice_settings = any_practice_settings.select().first()
        spacing = any_practice_settings.spacing
        interleaving = any_practice_settings.interleaving

        #  Now checking to see if there are practice settings for this course.
        #  If not, stick with the defaults.
        if (not practice_settings.isempty() and
                practice_settings.select().first().end_date is not None and
                practice_settings.select().first().end_date != ""):
            practice_setting = practice_settings.select().first()
            start_date = practice_setting.start_date
            end_date = practice_setting.end_date
            max_practice_days = practice_setting.max_practice_days
            max_practice_questions = practice_setting.max_practice_questions
            day_points = practice_setting.day_points
            question_points = practice_setting.question_points
            questions_to_complete_day = practice_setting.questions_to_complete_day
            flashcard_creation_method = practice_setting.flashcard_creation_method
            graded = practice_setting.graded
            spacing = practice_setting.spacing
            interleaving = practice_setting.interleaving
            already_exists = 1
    else:
        if randint(0, 1) == 1:
            spacing = 1
        if randint(0, 1) == 1:
            interleaving = 1
    if practice_settings.isempty():
        db.course_practice.insert(auth_user_id=auth.user.id,
                                  course_name=course.course_name,
                                  start_date=start_date,
                                  end_date=end_date,
                                  max_practice_days=max_practice_days,
                                  max_practice_questions=max_practice_questions,
                                  day_points=day_points,
                                  question_points=question_points,
                                  questions_to_complete_day=questions_to_complete_day,
                                  flashcard_creation_method=flashcard_creation_method,
                                  graded=graded,
                                  spacing=spacing,
                                  interleaving=interleaving
                                  )
        practice_settings = db((db.course_practice.auth_user_id == auth.user.id) &
                               (db.course_practice.course_name == course.course_name))

    toc = "''"
    if flashcard_creation_method == 2:
        toc = _get_toc_and_questions()

    # If the GET request is to open the page for the first time (they're not submitting the form):
    if not ('StartDate' in request.vars or
            'EndDate' in request.vars or
            'maxPracticeDays' in request.vars or
            'maxPracticeQuestions' in request.vars or
            'pointsPerDay' in request.vars or
            'pointsPerQuestion' in request.vars or
            'questionsPerDay' in request.vars or
            'flashcardsCreationType' in request.vars or
            'question_points' in request.vars or
            'graded' in request.vars):
        return dict(course_start_date=course_start_date,
                    start_date=start_date,
                    end_date=end_date,
                    max_practice_days=max_practice_days,
                    max_practice_questions=max_practice_questions,
                    day_points=day_points,
                    question_points=question_points,
                    questions_to_complete_day=questions_to_complete_day,
                    flashcard_creation_method=flashcard_creation_method,
                    graded=graded,
                    spacing=spacing,
                    interleaving=interleaving,
                    toc=toc,
                    error_start_date=error_start_date,
                    error_end_date=error_end_date,
                    error_max_practice_days=error_max_practice_days,
                    error_max_practice_questions=error_max_practice_questions,
                    error_day_points=error_day_points,
                    error_question_points=error_question_points,
                    error_questions_to_complete_day=error_questions_to_complete_day,
                    error_flashcard_creation_method=error_flashcard_creation_method,
                    error_graded=error_graded,
                    complete=already_exists,
                    course=course,
                    )
    else:
        try:
            start_date = datetime.datetime.strptime(request.vars.get('StartDate', None), '%Y-%m-%d').date()
            if start_date < course_start_date:
                error_start_date = 1
        except:
            error_start_date = 1
        try:
            end_date = datetime.datetime.strptime(request.vars.get('EndDate', None), '%Y-%m-%d').date()
            if end_date < start_date:
                error_end_date = 1
        except:
            error_end_date = 1
        if spacing == 1:
            try:
                max_practice_days = int(request.vars.get('maxPracticeDays', None))
            except:
                error_max_practice_days = 1
        else:
            try:
                max_practice_questions = int(request.vars.get('maxPracticeQuestions', None))
            except:
                error_max_practice_questions = 1
        if spacing == 1:
            try:
                day_points = float(request.vars.get('pointsPerDay', None))
            except:
                error_day_points = 1
        else:
            try:
                question_points = float(request.vars.get('pointsPerQuestion', None))
            except:
                error_question_points = 1
        if spacing == 1:
            try:
                questions_to_complete_day = int(request.vars.get('questionsPerDay', None))
            except:
                error_questions_to_complete_day = 1
        try:
            flashcard_creation_method = int(request.vars.get('flashcardsCreationType', None))
        except:
            error_flashcard_creation_method = 1
        try:
            graded = int(request.vars.get('graded', None))
        except:
            error_graded = 1

        no_error = 0
        if (error_start_date == 0 and
                error_end_date == 0 and
                error_max_practice_days == 0 and
                error_max_practice_questions == 0 and
                error_day_points == 0 and
                error_question_points == 0 and
                error_questions_to_complete_day == 0 and
                error_flashcard_creation_method == 0 and
                error_graded == 0):
            no_error = 1
        if no_error == 1:
            practice_settings.update(start_date=start_date,
                                     end_date=end_date,
                                     max_practice_days=max_practice_days,
                                     max_practice_questions=max_practice_questions,
                                     day_points=day_points,
                                     question_points=question_points,
                                     questions_to_complete_day=questions_to_complete_day,
                                     flashcard_creation_method=flashcard_creation_method,
                                     graded=graded,
                                     spacing=spacing,
                                     interleaving=interleaving
                                     )

        toc = "''"
        if flashcard_creation_method == 2:
            toc = _get_toc_and_questions()
        return dict(course_id=auth.user.course_name,
                    course_start_date=course_start_date,
                    start_date=start_date,
                    end_date=end_date,
                    max_practice_days=max_practice_days,
                    max_practice_questions=max_practice_questions,
                    day_points=day_points,
                    question_points=question_points,
                    questions_to_complete_day=questions_to_complete_day,
                    flashcard_creation_method=flashcard_creation_method,
                    graded=graded,
                    spacing=spacing,
                    interleaving=interleaving,
                    error_graded=error_graded,
                    toc=toc,
                    error_start_date=error_start_date,
                    error_end_date=error_end_date,
                    error_max_practice_days=error_max_practice_days,
                    error_max_practice_questions=error_max_practice_questions,
                    error_day_points=error_day_points,
                    error_question_points=error_question_points,
                    error_questions_to_complete_day=error_questions_to_complete_day,
                    error_flashcard_creation_method=error_flashcard_creation_method,
                    complete=no_error,
                    course=course,
                    )


# I was not sure if it's okay to import it from `assignmnets.py`.
# Only questions that are marked for practice are eligible for the spaced practice.
def _get_qualified_questions(base_course, chapter_label, sub_chapter_label):
    return db((db.questions.base_course == base_course) &
              ((db.questions.topic == "{}/{}".format(chapter_label, sub_chapter_label)) |
               ((db.questions.chapter == chapter_label) &
                (db.questions.topic == None) &
                (db.questions.subchapter == sub_chapter_label))) &
              (db.questions.practice == True))


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def add_practice_items():
    response.title = "Add Practice Items"
    course = db(db.courses.course_name == auth.user.course_name).select().first()
    data = json.loads(request.vars.data)

    # Was for Python 2.x
    # string_data = [x.encode('UTF8') for x in data]
    # Is for Python 3.x
    string_data = data

    now = datetime.datetime.utcnow()
    now_local = now - datetime.timedelta(hours=float(session.timezoneoffset))

    students = db((db.auth_user.course_name == auth.user.course_name)).select()
    chapters = db((db.chapters.course_id == course.base_course)).select()
    for chapter in chapters:
        subchapters = db((db.sub_chapters.chapter_id == chapter.id)).select()
        for subchapter in subchapters:
            subchapterTaught = db((db.sub_chapter_taught.course_name == auth.user.course_name) &
                               (db.sub_chapter_taught.chapter_label == chapter.chapter_label) &
                               (db.sub_chapter_taught.sub_chapter_label == subchapter.sub_chapter_label))
            questions = _get_qualified_questions(course.base_course,
                                                 chapter.chapter_label,
                                                 subchapter.sub_chapter_label)
            if "{}/{}".format(chapter.chapter_name, subchapter.sub_chapter_name) in string_data:
                if subchapterTaught.isempty() and not questions.isempty():
                    db.sub_chapter_taught.insert(
                        course_name=auth.user.course_name,
                        chapter_label=chapter.chapter_label,
                        sub_chapter_label=subchapter.sub_chapter_label,
                        teaching_date=now_local.date(),
                    )
                    for student in students:
                        flashcards = db((db.user_topic_practice.user_id == student.id) &
                                        (db.user_topic_practice.course_name == course.course_name) &
                                        (db.user_topic_practice.chapter_label == chapter.chapter_label) &
                                        (db.user_topic_practice.sub_chapter_label == subchapter.sub_chapter_label))
                        if flashcards.isempty():
                            db.user_topic_practice.insert(
                                user_id=student.id,
                                course_name=course.course_name,
                                chapter_label=chapter.chapter_label,
                                sub_chapter_label=subchapter.sub_chapter_label,
                                question_name=questions.select().first().name,
                                i_interval=0,
                                e_factor=2.5,
                                q=0,
                                next_eligible_date=now_local.date(),
                                # add as if yesterday, so can practice right away
                                last_presented=now.date() - datetime.timedelta(1),
                                last_completed=now.date() - datetime.timedelta(1),
                                creation_time=now,
                                timezoneoffset=float(session.timezoneoffset)
                            )
            else:
                if not subchapterTaught.isempty():
                    subchapterTaught.delete()
                    db((db.user_topic_practice.course_name == course.course_name) &
                       (db.user_topic_practice.chapter_label == chapter.chapter_label) &
                       (db.user_topic_practice.sub_chapter_label == subchapter.sub_chapter_label)).delete()
    return json.dumps(dict(complete=True))


# This is the primary controller when the instructor goes to the admin page.
@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def admin():
    response.title = "Admin"
    sidQuery = db(db.courses.course_name == auth.user.course_name).select().first()
    courseid = sidQuery.id
    sectionsQuery = db(db.sections.course_id == courseid).select() #Querying to find all sections for that given course_id found above
    sectionsList = []
    for row in sectionsQuery:
        sectionsList.append(row.name)
    #Now get the start date
    dateQuery = db(db.courses.course_name == auth.user.course_name).select()
    date = dateQuery[0].term_start_date
    date = date.strftime("%m/%d/%Y")
    cwd = os.getcwd()
    try:
        os.chdir(path.join('applications',request.application,'books',sidQuery.base_course))
        master_build = sh("git describe --long", capture=True)[:-1]
        with open('build_info','w') as bc:
            bc.write(master_build)
            bc.write("\n")
    except:
        master_build = ""
    finally:
        os.chdir(cwd)

    try:
        mbf_path = path.join('applications',request.application,'custom_courses',sidQuery.course_name,'build_info')
        mbf = open(mbf_path,'r')
        last_build = os.path.getmtime(mbf_path)
        my_build = mbf.read()[:-1]
        mbf.close()
    except:
        my_build = ""
        last_build = 0

    my_vers = 0
    mst_vers = 0
    bugfix = False

    cur_instructors = db(db.course_instructor.course == auth.user.course_id).select(db.course_instructor.instructor)
    instructordict = {}
    for row in cur_instructors:
        name = db(db.auth_user.id == row.instructor).select(db.auth_user.first_name, db.auth_user.last_name)
        for person in name:
            instructordict[str(row.instructor)] = person.first_name + " " + person.last_name

    cur_students = db(db.user_courses.course_id == auth.user.course_id).select(db.user_courses.user_id)
    studentdict = {}
    for row in cur_students:
        person = db(db.auth_user.id == row.user_id).select(db.auth_user.username, db.auth_user.first_name, db.auth_user.last_name)
        for identity in person:
            name = identity.first_name + " " + identity.last_name
            if row.user_id not in instructordict:
                studentdict[row.user_id]= name

    course = db(db.courses.course_name == auth.user.course_name).select().first()
    instructor_course_list = db( (db.course_instructor.instructor == auth.user.id) &
                                 (db.courses.id == db.course_instructor.course) &
                                 (db.courses.base_course == course.base_course) &
                                 (db.courses.course_name != course.course_name)).select(db.courses.course_name, db.courses.id)

    curr_start_date = course.term_start_date.strftime("%m/%d/%Y")
    return dict(sectionInfo=sectionsList,startDate=date,
                coursename=auth.user.course_name, course_id=auth.user.course_name,
                instructors=instructordict, students=studentdict,
                curr_start_date=curr_start_date, confirm=True,
                build_info=my_build, master_build=master_build, my_vers=my_vers,
                mst_vers=mst_vers,
                course=sidQuery,
                instructor_course_list=instructor_course_list
                )

# Called in admin.js from courseStudents to populate  the list of students
# eBookConfig.getCourseStudentsURL
@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def course_students():
    response.headers['content-type'] = 'application/json'
    cur_students = db(
        (db.user_courses.course_id == auth.user.course_id) &
        (db.auth_user.id == db.user_courses.user_id)
    ).select(db.auth_user.username, db.auth_user.first_name,db.auth_user.last_name, orderby= db.auth_user.last_name|db.auth_user.first_name)
    searchdict = OrderedDict()
    for row in cur_students:
        name = row.first_name + " " + row.last_name
        username = row.username
        searchdict[str(username)] = name
    return json.dumps(searchdict)

# Called when an instructor clicks on the grading tab
@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def grading():
    response.title = "Grading"
    assignments = {}
    assignments_query = db(db.assignments.course == auth.user.course_id).select()

    assignmentids = {}
    assignment_deadlines = {}
    question_points = {}

    for row in assignments_query:
        assignmentids[row.name] = int(row.id)
        # Retrieve relevant info for each question, ordering them based on their
        # order in the assignment.
        assignment_questions = db(
            db.assignment_questions.assignment_id == int(row.id)
        ).select(
            db.assignment_questions.question_id,
            db.assignment_questions.points,
            orderby=db.assignment_questions.sorting_priority)
        questions = []
        for q in assignment_questions:
            question_name = db(db.questions.id == q.question_id).select(db.questions.name).first().name
            questions.append(question_name)
            question_points[question_name] = q.points
        assignments[row.name] = questions
        assignment_deadlines[row.name] = row.duedate.isoformat()

    cur_students = db(db.user_courses.course_id == auth.user.course_id).select(db.user_courses.user_id)
    searchdict = {}
    for row in cur_students:
        isinstructor = db((db.course_instructor.course == auth.user.course_id) & (db.course_instructor.instructor == row.user_id)).select()
        instructorlist = []
        for line in isinstructor:
            instructorlist.append(line.instructor)
        if row.user_id not in instructorlist:
            person = db(db.auth_user.id == row.user_id).select(db.auth_user.username, db.auth_user.first_name,
                                                               db.auth_user.last_name)
            for identity in person:
                name = identity.first_name + " " + identity.last_name
                username = db(db.auth_user.id == int(row.user_id)).select(db.auth_user.username).first().username
                searchdict[str(username)] = name


    course = db(db.courses.id == auth.user.course_id).select().first()
    base_course = course.base_course
    chapter_labels = {}
    chapters_query = db(db.chapters.course_id == base_course).select()
    for row in chapters_query:
        q_list = []
        chapter_questions = db((db.questions.chapter == row.chapter_label) & (db.questions.base_course == base_course) & (db.questions.question_type != 'page')).select()
        for chapter_q in chapter_questions:
            q_list.append(chapter_q.name)
        chapter_labels[row.chapter_label] = q_list
    return dict(assignmentinfo=json.dumps(assignments), students=searchdict,
                chapters=json.dumps(chapter_labels),
                gradingUrl = URL('assignments', 'get_problem'),
                autogradingUrl = URL('assignments', 'autograde'),
                gradeRecordingUrl = URL('assignments', 'record_grade'),
                calcTotalsURL = URL('assignments', 'calculate_totals'),
                setTotalURL=URL('assignments', 'record_assignment_score'),
                sendLTIGradeURL=URL('assignments', 'send_assignment_score_via_LTI'),
                getCourseStudentsURL = URL('admin', 'course_students'),
                get_assignment_release_statesURL= URL('admin', 'get_assignment_release_states'),
                course_id = auth.user.course_name,
                assignmentids=json.dumps(assignmentids),
                assignment_deadlines=json.dumps(assignment_deadlines),
                question_points=json.dumps(question_points),
                course=course,
                )

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def removeStudents():
    """
    Remove one or more students from the current course
    The query string should contain the key studentList which can be either
    a single id from auth_user or it could be a list of ids.

    This does not remove a student from the database but rather marks them as inactive in
    the database and moves them to the basecourse.
    """

    baseCourseName = db(db.courses.course_name == auth.user.course_name).select(db.courses.base_course)[0].base_course
    baseCourseID = db(db.courses.course_name == baseCourseName).select(db.courses.id)[0].id
    answer_tables = ['mchoice_answers', 'clickablearea_answers', 'codelens_answers',
                     'dragndrop_answers', 'fitb_answers','parsons_answers',
                     'shortanswer_answers']

    if not isinstance(request.vars["studentList"], str):
        # Multiple ids selected
        studentList = request.vars["studentList"]
    elif request.vars["studentList"] == "None":
        # No id selected
        session.flash = T("No valid students were selected")
        return redirect('/%s/admin/admin' % (request.application))
    else:
        # One id selected
        studentList = [request.vars["studentList"]]

    for studentID in studentList:
        if studentID.isdigit() and int(studentID) != auth.user.id:
            sid = db(db.auth_user.id == int(studentID)).select(db.auth_user.username).first()
            db((db.user_courses.user_id == int(studentID)) & (db.user_courses.course_id == auth.user.course_id)).delete()
            section = db((db.sections.course_id == auth.user.course_id) &
                         (db.section_users.auth_user == int(studentID)) &
                         (db.section_users.section == db.sections.id)).select().first()
            if section:
                db(db.section_users.id == section.section_users.id).delete()

            db.user_courses.insert(user_id=int(studentID), course_id=baseCourseID)
            db(db.auth_user.id == int(studentID)).update(course_id=baseCourseID, course_name=baseCourseName, active='F')
            db( (db.useinfo.sid == sid) &
                (db.useinfo.course_id == auth.user.course_name)).update(course_id=baseCourseName)
            for tbl in answer_tables:
                db( (db[tbl].sid == sid) & (db[tbl].course_name == auth.user.course_name)).update(course_name=baseCourseName)
            db((db.code.sid == sid) &
               (db.code.course_id == auth.user.course_id)).update(course_id=baseCourseID)
            db((db.acerror_log.sid == sid) &
               (db.acerror_log.course_id == auth.user.course_name)).update(course_id=baseCourseName)
            # leave user_chapter_progress and user_sub_chapter_progress alone for now.

    session.flash = T("You have successfully removed students")
    return redirect('/%s/admin/admin' % (request.application))

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def removeinstructor():
    """
    admin/removeinstructor/<int>

    """
    removed = []
    if request.args[0] != str(auth.user.id):
        db((db.course_instructor.instructor == request.args[0]) & (db.course_instructor.course == auth.user.course_id)).delete()
        removed.append(True)
        return json.dumps(removed)
    else:
        session.flash = T("You cannot remove yourself as an instructor.")
        removed.append(False)
        return json.dumps(removed)

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def addinstructor():
    """
    admin/addinstructor/<int>

    """
    response.headers['content-type'] = 'application/json'
    instructor = request.args(0)
    res = db(db.auth_user.id == instructor).select().first()
    if res:
        db.course_instructor.insert(course=auth.user.course_id , instructor=instructor)
        retval = "Success"
    else:
        retval = "Cannot add non-existent user as instructor"
        logger.error("Trying to add non-user {} as instructor".format(instructor))

    return json.dumps(retval)


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def deletecourse():
    course_name = auth.user.course_name
    cset = db(db.courses.course_name == course_name)
    if not cset.isempty():
        res = cset.select(db.courses.id, db.courses.base_course).first()
        courseid = res.id
        basecourse = res.base_course
        bcid = db(db.courses.course_name == basecourse).select(db.courses.id).first()
        qset = db((db.course_instructor.course == courseid) & (db.course_instructor.instructor == auth.user.id))
        if not qset.isempty():
            qset.delete()
            students = db(db.auth_user.course_id == courseid)
            students.update(course_id=bcid)
            uset=db(db.user_courses.course_id == courseid)
            uset.delete()
            db(db.courses.id == courseid).delete()
            try:
                shutil.rmtree(path.join('applications', request.application, 'static', course_name))
                shutil.rmtree(path.join('applications', request.application, 'custom_courses', course_name))
                session.clear()
            except:
                session.flash = 'Error, %s does not appear to exist' % course_name
        else:
            session.flash = 'You are not the instructor of %s' % course_name
    else:
        session.flash = 'course, %s, not found' % course_name

    redirect(URL('default','index'))


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def removeassign():
    response.headers['content-type'] = 'application/json'
    try:
        assignment_id = int(request.vars['assignid'])
    except:
        session.flash = "Cannot remove assignment with id of {}".format(request.vars['assignid'])
        logger.error("Cannot Remove Assignment {}".format(request.args(0)))
        return "Error"

    ct = db(db.assignments.id == assignment_id).delete()

    if ct == 1:
        return "Success"
    else:
        return "Error"

#
# This is only called by the create button in the popup where you give the assignment
# its initial name.  We might be able to refactor save_assignment to work in all cases.
@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def createAssignment():
    response.headers['content-type'] = 'application/json'
    due = None
    logger.debug(type(request.vars['name']))
    try:
        name=request.vars['name']
        course=auth.user.course_id
        logger.debug("Adding new assignment {} for course".format(request.vars['name'], course))
        name_existsQ = len(db((db.assignments.name == name) & (db.assignments.course == course)).select())
        if name_existsQ>0:
            return json.dumps("EXISTS")
        newassignID = db.assignments.insert(course=course, name=name, duedate=datetime.datetime.utcnow() + datetime.timedelta(days=7))
    except Exception as ex:
        logger.error(ex)
        return json.dumps('ERROR')
    try:
        returndict = {request.vars['name']: newassignID}
        return json.dumps(returndict)
    except Exception as ex:
        logger.error(ex)
        return json.dumps('ERROR')

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def renameAssignment():
    response.headers['content-type'] = 'application/json'
    try:
        logger.debug("Renaming {} to {} for course {}.".format(request.vars['original'],request.vars['name'],auth.user.course_id))
        assignment_id=request.vars['original']
        name=request.vars['name']
        course=auth.user.course_id
        name_existsQ = len(db((db.assignments.name == name) & (db.assignments.course == course)).select())
        if name_existsQ>0:
            return json.dumps("EXISTS")
        db(db.assignments.id == assignment_id).update(name=name)
    except Exception as ex:
        logger.error(ex)
        return json.dumps('ERROR')
    try:
        returndict={name: assignment_id}
        return json.dumps(returndict)
    except Exception as ex:
        logger.error(ex)
        return json.dumps('ERROR')

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def questionBank():
    response.headers['content-type'] = 'application/json'
    logger.error("in questionbank")
    row = db(db.courses.id == auth.user.course_id).select(db.courses.course_name, db.courses.base_course).first()
    base_course = row.base_course

    tags = False
    if request.vars['tags']:
        tags = True
    term = False
    if request.vars['term']:
        term = True
    chapterQ = None
    if request.vars['chapter']:
        chapter_label = db(db.chapters.chapter_label == request.vars['chapter']).select(db.chapters.chapter_label).first().chapter_label
        chapterQ =  db.questions.chapter == chapter_label
    difficulty = False
    if request.vars['difficulty']:
        difficulty = True
    authorQ = None
    if request.vars['author'] :
        authorQ = db.questions.author == request.vars['author']
    rows = []
    questions = []

    base_courseQ = db.questions.base_course == base_course
    try:

        if chapterQ != None and authorQ != None:

            questions_query = db(chapterQ & authorQ & base_courseQ).select()

        elif chapterQ == None and authorQ != None:

            questions_query = db(authorQ & base_courseQ).select()

        elif chapterQ != None and authorQ == None:

            questions_query = db(chapterQ & base_courseQ).select()

        else:
            questions_query = db(base_courseQ).select()

        for question in questions_query: #Initially add all questions that we can to the list, and then remove the rows that don't match search criteria
            rows.append(question)

        for row in questions_query:
            removed_row = False
            if term:
                if (request.vars['term'] not in row.name and row.question and request.vars['term'] not in row.question) or row.question_type == 'page':
                    try:
                        rows.remove(row)
                        removed_row = True
                    except Exception as err:
                        ex = err
            if removed_row == False:
                if difficulty:
                    if int(request.vars['difficulty']) != row.difficulty:
                        try:
                            rows.remove(row)
                            removed_row = True
                        except Exception as err:
                            ex = err

            if removed_row == False:
                if tags:
                    tags_query = db(db.question_tags.question_id == row.id).select()
                    tag_list = []
                    for q_tag in tags_query:
                        tag_names = db(db.tags.id == q_tag.tag_id).select()
                        for tag_name in tag_names:
                            tag_list.append(tag_name.tag_name)
                    needsRemoved = False
                    for search_tag in request.vars['tags'].split(','):
                        if search_tag not in tag_list:
                            needsRemoved = True
                    if needsRemoved:
                        try:
                            rows.remove(row)
                        except Exception as err:
                            print(err)
        for q_row in rows:
            questions.append(q_row.name)

    except Exception as ex:
        logger.error(ex)
        return json.dumps('Error ' + str(ex))

    return json.dumps(questions)


# Deprecated; use add__or_update_assignment_question instead
@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def addToAssignment():
    return add__or_update_assignment_question()


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def getQuestionInfo():
    """
    called by the questionBank search  interface
    Request Vars required:
    * assignment -- integer assignment id
    * question -- the name of the question
    """
    assignment_id = int(request.vars['assignment'])
    question_name = request.vars['question']
    base_course = db(db.courses.course_name == auth.user.course_name).select().first().base_course
    row = db((db.questions.name == question_name) & (db.questions.base_course == base_course)).select().first()

    question_code = row.question
    htmlsrc = row.htmlsrc
    question_author = row.author
    question_difficulty = row.difficulty
    question_id = row.id

    tags = []
    question_tags = db((db.question_tags.question_id == question_id)).select()
    for row in question_tags:
        tag_id = row.tag_id
        tag_name = db((db.tags.id == tag_id)).select(db.tags.tag_name).first().tag_name
        tags.append(" " + str(tag_name))
    if question_difficulty != None:
        returnDict = {'code':question_code, 'htmlsrc': htmlsrc, 'author':question_author, 'difficulty':int(question_difficulty), 'tags': tags}
    else:
        returnDict = {'code':question_code, 'htmlsrc': htmlsrc, 'author':question_author, 'difficulty':None, 'tags': tags}

    return json.dumps(returnDict)

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def edit_question():
    vars = request.vars
    old_qname = vars['question']
    new_qname = vars['name']
    try:
        difficulty = int(vars['difficulty'])
    except:
        difficulty = 0
    tags = vars['tags']
    base_course = db(db.courses.id == auth.user.course_id).select(db.courses.base_course).first().base_course
    old_question = db((db.questions.name == old_qname) & (db.questions.base_course == base_course)).select().first()

    if not old_question:
        return "Could not find question {} to update".format(old_qname)

    author = auth.user.first_name + " " + auth.user.last_name
    timestamp = datetime.datetime.utcnow()
    chapter = old_question.chapter
    question_type = old_question.question_type
    subchapter = old_question.subchapter

    question = vars['questiontext']
    htmlsrc = vars['htmlsrc']

    if old_qname == new_qname and old_question.author != author:
        return "You do not own this question, Please assign a new unique id"

    if old_qname != new_qname:
        newq = db(db.questions.name == new_qname).select().first()
        if newq and newq.author != author:
            return "You cannot replace a question you did not author"

    try:
        new_qid = db.questions.update_or_insert(
            (db.questions.name == new_qname) & (db.questions.base_course == base_course),
            difficulty=difficulty, question=question,
            name=new_qname, author=author, base_course=base_course, timestamp=timestamp,
            chapter=chapter, subchapter=subchapter, question_type=question_type,
            htmlsrc=htmlsrc)
        if tags and tags != 'null':
            tags = tags.split(',')
            for tag in tags:
                logger.error("TAG = %s",tag)
                tag_id = db(db.tags.tag_name == tag).select(db.tags.id).first().id
                db.question_tags.insert(question_id = new_qid, tag_id=tag_id)
        return "Success - Edited Question Saved"
    except Exception as ex:
        logger.error(ex)
        return "An error occurred saving your question {}".format(str(ex))


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def question_text():
    qname = request.vars['question_name']
    base_course = db(db.courses.id == auth.user.course_id).select(db.courses.base_course).first().base_course
    try:
        q_text = db((db.questions.name == qname) & (db.questions.base_course == base_course)).select(db.questions.question).first().question
    except:
        q_text = "Error: Could not find source for {} in the database".format(qname)

    if q_text[0:2] == '\\x':  # workaround Python2/3 SQLAlchemy/DAL incompatibility with text
        q_text = q_text[2:].decode('hex')
    logger.debug(q_text)
    return json.dumps(q_text)


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def gettemplate():
    template = request.args[0]
    returndict = {}
    base = ''

    returndict['template'] = base + cmap.get(template,'').__doc__

    base_course = db(db.courses.id == auth.user.course_id).select(db.courses.base_course).first().base_course
    chapters = []
    chaptersrow = db(db.chapters.course_id == base_course).select(db.chapters.chapter_name, db.chapters.chapter_label)
    for row in chaptersrow:
        chapters.append((row['chapter_label'], row['chapter_name']))
    logger.debug(chapters)
    returndict['chapters'] = chapters

    return json.dumps(returndict)


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def createquestion():
    """
    called from the questionBank interface when an instructor adds a new question to
    an assignment by writing it themselves
    request.vars parameters include
    * template - The kind  of question
    * name - the unique identifier
    * question - rst source for the question
    * difficulty 0-5
    * tags
    * chapter
    * subchapter  'Exercises' by default
    * isprivate is this question shared with everyone?
    * tab
    * assignmentid': assignmentid
    * points integer number of points
    * timed- is this part of a timed exam
    * htmlsrc htmlsrc from the previewer
    """
    row = db(db.courses.id == auth.user.course_id).select(db.courses.course_name, db.courses.base_course).first()
    base_course = row.base_course
    tab = request.vars['tab']
    aid = request.vars['assignmentid']
    if aid == 'undefined':
        logger.error("undefined assignmentid by {} for name {} subchap {} question {}".format(auth.user.username,
                                                                        request.vars.name,
                                                                        request.vars.subchapter,
                                                                        request.vars.question))
        return json.dumps("ERROR")

    assignmentid = int(aid)
    points = int(request.vars['points']) if request.vars['points'] else 1
    timed = request.vars['timed']

    try:
        newqID = db.questions.insert(base_course=base_course, name=request.vars['name'], chapter=request.vars['chapter'],
                 subchapter=request.vars['subchapter'], author=auth.user.first_name + " " + auth.user.last_name, difficulty=request.vars['difficulty'],
                 question=request.vars['question'], timestamp=datetime.datetime.utcnow(), question_type=request.vars['template'],
                 is_private=request.vars['isprivate'], htmlsrc=request.vars['htmlsrc'])

        assignment_question = db.assignment_questions.insert(assignment_id=assignmentid, question_id=newqID, timed=timed, points=points)

        returndict = {request.vars['name']: newqID, 'timed':timed, 'points': points}

        return json.dumps(returndict)
    except Exception as ex:
        logger.error(ex)
        return json.dumps('ERROR')

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def htmlsrc():
    acid = request.vars['acid']
    htmlsrc = ""
    res = db(
        (db.questions.name == acid) &
        (db.questions.base_course == db.courses.base_course) &
        (db.courses.course_name == auth.user.course_name)
         ).select(db.questions.htmlsrc).first()
    if res and res.htmlsrc:
        htmlsrc = res.htmlsrc
    else:
        logger.error("HTML Source not found for %s in course %s", acid, auth.user.course_name)
        htmlsrc = "<p>No preview Available</p>"
    if htmlsrc and htmlsrc[0:2] == '\\x':    # Workaround Python3/Python2  SQLAlchemy/DAL incompatibility with text columns
        htmlsrc = htmlsrc.decode('hex')
    return json.dumps(htmlsrc)


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def getGradeComments():

    acid = request.vars['acid']
    sid = request.vars['sid']

    c =  db((db.question_grades.sid == sid) \
             & (db.question_grades.div_id == acid) \
             & (db.question_grades.course_name == auth.user.course_name)\
            ).select().first()
    if c != None:
        return json.dumps({'grade':c.score, 'comments':c.comment})
    else:
        return json.dumps("Error")

def _get_assignment(assignment_id):
    return db(db.assignments.id == assignment_id).select().first()

def _get_lti_record(oauth_consumer_key):
    if oauth_consumer_key:
        return db(db.lti_keys.consumer == oauth_consumer_key).select().first()

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def releasegrades():
    try:
        assignmentid = request.vars['assignmentid']
        released = (request.vars['released'] == 'yes')
        assignment = db(db.assignments.id == assignmentid).select().first()
        assignment.update_record(released=released)

    except Exception as ex:
        logger.error(ex)
        return "ERROR"

    if released:
        # send lti grades
        assignment = _get_assignment(assignmentid)
        lti_record = _get_lti_record(session.oauth_consumer_key)
        if assignment and lti_record:
            send_lti_grades(assignment.id, assignment.points, auth.user.course_id, lti_record, db)
    return "Success"


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def get_assignment_release_states():
    # return a dictionary with the release status of whether grades have been
    # released for each of the assignments for the current course
    try:
        assignments_query = db(db.assignments.course == auth.user.course_id).select()
        return json.dumps({row.name: row.released for row in assignments_query})
    except Exception as ex:
        print(ex)
        return json.dumps({})

def _get_toc_and_questions():
    # return a dictionary with a nested dictionary representing everything the
    # picker will need in the instructor's assignment authoring tab

    # Format is documented at https://www.jstree.com/docs/json/

    #try:
        course_row = get_course_row()
        base_course = course_row.base_course

        # First get the chapters associated with the current course, and insert them into the tree
        # Recurse, with each chapter:
        #   -- get the subchapters associated with it, and insert into the subdictionary
        #   -- Recurse; with each subchapter:
        #      -- get the divs associated with it, and insert into the sub-sub-dictionary

        question_picker = []
        # This one doesn't include the questions, but otherwise the same
        reading_picker = []
        # This one is similar to reading_picker, but does not include sub-chapters with no practice question.
        practice_picker = []
        subchapters_taught_query = db((db.sub_chapter_taught.course_name == auth.user.course_name) &
                                      (db.chapters.course_id == base_course) &
                                      (db.chapters.chapter_label == db.sub_chapter_taught.chapter_label) &
                                      (db.sub_chapters.chapter_id == db.chapters.id) &
                                      (db.sub_chapters.sub_chapter_label == db.sub_chapter_taught.sub_chapter_label)
                                      ).select(db.chapters.chapter_name,
                                               db.sub_chapters.sub_chapter_name)
        chapters_and_subchapters_taught = [(row.chapters.chapter_name, row.sub_chapters.sub_chapter_name)
                                           for row in subchapters_taught_query]
        topic_query = db((db.courses.course_name == auth.user.course_name) &
                         (db.questions.base_course == db.courses.base_course) &
                         (db.questions.practice == True)).select(db.questions.topic,
                                                                 db.questions.chapter,
                                                                 db.questions.subchapter,
                                                                 orderby=db.questions.id)
        for q in topic_query:
            # We know chapter_name and sub_chapter_name include spaces.
            # So we cannot directly use the labels retrieved from q.topic as chapter_name and
            # sub_chapter_name and we need to query the corresponding chapter_name and sub_chapter_name from the
            # corresponding tables.
            topic_not_found = True
            if q.topic is not None:
                topic_not_found = False
                try:
                    chap, subch = q.topic.split('/')
                except:
                    # a badly formed "topic" for the question; just ignore it
                    logger.info("Bad Topic: {}".format(q.topic))
                    topic_not_found = True
                try:
                    chapter = db((db.chapters.course_id == base_course) &
                                  (db.chapters.chapter_label == chap)) \
                                  .select()[0]

                    sub_chapter_name = db((db.sub_chapters.chapter_id == chapter.id) &
                                  (db.sub_chapters.sub_chapter_label == subch)) \
                                  .select()[0].sub_chapter_name
                except:
                    # topic's chapter and subchapter are not in the book; ignore this topic
                    logger.info("Missing Chapter {} or Subchapter {} for topic {}".format(chap, subch, q.topic))
                    topic_not_found = True

            if topic_not_found:
                topic_not_found = False
                chap = q.chapter
                subch = q.subchapter
                try:
                    chapter = db((db.chapters.course_id == base_course) &
                                 (db.chapters.chapter_label == chap)) \
                        .select()[0]

                    sub_chapter_name = db((db.sub_chapters.chapter_id == chapter.id) &
                                          (db.sub_chapters.sub_chapter_label == subch)) \
                        .select()[0].sub_chapter_name
                except:
                    # topic's chapter and subchapter are not in the book; ignore this topic
                    logger.info("Missing Chapter {} or Subchapter {}".format(chap, subch))
                    topic_not_found = True

            if not topic_not_found:
                chapter_name = chapter.chapter_name
                # Find the item in practice picker for this chapter
                p_ch_info = None
                for ch_info in practice_picker:
                    if ch_info['text'] == chapter_name:
                        p_ch_info = ch_info
                if not p_ch_info:
                    # if there isn't one, add one
                    p_ch_info = {}
                    practice_picker.append(p_ch_info)
                    p_ch_info['text'] = chapter_name
                    p_ch_info['children'] = []
                # add the subchapter
                p_sub_ch_info = {}
                if sub_chapter_name not in [child['text'] for child in p_ch_info['children']]:
                    p_ch_info['children'].append(p_sub_ch_info)
                    p_sub_ch_info['id'] = "{}/{}".format(chapter_name, sub_chapter_name)
                    p_sub_ch_info['text'] = sub_chapter_name
                    # checked if
                    p_sub_ch_info['state'] = {'checked':
                                              (chapter_name, sub_chapter_name) in chapters_and_subchapters_taught}

        # chapters are associated base_course.
        chapters_query = db((db.chapters.course_id == base_course)).select(orderby=db.chapters.id)
        ids = {row.chapter_name: row.id for row in chapters_query}
        practice_picker.sort(key=lambda d: ids[d['text']])

        for ch in chapters_query:
            q_ch_info = {}
            question_picker.append(q_ch_info)
            q_ch_info['text'] = ch.chapter_name
            q_ch_info['children'] = []
            # Copy the same stuff for reading picker.
            r_ch_info = {}
            reading_picker.append(r_ch_info)
            r_ch_info['text'] = ch.chapter_name
            r_ch_info['children'] = []
            # practice_questions = db((db.questions.chapter == ch.chapter_label) & \
            #                         (db.questions.practice == True))
            # if not practice_questions.isempty():
            #     # Copy the same stuff for practice picker.
            #     p_ch_info = {}
            #     practice_picker.append(p_ch_info)
            #     p_ch_info['text'] = ch.chapter_name
            #     p_ch_info['children'] = []
            # todo:  check the chapters attribute to see if its available for readings
            subchapters_query = db(db.sub_chapters.chapter_id == ch.id).select(orderby=db.sub_chapters.id)
            for sub_ch in subchapters_query:
                q_sub_ch_info = {}
                q_ch_info['children'].append(q_sub_ch_info)
                q_sub_ch_info['text'] = sub_ch.sub_chapter_name
                # Make the Exercises sub-chapters easy to access, since user-written problems will be added there.
                if sub_ch.sub_chapter_name == 'Exercises':
                    q_sub_ch_info['id'] = ch.chapter_name + ' Exercises'
                q_sub_ch_info['children'] = []
                # Copy the same stuff for reading picker.
                if sub_ch.skipreading == 'F' or sub_ch.skipreading == False or sub_ch.skipreading == None:
                    r_sub_ch_info = {}
                    r_ch_info['children'].append(r_sub_ch_info)
                    r_sub_ch_info['id'] = "{}/{}".format(ch.chapter_name, sub_ch.sub_chapter_name)
                    r_sub_ch_info['text'] = sub_ch.sub_chapter_name
                # practice_questions = db((db.questions.chapter == ch.chapter_label) & \
                #                (db.questions.subchapter == sub_ch.sub_chapter_label) & \
                #                (db.questions.practice == True))
                # if not practice_questions.isempty():
                #     # Copy the same stuff for reading picker.
                #     p_sub_ch_info = {}
                #     p_ch_info['children'].append(p_sub_ch_info)
                #     p_sub_ch_info['id'] = "{}/{}".format(ch.chapter_name, sub_ch.sub_chapter_name)
                #     p_sub_ch_info['text'] = sub_ch.sub_chapter_name
                #     # checked if
                #     p_sub_ch_info['state'] = {'checked':
                #                               (ch.chapter_name, sub_ch.sub_chapter_name) in chapters_and_subchapters_taught}
                # include another level for questions only in the question picker
                questions_query = db((db.courses.course_name == auth.user.course_name) & \
                                     (db.questions.base_course == db.courses.base_course) & \
                                  (db.questions.chapter == ch.chapter_label) & \
                                  (db.questions.question_type != 'page') & \
                                  (db.questions.subchapter == sub_ch.sub_chapter_label)).select(orderby=db.questions.id)
                for question in questions_query:
                    q_info = dict(
                        text=question.questions.name + _add_q_meta_info(question),
                        id=question.questions.name,
                    )
                    q_sub_ch_info['children'].append(q_info)
        return json.dumps({'reading_picker': reading_picker,
                          'practice_picker': practice_picker,
                          'question_picker': question_picker})
    # except Exception as ex:
    #     print(ex)
    #     return json.dumps({})

def _add_q_meta_info(qrow):
    res = ""
    qt = {
        'mchoice': 'Mchoice ✓',
        'clickablearea':'Clickable ✓',
        'youtube': 'Video',
        'activecode': 'ActiveCode',
        'poll': 'Poll',
        'showeval': 'ShowEval',
        'video': 'Video',
        'dragndrop': 'Matching ✓',
        'parsonsprob': 'Parsons ✓',
        'codelens': 'CodeLens',
        'lp_build': 'LP ✓',
        'shortanswer': 'ShortAns',
        'actex': 'ActiveCode',
        'fillintheblank': 'FillB ✓'
    }
    res += qt.get(qrow.questions.question_type,"")

    if qrow.questions.autograde:
        res += ' ✓'

    if res != "":
        res = """ <span style="color: green">[{}] </span>""".format(res)

    return res

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def get_assignment():
    assignment_id = request.vars['assignmentid']
    # Assemble the assignment-level properties
    if assignment_id == 'undefined':
        logger.error('UNDEFINED assignment {} {}'.format(auth.user.course_name, auth.user.username))
        session.flash = 'Error assignment ID is undefined'
        return redirect(URL('assignments','index'))

    assignment_data = {}
    assignment_row = db(db.assignments.id == assignment_id).select().first()
    assignment_data['assignment_points'] = assignment_row.points
    try:
        assignment_data['due_date'] = assignment_row.duedate.strftime("%Y/%m/%d %H:%M")
    except Exception as ex:
        logger.error(ex)
        assignment_data['due_date'] = None
    assignment_data['description'] = assignment_row.description
    assignment_data['visible'] = assignment_row.visible

    # Still need to get:
    #  -- timed properties of assignment
    #  (See https://github.com/RunestoneInteractive/RunestoneServer/issues/930)
    base_course = db(db.courses.id == auth.user.course_id).select(db.courses.base_course).first().base_course
    # Assemble the readings (subchapters) that are part of the assignment
    a_q_rows = db((db.assignment_questions.assignment_id == assignment_id) &
                  (db.assignment_questions.question_id == db.questions.id) &
                  (db.questions.question_type == 'page')
                  ).select(orderby=db.assignment_questions.sorting_priority)
    pages_data = []
    for row in a_q_rows:
        if row.questions.question_type == 'page':
            # get the count of 'things to do' in this chap/subchap
            activity_count = db((db.questions.chapter==row.questions.chapter) &
                       (db.questions.subchapter==row.questions.subchapter) &
                       (db.questions.from_source == 'T') &
                       (db.questions.base_course == base_course)).count()

        pages_data.append(dict(
            name = row.questions.name,
            points = row.assignment_questions.points,
            autograde = row.assignment_questions.autograde,
            activity_count = activity_count,
            activities_required = row.assignment_questions.activities_required,
            which_to_grade = row.assignment_questions.which_to_grade,
            autograde_possible_values = AUTOGRADE_POSSIBLE_VALUES[row.questions.question_type],
            which_to_grade_possible_values = WHICH_TO_GRADE_POSSIBLE_VALUES[row.questions.question_type]
        ))

    # Assemble the questions that are part of the assignment
    a_q_rows = db((db.assignment_questions.assignment_id == assignment_id) &
                  (db.assignment_questions.question_id == db.questions.id) &
                  (db.assignment_questions.reading_assignment == None)
                  ).select(orderby=db.assignment_questions.sorting_priority)
    #return json.dumps(db._lastsql)
    questions_data = []
    for row in a_q_rows:
        logger.debug(row.questions.question_type)
        if row.questions.question_type != 'page':
            questions_data.append(dict(
                name = row.questions.name,
                points = row.assignment_questions.points,
                autograde = row.assignment_questions.autograde,
                which_to_grade = row.assignment_questions.which_to_grade,
                autograde_possible_values = AUTOGRADE_POSSIBLE_VALUES[row.questions.question_type],
                which_to_grade_possible_values = WHICH_TO_GRADE_POSSIBLE_VALUES[row.questions.question_type]
            ))

    return json.dumps(dict(assignment_data=assignment_data,
                           pages_data=pages_data,
                           questions_data=questions_data))

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def save_assignment():
    # This endpoint is for saving (updating) an assignment's top-level information, without any
    # questions or readings that might be part of the assignment
    # Should return the id of the assignment, if one is not passed in

    # The following fields must be provided in request.vars (see modesl/grouped_assignments.py for model definition):
    # -- assignment_id (if it's an existing assignment; if none provided, then we insert a new assignment)
    # -- description
    # -- duedate

    assignment_id = request.vars.get('assignment_id')
    isVisible = request.vars['visible']

    try:
        d_str = request.vars['due']
        format_str = "%Y/%m/%d %H:%M"
        due = datetime.datetime.strptime(d_str, format_str)
    except:
        logger.error("Bad Date format for assignment: {}".format(d_str))
        due = datetime.datetime.utcnow() + datetime.timedelta(7)
    try:
        db(db.assignments.id == assignment_id).update(
            course=auth.user.course_id,
            description=request.vars['description'],
            duedate=due,
            visible=request.vars['visible']
        )
        return json.dumps({request.vars['name']: assignment_id,
                           'status': 'success'})
    except Exception as ex:
        logger.error(ex)
        return json.dumps('ERROR')


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def add__or_update_assignment_question():
    # This endpoint is for adding a question to an assignment, or updating an existing assignment_question

    # The following fields should be provided in request.vars:
    # -- assignment (an integer)
    # -- question (the question_name)
    # -- points
    # -- autograde
    # -- which_to_grade
    # -- reading_assignment (boolean, true if it's a page to visit rather than a directive to interact with)
    if request.vars.assignment == 'undefined':
        session.flash = "Error: Unable to update assignment in DB. No assignment is selected"
        return redirect(URL('admin','assignments'))

    assignment_id = int(request.vars['assignment'])
    question_name = request.vars['question']
    logger.debug("adding or updating assign id {} question_name {}".format(assignment_id, question_name))
    # This assumes that question will always be in DB already, before an assignment_question is created
    logger.debug("course_id %s",auth.user.course_id)
    question_id = _get_question_id(question_name, auth.user.course_id)
    if question_id == None:
        logger.error("Question Not found for name = {} course = {}".format(question_name, auth.user.course_id))
        session.flash = "Error: Cannot find question {} in the database".format(question_name)
        return redirect(URL('admin','assignments'))

    base_course = db(db.courses.id == auth.user.course_id).select(db.courses.base_course).first().base_course
    logger.debug("base course %s", base_course)
    question_type = db.questions[question_id].question_type
    chapter = db.questions[question_id].chapter
    subchapter = db.questions[question_id].subchapter
    auto_grade = db.questions[question_id].autograde
    tmpSp = _get_question_sorting_priority(assignment_id, question_id)
    if tmpSp != None:
        sp = 1 + tmpSp
    else:
        sp = 0

    activity_count = 0
    if question_type == 'page':
        reading_assignment = 'T'
        # get the count of 'things to do' in this chap/subchap
        activity_count = db((db.questions.chapter == chapter) &
                   (db.questions.subchapter == subchapter) &
                   (db.questions.from_source == 'T') &
                   (db.questions.base_course == base_course)).count()
        try:
            activities_required = int(request.vars.get('activities_required'))
            if activities_required == -1:
                activities_required = max(int(activity_count * .8),1)
        except:
            logger.error("No Activities set for RA %s", question_name)
            activities_required = None

    else:
        reading_assignment = None
        activities_required = None

    # Have to use try/except here instead of request.vars.get in case the points is '',
    # which doesn't convert to int
    try:
        points = int(request.vars['points'])
    except:
        points = activity_count


    autograde = request.vars.get('autograde')
    which_to_grade = request.vars.get('which_to_grade')
    # Make sure the defaults are set correctly for activecode Qs
    if question_type in ('activecode', 'actex'):
        if auto_grade != 'unittest':
            autograde = 'manual'
            which_to_grade = ""
    try:
        # save the assignment_question
        db.assignment_questions.update_or_insert(
            (db.assignment_questions.assignment_id==assignment_id) & (db.assignment_questions.question_id==question_id),
            assignment_id = assignment_id,
            question_id = question_id,
            activities_required=activities_required,
            points=points,
            autograde=autograde,
            which_to_grade = which_to_grade,
            reading_assignment = reading_assignment,
            sorting_priority = sp
        )
        total = _set_assignment_max_points(assignment_id)
        return json.dumps(dict(
            total = total,
            activity_count=activity_count,
            activities_required=activities_required,
            autograde_possible_values=AUTOGRADE_POSSIBLE_VALUES[question_type],
            which_to_grade_possible_values=WHICH_TO_GRADE_POSSIBLE_VALUES[question_type],
            status = 'success'
        ))
    except Exception as ex:
        logger.error(ex)
        return json.dumps("Error")

def _get_question_id(question_name, course_id):
    question = db((db.questions.name == question_name) &
              (db.questions.base_course == db.courses.base_course) &
              (db.courses.id == course_id)
              ).select(db.questions.id).first()
    if question:
        return int(question.id)
    else:
        # Hmmm, what should we do if not found?
        return None

    # return int(db((db.questions.name == question_name) &
    #           (db.questions.base_course == db.courses.base_course) &
    #           (db.courses.id == course_id)
    #           ).select(db.questions.id).first().id)

def _get_question_sorting_priority(assignment_id, question_id):
    max = db.assignment_questions.sorting_priority.max()
    return db((db.assignment_questions.assignment_id == assignment_id)).select(max).first()[max]

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def delete_assignment_question():
    ## Deletes one assignment_question
    try:
        question_name = request.vars['name']
        assignment_id = int(request.vars['assignment_id'])
        question_id = _get_question_id(question_name, auth.user.course_id)
        logger.debug("DELETEING A: %s Q:%s ", assignment_id, question_id)
        db((db.assignment_questions.assignment_id == assignment_id) & \
           (db.assignment_questions.question_id == question_id)).delete()
        total = _set_assignment_max_points(assignment_id)
        return json.dumps({'total': total})
    except Exception as ex:
        logger.error(ex)
        return json.dumps("Error")

def _set_assignment_max_points(assignment_id):
    """Called after a change to assignment questions.
    Recalculate the total, save it in the assignment row
    and return it."""
    sum_op = db.assignment_questions.points.sum()
    total = db(db.assignment_questions.assignment_id == assignment_id).select(sum_op).first()[sum_op]
    db(db.assignments.id == assignment_id).update(
        points=total
    )
    return total


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def reorder_assignment_questions():
    """Called when the questions are reordered in the instructor assignments interface.
    request.vars must include:
    -- names: a list of strings for question_names
    -- assignment_id: a database record id

    The names list should be a list of *all* assignment_questions of that type (i.e., all that have the
    boolean reading_assignment flag set to True, or all that have it set to False).
    We will reassign sorting_priorities to all of them.
    """
    question_names = request.vars['names[]']  # a list of question_names
    assignment_id = int(request.vars['assignment_id'])
    i = 0
    for name in question_names:
        i += 1
        question_id = _get_question_id(name, auth.user.course_id)
        db((db.assignment_questions.question_id == question_id) &
           (db.assignment_questions.assignment_id == assignment_id)) \
           .update(sorting_priority = i)

    return json.dumps("Reordered in DB")

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def copy_assignment():
    """
    vars:
      - oldassignment id or  todo (-1 for all assignments)
      - course
    """

    res = None
    if not verifyInstructorStatus(request.vars['course'], auth.user):
        return "Error: Not Authorized"
    else:
        if request.vars.oldassignment == '-1':
            assignments = db((db.assignments.course == db.courses.id) &
                             (db.courses.course_name == request.vars['course'])).select()
            for a in assignments:
                print("A = {}".format(a))
                res = _copy_one_assignment(request.vars['course'], a.assignments['id'])
                if res != "success":
                    break
        else:
            res = _copy_one_assignment(request.vars['course'], request.vars['oldassignment'])
    if res is None:
        return "Error: No Assignments to copy"
    else:
        return res

def _copy_one_assignment(course, oldid):
        old_course = db(db.courses.course_name == course).select().first()
        this_course = db(db.courses.course_name == auth.user.course_name).select().first()
        old_assignment = db(db.assignments.id == int(oldid)).select().first()
        due_delta = old_assignment.duedate.date() - old_course.term_start_date
        due_date = this_course.term_start_date + due_delta
        newassign_id = db.assignments.insert(course=auth.user.course_id, name=old_assignment.name,
            duedate=due_date, description=old_assignment.description,
            points=old_assignment.points,
            threshold_pct=old_assignment.threshold_pct)

        old_questions = db(db.assignment_questions.assignment_id == old_assignment.id).select()
        for q in old_questions:
            dq = q.as_dict()
            dq['assignment_id'] = newassign_id
            del dq['id']
            db.assignment_questions.insert(**dq)

        return "success"


@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def courselog():
    thecourse = db(db.courses.id == auth.user.course_id).select().first()
    course = auth.user.course_name

    data = pd.read_sql_query("""
    select sid, useinfo.timestamp, event, act, div_id, chapter, subchapter
    from useinfo left outer join questions on div_id = name and questions.base_course = '{}'
    where course_id = '{}'
    order by useinfo.id
    """.format(thecourse.base_course, course), settings.database_uri)
    data = data[~data.sid.str.contains('@')]

    response.headers['Content-Type']='application/vnd.ms-excel'
    response.headers['Content-Disposition']= 'attachment; filename=data_for_{}.csv'.format(auth.user.course_name)
    return data.to_csv(na_rep=" ")

def killer():
    print(routes_onerror)
    x = 5 / 0
    return 'ERROR'
