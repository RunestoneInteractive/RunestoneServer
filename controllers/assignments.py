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
