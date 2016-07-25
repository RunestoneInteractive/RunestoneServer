from os import path
import os
import pygal
import logging
from datetime import date, timedelta
from operator import itemgetter
from paver.easy import sh


# this is for admin links
# use auth.requires_membership('manager')
#
# create a simple index to provide a page of links
# - re build the book
# - list assignments
# - find assignments for a student
# - show totals for all students

# select acid, sid from code as T where timestamp = (select max(timestamp) from code where sid=T.sid and acid=T.acid);

@auth.requires_login()
def index():
    selected_chapter = None
    questions = []
    sections = []

    chapters = db(db.chapters.course_id == auth.user.course_name).select()
    for chapter in chapters.find(lambda chapter: chapter.chapter_label==request.get_vars['chapter']):
        selected_chapter = chapter
    if selected_chapter is None:
        selected_chapter = chapters.first()

    data_analyzer = DashboardDataAnalyzer(auth.user.course_id)
    data_analyzer.load_chapter_metrics(selected_chapter)
    problem_metrics = data_analyzer.problem_metrics
    progress_metrics = data_analyzer.progress_metrics

    for problem_id, metric in problem_metrics.problems.iteritems():
        stats = metric.user_response_stats()

        questions.append({
            "id": problem_id,
            "text": metric.problem_text,
            "correct": stats[2],
            "correct_mult_attempt": stats[3],
            "incomplete": stats[1],
            "not_attempted": stats[0],
            "attemptedBy": stats[1] + stats[2] + stats[3]
            })
    questions = sorted(questions, key=itemgetter("correct"), reverse=True)
    for sub_chapter, metric in progress_metrics.sub_chapters.iteritems():
        sections.append({
            "id": metric.sub_chapter_label,
            "text": metric.sub_chapter_text,
            "readPercent": metric.get_completed_percent(),
            "startedPercent": metric.get_started_percent(),
            "unreadPercent": metric.get_not_started_percent()
            })

    read_data = []
    user_activity = data_analyzer.user_activity
    for user, activity in user_activity.user_activities.iteritems():
        read_data.append({
            "student":activity.name,
            "count":activity.get_page_views()
            })

    studentactivity = [{
    "data":read_data,
    "name":"Sections Read"
    },{
    "data":read_data,
    "name":"Exercises Correct"
    },{
    "data":read_data,
    "name":"Exercises Missed"
    }]
    return dict(course_name=auth.user.course_name, questions=questions, sections=sections, chapters=chapters, selected_chapter=selected_chapter, studentactivity=studentactivity)

@auth.requires_login()
def studentreport():
    data_analyzer = DashboardDataAnalyzer(auth.user.course_id)
    data_analyzer.load_user_metrics(request.get_vars["id"])

    chapters = []
    for chapter_label, chapter in data_analyzer.chapter_progress.chapters.iteritems():
        chapters.append({
            "label": chapter.chapter_label,
            "status": chapter.status_text(),
            "subchapters": chapter.get_sub_chapter_progress()
            })
    activity = data_analyzer.formatted_activity.activities
    return dict(course_name=auth.user.course_name,user=data_analyzer.user, chapters=chapters, activity=activity)

def studentprogress():
    return dict(course_name=auth.user.course_name)

def grades():
    row = db(db.courses.id == auth.user.course_id).select(db.courses.course_name, db.courses.base_course).first()
    course = db(db.courses.id == auth.user.course_id).select().first()

    return dict(course_name=auth.user.course_name)

def exercisemetrics():
    data_analyzer = DashboardDataAnalyzer(auth.user.course_id)
    data_analyzer.load_exercise_metrics(request.get_vars["id"])
    problem_metrics = data_analyzer.problem_metrics

    prob_id = request.get_vars["id"]
    answers = []
    attempt_histogram = []

    problem_metric = problem_metrics.problems[prob_id]
    response_frequency = problem_metric.aggregate_responses

    for username, user_responses in problem_metric.user_responses.iteritems():
        responses = user_responses.responses[:4]
        responses += [''] * (4 - len(responses))
        answers.append({
            "user":user_responses.user,
            "username": user_responses.username,
            "answers":responses
            })

    for attempts, count in problem_metric.user_number_responses().iteritems():
        attempt_histogram.append({
            "attempts": attempts,
            "frequency": count
            })

    return dict(course_name=auth.user.course_name, answers=answers, response_frequency=response_frequency, attempt_histogram=attempt_histogram, exercise_label=problem_metric.problem_text)
