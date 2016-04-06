from os import path
import os
import pygal
import logging
from datetime import date, timedelta
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
    row = db(db.courses.id == auth.user.course_id).select(db.courses.course_name, db.courses.base_course).first()
    course = db(db.courses.id == auth.user.course_id).select().first()

    sections = [
        {
            "id": "5",
            "text": "Assign a Name to a String",
            "readPercent": '75%',
            "startedPercent": '20%',
            "unreadPercent": '5%',
        },        {
            "id": "6",
            "text": "Strings are Objects",
            "readPercent": '60%',
            "startedPercent": '30%',
            "unreadPercent": '10%',
        },        {
            "id": "7",
            "text": "Strings are Immutable",
            "readPercent": '25%',
            "startedPercent": '40%',
            "unreadPercent": '35%',
        },        {
            "id": "8",
            "text": "Making a MadLib Story",
            "readPercent": '15%',
            "startedPercent": '10%',
            "unreadPercent": '75%',
        },        {
            "id": "8",
            "text": "Chapter 4 - Summary",
            "readPercent": '45%',
            "startedPercent": '10%',
            "unreadPercent": '45%',
        },        {
            "id": "8",
            "text": "Chapter 4 Exercises",
            "readPercent": '5%',
            "startedPercent": '10%',
            "unreadPercent": '85%',
        }
    ]
    users = db(db.auth_user.course_id == auth.user.course_id).select(db.auth_user.username, db.auth_user.first_name,db.auth_user.last_name)
    #print users
    data_analyzer = DashboardDataAnalyzer(auth.user.course_id)
    problem_metrics = data_analyzer.problem_metrics

    questions = []
    for problem_id, metric in problem_metrics.problems.iteritems():
        stats = metric.user_response_stats()

        questions.append({
            "id": problem_id,
            "text": problem_id,
            "correct": stats[2],
            "correct_mult_attempt": stats[3],
            "incomplete": stats[1],
            "not_attempted": stats[0],
            "attemptedBy": stats[1] + stats[2] + stats[3]
            })

    #logging.warning(res)
    return dict(course_name=auth.user.course_name, questions=questions, sections=sections)

@auth.requires_login()
def studentreport():
    row = db(db.courses.id == auth.user.course_id).select(db.courses.course_name, db.courses.base_course).first()
    course = db(db.courses.id == auth.user.course_id).select().first()

    chapters = [{
        "text":"Chapter 1: What is this book about?",
        "sections":[{
            "text"
        }]
    }]
    return dict(course_name=auth.user.course_name,student_name=auth.user.first_name + " " + auth.user.last_name, chapters=chapters)

def studentprogress():
    row = db(db.courses.id == auth.user.course_id).select(db.courses.course_name, db.courses.base_course).first()
    course = db(db.courses.id == auth.user.course_id).select().first()





    return dict(course_name=auth.user.course_name)

def grades():
    row = db(db.courses.id == auth.user.course_id).select(db.courses.course_name, db.courses.base_course).first()
    course = db(db.courses.id == auth.user.course_id).select().first()

    return dict(course_name=auth.user.course_name)

def exercisemetrics():
    row = db(db.courses.id == auth.user.course_id).select(db.courses.course_name, db.courses.base_course).first()
    course = db(db.courses.id == auth.user.course_id).select().first()

    answers = [{
        "student":"Bob Brown",
        "answers":["4.0", "0", "2","4"]
    },{
        "student":"Nick Collans",
        "answers":["2.0", "4.0", "2","4"]
    },{
        "student":"Tim Collans",
        "answers":["8", "4", "",""]
    },{
        "student":"Xu Hung",
        "answers":["8", "4", "", ""]
    },{
        "student":"Jack Jackson",
        "answers":["5", "4", "", ""]
    },{
        "student":"Brittany Jones",
        "answers":["4", "", "", ""]
    }]

    data_analyzer = DashboardDataAnalyzer(auth.user.course_id)
    problem_metrics = data_analyzer.problem_metrics

    prob_id = request.get_vars["id"]
    answers = []
    problem_metric = problem_metrics.problems[prob_id]
    for username, user_responses in problem_metric.user_responses.iteritems():
        responses = user_responses.responses[:4]
        responses += [''] * (4 - len(responses))
        answers.append({
            "student":username,
            "answers":responses
            })
    print answers
    response_frequency = problem_metric.aggregate_responses
    print response_frequency
    attempt_histogram = []
    for attempts, count in problem_metric.user_number_responses().iteritems():
        attempt_histogram.append({
            "attempts": attempts,
            "frequency": count
            })

    print attempt_histogram
    return dict(course_name=auth.user.course_name, answers=answers, response_frequency=response_frequency, attempt_histogram=attempt_histogram)
