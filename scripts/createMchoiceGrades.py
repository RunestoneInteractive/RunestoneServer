

from sqlalchemy import create_engine, Table, MetaData, select
import datetime
import os, re

def insertAnswer(ans, sid, divid, info, ts, course):
    x,response,result = info.split(':')
    if response == 'undefined':
        return False
    responseMap = {'0':'a', '1':'b','2':'c','3':'d','4':'e'}
    print("inserting ", sid, divid, response, result)
    iscorrect = 'T' if result == 'correct' else 'F'
    s = mcanswers.insert().values(timestamp=ts, div_id=divid, sid=sid, course_name=course, answer=responseMap.get(response,response), correct=iscorrect)
    engine.execute(s)
    return result == 'correct'


engine = create_engine('postgresql://bmiller@localhost/runestone')
#engine = create_engine('postgresql://runestone@web407.webfaction.com/bnmnetp_courselib')

meta = MetaData()
useinfo = Table('useinfo', meta, autoload=True, autoload_with=engine)
mcanswers = Table('mchoice_answers', meta, autoload=True, autoload_with=engine)

s = select([useinfo]).where((useinfo.c.timestamp > datetime.datetime(2015,01,01)) & (useinfo.c.event=='mChoice')).order_by(useinfo.c.div_id,useinfo.c.sid,useinfo.c.id)
result = engine.execute(s)
first = result.fetchone()
print(first['div_id'], first['sid'], first['act'])
currentDiv = first['div_id']
currentSid = first['sid']
correctSeen = False

correctSeen = insertAnswer(None, currentSid, currentDiv, first['act'], first['timestamp'], first['course_id'])

for row in result:
    # ignore sid's of the form:  1423153196780@199.185.67.12 or 208.191.24.178@anon.user
    if re.match(r'^\d+@[\d\.]+$', row['sid']):
        continue
    if row['div_id'] == currentDiv:
        if row['sid'] == currentSid:
            if not correctSeen:
                correctSeen = insertAnswer(None,currentSid, currentDiv, row['act'], row['timestamp'], row['course_id'])
            else:
                print "ignoring all answers after first correct for ", currentDiv, currentSid
        else:
            currentSid = row['sid']
            correctSeen = insertAnswer(None,currentSid, currentDiv, row['act'], row['timestamp'], row['course_id'])
    else:
        currentDiv = row['div_id']
        currentSid = row['sid']
        correctSeen = insertAnswer(None,currentSid, currentDiv, row['act'], row['timestamp'], row['course_id'])




