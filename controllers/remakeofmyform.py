-*- coding: utf-8 -*-
import json
#from models.db.py import createUser
import os
import requests
from six.moves.urllib.parse import unquote
from six.moves.urllib.error import HTTPError
import logging
import subprocess

from gluon.restricted import RestrictedError
from stripe_form import StripeForm

logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)

def registerinstructor():

    username = request.vars.username
    fname = request.vars.first_name
    lname = request.vars.last_name
    institution = request.vars.institution
    faculty_url = request.vars.faculty_url
    email = request.vars.email
    password = request.vars.password
    

    if username:
        createUser(username, password, fname, lname, email, institution, faculty_url, instructor=True)
        redirect(URL('default','copyofuser'))
        redirect(URL('copyofuser?username='+ username))
    

    return dict()
    

def copyofuser():
    
    username=request.vars.username
    fname=request.vars.first_name
    lname = request.vars.last_name
    institution = request.vars.institution
    faculty_url = request.vars.faculty_url
    email = request.vars.email
    password = request.vars.password
    
    users=[]

    users.append(username)
    users.append(fname)
    users.append(lname)
    users.append(institution)
    users.append(faculty_url)
    users.append(email)
    users.append(password)


    return dict(users=users)

    
def _validateUser(username, password, fname, lname, email, institution, faculty_url,  line):
    errors = []

    # if auth.user.course_name != course_name:
    #     errors.append(f"Course name does not match your course on line {line}")
    # cinfo = db(db.courses.course_name == course_name).select().first()
    # if not cinfo:
    #     errors.append(f"Course {course_name} does not exist on line {line}")
    match = re.search(r"""[!"#$%&'()*+,./:;<=>?@[\]^`{|}~ ]""", username)
    if match:
        errors.append(
            f"""Username cannot contain a {match.group(0).replace(" ", "space")} on line {line}"""
        )
    uinfo = db(db.auth_user.username == username).count()
    if uinfo > 0:
        errors.append(f"Username {username} already exists on line {line}")

    if fname == "":
        errors.append(f"First name cannot be blank on line {line}")
    if lname == "":
        errors.append(f"Last name cannot be blank on line {line}")
    if institution == "":
        errors.append(f"Institution name cannot be blank on line {line}")
    if faculty_url == "":
        errors.append(f"Faculty URL cannot be blank on line {line}")
    if password == "":
        errors.append(f"Password cannot be blank on line {line}")
    if "@" not in email:
        errors.append(f"Email address missing @ on line {line}")

    return errors

# def enroll_students():
#     if "students" not in request.vars:
#         session.flash = "please choose a CSV file with student data"
#         return redirect(URL("admin", "admin"))
#     students = request.vars.students
#     the_course = db(db.courses.course_name == auth.user.course_name).select().first()
#     try:
#         use utf-8-sig because it will work with files from excel that have
#         the byte order marker BOM set as an invisible first character in the file
#         strfile = io.TextIOWrapper(students.file, encoding="utf-8-sig")
#         logger.debug(type(students.file))
#         student_reader = csv.reader(strfile)
#         validfile = io.TextIOWrapper(students.file, encoding="utf-8-sig")
#         validation_reader = csv.reader(validfile)
#     except Exception as e:
#         session.flash = "please choose a CSV file with student data"
#         logger.error(e)
#         return redirect(URL("admin", "admin"))
#     messages = []
#     line = 0
#     for row in validation_reader:
#         line += 1
#         if len(row) == 6:
#             res = _validateUser(row[0], row[4], row[2], row[3], row[1], row[5], line)
#         else:
#             res = [f"Error on line {line} you should have 6 fields"]
#         if res:
#             messages.extend(res)

#     if messages:
#         return dict(
#             coursename=auth.user.course_name,
#             course_id=auth.user.course_name,
#             course=the_course,
#             messages=messages,
#         )