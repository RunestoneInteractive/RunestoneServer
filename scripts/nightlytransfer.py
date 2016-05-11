from sqlalchemy import create_engine, Table, MetaData, select, func
from sqlalchemy.orm import sessionmaker
import os

rspw = os.environ['RUNESTONEPW']

localengine = create_engine('postgresql://millbr02@localhost/runestoneanalysis')
remoteengine = create_engine('postgresql://bnmnetp_courselib:{}@web407.webfaction.com/bnmnetp_courselib'.format(rspw))

meta = MetaData()
remoteuseinfo = Table('useinfo', meta, autoload=True, autoload_with=remoteengine)
localuseinfo = Table('useinfo', meta, autoload=True, autoload_with=localengine)

remoteacel = Table('acerror_log', meta, autoload=True, autoload_with=remoteengine)
localacel = Table('acerror_log', meta, autoload=True, autoload_with=localengine)

print(localuseinfo.columns.keys())

# create a configured "Session" class
Session = sessionmaker(bind=localengine)
# create a Session
session = Session()
last = session.query(func.max(localuseinfo.c.id)).first()[0]
print(last)

#print(localengine.execute("select max(id) from useinfo")).first()

s = select([remoteuseinfo]).where((remoteuseinfo.c.id > last))
result = remoteengine.execute(s)

for row in result:
    newrow = {}
    for column in localuseinfo.columns.keys():
        newrow[column] = row[column]
    s = localuseinfo.insert().values(**newrow)
    localengine.execute(s)


last = localengine.execute("select max(id) from acerror_log").first()[0]
print(last)
s = select([remoteacel]).where((remoteacel.c.id > last))
result = remoteengine.execute(s)

for row in result:
    newrow = {}
    for column in localacel.columns.keys():
        newrow[column] = row[column]
    s = localacel.insert().values(**newrow)
    localengine.execute(s)
