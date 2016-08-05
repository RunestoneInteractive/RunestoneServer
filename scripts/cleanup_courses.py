import psycopg2
import shutil
import os

conn = psycopg2.connect(host="localhost",user="bnmnetp_courselib", 
                 password="al3xandria", database="bnmnetp_courselib");

curs = conn.cursor()
curs.execute('set session statement_timeout to 0')
curs.execute('''select course_id, count(*), max(timestamp) from useinfo group by course_id having max(timestamp) < now() - interval '365 days' and count(*) < 100''')

cleancount = 0

for row in curs:
    course = row[0]
    if course and os.path.exists("./live/static/{}".format(course)):
        print ('removing {} count: {} last_access: {}'.format(course, row[1], row[2]))
        try:
            shutil.rmtree("./live/static/{}".format(course))
            shutil.rmtree("./live/custom_courses/{}".format(course))
            cleancount += 1
        except:
            print("failed to remove {} in file system".format(course))

print("Cleaned up {} old courses".format(cleancount))
