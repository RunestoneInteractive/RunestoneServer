import psycopg2
import shutil
import os, sys
import filecmp
import difflib

conn = psycopg2.connect(os.environ['DBURL'])
curs = conn.cursor()
curs.execute('set session statement_timeout to 0')
curs.execute('''select course_name, base_course from courses''')

cleancount = 0

for row in curs:
    course = "custom_courses/{}/index.rst".format(row[0])
    bc = "books/{}/_sources/index.rst".format(row[1])

    if os.path.exists(course) and os.path.exists(bc):
        print ("comparing {} to {}".format(course,bc))
        res = filecmp.cmp(course, bc)
        if not res:
            print("{} is DIFFERENT".format(course))
            sys.stdout.writelines(difflib.context_diff(open(course).readlines(), open(bc).readlines()))
