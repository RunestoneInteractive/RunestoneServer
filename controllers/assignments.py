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
	existing_record = db(db.assignments.id == request.vars.id).select().first()
	db.assignments.grade_type.widget = SQLFORM.widgets.radio.widget
	form = SQLFORM(db.assignments, existing_record,
	    showid = False,
	    fields=['name','points','query','grade_type','threshold'],
	    keepvalues = True,
	    formstyle='table3cols',
	    )
	form.vars.course = course.id
	if form.process().accepted:
		session.flash = 'form accepted'
		redirect(URL('assignments','index'))
	elif form.errors:
		response.flash = 'form has errors'
	return dict(
		form = form,
		)