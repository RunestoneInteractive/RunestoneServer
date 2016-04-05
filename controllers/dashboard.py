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
    

    questions = [
        {
        "id": "5",
        "text": "CSP-4-4-4: Put the blocks below into the correct order to print a twist on a famous poem.",
        "correctPercent": '15%',
        "attemptPercent": '40%',
        "missedPercent": '45%',
        "neverPercent": '5%',
        "correct":5,
        "attempted":4,
        "missed":9,
        "never":2,
        "completedStudents": '18'
        },
                {
        "id": "6",
        "text": "CSP-4-2-3: Given the following code segment, what will be printed?",
        "correctPercent": '35%',
        "attemptPercent": '20%',
        "missedPercent": '45%',
        "correct":7,
        "attempted":3,
        "missed":8,
        "never":2,
        "completedStudents": '18'
        },
                {
        "id": "7",
        "text": "CSP-4-2-1: What will be printed when the following executes?",
        "correctPercent": '40%',
        "attemptPercent": '40%',
        "missedPercent": '20%',
        "correct":8,
        "attempted":3,
        "missed":4,
        "never":5,
        "completedStudents": '15'
        },
                {
        "id": "8",
        "text": "CSP-4-1-2: What will be printed when the following executes?",
        "correctPercent": '55%',
        "attemptPercent": '30%',
        "missedPercent": '15%',
        "correct":10,
        "attempted":4,
        "missed":3,
        "never":3,
        "completedStudents": '17'
        },
                {
        "id": "9",
        "text": "CSP-4-1-1: : Given the following code segment, what will be printed?",
        "correctPercent": '60%',
        "attemptPercent": '30%',
        "missedPercent": '10%',
        "correct":14,
        "attempted":3,
        "missed":1,
        "never":2,
        "completedStudents": '18'
        }
    ]
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

    res = db((db.useinfo.course_id==course.course_name) & (db.useinfo.timestamp >= course.term_start_date)).select(db.useinfo.timestamp,db.useinfo.sid, db.useinfo.event,db.useinfo.act,db.useinfo.div_id,
        orderby=~db.useinfo.timestamp)

    #count answer frequency
    problemStats = {}
    for result in res:
        if result.event == "mChoice":
            if not result.div_id in problemStats:
                problemStats[result.div_id] = {}

            answer = result.act.split(':')
            choice = answer[1]
            problemStats[result.div_id][choice] = problemStats[result.div_id].get(choice, 0) + 1
            
        if result.event == "fillb":
            if not result.div_id in problemStats:
                problemStats[result.div_id] = {}
            answer = result.act.split(':')
            choice = answer[1]
            problemStats[result.div_id][choice] = problemStats[result.div_id].get(choice, 0) + 1
    print problemStats

    #each problem by numb
    problemStats = {}
    for result in res:
        if result.event == "mChoice":
            if not result.div_id in problemStats:
                problemStats[result.div_id] = {}

            answer = result.act.split(':')
            choice = answer[1]
            problemStats[result.div_id][choice] = problemStats[result.div_id].get(choice, 0) + 1
            
        if result.event == "fillb":
            if not result.div_id in problemStats:
                problemStats[result.div_id] = {}
            answer = result.act.split(':')
            choice = answer[1]
            problemStats[result.div_id][choice] = problemStats[result.div_id].get(choice, 0) + 1
    print problemStats

    logging.warning(res)
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

    return dict(course_name=auth.user.course_name, answers=answers)
