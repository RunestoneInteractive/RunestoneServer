#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import stat
import datetime
import pickle
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm.session import sessionmaker

SLEEP_MINUTES = 5

errors_path = os.path.join(request.folder, 'errors')

if os.environ['WEB2PY_CONFIG'] == "production":
    db_string = os.environ['DBURL']
elif os.environ['WEB2PY_CONFIG'] == "development":
    db_string = os.environ['DEV_DBURL']
else:
    # no need to run during testing
    sys.exit(0)

engine = create_engine(db_string)
Session = sessionmaker()
engine.connect()
Session.configure(bind=engine)
sess = Session()
meta = MetaData()
# the traceback table is defined by bookserver.models
traceback = Table("traceback", meta, autoload=True, autoload_with=engine)

hashes = {}

while 1:

    for file in os.listdir(errors_path):
        filename = os.path.join(errors_path, file)

        modified_time = os.stat(filename)[stat.ST_MTIME]
        modified_time = datetime.datetime.fromtimestamp(modified_time)
        with open(filename, 'rb') as f:
            ticket_data = pickle.load(f)
        ticket_id = file
        traceback_str = ticket_data['traceback']
        emess = ticket_data['output']

        newtb = traceback.insert().values(
            traceback=traceback_str,
            timestamp=datetime.datetime.utcnow(),
            err_message=ticket_data['output'],
            hostname='web2py',
        )
        sess.execute(newtb)
        sess.commit()
        #os.unlink(filename)

    time.sleep(SLEEP_MINUTES * 60)
