from os import path
import os
import shutil
import sys
from sphinx.application import Sphinx

def index():
	course = db(db.courses.id == auth.user.course_id).select().first()
	# get all assignments
	assignments = db(db.assignments.course == course.id).select()
	return dict(
		assignments = assignments,
		)

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def create_or_update():
	course = db(db.courses.id == auth.user.course_id).select().first()
	assignment = db(db.assignments.id == request.vars.id).select().first()
	db.assignments.grade_type.widget = SQLFORM.widgets.radio.widget
	form = SQLFORM(db.assignments, assignment,
	    showid = False,
	    fields=['name','points','query','grade_type','threshold'],
	    keepvalues = True,
	    formstyle='table3cols',
	    )
	form.vars.course = course.id
	if form.process().accepted:
		session.flash = 'form accepted'
		return redirect(URL('assignments','index'))
	elif form.errors:
		response.flash = 'form has errors'

	if not assignment:
		return dict(
			form = form,
			)

	new_deadline_form = SQLFORM(db.deadlines,
		showid = False,
		fields=['section','deadline'],
		keepvalues = True,
		formstyle='table3cols',
		)
	new_deadline_form.vars.assignment = assignment
	if new_deadline_form.process().accepted:
		session.flash = 'added new deadline'
	elif new_deadline_form.errors:
		response.flash = 'error adding deadline'

	return dict(
		form = form,
		new_deadline_form = new_deadline_form,
		)

def detail():
	course = db(db.courses.id == auth.user.course_id).select().first()
	assignment = db(db.assignments.id == request.vars.id and db.assignments.course == course.id).select().first()
	if not assignment:
		return redirect(URL("assignments","index"))
	user_id = auth.user.id
	if 'sid' in request.vars:
		user_id = request.vars.sid
	user = db(db.auth_user.id == user_id).select().first()
	# Get acid and list
	problems = assignment.problems(user)

	return dict(
		assignment = assignment,
		problems = problems,
		)