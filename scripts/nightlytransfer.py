from sqlalchemy import create_engine, Table, MetaData, select, func
from sqlalchemy.orm import sessionmaker
import os

rspw = os.environ['RUNESTONEPW']

localengine = create_engine('postgresql://millbr02@localhost/runestoneanalysis')
remoteengine = create_engine('postgresql://bnmnetp_courselib:{}@web407.webfaction.com/bnmnetp_courselib'.format(rspw))

meta = MetaData()


def mirror_table(fromeng, toeng, tablename):
    print("Mirroring {}".format(tablename))
    from_tbl = Table(tablename, meta, autoload=True, autoload_with=fromeng)
    to_tbl = Table(tablename, meta, autoload=True, autoload_with=toeng)

    last = toeng.execute("select max(id) from {}".format(tablename)).first()[0]

    s = select([from_tbl]).where((from_tbl.c.id > last))
    result = fromeng.execute(s)

    ct = 0
    for row in result:
        newrow = {}
        for column in to_tbl.columns.keys():
            newrow[column] = row[column]
        s = to_tbl.insert().values(**newrow)
        toeng.execute(s)
        ct += 1

    print("Inserted {} new rows into {}".format(ct,tablename))


for tbl in ['useinfo','acerror_log','courses','div_ids', 'code', 'timed_exam']:
    mirror_table(remoteengine, localengine, tbl)

