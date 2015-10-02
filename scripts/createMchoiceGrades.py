

from sqlalchemy import create_engine, Table, MetaData, select
import datetime
import os

def insertAnswer(ans, sid, divid, info):
    x,response,result = info.split(':')
    print("inserting ", sid, divid, response, result)
    return result == 'correct'


engine = create_engine('postgresql://millbr02@localhost/runestone')
#engine = create_engine('postgresql://runestone@web407.webfaction.com/bnmnetp_courselib')

meta = MetaData()
useinfo = Table('useinfo', meta, autoload=True, autoload_with=engine)
#mcanswers = Table('mchoice_answers', meta, autoload=True, autoload_with=engine)

s = select([useinfo]).where((useinfo.c.timestamp > datetime.datetime(2015,01,01)) & (useinfo.c.event=='mChoice')).order_by(useinfo.c.div_id,useinfo.c.sid,useinfo.c.id)
result = engine.execute(s)
first = result.fetchone()
print(first['div_id'], first['sid'], first['act'])
currentDiv = first['div_id']
currentSid = first['sid']
correctSeen = False

correctSeen = insertAnswer(None, currentSid, currentDiv, first['act'])

for row in result:
    if row['div_id'] == currentDiv:
        if row['sid'] == currentSid:
            if not correctSeen:
                correctSeen = insertAnswer(None,currentSid, currentDiv, row['act'])
            else:
                print "ignoring all answers after first correct for ", currentDiv, currentSid
        else:
            currentSid = row['sid']
            correctSeen = insertAnswer(None,currentSid, currentDiv, row['act'])
    else:
        currentDiv = row['div_id']
        currentSid = row['sid']
        correctSeen = insertAnswer(None,currentSid, currentDiv, row['act'])




