from os import path
import os
import shutil
import sys
from sphinx.application import Sphinx

def index():
	if not auth.user:
		session.flash = "Please Login"
		return redirect(URL('default','index'))
	if 'sid' not in request.vars and verifyInstructorStatus(auth.user.course_name, auth.user):
		return redirect(URL('assignments','admin'))
	if 'sid' not in request.vars:
		return redirect(URL('assignments','index') + '?sid=%d' % (auth.user.id))
	if str(auth.user.id) != request.vars.sid and not verifyInstructorStatus(auth.user.course_name, auth.user):
		return redirect(URL('assignments','index'))
	student = db(db.auth_user.id == request.vars.sid).select(
		db.auth_user.id,
		db.auth_user.username,
		db.auth_user.first_name,
		db.auth_user.last_name,
		db.auth_user.email,
		).first()
	if not student:
		return redirect(URL('assignments','index'))

	course = db(db.courses.id == auth.user.course_id).select().first()
	assignments = db(db.assignments.id == db.grades.assignment)
	assignments = assignments(db.assignments.course == course.id)
	assignments = assignments(db.grades.auth_user == student.id)
	assignments = assignments.select(
		db.assignments.ALL,
		db.grades.ALL,
		orderby = db.assignments.name,
		)

	points_total = 0
	points_possible = 0
	for row in assignments:
		points_total += row.grades.score
		points_possible += row.assignments.points
	if points_possible == 0:
		points_possible = 1	# no rows; degenerate case
	student.points_possible = points_possible
	student.points_total = points_total
	student.points_percentage = round((points_total/points_possible)*100)

	last_action = db(db.useinfo.sid == student.username)(db.useinfo.course_id == course.course_name).select(orderby=~db.useinfo.timestamp).first()

	return dict(
		assignments = assignments,
		student = student,
		last_action = last_action,
		)

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def admin():
	course = db(db.courses.id == auth.user.course_id).select().first()
	assignments = db(db.assignments.course == course.id).select(db.assignments.ALL, orderby=db.assignments.name)
	students = db(db.auth_user.course_id == course.id).select()
	return dict(
		assignments = assignments,
		students = students,
		)

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def create():
	course = db(db.courses.id == auth.user.course_id).select().first()
	assignment = db(db.assignments.id == request.get_vars.id).select().first()
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
		return redirect(URL('assignments','update')+'?id=%d' % (form.vars.id))
	elif form.errors:
		response.flash = 'form has errors'
	return dict(
		form = form,
		)

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def update():
	course = db(db.courses.id == auth.user.course_id).select().first()
	assignment = db(db.assignments.id == request.get_vars.id).select().first()

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
		return redirect(URL('assignments','update')+'?id=%d' % (form.vars.id))
	elif form.errors:
		response.flash = 'form has errors'
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

	deadlines = db(db.deadlines.assignment == assignment.id).select()
	delete_deadline_form = FORM()
	for deadline in deadlines:
		deadline_label = "On %s" % (deadline.deadline)
		if deadline.section:
			section = db(db.sections.id == deadline.section).select().first()
			deadline_label = deadline_label + " for %s" % (section.name)
		delete_deadline_form.append(
			DIV(
				LABEL(
				INPUT(_type="checkbox", _name=deadline.id, _value="delete"),
				deadline_label,
				),
				_class="checkbox"
			))
	delete_deadline_form.append(
		INPUT(
			_type="submit",
			_value="Delete Deadlines",
			_class="btn btn-default"
			))

	if delete_deadline_form.accepts(request,session):
		for var in delete_deadline_form.vars:
			if delete_deadline_form.vars[var] == "delete":
				db(db.deadlines.id == var).delete()
		session.flash = 'Deleted deadline(s)'
		return redirect(URL('assignments','update')+'?id=%d' % (assignment.id))

	return dict(
		assignment = assignment,
		form = form,
		new_deadline_form = new_deadline_form,
		delete_deadline_form = delete_deadline_form,
		)

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def grade():
	course = db(db.courses.id == auth.user.course_id).select().first()
	assignment = db(db.assignments.id == request.get_vars.id).select().first()

	count_graded = 0
	for row in db(db.auth_user.course_id == course.id).select():
		assignment.grade(row)
		count_graded += 1
	session.flash = "Graded %d Assignments" % (count_graded)
	if request.env.HTTP_REFERER:
		return redirect(request.env.HTTP_REFERER)
	return redirect("%s?id=%d" % (URL('assignments','detail'), assignment.id))

@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def detail():
	course = db(db.courses.id == auth.user.course_id).select().first()
	assignment = db(db.assignments.id == request.vars.id)(db.assignments.course == course.id).select().first()
	if not assignment:
		return redirect(URL("assignments","index"))

	sections = db(db.sections.course_id == course.id).select(db.sections.ALL)
	selected_section = None
	if "section_id" in request.vars:
		selected_section = int(request.vars.section_id)
	acid = None
	if "acid" in request.vars:
		acid = request.vars.acid

	students = assignment.grades_get(section=selected_section, problem=acid)
	
	student = None
	if 'sid' in request.vars:
		student_id = request.vars.sid
		student = db(db.auth_user.id == student_id).select().first()
		problems = assignment.problems(student)
	else:
	    q = db(db.code.course_id == auth.user.course_id)
	    q = q(db.code.acid.like(assignment.query+"%"))
	    problems = q.select(
	    	db.code.acid,
	    	db.code.course_id,
	    	orderby = db.code.acid,
	    	distinct = db.code.acid,
	    	)

	# Used as a convinence function for navigating within the page template
	def page_args(id=assignment.id, section_id=selected_section, student=student, acid=acid):
		arg_str = "?id=%d" % (id)
		if section_id:
			arg_str += "&section_id=%d" % section_id
		if student:
			arg_str += "&sid=%d" % student.id
		if acid:
			arg_str += "&acid=%s" % acid
		return arg_str

	return dict(
		assignment = assignment,
		problems = problems,
		students = students,
		student = student,
		sections = sections,
		selected_section = selected_section,
		page_args = page_args,
		acid = acid,
		course_id = auth.user.course_name,
		gradingUrl = URL('assignments', 'problem'),
		)

import json
@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def problem():
	if 'acid' not in request.vars or 'sid' not in request.vars:
		return json.dumps({'success':False})
	q = db(db.code.sid == db.auth_user.username)
	q = q(db.code.acid == request.vars.acid)
	q = q(db.auth_user.id == request.vars.sid)
	q = q.select(
		db.auth_user.ALL,
		db.code.ALL,
		orderby = db.code.acid|db.code.timestamp,
		distinct = db.code.acid,
		).first()
	if not q:
		return json.dumps({'success':False})
	if 'grade' in request.vars:
		q.code.grade = float(request.vars.grade)
	if 'comment' in request.vars:
		q.code.comment = request.vars.comment
	if 'grade' in request.vars or 'comment' in request.vars:
		q.code.update_record()
	return json.dumps({
		'id':"%s-%d" % (q.code.acid, q.auth_user.id),
		'acid':q.code.acid,
		'sid':q.auth_user.username,
		'name':"%s %s" % (q.auth_user.first_name, q.auth_user.last_name),
		'code':q.code.code,
		'grade':q.code.grade,
		'comment':q.code.comment,
		})
