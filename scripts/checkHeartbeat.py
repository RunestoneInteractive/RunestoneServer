#!/usr/bin/env python3

__author__ = 'bmiller'

from sqlalchemy import create_engine, Table, MetaData, select
import datetime
import os

#engine = create_engine('postgresql://bmiller@localhost/runestone')
engine = create_engine('postgresql://bnmnetp_courselib@web407.webfaction.com/bnmnetp_courselib')

meta = MetaData()
worker = Table('scheduler_worker', meta, autoload=True, autoload_with=engine)

s = select([worker])
result = engine.execute(s)

row = result.fetchone()

diff = datetime.datetime.utcnow() - row['last_heartbeat']

if diff.seconds > 30:
    os.system("/Users/bmiller/bin/sendIMessage bonelake@mac.com 'No Heartbeat for 30 seconds' ")

