#
# Unit Tests for AJAX API endpoints
# Set up the environment variables
# WEB2PY_CONFIG=test
# TEST_DBURL=postgres://user:pw@host:port/dbname
#
#
# Run these from the main web2py directory with the command:
# python web2py.py -S runestone -M -R applications/runestone/tests/test_dashboard.py
#

import unittest
import sys
from bs4 import BeautifulSoup

from gluon.globals import Request, Session
from gluon.tools import Auth
from six import StringIO

import pytest
import six

from .utils import web2py_controller_import


def test_student_report(test_client, runestone_db_tools, test_user, test_user_1):
    with runestone_db_tools.create_course('test_course_3') as course_3:
        with test_user('test_instructor_1', 'password_1', course_3.course_name) as test_instructor_1, \
            test_instructor_1.make_instructor():

            test_instructor_1.login()
            db = runestone_db_tools.db

            # Create an assignment -- using createAssignment
            #test_client.post('dashboard/studentreport',
            #     data=dict(id='test_user_1'))

            test_client.validate('dashboard/studentreport','Recent Activity', data=dict(id='test_instructor_1'))

            with test_instructor_1.hsblog(event="mChoice",
                    act="answer:1:correct",answer="1",correct="T",div_id="subc_b_1",
                    course="test_course_3"):

                test_client.validate('dashboard/studentreport','subc_b_1', data=dict(id='test_instructor_1'))

def test_subchapteroverview(test_client, runestone_db_tools, test_user, test_user_1):
    with runestone_db_tools.create_course('test_course_3') as course_3:
        with test_user('test_instructor_1', 'password_1', course_3.course_name) as test_instructor_1, \
            test_instructor_1.make_instructor():

            test_instructor_1.login()
            db = runestone_db_tools.db

            test_client.validate('dashboard/subchapoverview','chapter_num')
            test_client.validate('dashboard/subchapoverview','div_id', data=dict(tablekind='dividnum'))

            with test_instructor_1.hsblog(event="mChoice",
                    act="answer:1:correct",answer="1",correct="T",div_id="subc_b_1",
                    course="test_course_3"):

                test_client.validate('dashboard/subchapoverview','subc_b_1', data=dict(tablekind='dividnum'))
                test_client.validate('dashboard/subchapoverview','div_id', data=dict(tablekind='dividmin'))
                test_client.validate('dashboard/subchapoverview','div_id', data=dict(tablekind='dividmax'))
